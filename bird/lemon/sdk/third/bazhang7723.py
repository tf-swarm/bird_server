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

GAMEID = '294'
APPID = '271'
APPKEY = '87c5264025e0985dbc4e4ddeb98e9d28'


def login(mi, request):
    param = User.getParam(mi, 'sign', 'userName', 'loginTime', 'devName')
    if len(param['sign']) <= 1:
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
    res = verify_login(param['sign'], param['userName'], param['loginTime'])

    if not res:
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)

    gid = param['gameId']
    openid = param['userName']
    userId = Context.RedisMix.hash_get('bazhang7723.%s.uid' % gid, openid, None)
    if not userId:
        channel = 'bazhang7723'
        idType = Const.IDTYPE_BAZHANG7723
        userId = User.register(param, request, openid, idType, channel)
        if not userId:
            return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
        Context.RedisMix.hash_set('bazhang7723.%s.uid' % gid, openid, userId)
    userId = int(userId)
    userInfo = Account.getUserInfo(userId)

    return User.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, False, openid=openid, loginChannelId=param['channelid'])


def verify_login(sign, userName, loginTime):
    sign_data = 'username=%s&appkey=%s&logintime=%s' % (userName, APPKEY, loginTime)
    _sign = Algorithm.md5_encode(sign_data)
    if sign == _sign:
        return True
    return False


def parse(dt):
    # sign=MD5(“orderid=100000&username=zhangsan&gameid=6&roleid=zhangsanfeng& serverid=1&paytype=1&amount=1&paytime=20130101125612&attach=test&appkey=12312 3123213”)
    param = {
        "orderid": dt.get('orderid', ''),
        "username": dt.get('username', 0),
        "gameid": dt.get('gameid', ''),
        "roleid": dt.get('roleid', ''),
        "serverid": dt.get('serverid', 0),
        "paytype": dt.get('paytype', ''),
        "amount": dt.get('amount', 0),
        "paytime": dt.get('paytime', 0),
        "attach": dt.get('attach', ''),
        "sign": dt.get('sign', '')
    }
    return param


def check_sign(param):
    keys = ["orderid", "username", "gameid", "roleid", "serverid", "paytype", "amount", "paytime", "attach"]
    sign_data = ''
    for key in keys:
        if sign_data:
            sign_data += '&'
        sign_data += key
        sign_data += '='
        sign_data += param.get(key, '')
    sign = Algorithm.md5_encode(sign_data + '&appkey=' + APPKEY)
    if sign == param['sign']:
        return Order.state_verify_success
    return Order.state_verify_failed_sign


def pay_callback(request):
    args = request.get_args()
    param = parse(args)

    orderId = param['attach']
    price = param['amount']

    parseInfo = Order.parse_order(orderId)
    if not parseInfo:
        return 'error'

    orderInfo = Order.getOrderInfo(orderId)
    Context.Log.debug('orderInfo-----', orderInfo)
    if not orderInfo:
        return 'error'

    state = int(orderInfo['state'])
    if state >= Order.state_pre_deliver:  # 可能并没有成功, 需要检查对单
        return 'success'

    cost = int(orderInfo['cost'])
    if int(float(price)) != cost:
        Context.Log.warn('price not equal', orderId, orderInfo, parseInfo)
        return 'error'

    userId = int(orderInfo['userId'])
    gameId = int(orderInfo['gameId'])
    channel = orderInfo['channel']
    productId = orderInfo['productId']

    if not Order.judge_exist_product_id(2, productId):
        Context.Log.error('productId not exist', orderId, productId)
        return 'error'

    result = check_sign(param)
    Order.updateOrder(orderId, state=result)
    if result != Order.state_verify_success:
        return 'error'

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
    return 'success'
