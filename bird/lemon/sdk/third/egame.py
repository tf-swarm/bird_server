# -*- coding:utf-8 -*-
""" created by cui """

import xmltodict
from sdk.const import Const
from sdk.modules.user import User
from sdk.modules.order import Order
from framework.context import Context
from framework.util.tool import Time
from framework.util.tool import Algorithm
from framework.entity.msgpack import MsgPack
from sdk.modules.account import Account


EGAME_URL = 'https://open.play.cn/oauth/token'
CLIENTID = '91181221'
APPKEY = '35b5cfab4d3d6cd1c546acb0d0bc5a6c'
CLIENTSECRET = 'be4aae83d086414aa3f837f80585153c'


def login(mi, request):
    param = User.getParam(mi, 'code',  'devName')
    if len(param['code']) <= 1:
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
    res = verify_login(param['code'])

    if res.get('error') or not res.get('user_id'):
        Context.Log.info('egame login res error:', res.get('error'))
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)

    gid = param['gameId']
    openid = res['user_id']
    userId = Context.RedisMix.hash_get('egame.%s.uid' % gid, openid, None)
    if not userId:
        channel = 'egame'
        idType = Const.IDTYPE_EGAME
        userId = User.register(param, request, openid, idType, channel)
        if not userId:
            return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
        Context.RedisMix.hash_set('egame.%s.uid' % gid, openid, userId)
    userId = int(userId)
    userInfo = Account.getUserInfo(userId)

    return User.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, False, openid=openid, loginChannelId=param['channelid'])

def verify_login(code):
    param = {'client_secret': CLIENTSECRET, 'client_id': CLIENTID, 'sign_method': 'MD5', 'version': '2.1.0', 'timestamp': str(Time.current_ts()),
            'sign_sort': 'timestamp&sign_method&client_secret&client_id&version', 'code': code,
            'grant_type': 'authorization_code'}
    sign = get_sign(param)
    param['signature'] = sign.upper()
    res = Context.WebPage.wait_for_json(EGAME_URL, postdata=param)
    return res


def get_sign(data):
    keys = data['sign_sort'].rsplit('&')
    sign_data = ''
    for key in keys:
        sign_data += data[key]
    return Algorithm.md5_encode(sign_data)


def check(args):
    # cp_order_id correlator order_time method  sign  version
    param = {
        "cp_order_id": args.get('cp_order_id'),
        "correlator": args.get('correlator', ''),
        "order_time": args.get('order_time', ''),
        "sign": args.get('sign', ''),
        "method": args.get('method', ''),
        "version": args.get('version', ''),
    }
    # cp_order_id+correlator+order_time+method+appKey
    sign_data = param['cp_order_id'] + param['correlator'] + param['order_time'] + param['method'] + APPKEY
    _sign = Algorithm.md5_encode(sign_data)
    if _sign != param['sign']:
        return 'failed'
    orderId = param['cp_order_id']
    parseInfo = Order.parse_order(orderId)
    if not parseInfo:
        return 'failed'
    orderInfo = Order.getOrderInfo(orderId)
    Context.Log.debug('orderInfo-----', orderInfo)
    if not orderInfo:
        return 'failed'

    res = {'sms_pay_check_resp':
            {'cp_order_id': param['cp_order_id'],
             'correlator': param['correlator'],
             'game_account': orderInfo['userId'],
             'fee': orderInfo['cost'],
             'if_pay': 0,
             'order_time': Time.current_ts(),
            }
          }
    return xmltodict.unparse(res)


def check_sign(param):
    # MD5(cp_order_id+correlator+result_code+fee+pay_type+method+appKey)
    sign_data = param['cp_order_id'] + param['correlator'] + param['result_code'] + param['fee'] + param['pay_type'] + param['method'] + APPKEY
    _sign = Algorithm.md5_encode(sign_data)
    if _sign == param['sign']:
        return Order.state_verify_success
    return Order.state_verify_failed_sign


def pay_callback(request):
    # {'correlator': 'F146580068521987', 'cp_order_id': '10020001Bcly60r5', 'result_code': '00', 'result_desc': '\xe6\x89\xa3\xe8\xb4\xb9\xe6\x88\x90\xe5\x8a\x9f', 'fee': '1', 'pay_type': 'alipay', 'method': 'callback', 'version': '1', 'sign': '732720cb83869e2a062deda60cde4f2e'}
    args = request.get_args()
    # cp_order_id correlator result_code fee pay_type method sign version
    param = {
        "cp_order_id": args.get('cp_order_id'),
        "correlator": args.get('correlator', ''),
        "result_code": args.get('result_code', ''),
        "fee": args.get('fee', ''),
        "pay_type": args.get('pay_type', ''),
        "method": args.get('method', ''),
        "sign": args.get('sign', ''),
        "version": args.get('version', ''),
    }

    orderId = param['cp_order_id']
    price = param['fee']

    if param['result_code'] != '00':
        Context.Log.info('result_code error-----', param['result_code'])
        return 'failed'

    parseInfo = Order.parse_order(orderId)
    if not parseInfo:
        return 'failed'

    orderInfo = Order.getOrderInfo(orderId)
    Context.Log.debug('orderInfo-----', orderInfo)
    if not orderInfo:
        return 'failed'

    state = int(orderInfo['state'])
    if state >= Order.state_pre_deliver:  # 可能并没有成功, 需要检查对单
        return '<cp_notify_resp><h_ret>0</h_ret><cp_order_id>%s</cp_order_id></cp_notify_resp>' % param['cp_order_id']

    cost = int(orderInfo['cost'])
    if int(float(price)) != cost:
        Context.Log.warn('price not equal', orderId, orderInfo, parseInfo)
        return 'failed'

    userId = int(orderInfo['userId'])
    gameId = int(orderInfo['gameId'])
    channel = orderInfo['channel']
    productId = orderInfo['productId']

    if not Order.judge_exist_product_id(2, productId):
        Context.Log.error('productId not exist', orderId, productId)
        return 'failed'

    result = check_sign(param)
    Order.updateOrder(orderId, state=result)
    if result != Order.state_verify_success:
        return 'failed'

    Order.updateOrder(orderId, state=Order.state_pre_deliver)
    kvs = {
        'payTime': Time.current_time(),
        'deliverTime': Time.current_time(),
        'thirdOrderId': param['correlator']
    }
    if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, 'NaN'):
        kvs['state'] = Order.state_deliver_success
    else:
        kvs['state'] = Order.state_deliver_failed

    Order.updateOrder(orderId, **kvs)
    return '<cp_notify_resp><h_ret>0</h_ret><cp_order_id>%s</cp_order_id></cp_notify_resp>' % param['cp_order_id']
