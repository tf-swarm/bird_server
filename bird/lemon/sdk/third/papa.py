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

PAPA_URL = 'https://sdk.papa91.com/auth/check_token'

APPID = '16000183'
APPKEY = '16000183'
SECRETKEY = 'b46c07d094b70a8fd6c509bc9f93900e24479cc6de1938e2c735f65ba8140839'


def login(mi, request):
    param = User.getParam(mi, 'accessToken', 'devName', 'uid')
    if len(param['accessToken']) <= 1:
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
    res = verify_login(param['accessToken'], param['uid'])

    if not res.get('data') or not res.get('data').get('is_success'):
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)

    gid = param['gameId']
    openid = param['uid']
    # user_name = result.get('name')
    userId = Context.RedisMix.hash_get('papa.%s.uid' % gid, openid, None)
    if not userId:
        channel = 'papa'
        idType = Const.IDTYPE_PAPA
        userId = User.register(param, request, openid, idType, channel)
        if not userId:
            return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
        Context.RedisMix.hash_set('papa.%s.uid' % gid, openid, userId)
    userId = int(userId)
    userInfo = Account.getUserInfo(userId)

    return User.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, False, openid=openid, loginChannelId=param['channelid'])


def verify_login(token, uid):
    sign_data = 'app_key=%s&token=%s&uid=%s' % (APPKEY, token, uid)
    sign = Algorithm.md5_encode(APPKEY + SECRETKEY + sign_data)
    data = {'app_key': APPKEY, 'token': token, 'uid': uid, 'sign': sign}
    res = Context.WebPage.wait_for_json(PAPA_URL, postdata=data)
    return res


def parse(dt):
    Context.Log.debug(dt)
    param = {
        "app_key": dt.get('app_key'),
        "app_order_id": dt.get('app_order_id', ''),
        "app_district": dt.get('app_district', 0),
        "app_server": dt.get('app_server', 0),
        "app_user_id": dt.get('app_user_id', 0),
        "app_user_name": dt.get('app_user_name', ''),
        "product_id": dt.get('product_id', ''),
        "product_name": dt.get('product_name', ''),
        "money_amount": dt.get('money_amount', ''),
        "pa_open_uid": dt.get('pa_open_uid', ''),
        "app_extra1": dt.get('app_extra1', ''),
        "app_extra2": dt.get('app_extra2', ''),
        "pa_open_order_id": dt.get('pa_open_order_id', ''),
        "sign": dt.get('sign')
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
    sign = Algorithm.md5_encode(APPKEY + SECRETKEY + sign_data)
    if sign == param['sign']:
        return Order.state_verify_success
    return Order.state_verify_failed_sign


def pay_callback(request):
    args = request.get_args()
    param = parse(args)

    orderId = param['app_order_id']
    price = param['money_amount']

    parseInfo = Order.parse_order(orderId)
    if not parseInfo:
        return 'failed'

    orderInfo = Order.getOrderInfo(orderId)
    Context.Log.debug('orderInfo-----', orderInfo)
    if not orderInfo:
        return 'failed'

    state = int(orderInfo['state'])
    if state >= Order.state_pre_deliver:  # 可能并没有成功, 需要检查对单
        return 'ok'

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
        'thirdOrderId': param['pa_open_order_id']
    }
    if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, 'NaN'):
        kvs['state'] = Order.state_deliver_success
    else:
        kvs['state'] = Order.state_deliver_failed

    Order.updateOrder(orderId, **kvs)
    return 'ok'
