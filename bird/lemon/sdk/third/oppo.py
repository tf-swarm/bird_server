# -*- coding:utf-8 -*-
"""
created by cui
"""

import urllib
import random
from sdk.const import Const
from sdk.modules.user import User
from sdk.modules.order import Order
from framework.context import Context
from framework.util.tool import Time
from framework.util.tool import Algorithm
from framework.entity.msgpack import MsgPack
from sdk.modules.account import Account

URL_NOTIFY_PAY = 'http://xmttbn.zxyzttbn.com:8080/v2/third/callback/oppo/pay'

OPPO_URL = 'http://i.open.game.oppomobile.com/gameopen/user/fileIdInfo'
APPID = '6840'
APPKEY = 'c5OU7l7vu6o80sg4G0KK8wK8G'
SECRETKEY = '9a2701ab8B39e7f228250744a2b8A47B'

publickey = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCmreYIkPwVovKR8rLHWlFV
w7YDfm9uQOJKL89Smt6ypXGVdrAKKl0wNYc3/jecAoPi2ylChfa2iRu5gunJy
NmpWZzlCNRIau55fxGW0XEu553IiprOZcaw5OuYGlf60ga8QT6qToP0/dpiL/Z
bmNUO9kUhosIjEu22uFgR+5cYyQIDAQAB
-----END PUBLIC KEY-----'''


def login(mi, request):
    param = User.getParam(mi, 'uid')
    nick = param['nick']
    gid = param['gameId']
    openid = param['uid']
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

    userId = int(userId)
    userInfo = Account.getUserInfo(userId)
    return User.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, True, openid=openid, loginChannelId=param['channelid'])

def verify_login(token, ssoid):
    # _url = 'fileId=URLEncoder.encode(ssoid ， "UTF-8")&token= URLEncoder.encode(token,"UTF-8")'
    _token = urllib.quote_plus(token)
    data = {"fileId": ssoid, "token": token}

    param = 'oauthConsumerKey=%s&oauthToken=%s&oauthSignatureMethod=HMAC-SHA1&oauthTimestamp=%s&oauthNonce=%s&oauthVersion=1.0&' % (APPKEY, _token, Time.current_ts(), random.randint(1, 10))
    sign = Algorithm.hmac_sha1(SECRETKEY + '&', param).digest().encode('base64').rstrip()
    sign = urllib.quote_plus(sign)
    headers = {'param': param, 'oauthSignature': sign}
    res = Context.WebPage.wait_for_json(OPPO_URL, method='GET', query=data, headers=headers)
    return res


def parse(dt):
    param = {
        "notifyId": dt.get('notifyId', ''),
        "partnerOrder": dt.get('partnerOrder', ''),
        "productName": dt.get('productName', ''),
        "productDesc": dt.get('productDesc', ''),
        "price": dt.get('price', 0),
        "count": dt.get('count', 0),
        "attach": dt.get('attach', ''),
        "sign": dt.get('sign', ''),
    }
    return param


def check_sign(param):
    fields = ['notifyId', 'partnerOrder', 'productName', 'productDesc', 'price', 'count', 'attach']
    sign_data = '&'.join('%s=%s' % (f, param[f]) for f in fields)

    if Algorithm.verify_rsa_oppo(publickey, sign_data, param['sign']):
        return Order.state_verify_success
    return Order.state_verify_failed_sign


def pay_callback(request):
    args = request.get_args()
    param = parse(args)

    orderId = param['partnerOrder']
    price = param['price']

    parseInfo = Order.parse_order(orderId)
    if not parseInfo:
        return urllib.urlencode({'result': 'FAIL', 'resultMsg': 'orderId1 error'})

    orderInfo = Order.getOrderInfo(orderId)
    Context.Log.debug('orderInfo-----', orderInfo)
    if not orderInfo:
        return urllib.urlencode({'result': 'FAIL', 'resultMsg': 'orderId error'})

    state = int(orderInfo['state'])
    if state >= Order.state_pre_deliver:  # 可能并没有成功, 需要检查对单
        return urllib.urlencode({'result': 'OK', 'resultMsg': 'success'})

    cost = float(orderInfo['cost'])
    if int(float(price)) != int(cost * 100):
        Context.Log.warn('price not equal', orderId, orderInfo, parseInfo)
        return urllib.urlencode({'result': 'FAIL', 'resultMsg': 'price error'})

    userId = int(orderInfo['userId'])
    gameId = int(orderInfo['gameId'])
    channel = orderInfo['channel']
    productId = orderInfo['productId']

    if not Order.judge_exist_product_id(2, productId):
        Context.Log.error('productId not exist', orderId, productId)
        return urllib.urlencode({'result': 'FAIL', 'resultMsg': 'productId error'})

    result = check_sign(param)
    Order.updateOrder(orderId, state=result)
    if result != Order.state_verify_success:
        return urllib.urlencode({'result': 'FAIL', 'resultMsg': 'fail to verify signature'})

    Order.updateOrder(orderId, state=Order.state_pre_deliver)
    kvs = {
        'payTime': Time.current_time(),
        'deliverTime': Time.current_time(),
        'thirdOrderId': param['notifyId']
    }
    if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, orderInfo['paytype']):
        kvs['state'] = Order.state_deliver_success
    else:
        kvs['state'] = Order.state_deliver_failed

    Order.updateOrder(orderId, **kvs)
    return urllib.urlencode({'result': 'OK', 'resultMsg': 'success'})

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
    order_info = Order.otherCreateOrder(gid, uid, productId, "oppo", "android")
    if order_info.is_error():
        return MsgPack.Error(0, 8, 'order create fail')

    order_id = order_info.get_param('orderId')

    kvs = {
        'thirdOrderId': 0,
        'paytype': payType
    }
    Order.updateOrder(order_id, **kvs)

    dictInfo = {}
    dictInfo['pid'] = productId
    dictInfo['orderid'] = order_id
    dictInfo['paytype'] = payType
    dictInfo['notify_url'] = URL_NOTIFY_PAY
    dictInfo['p_name'] = order_info.get_param('title')
    dictInfo['p_desc'] = order_info.get_param('title')
    dictInfo['price'] = order_info.get_param('price')

    return MsgPack(0, dictInfo)
