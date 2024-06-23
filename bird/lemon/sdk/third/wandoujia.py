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

WANDOUJIA_URL = 'https://pay.wandoujia.com/api/uid/check'

APPID = '100039060'
APPKEY = '89aa39533669b3869367ee33d6625deb'

publickey = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCd95FnJFhPinpNiE/h4VA6bU1rzRa5+a25BxsnFX8TzquWxqDCoe4xG6QKXMXuKvV57tTRpzRo2jeto40eHKClzEgjx9lTYVb2RFHHFWio/YGTfnqIPTVpi7d7uHY+0FZ0lYL5LlW4E2+CQMxFOPRwfqGzMjs1SDlH7lVrLEVy6QIDAQAB
-----END PUBLIC KEY-----'''


def login(mi, request):
    param = User.getParam(mi, 'accessToken', 'devName', 'uid')
    if len(param['accessToken']) <= 1:
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
    res = verify_login(param['accessToken'], param['uid'])

    if not res:
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)

    gid = param['gameId']
    openid = param['uid']
    userId = Context.RedisMix.hash_get('wandoujia.%s.uid' % gid, openid, None)
    if not userId:
        channel = 'wandoujia'
        idType = Const.IDTYPE_WANDOUJIA
        userId = User.register(param, request, openid, idType, channel)
        if not userId:
            return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
        Context.RedisMix.hash_set('wandoujia.%s.uid' % gid, openid, userId)
    userId = int(userId)
    userInfo = Account.getUserInfo(userId)

    return User.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, False, openid=openid, loginChannelId=param['channelid'])


def verify_login(token, uid):
    data = {'appkey_id': APPKEY, 'token': token, 'uid': uid}
    res = Context.WebPage.wait_for_json(WANDOUJIA_URL, postdata=data)
    return res


def parse(dt):
    Context.Log.debug(dt)
    param = {}
    content = dt.get('content')
    if content:
        param['content'] = content
        param['sign'] = dt.get('sign')

        content = Context.json_loads(content)

        param['timeStamp'] = content.get('timeStamp')
        param['orderId'] = content.get('orderId')
        param['money'] = content.get('money')
        param['chargeType'] = content.get('chargeType')
        param['appKeyId'] = content.get('appKeyId')
        param['buyerId'] = content.get('buyerId')
        param['cardNo'] = content.get('cardNo')

        if content.get('cardNo'):
            param['cardNo'] = content.get('cardNo')
        else:
            param['cardNo'] = 'null'

        param['out_trade_no'] = content.get('out_trade_no', '')

    return param


def check_sign(param):
    if Algorithm.verify_rsa(publickey, param['content'], param['sign']):
        return Order.state_verify_success
    return Order.state_verify_failed_sign


def pay_callback(request):
    args = request.get_args()
    param = parse(args)

    if not param.get('content'):
        return 'failed'

    orderId = param['out_trade_no']
    price = param['money']

    parseInfo = Order.parse_order(orderId)
    if not parseInfo:
        return 'failed'

    orderInfo = Order.getOrderInfo(orderId)
    Context.Log.debug('orderInfo-----', orderInfo)
    if not orderInfo:
        return 'failed'

    state = int(orderInfo['state'])
    if state >= Order.state_pre_deliver:  # 可能并没有成功, 需要检查对单
        return 'success'

    cost = int(orderInfo['cost'])
    if int(float(price)) != cost * 100:
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
        'thirdOrderId': param['orderId']
    }
    if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, 'NaN'):
        kvs['state'] = Order.state_deliver_success
    else:
        kvs['state'] = Order.state_deliver_failed

    Order.updateOrder(orderId, **kvs)
    return 'success'
