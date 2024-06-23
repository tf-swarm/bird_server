# -*- coding:utf-8 -*-
"""
created by cui
"""

from sdk.const import Const
from sdk.modules.user import User
from sdk.modules.order import Order
from framework.context import Context
from framework.util.tool import Time
from sdk.modules.entity import Entity
from sdk.modules.account import Account
from framework.entity.msgpack import MsgPack

MEIZU_URL = 'https://api.game.meizu.com/game/security/checksession'
APPKEY = 'a03a46df21114f84a1d84021d0b15a23'


def login(mi, request):
    param = User.getParam(mi, 'accessToken', 'devName', 'uid')
    if len(param['accessToken']) <= 1:
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
    res = verify_login(param['accessToken'], param['uid'])

    if res.get('code') != 200:
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)

    gid = param['gameId']
    openid = param['uid']
    userId = Context.RedisMix.hash_get('meizu.%s.uid' % gid, openid, None)
    if not userId:
        channel = 'meizu'
        idType = Const.IDTYPE_MEIZU
        userId = User.register(param, request, openid, idType, channel)
        if not userId:
            return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
        Context.RedisMix.hash_set('meizu.%s.uid' % gid, openid, userId)
    userId = int(userId)
    userInfo = Account.getUserInfo(userId)

    return User.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, False, openid=openid, loginChannelId=param['channelid'])


def verify_login(token, uid):
    # app_id long Y  session_id  Y  uid Y ts Y sign_type Y sign
    data = {'app_id': Const.MEIZU_APPID, 'session_id': token, 'ts': Time.current_ts(), 'uid': uid, 'sign_type': 'md5'}
    sign = Entity.meizu_get_sign(data)
    data['sign'] = sign
    res = Context.WebPage.wait_for_json(MEIZU_URL, postdata=data)
    return res


def parse(dt):
    # app_id=464013&buy_amount=1&cp_order_id=2680&create_time=1413776092239&notify_id=1413776113206&notify_time=2014-10-20 11:35:13&order_id=14102000000298934&partner_id=5458428&pay_time=1413776113219&pay_type=0&product_id=2 &product_per_price=1.0&product_unit=枚&total_price=1.0&trade_status=3&uid=9700193&user_info=这里填写游戏相 关附加信息，发货时将回传该字段:appSecret 
    Context.Log.debug(dt)

    param = {
        "app_id": dt.get('app_id'),
        "buy_amount": dt.get('buy_amount', ''),
        "cp_order_id": dt.get('cp_order_id', ''),
        "create_time": dt.get('create_time', ''),
        "notify_id": dt.get('notify_id', ''),
        "notify_time": dt.get('notify_time', ''),
        "order_id": dt.get('order_id', ''),
        "partner_id": dt.get('partner_id', ''),
        "pay_time": dt.get('pay_time', ''),
        "pay_type": dt.get('pay_type', ''),
        "product_id": dt.get('product_id', ''),
        "product_per_price": dt.get('product_per_price', ''),
        "product_unit": dt.get('product_unit', ''),
        "total_price": dt.get('total_price', ''),
        "trade_status": dt.get('trade_status', ''),
        "uid": dt.get('uid', ''),
        "user_info": dt.get('user_info', ''),
        "sign": dt.get('sign'),
        "sign_type": dt.get('sign_type', ''),
    }
    return param


def check_sign(param):
    sign = Entity.meizu_get_sign(param)
    if sign == param['sign']:
        return Order.state_verify_success
    return Order.state_verify_failed_sign


def pay_callback(request):
    args = request.get_args()
    param = parse(args)

    orderId = param['cp_order_id']
    price = param['total_price']

    parseInfo = Order.parse_order(orderId)
    if not parseInfo:
        return 900000

    orderInfo = Order.getOrderInfo(orderId)
    Context.Log.debug('orderInfo-----', orderInfo)
    if not orderInfo:
        return 900000

    state = int(orderInfo['state'])
    if state >= Order.state_pre_deliver:  # 可能并没有成功, 需要检查对单
        return 200

    cost = int(orderInfo['cost'])
    if int(float(price)) != cost:
        Context.Log.warn('price not equal', orderId, orderInfo, parseInfo)
        return 900000

    userId = int(orderInfo['userId'])
    gameId = int(orderInfo['gameId'])
    channel = orderInfo['channel']
    productId = orderInfo['productId']

    if not Order.judge_exist_product_id(2, productId):
        Context.Log.error('productId not exist', orderId, productId)
        return 900000

    result = check_sign(param)
    Order.updateOrder(orderId, state=result)
    if result != Order.state_verify_success:
        return 900000

    Order.updateOrder(orderId, state=Order.state_pre_deliver)
    kvs = {
        'payTime': Time.current_time(),
        'deliverTime': Time.current_time(),
        'thirdOrderId': param['order_id']
    }
    if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, 'NaN'):
        kvs['state'] = Order.state_deliver_success
    else:
        kvs['state'] = Order.state_deliver_failed

    Order.updateOrder(orderId, **kvs)
    return 200
