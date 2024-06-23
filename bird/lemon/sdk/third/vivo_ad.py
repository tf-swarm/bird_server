# -*- coding:utf-8 -*-
"""
created by cui
"""

from sdk.modules.order import Order
from sdk.modules.entity import Entity
from framework.context import Context
from framework.util.tool import Time
from framework.util.exceptions import NotFoundException
from sdk.modules.user import User
from sdk.const import Const
from framework.entity.msgpack import MsgPack
from sdk.modules.account import Account
from framework.util.tool import Algorithm

URL_LOGIN = 'https://usrsys.vivo.com.cn/sdk/user/auth.do'
CP_ID = 'e571c8505c833f7a8641'
APPID = '101677385'
APPKEY = 'ce7776b7adac7234b6ad6d5fd6db3c99'

URL_GET_ORDER = 'https://pay.vivo.com.cn/vcoin/trade'
URL_QUERY_ORDER = 'https://pay.vivo.com.cn/vcoin/queryv2'
URL_NOTIFY_PAY = 'http://xmttbn.zxyzttbn.com:8080/v2/third/callback/vivo_ad/pay'

def verify_login(code):
    # 登录校验
    url = URL_LOGIN + '?authtoken=' + code
    res = Context.WebPage.wait_for_json(url)
    return res

def login(mi, request):
    param = User.getParam(mi, 'uid', 'accessToken')
    nick = param['nick']
    gid = param['gameId']
    openid = param['uid']
    paramAccess = param['accessToken']
    # 登录验证
    res = verify_login(paramAccess)
    if res.get('retcode'):
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)

    paramChannel = param['channelid']
    realChannel = paramChannel.split('_')[0]
    userId = Context.RedisMix.hash_get('%s.%s.uid' % (realChannel, gid), openid, None)

    if not userId:
        param['nick'] = nick
        channel = paramChannel
        idType = Const.IDTYPE_SDK
        userId = User.register(param, request, openid, idType, channel)
        if not userId:
            return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
        Context.RedisMix.hash_set('%s.%s.uid' % (realChannel, gid), openid, userId)

    access = mi.get_param('channelID')
    if access:
        Context.Data.setnx_attr(userId, 'in_access', access)

    userId = int(userId)
    userInfo = Account.getUserInfo(userId)
    return User.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, True, openid=openid, loginChannelId=param['channelid'])


def parse(dt):
    Context.Log.debug(dt)
    param = {
        "respCode": dt.get('respCode', ''),
        "respMsg": dt.get('respMsg', ''),
        "signMethod": dt.get('signMethod', ''),
        "signature": dt.get('signature', ''),
        "tradeType": dt.get('tradeType', ''),
        "tradeStatus": dt.get('tradeStatus', ''),
        "cpId": dt.get('cpId', ''),
        "appId": dt.get('appId', ''),
        "uid": dt.get('uid', ''),
        "cpOrderNumber": dt.get('cpOrderNumber', ''),
        "orderNumber": dt.get('orderNumber', ''),
        "orderAmount": dt.get('orderAmount', ''),
        "extInfo": dt.get('extInfo', ''),
        "payTime": dt.get('payTime', ''),
    }
    return param


def check_sign(param):
    sign = get_sign(param)
    if sign == param['signature']:
        return Order.state_verify_success
    return Order.state_verify_failed_sign


def pay_callback(request):
    args = request.get_args()
    param = parse(args)

    orderId = param['cpOrderNumber']
    price = param['orderAmount']

    if param.get('respCode', 0) != '200':
        raise NotFoundException

    parseInfo = Order.parse_order(orderId)
    if not parseInfo:
        raise NotFoundException

    orderInfo = Order.getOrderInfo(orderId)
    Context.Log.debug('orderInfo-----', orderInfo)
    if not orderInfo:
        raise NotFoundException

    state = int(orderInfo['state'])
    if state >= Order.state_pre_deliver:  # 可能并没有成功, 需要检查对单
        return 'success'

    cost = int(float(orderInfo['cost']) * 100)
    if int(float(price)) != cost:
        Context.Log.warn('price not equal', orderId, orderInfo, parseInfo)
        raise NotFoundException

    userId = int(orderInfo['userId'])
    gameId = int(orderInfo['gameId'])
    channel = orderInfo['channel']
    productId = orderInfo['productId']

    if not Order.judge_exist_product_id(2, productId):
        Context.Log.error('productId not exist', orderId, productId)
        raise NotFoundException

    result = check_sign(param)
    Order.updateOrder(orderId, state=result)
    if result != Order.state_verify_success:
        raise NotFoundException

    Order.updateOrder(orderId, state=Order.state_pre_deliver)
    kvs = {
        'payTime': Time.current_time(),
        'deliverTime': Time.current_time(),
        'thirdOrderId2': param['orderNumber']
    }
    if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, orderInfo['paytype']):
        kvs['state'] = Order.state_deliver_success
    else:
        kvs['state'] = Order.state_deliver_failed

    Order.updateOrder(orderId, **kvs)
    return 'success'

def get_sign(param):
    keys = param.keys()
    keys.sort()
    if 'signMethod' in keys:
        keys.remove('signMethod')
    if 'signature' in keys:
        keys.remove('signature')
    sign_data = ''
    for key in keys:
        v = param.get(key)
        if v == None or v == '':
            continue
        if sign_data:
            sign_data += '&'
        sign_data += key
        sign_data += '='
        if type(v) == int:
            v = str(v)
        if type(v) == unicode:
            v = v.encode('utf8')
        sign_data += v
    _CPKEY = Algorithm.md5_encode(APPKEY)
    sign = Algorithm.md5_encode(sign_data + '&' + _CPKEY)
    return sign

def get_vivo_trade(cpOrderNumber, price, orderTitle, orderDesc):
    # 登录校验
    data = {
        'version': '1.0.0',
        'signMethod': 'MD5',
        'cpId': CP_ID,
        'appId': APPID,
        'cpOrderNumber': cpOrderNumber,
        'notifyUrl': URL_NOTIFY_PAY,
        'orderTime': Time.current_time('%Y%m%d%H%M%S'),
        'orderAmount': price,       # 单位为分
        'orderTitle': orderTitle,   # 商品名
        'orderDesc': orderDesc,     # 商品描述
        'extInfo': 'vivopay'
    }
    sign = get_sign(data)
    data.update({'signature': sign})

    res = Context.WebPage.wait_for_json(URL_GET_ORDER, postdata=data)
    return res

# 获取预订单
def unifiedOrderPay(mi, request):
    gid = mi.get_param('gameId', 2)
    productId = mi.get_param('pid', '0')
    uid = mi.get_param('uid', 0)
    payType = 3 #mi.get_param('paytype', 3)  # 第三方支付方式
    if not Order.judge_exist_product_id(gid, productId):
        return MsgPack.Error(0, 1, 1)  # 无此产品
    # 获取产品信息
    #productInfo = product_config[productId]
    dt = Time.datetime()
    # 生成订单id
    order_info = Order.otherCreateOrder(gid, uid, productId, "vivo", "android")
    if order_info.is_error():
        return MsgPack.Error(0, 8, 'order create fail')

    order_id = order_info.get_param('orderId')

    kvs = {
        'thirdOrderId': 0,
        'paytype': payType
    }
    Order.updateOrder(order_id, **kvs)

    ret = get_vivo_trade(order_id, int(order_info.get_param('price') * 100), order_info.get_param('title'), order_info.get_param('title'))
    if ret.get('respCode', 0) != '200':
        return MsgPack.Error(0, 8, 'order create fail')

    kvs = {
        'thirdOrderId': ret.get('orderNumber', 0),
    }
    Order.updateOrder(order_id, **kvs)

    #orderAmount
    #signMethod
    #signature

    dictInfo = {}
    dictInfo['pid'] = productId
    dictInfo['orderid'] = order_id
    dictInfo['paytype'] = payType
    dictInfo['notify_url'] = URL_NOTIFY_PAY
    dictInfo['p_name'] = order_info.get_param('title')
    dictInfo['p_desc'] = order_info.get_param('title')
    dictInfo['price'] = order_info.get_param('price')
    dictInfo['accessKey'] = ret.get('accessKey', 0)
    dictInfo['orderNumber'] = ret.get('orderNumber', 0)

    return MsgPack(0, dictInfo)

# 主动向平台sdk验证订单
def verify_order(orderId):
    parseInfo = Order.parse_order(orderId)
    if not parseInfo:
        raise NotFoundException

    orderInfo = Order.getOrderInfo(orderId)
    Context.Log.debug('orderInfo-----', orderInfo)
    if not orderInfo:
        raise NotFoundException

    price = int(float(orderInfo['cost']) * 100)
    thirdOrderId = orderInfo['thirdOrderId']

    data = {
        'version': '1.0.0',
        'signMethod': 'MD5',
        'cpId': CP_ID,
        'appId': APPID,
        'cpOrderNumber': orderId,
        'orderNumber': thirdOrderId,
        'orderAmount': price,  # 单位为分
    }
    sign = get_sign(data)
    data.update({'signature': sign})

    res = Context.WebPage.wait_for_json(URL_QUERY_ORDER, postdata=data)
    if res.get('respCode', 0) == '200' and res.get('tradeStatus', 0) == '0000':
        return order_success
    else:
        return order_wait


order_wait = 0   # 订单等待中，等待一段时间再次校验
order_fail = -1   # 订单不存在或者是失败订单
order_success = 1  # 订单成功

# 主动查询订单
def orderquery(orderId):
    res = verify_order(orderId)
    return res
