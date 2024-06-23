# -*- coding:utf-8 -*-
"""
created by cui
"""

from sdk.modules.order import Order
from framework.context import Context
from framework.util.tool import Time, Tool

from sdk.modules.user import User
from framework.entity.msgpack import MsgPack
from framework.util.tool import Algorithm
from sdk.const import Const
from sdk.modules.account import Account
import urllib



URL_LOGIN_QQ = 'http://ysdk.qq.com/auth/qq_check_token'     #'http://ysdktest.qq.com/auth/qq_check_token'    #
URL_LOGIN_WX = 'http://ysdk.qq.com/auth/wx_check_token'     #'http://ysdktest.qq.com/auth/wx_check_token'     #

APP_ID_QQ = '1108253395'
APP_KEY_QQ = 'H1sypOEn5izcfAWA'
APP_ID_WX = 'wx557b16d8c182a2a7'
APP_KEY_WX = 'd62f49b3a2e87a2b6c0715c6b96a52bc'

PAY_APPKEY = 'RrtIuIa4abnhfB9eXYYIFSCxnrtad4cI'     #'H1sypOEn5izcfAWA'    #

#APP_PAY_ID = '1107867123'
#APP_PAY_KEY = '72n40BvRBoWERR0i'


def verify_login(openid, openkey, platformType):
    url = ''
    appid = ''
    appkey = ''
    if platformType == 'WX':
        url = URL_LOGIN_WX
        appid = APP_ID_WX
        appkey = APP_KEY_WX
    else:
        url = URL_LOGIN_QQ
        appid = APP_ID_QQ
        appkey = APP_KEY_QQ
    # 登录校验
    ts = str(Time.current_ts())
    sig = Algorithm.md5_encode(appkey + ts)

    data = '?timestamp=' + str(ts) + '&appid=' + appid + '&sig=' + sig + '&openid=' + openid + '&openkey=' + openkey
    res = Context.WebPage.wait_for_json(url + data)
    return res

# =================登录相关=================
def login(mi, request):
    param = User.getParam(mi, 'accessToken', 'channelid', 'uid')
    paramAccess = param['accessToken']
    if len(paramAccess) <= 1:
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)

    # 登录验证
    real_openid = param['uid'][2:]
    sdk_platform = param['uid'][0: 2]
    res = verify_login(real_openid, paramAccess, sdk_platform)
    if res.get('ret'):
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)

    openid = param['uid']
    gid = param['gameId']
    paramChannel = param['channelid']
    realChannel = paramChannel.split('_')[0]
    userId = Context.RedisMix.hash_get('%s.%s.uid' % (realChannel, gid), openid, None)

    if not userId:
        if '' == param['nick']:
            param['nick'] = 'Y' + str(Time.current_ts())
        channel = paramChannel
        idType = Const.IDTYPE_SDK
        userId = User.register(param, request, openid, idType, channel)
        if not userId:
            return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
        Context.RedisMix.hash_set('%s.%s.uid' % (realChannel, gid), openid, userId)

    userId = int(userId)
    userInfo = Account.getUserInfo(userId)
    return User.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, True, openid=openid,
                             loginChannelId=param['channelid'])


order_wait = 0   # 订单等待中，等待一段时间再次校验
order_fail = -1   # 订单不存在或者是失败订单
order_success = 1  # 订单成功

def parse(dt):
    param = {
        "openid": dt.get('openid', ''),
        "appid": dt.get('appid', ''),
        "ts": dt.get('ts', ''),
        "payitem": dt.get('payitem', ''),
        "token": dt.get('token', 0),
        "billno": dt.get('billno', 0),
        "version": dt.get('version', ''),
        "zoneid": dt.get('zoneid', ''),
        "providetype": dt.get('providetype', ''),
        "amt": dt.get('amt', ''),
        "payamt_coins": dt.get('payamt_coins', ''),
        "pubacct_payamt_coins": dt.get('pubacct_payamt_coins', ''),
        "appmeta": dt.get('appmeta', ''),
        "clientver": dt.get('clientver', ''),
        "sig": dt.get('sig', ''),
    }
    return param

def get_sign_data(param):
    keys = param.keys()
    keys.sort()
    if 'sig' in keys:
        keys.remove('sig')
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
        else:
            str_v = v
            v = ''
            for c_v in str_v:
                if (c_v > '9' or c_v < '0') and (c_v > 'z' or c_v < 'a') \
                        and (c_v > 'Z' or c_v < 'A') and c_v not in '!*()':
                    c_v = '%' + c_v.encode('hex').upper()
                v += c_v
        sign_data += v
    return sign_data

def check_sign(param):
    sign_data = get_sign_data(param)
    head = '/v2/third/callback/yyb/pay'
    head = 'GET&' + urllib.quote_plus(head)
    Context.Log.debug('head', head)
    sign_data = urllib.quote_plus(sign_data)
    Context.Log.debug('sign_data2', sign_data)
    sign = Algorithm.hmac_sha1(PAY_APPKEY + '&', head + '&' + sign_data).digest().encode('base64').rstrip()
    Context.Log.debug('sign', sign)
    if sign == param['sig']:
        return Order.state_verify_success
    else:
        return Order.state_verify_failed_sign

def pay_callback(request):
    param = request.get_args()
    #param = parse(args)

    orderId = param['appmeta'].split('*')[0]
    price = param['payitem'].split('*')[1]
    parseInfo = Order.parse_order(orderId)
    if not parseInfo:
        return {'ret': 4, 'msg': 'orderId1 error'}

    orderInfo = Order.getOrderInfo(orderId)
    Context.Log.debug('orderInfo-----', orderInfo)
    if not orderInfo:
        return {'ret': 4, 'msg': 'orderId error'}

    state = int(orderInfo['state'])
    if state >= Order.state_pre_deliver:  # 可能并没有成功, 需要检查对单
        return {'ret': 0, 'msg': 'OK'}

    cost = float(orderInfo['cost'])
    if int(float(price)) != int(cost * 10):
        Context.Log.warn('price not equal', orderId, orderInfo, parseInfo)
        return {'ret': 4, 'msg': 'price error'}

    userId = int(orderInfo['userId'])
    gameId = int(orderInfo['gameId'])
    productId = orderInfo['productId']

    if not Order.judge_exist_product_id(2, productId):
        Context.Log.error('productId not exist', orderId, productId)
        return {'ret': 4, 'msg': 'productId error'}

    result = check_sign(param)
    Order.updateOrder(orderId, state=result)
    if result != Order.state_verify_success:
        return {'ret': 4, 'msg': 'fail to verify signature'}

    Order.updateOrder(orderId, state=Order.state_pre_deliver)
    kvs = {
        'payTime': Time.current_time(),
        'deliverTime': Time.current_time(),
        'thirdOrderId': param['billno']
    }
    if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, orderInfo['paytype']):
        kvs['state'] = Order.state_deliver_success
    else:
        kvs['state'] = Order.state_deliver_failed

    Order.updateOrder(orderId, **kvs)
    return {'ret': 0, 'msg': 'OK'}


# 主动查询订单
def orderquery(orderId):
    #res = verify_order(orderId)
    return 0

def format_url(params, sig=None):
    url = "&".join(['%s=%s'%(key, Algorithm.smart_str(params[key])) for key in sorted(params)])
    if sig:
        url = '%s&sig=%s' % (url, sig)
    return url


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
    order_info = Order.otherCreateOrder(gid, uid, productId, "yyb", "android")
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
    dictInfo['p_name'] = order_info.get_param('title')
    dictInfo['p_desc'] = order_info.get_param('title')
    dictInfo['price'] = int(float(order_info.get_param('price')) * 10)
    dictInfo['pay_app_key'] = PAY_APPKEY
    return MsgPack(0, dictInfo)

