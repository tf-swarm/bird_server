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

XUNLEI_URL = 'http://websvr.niu.xunlei.com/checkAppUser.gameUserInfo'
GAME_ID = '050373'

APPKEY = 'tZdOU1ujtABuWbIQYTSIa8JtVAhWUGBs'
PAYKEY = '02wt4vRmSxfbR6lJmkZzMSia'


def login(mi, request):
    param = User.getParam(mi, 'accessToken', 'devName', 'uid')
    if len(param['accessToken']) <= 1:
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
    res = verify_login(param['accessToken'], param['uid'])

    if res.get('code') != 0:
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)

    gid = param['gameId']
    openid = param['uid']
    # user_name = result.get('name')
    userId = Context.RedisMix.hash_get('xunlei.%s.uid' % gid, openid, None)
    if not userId:
        channel = 'xunlei'
        idType = Const.IDTYPE_XUNLEI
        userId = User.register(param, request, openid, idType, channel)
        if not userId:
            return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
        Context.RedisMix.hash_set('xunlei.%s.uid' % gid, openid, userId)
    userId = int(userId)
    userInfo = Account.getUserInfo(userId)

    return User.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, False, openid=openid, loginChannelId=param['channelid'])


def verify_login(customerKey, customerid):
    data = {'gameid': GAME_ID, 'customerid': customerid, 'customerKey': customerKey}
    res = Context.WebPage.wait_for_json(XUNLEI_URL, postdata=data)
    return res


def parse(dt):
    Context.Log.debug(dt)
    param = {
        # orderid user gold money time sign server ext
        "orderid": dt.get('orderid', ''),
        "user": dt.get('user', ''),
        "gold": dt.get('gold', ''),
        "money": dt.get('money', ''),
        "time": dt.get('time', ''),
        "sign": dt.get('sign', ''),
        "ext": dt.get('ext', ''),
    }
    return param


def check_sign(param):
    sign = Algorithm.md5_encode(param['orderid'] + param['user'] + param['gold'] + param['money'] + param['time'] + PAYKEY)
    if sign == param['sign']:
        return Order.state_verify_success
    return Order.state_verify_failed_sign


def pay_callback(request):
    args = request.get_args()
    param = parse(args)

    orderId = param['ext']
    price = param['money']

    parseInfo = Order.parse_order(orderId)
    if not parseInfo:
        return -2

    orderInfo = Order.getOrderInfo(orderId)
    Context.Log.debug('orderInfo-----', orderInfo)
    if not orderInfo:
        return -2

    state = int(orderInfo['state'])
    if state >= Order.state_pre_deliver:  # 可能并没有成功, 需要检查对单
        return 1

    cost = int(orderInfo['cost'])
    if int(float(price)) != cost:
        Context.Log.warn('price not equal', orderId, orderInfo, parseInfo)
        return -2

    userId = int(orderInfo['userId'])
    gameId = int(orderInfo['gameId'])
    channel = orderInfo['channel']
    productId = orderInfo['productId']

    if not Order.judge_exist_product_id(2, productId):
        Context.Log.error('productId not exist', orderId, productId)
        return -2

    result = check_sign(param)
    Order.updateOrder(orderId, state=result)
    if result != Order.state_verify_success:
        return -2

    Order.updateOrder(orderId, state=Order.state_pre_deliver)
    kvs = {
        'payTime': Time.current_time(),
        'deliverTime': Time.current_time(),
        'thirdOrderId': param['orderid']
    }
    if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, 'NaN'):
        kvs['state'] = Order.state_deliver_success
    else:
        kvs['state'] = Order.state_deliver_failed

    Order.updateOrder(orderId, **kvs)
    return 1
