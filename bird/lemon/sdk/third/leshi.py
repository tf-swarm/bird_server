# -*- coding:utf-8 -*-
"""
created by cui
"""

from sdk.const import Const
from sdk.modules.user import User
from sdk.modules.order import Order
from framework.context import Context
from framework.util.tool import Time
from framework.util.tool import Algorithm
from framework.entity.msgpack import MsgPack
from sdk.modules.account import Account

LESHI_URL = 'https://sso.letv.com/oauthopen/userbasic'

CLIENTID = '297878'
APPKEY = '40e77f12cda342299ae66ef00cf661c3'
SECRETKEY = 'a1026287465b4ee8b268754ecd3ee609'


def login(mi, request):
    param = User.getParam(mi, 'accessToken', 'devName', 'uid')
    if len(param['accessToken']) <= 1:
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
    res = verify_login(param['accessToken'], param['uid'])

    gid = param['gameId']
    openid = param['uid']
    if not res.get('result') or res.get('result').get('letv_uid') != openid:
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)

    userId = Context.RedisMix.hash_get('leshi.%s.uid' % gid, openid, None)
    if not userId:
        channel = 'leshi'
        idType = Const.IDTYPE_LESHI
        userId = User.register(param, request, openid, idType, channel)
        if not userId:
            return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
        Context.RedisMix.hash_set('leshi.%s.uid' % gid, openid, userId)
    userId = int(userId)
    userInfo = Account.getUserInfo(userId)

    return User.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, False, openid=openid, loginChannelId=param['channelid'])


def verify_login(token, uid):
    data = {'client_id': CLIENTID, 'access_token': token, 'uid': uid}
    res = Context.WebPage.wait_for_json(LESHI_URL, method='GET', query=data)
    return res


def parse(dt):
    Context.Log.debug(dt)
    param = {
        "app_id": dt.get('app_id'),
        "lepay_order_no": dt.get('lepay_order_no', ''),
        "letv_user_id": dt.get('letv_user_id', ''),
        "out_trade_no": dt.get('out_trade_no', ''),
        "pay_time": dt.get('pay_time', ''),
        "price": dt.get('price', ''),
        "product_id": dt.get('product_id', ''),
        "sign": dt.get('sign', ''),
        "sign_type": dt.get('sign_type', ''),
        "trade_result": dt.get('trade_result', ''),
        "version": dt.get('version', ''),
        "cooperator_order_no": dt.get('cooperator_order_no', ''),
        "extra_info": dt.get('extra_info'),
        "original_price": dt.get('original_price'),
    }
    return param


def check_sign(param):
    keys = param.keys()
    keys.sort()
    keys.remove('sign')
    sign_data = ''
    for key in keys:
        if sign_data:
            sign_data += '&'
        sign_data += key
        sign_data += '='
        sign_data += param.get(key, '')
    sign = Algorithm.md5_encode(sign_data + '&key=' + SECRETKEY)
    if sign == param['sign']:
        return Order.state_verify_success
    return Order.state_verify_failed_sign


def pay_callback(request):
    args = request.get_args()
    param = parse(args)

    orderId = param['cooperator_order_no']
    price = param['original_price']

    parseInfo = Order.parse_order(orderId)
    if not parseInfo:
        return 'fail'

    orderInfo = Order.getOrderInfo(orderId)
    Context.Log.debug('orderInfo-----', orderInfo)
    if not orderInfo:
        return 'fail'

    state = int(orderInfo['state'])
    if state >= Order.state_pre_deliver:  # 可能并没有成功, 需要检查对单
        return 'success'

    cost = int(orderInfo['cost'])
    if int(float(price)) != cost:
        Context.Log.warn('price not equal', orderId, orderInfo, parseInfo)
        return 'fail'

    userId = int(orderInfo['userId'])
    gameId = int(orderInfo['gameId'])
    channel = orderInfo['channel']
    productId = orderInfo['productId']

    if not Order.judge_exist_product_id(2, productId):
        Context.Log.error('productId not exist', orderId, productId)
        return 'fail'

    result = check_sign(param)
    Order.updateOrder(orderId, state=result)
    if result != Order.state_verify_success:
        return 'fail'

    Order.updateOrder(orderId, state=Order.state_pre_deliver)
    kvs = {
        'payTime': Time.current_time(),
        'deliverTime': Time.current_time(),
        'thirdOrderId': param['lepay_order_no']
    }
    if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, 'NaN'):
        kvs['state'] = Order.state_deliver_success
    else:
        kvs['state'] = Order.state_deliver_failed

    Order.updateOrder(orderId, **kvs)
    return 'success'
