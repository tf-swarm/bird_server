# -*- coding:utf-8 -*-
"""
created by cui
"""

import urllib
from sdk.const import Const
from sdk.modules.user import User
from sdk.modules.order import Order
from framework.context import Context
from framework.util.tool import Time
from sdk.modules.account import Account
from framework.util.tool import Algorithm
from framework.entity.msgpack import MsgPack
from framework.util.exceptions import NotFoundException

S360_URL = 'https://openapi.360.cn/user/me.json?'

URL_QUERY_ORDER = 'https://mgame.360.cn/pay/order_verify.json'

URL_GET_ORDER = 'https://mgame.360.cn/srvorder/get_token.json'

APPID = '204482411'
APPKEY = 'c10a9d7ae76b18e9d3bb05a93ca76768'
APPSECRET = '61d5d3c6edebe54b808ca6b82b6d47de'

URL_NOTIFY_PAY = 'http://xmttbn.zxyzttbn.com:8080/v2/third/callback/q360/pay' #'http://xmttbn.zxyzttbn.com:8080/v2/third/callback/vivo/pay'


def verify_login(token):
    url = '%saccess_token=%s&fields=id,name,avatar,sex,area,nick' % (S360_URL, token)
    response = Context.WebPage.wait_for_json(url, method='GET')
    return response


def login(mi, request):
    param = User.getParam(mi, 'accessToken', 'devName')
    if len(param['accessToken']) <= 1:
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
    result = verify_login(param['accessToken'])

    if result is None:
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)

    gid = param['gameId']
    openid = result.get('id')
    nick = result.get('name')
    avatar = result.get('avatar')
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
    #if avatar != '':
    #    kvs = {}
    #    kvs['avatar'] = avatar
    #    Account.updateUserInfo(userId, **kvs)


    userInfo = Account.getUserInfo(userId)
    return User.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, True, openid=openid, loginChannelId=param['channelid'])

def parse(dt):
    Context.Log.debug(dt)
    param = {
        "app_key": dt.get('app_key', ''),
        "product_id": dt.get('product_id', ''),
        "amount": dt.get('amount', ''),
        "app_uid": dt.get('app_uid', ''),
        "user_id": dt.get('user_id', ''),
        "order_id": dt.get('order_id', ''),
        "gateway_flag": dt.get('gateway_flag', ''),
        "sign_type": dt.get('sign_type', ''),
        "app_order_id": dt.get('app_order_id', ''),
        "sign_return": dt.get('sign_return', ''),
        "sign": dt.get('sign', ''),

    }
    return param

def pay_callback(request):
    args = request.get_args()
    param = parse(args)

    orderId = param['app_order_id']

    orderInfo = Order.getOrderInfo(orderId)
    if not orderInfo:
        return urllib.urlencode({'status': 'fail', 'delivery': 'mismatch', 'msg': 'order error'})

    parseInfo = Order.parse_order(orderId)
    if not parseInfo:
        return urllib.urlencode({'status': 'fail', 'delivery': 'mismatch', 'msg': 'order error'})

    productId = orderInfo['productId']

    if int(param['amount']) != int(float(orderInfo['cost']) * 100):
        Context.Log.warn('price not equal', orderId, orderInfo, parseInfo)
        return urllib.urlencode({'status': 'fail', 'delivery': 'mismatch', 'msg': 'price not equal'})

    state = int(orderInfo['state'])
    if state >= Order.state_pre_deliver:  # 可能并没有成功, 需要检查对单
        return urllib.urlencode({'status': 'ok', 'delivery': 'success', 'msg': 'already'})

    gameId = int(orderInfo['gameId'])

    if APPKEY != param['app_key']:
        return urllib.urlencode({'status': 'fail', 'delivery': 'mismatch', 'msg': 'appkey not equal'})

    if not int(orderInfo['userId']) == int(param['app_uid']):
        return urllib.urlencode({'status': 'fail', 'delivery': 'mismatch', 'msg': 'app uid not equal'})

    if param['gateway_flag'] != 'success':
        return urllib.urlencode({'status': 'ok', 'delivery': 'success', 'msg': 'gateway_flag fail'})

    # 验证签名
    sign_data = ''
    calc_sign = get_sign(param)
    if calc_sign != param['sign']:
        Context.Log.error('sign not match', calc_sign, param['sign'])
        return urllib.urlencode({'status': 'fail', 'delivery': 'mismatch', 'msg': 'sign not equal'})

    Order.updateOrder(orderId, state=Order.state_pre_deliver)
    kvs = {
        'payTime': Time.current_time(),
        'deliverTime': Time.current_time(),
        'thirdOrderId2': param['order_id']
    }
    if Order.deliver_product(int(param['app_uid']), gameId, orderId, orderInfo, productId, orderInfo['paytype']):
        kvs['state'] = Order.state_deliver_success
    else:
        kvs['state'] = Order.state_deliver_failed

    Order.updateOrder(orderId, **kvs)
    return urllib.urlencode({'status': 'ok', 'delivery': 'success', 'msg': ''})

def get_360_order(product_id, product_name, strPrice, app_uid, app_uname, user_id, app_order_id):
    data = {
        'app_key': APPKEY,
        'product_id': product_id,
        'product_name': product_name,
        'amount': strPrice,
        'app_uid': app_uid,
        'app_uname': app_uname,
        'user_id': user_id,
        'sign_type': 'md5',
        'app_order_id': app_order_id,
    }
    sign = get_sign(data)

    real_url = '%s?app_key=%s&product_id=%s&product_name=%s&amount=%s&app_uid=%s&app_uname=%s&user_id=%s&sign_type=md5&app_order_id=%s&sign=%s' \
               % (URL_GET_ORDER, APPKEY, product_id, product_name, strPrice, app_uid, app_uname, user_id, app_order_id, sign)
    response = Context.WebPage.wait_for_json(real_url, method='GET')

    if response.get('error_code'):
        return None, None
    else:
        return response.get('token_id'), response.get('order_token')


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

    # 生成订单id
    order_info = Order.otherCreateOrder(gid, uid, productId, "q360", "android")
    if order_info.is_error():
        return MsgPack.Error(0, 8, 'order create fail')

    order_id = order_info.get_param('orderId')

    orderInfo = Order.getOrderInfo(order_id)
    Context.Log.debug('orderInfo-----', orderInfo)
    if not orderInfo:
        return MsgPack.Error(0, 8, 'order create fail')

    price = int(float(orderInfo['cost']) * 100)
    open_id = Context.Data.get_attr(uid, 'openid')
    token_id, order_token = get_360_order(productId, order_info.get_param('title'), str(price), uid, uid, open_id, order_id)
    if token_id == None or order_token == None:
        return MsgPack.Error(0, 8, 'order create fail')

    kvs = {
        'thirdOrderId': token_id,
        'paytype': payType
    }
    Order.updateOrder(order_id, **kvs)

    dictInfo = {}
    dictInfo['uid'] = uid
    dictInfo['openid'] = Context.Data.get_attr(uid, 'openid')
    dictInfo['pid'] = productId
    dictInfo['orderid'] = order_id
    dictInfo['paytype'] = payType
    dictInfo['notify_url'] = URL_NOTIFY_PAY
    dictInfo['p_name'] = order_info.get_param('title')
    dictInfo['p_desc'] = order_info.get_param('title')
    dictInfo['price'] = order_info.get_param('price')
    dictInfo['token_id'] = token_id
    dictInfo['order_token'] = order_token

    return MsgPack(0, dictInfo)

def get_sign(param):
    keys = param.keys()
    keys.sort()
    if 'sign' in keys:
        keys.remove('sign')
    if 'sign_return' in keys:
        keys.remove('sign_return')

    sign_data = ''
    for key in keys:
        v = param.get(key)
        if v == None or v == '':
            continue
        if sign_data:
            sign_data += '#'
        if type(v) == int:
            v = str(v)
        if type(v) == unicode:
            v = v.encode('utf8')
        sign_data += v
    sign = Algorithm.md5_encode(sign_data + '#' + APPSECRET)
    return sign

# 主动向平台sdk验证订单
def verify_order(orderId):
    parseInfo = Order.parse_order(orderId)
    if not parseInfo:
        raise NotFoundException

    orderInfo = Order.getOrderInfo(orderId)
    Context.Log.debug('orderInfo-----', orderInfo)
    if not orderInfo:
        raise NotFoundException

    product_id = orderInfo['productId']
    price = int(float(orderInfo['cost']) * 100)
    uid = orderInfo['userId']
    qhOrderId = orderInfo['thirdOrderId']
    open_id = Context.Data.get_attr(int(uid), 'openid')
    data = {
        'app_key': APPKEY,
        'product_id': product_id,
        'amount': price,
        'app_uid': open_id,
        'order_id': qhOrderId,
        'app_order_id': orderId,
        'sign_type': 'md5',
        'sign_return': 'q360query'
    }
    sign = get_sign(data)
    data.update({'sign': sign})

    real_url = '%s?app_key=%s&product_id=%s&amount=%s&app_uid=%s&order_id=%s&sign_type=md5&sign=%s&sign_return=q360query&app_order_id=%s' \
               % (URL_QUERY_ORDER, APPKEY, product_id, str(price), open_id, qhOrderId, sign, orderId)
    response = Context.WebPage.wait_for_json(real_url, method='GET')

    if response.get('ret', 0) == 'verified':
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
