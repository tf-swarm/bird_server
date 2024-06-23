# -*- coding:utf-8 -*-
"""
created by cui
"""

from sdk.const import Const
from sdk.modules.user import User
from sdk.modules.order import Order
from framework.context import Context
from framework.util.tool import Time
from sdk.modules.account import Account
from framework.util.tool import Algorithm
from framework.entity.msgpack import MsgPack

URL = 'http://passport.qiaogame.com/user/visit/'

cid = '0000000057fb6b110157fb6b11200000'
cpid = '0000000057e4f5c20157e4f5c28e0000'
cKey = 'uaI4wi+2XcQ='


def verify_login(token):
    data = {'access_token': token, 'cid': cid, 'timestamp': Time.current_ts()}
    sign = get_sign(data)
    data['signatrue'] = sign
    res = Context.WebPage.wait_for_json(URL, postdata=data)
    code = res.get('code')
    if code == 200:
        return 1, res.get('data')
    else:
        Context.Log.debug('HX pay login error', res.get('msg'))
        return 0, res.get('msg')


def login(mi, request):
    param = User.getParam(mi, 'accessToken', 'devName')
    if len(param['accessToken']) <= 1:
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)

    result, data = verify_login(param['accessToken'])
    if not result or not data:
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)

    gid = param['gameId']
    openid = data.get('uid')
    # user_name = result.get('name')
    userId = Context.RedisMix.hash_get('hxpay.%s.uid' % gid, openid, None)
    if not userId:
        channel = 'hxpay'
        idType = Const.IDTYPE_hxpay
        userId = User.register(param, request, openid, idType, channel)
        if not userId:
            return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
        Context.RedisMix.hash_set('hxpay.%s.uid' % gid, openid, userId)
    userId = int(userId)
    userInfo = Account.getUserInfo(userId)

    return User.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, False, openid=openid, loginChannelId=param['channelid'])


def parse(dt):
    Context.Log.debug(dt)

    param = {
        "chid": dt.get('chid'),
        "order_no": dt.get('order_no'),
        "subject": dt.get('subject'),
        "cid": dt.get('cid'),
        "amount": dt.get('amount'),
        "time": dt.get('time'),
        "user_id": dt.get('user_id'),
        "out_trade_no": dt.get('out_trade_no'),
        "billing_code": dt.get('billing_code'),
        "trade_status": dt.get('trade_status'),
        "payment_id": dt.get('payment_id'),
        "extra": dt.get('extra'),
        "sign_type": dt.get('sign_type'),
        "sign": dt.get('sign'),
    }
    return param


def get_sign(param):
    keys = param.keys()
    keys.sort()
    if 'sign' in keys:
        keys.remove('sign')
    if 'sign_type' in keys:
        keys.remove('sign_type')
    sign_data = ''
    for k in sorted(keys, key=str.lower):
        v = param.get(k)
        if v is None:
            continue
        if sign_data:
            sign_data += '&'
        sign_data += k
        sign_data += '='
        if type(v) == int:
            v = str(v)
        if type(v) == unicode:
            v = v.encode('utf8')
        sign_data += v
    sign_data += cKey
    return Algorithm.md5_encode(sign_data)


def check_sign(param):
    if param['sign'] != get_sign(param):
        return Order.state_verify_failed_sign
    return Order.state_verify_success


def pay_callback(request):
    args = request.get_args()
    param = parse(args)
    Context.Log.debug(param)

    if 'trade_status' not in param or param['trade_status'] != 'SUCCESS':
        return '1'
    orderId = param['out_trade_no']
    price = param['amount']

    parseInfo = Order.parse_order(orderId)
    if not parseInfo:
        return '2'

    orderInfo = Order.getOrderInfo(orderId)
    Context.Log.debug('orderInfo-----', orderInfo)
    if not orderInfo:
        return '3'

    state = int(orderInfo['state'])
    if state >= Order.state_pre_deliver:  # 可能并没有成功, 需要检查对单
        return 'SUCCESS'

    cost = int(orderInfo['cost']) * 100
    if int(float(price)) != cost:
        Context.Log.warn('price not equal', orderId, orderInfo, parseInfo)
        return '4'

    userId = int(orderInfo['userId'])
    gameId = int(orderInfo['gameId'])
    productId = orderInfo['productId']

    if not Order.judge_exist_product_id(2, productId):
        Context.Log.error('productId not exist', orderId, productId)
        return '5'

    result = check_sign(param)
    Order.updateOrder(orderId, state=result)
    if result != Order.state_verify_success:
        return '6'

    Order.updateOrder(orderId, state=Order.state_pre_deliver)
    kvs = {
        'payTime': Time.current_time(),
        'deliverTime': Time.current_time(),
        'thirdOrderId': param['order_no']
    }
    if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, 'NaN'):
        kvs['state'] = Order.state_deliver_success
    else:
        kvs['state'] = Order.state_deliver_failed

    Order.updateOrder(orderId, **kvs)
    return 'SUCCESS'
