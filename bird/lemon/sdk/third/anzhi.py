# -*- coding:utf-8 -*-
"""
created by cui
"""

from Crypto.Cipher import DES3
from sdk.const import Const
from sdk.modules.user import User
from sdk.modules.order import Order
from framework.context import Context
from framework.util.tool import Time
from framework.util.tool import Algorithm
from sdk.modules.account import Account
from framework.entity.msgpack import MsgPack

ANZHI_URL = 'http://user.anzhi.com/web/api/sdk/third/1/queryislogin'

APPKEY = '1461652316012fsM7rLJ5OW2QUzOAy'
APPSECRET = '8Y1Foa3xY9CtK9QLIU4Tgq40'


def verify_login(sid):
    _time = Time.datetime_now('%Y%m%d%H%M%S001')
    sign = Algorithm.base64_encode(APPKEY + sid + APPSECRET)
    data = {'time': int(_time), 'appkey': APPKEY, 'sid': sid, 'sign': sign}
    res = Context.WebPage.wait_for_page(ANZHI_URL, postdata=data)
    # todo: 安智的bug, 等安智修改后恢复
    return Context.json_loads(res, ex=True)


def UnPaddingPKCS7(data):
    padlen = ord(data[-1])
    if padlen > 8:
        return data

    end = len(data)
    start = len(data) - padlen
    for i in range(start, end):
        if ord(data[i]) != padlen:
            return False
    return data[:start]


def PaddingPKCS7(data):
    padlen = 8 - len(data) % 8
    for i in range(padlen):
        data += chr(padlen)
    return data


def login_anzhi(mi, request):
    param = User.getParam(mi, 'accessToken', 'devName', 'nickName')
    result = verify_login(param['accessToken'])

    if result.get('sc') != '1':
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)

    # todo: 安智的bug, 等安智修改后恢复
    msg = Context.json_loads(Algorithm.base64_decode(result['msg']), ex=True)
    gid = param['gameId']
    openid = msg['uid']
    userId = Context.RedisMix.hash_get('anzhi.%s.uid' % gid, openid, None)
    if not userId:
        channel = 'anzhi'
        idType = Const.IDTYPE_ANZHI
        userId = User.register(param, request, openid, idType, channel)
        if not userId:
            return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
        Context.RedisMix.hash_set('anzhi.%s.uid' % gid, openid, userId)
    userId = int(userId)
    userInfo = Account.getUserInfo(userId)

    return User.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, False, openid=openid, loginChannelId=param['channelid'])


def pay_callback(request):
    if not request.args.get('data'):
        return 'failed'

    data = request.args.get('data')[0]

    Context.Log.debug('anzhi data-----------', data)
    d = DES3.new(APPSECRET, DES3.MODE_ECB)
    data = Algorithm.base64_decode(data)
    try:
        c = d.decrypt(data)
        c = UnPaddingPKCS7(c)
        data = Context.json_loads(c)
    except Exception, e:
        Context.Log.exception('anzhi pay callback-----------')
        return 'failed'

    Context.Log.debug(data)

    if type(data) is not dict or not data.get('code'):
        Context.Log.debug('anzhi code error-----------')
        return 'failed'

    orderId = ''
    if data.get('cpInfo'):
        orderId = data.get('cpInfo')

    orderAmount = data.get('orderAmount', 0)
    redBagMoney = data.get('redBagMoney', 0)

    code = ''
    if data.get('code'):
        code = data.get('code')

    orderInfo = Order.getOrderInfo(orderId)
    if not orderInfo:
        Context.Log.debug('anzhi orderInfo error-----------')
        return 'failed'

    parseInfo = Order.parse_order(orderId)
    if not parseInfo:
        Context.Log.debug('anzhi parseInfo error-----------')
        return 'failed'

    productId = orderInfo['productId']

    cost = int(orderInfo['cost'])
    if int(orderAmount) + int(redBagMoney) != cost * 100:
        Context.Log.warn('price not equal', cost, orderAmount)
        return 'failed'

    state = int(orderInfo['state'])
    if state >= Order.state_pre_deliver:  # 可能并没有成功, 需要检查对单
        return 'success'

    gameId = int(orderInfo['gameId'])
    userId = int(orderInfo['userId'])

    if code != 1:
        Context.Log.debug('anzhi code error-----------')
        return 'failed'

    Order.updateOrder(orderId, state=Order.state_pre_deliver)
    kvs = {
        'payTime': Time.current_time(),
        'deliverTime': Time.current_time(),
        'thirdOrderId': data.get('orderId', '')
    }
    if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, 'NaN'):
        kvs['state'] = Order.state_deliver_success
    else:
        kvs['state'] = Order.state_deliver_failed

    Order.updateOrder(orderId, **kvs)
    return 'success'
