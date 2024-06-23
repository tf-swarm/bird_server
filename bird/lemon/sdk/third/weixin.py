# -*- coding:utf-8 -*-
"""
created by cui
"""

from sdk.modules.order import Order
from framework.context import Context
from framework.util.tool import Time
from sdk.lib.yuntongxun.xmltojson import xmltojson
from framework.util.tool import Algorithm

from sdk.modules.user import User
from framework.entity.msgpack import MsgPack
from sdk.const import Const
from sdk.modules.account import Account

import types
import hashlib
import re
import time

URL_LOGIN = 'https://api.weixin.qq.com/sns/oauth2/access_token'
URL_USERINFO = 'https://api.weixin.qq.com/sns/userinfo'
URL_UNIFIEDORDER = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
URL_NOTIFY_PAY = 'http://39.103.150.106:8080/v2/third/callback/weixin/pay'
URL_ORDER_QUERY = 'https://api.mch.weixin.qq.com/pay/orderquery'

APPID = 'wxdcfcc6faa8ea2001'
SECRET = 'b447c073405c76117e0d6c57cf60e3bb'
MCH_ID = '1528035141' # 商户id
API_KEY = 'D134DAD0FB90488297086C88B933A856' #商户支付密钥Key。审核通过后，在微信发送的邮件中查看


res_success = '<xml><return_code><![CDATA[SUCCESS]]></return_code></xml>'
res_fail = '<xml><return_code><![CDATA[FAIL]]></return_code></xml>'


def check_sign(param):
    keys = param.keys()
    if 'sign' in keys:
        keys.remove('sign')
    keys.sort()
    sign_data = ''
    for key in keys:
        if key in ("templateSMS", 'statusCode', 'statusMsg'):
            continue
        v = param.get(key)
        if sign_data:
            sign_data += '&'
        sign_data += key
        sign_data += '='
        if type(v) == int:
            v = str(v)
        if type(v) == unicode:
            v = v.encode('utf8')
        sign_data += v
    sign = Algorithm.md5_encode(sign_data + '&key=' + API_KEY)
    sign = sign.upper()
    if sign == param['sign']:
        return Order.state_verify_success
    return Order.state_verify_failed_sign

# 支付回调
def pay_callback(request):
    Context.Log.report("pay_callback s")
    # {'appid': 'wxdb9f9548f1418e81', 'attach': '20471', 'bank_type': 'CFT', 'cash_fee': '1', 'fee_type': 'CNY', 'is_subscribe': 'N', 'mch_id': '1359764502', 'nonce_str': 'w2bwfp9acxqm3zl9zxgl8bp9vc71qjwy', 'openid': 'o0z7Rv6m_wIPWEKPZ0JYIPeJjRKc', 'out_trade_no': '10020001BHUwF0EZ', 'result_code': 'SUCCESS', 'return_code': 'SUCCESS', 'sign': 'FB1AF3663CE0177C42998F519DE8371B', 'time_end': '20160908161743', 'total_fee': '1', 'trade_type': 'JSAPI', 'transaction_id': '4009362001201609083427120979'}
    args = request.raw_data()
    #Context.Log.debug(args)
    Context.Log.report("pay_callback:", args)
    xtj = xmltojson()
    param = xtj.main(args)
    #Context.Log.debug(param)

    if 'result_code' not in param or param['result_code'] != 'SUCCESS':
        return res_fail
    orderId = param['out_trade_no']
    price = param['total_fee']

    parseInfo = Order.parse_order(orderId)    # 校验订单号
    if not parseInfo:
        return res_fail

    orderInfo = Order.getOrderInfo(orderId)
    Context.Log.debug('orderInfo-----', orderInfo)
    if not orderInfo:
        return res_fail

    state = int(orderInfo['state'])
    if state >= Order.state_pre_deliver:  # 可能并没有成功, 需要检查对单
        return res_success

    cost = int(float(orderInfo['cost']) * 100)
    if int(float(price)) != cost:
        Context.Log.warn('price not equal', orderId, orderInfo, parseInfo)
        return res_fail

    userId = int(orderInfo['userId'])
    gameId = int(orderInfo['gameId'])
    productId = orderInfo['productId']

    if not Order.judge_exist_product_id(2, productId):
        Context.Log.error('productId not exist', orderId, productId)
        return res_fail

    result = check_sign(param)
    Order.updateOrder(orderId, state=result)
    if result != Order.state_verify_success:
        return res_fail

    Order.updateOrder(orderId, state=Order.state_pre_deliver)
    kvs = {
        'payTime': Time.current_time(),
        'deliverTime': Time.current_time(),
        'thirdOrderId': param['transaction_id']
    }
    if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, orderInfo['paytype']):
        kvs['state'] = Order.state_deliver_success
    else:
        kvs['state'] = Order.state_deliver_failed

    Order.updateOrder(orderId, **kvs)
    key = 'weixin.order.%s' % Time.current_time(fmt='%Y-%m')
    Context.RedisMix.hash_set(key, param['transaction_id'], orderId)
    return res_success

#================支付预订单================

def set_params(**kwargs):
     params = {}
     for (k, v) in kwargs.items():
         params[k] = smart_str(v)
     return params

def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Returns a bytestring version of 's', encoded as specified in 'encoding'.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if strings_only and isinstance(s, (types.NoneType, int)):
        return s
    if not isinstance(s, basestring):
        try:
            return str(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return ' '.join([smart_str(arg, encoding, strings_only,
                        errors) for arg in s])
            return unicode(s).encode(encoding, errors)
    elif isinstance(s, unicode):
        return s.encode(encoding, errors)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)
    else:
        return s

def format_url(params, api_key=None):
    url = "&".join(['%s=%s'%(key, smart_str(params[key])) for key in sorted(params)])
    if api_key:
        url = '%s&key=%s' % (url, api_key)
    return url

def calculate_sign(params, api_key):
    #签名步骤一：按字典序排序参数, 在string后加入KEY
    url = format_url(params, api_key)
    Context.Log.report(url)
    #签名步骤二：MD5加密, 所有字符转为大写
    return hashlib.md5(url).hexdigest().upper()

def dict_to_xml(params, sign):
    xml = ["<xml>",]
    for (k, v) in params.items():
        if (v.isdigit()):
            xml.append('<%s>%s</%s>' % (k, v, k))
        else:
            xml.append('<%s><![CDATA[%s]]></%s>' % (k, v, k))
    xml.append('<sign><![CDATA[%s]]></sign></xml>' % sign)
    return ''.join(xml)


def xml_to_dict(xml):
    if xml[0:5].upper() != "<XML>" and xml[-6].upper() != "</XML>":
        return None, None

    result = {}
    sign = None
    content = ''.join(xml[5:-6].strip().split('\n'))

    pattern = re.compile(r"<(?P<key>.+)>(?P<value>.+)</(?P=key)>")
    m = pattern.match(content)
    while(m):
        key = m.group("key").strip()
        value = m.group("value").strip()
        if value != "<![CDATA[]]>":
            pattern_inner = re.compile(r"<!\[CDATA\[(?P<inner_val>.+)\]\]>")
            inner_m = pattern_inner.match(value)
            if inner_m:
                value = inner_m.group("inner_val").strip()
            if key == "sign":
                sign = value
            else:
                result[key] = value

        next_index = m.end("value") + len(key) + 3
        if next_index >= len(content):
            break
        content = content[next_index:]
        m = pattern.match(content)

    return sign, result

def post_xml(url, xml):
    return Context.WebPage.wait_for_page(url, postdata=xml)

def getUnifiedOrderInfo(prepay_id):
    js_params = {
                 "appid": APPID,
                 "partnerid": MCH_ID,
                 "prepayid": "%s" % prepay_id,
                 "package": "Sign=WXPay",
                 "noncestr": Order.random_str(32),
                 "timestamp": "%d" % time.time(),
                }
    params = set_params(**js_params)
    params["sign"] = calculate_sign(params, API_KEY)
    return params

# 获取预订单
def unifiedOrderPay(mi, request):
    gid = mi.get_param('gameId', 2)
    productId = mi.get_param('pid', '0')
    uid = mi.get_param('uid', 0)
    payType = mi.get_param('paytype', 0)

    if not Order.judge_exist_product_id(gid, productId):
        return MsgPack.Error(0, 1, 1)  # 无此产品
    # 获取产品信息
    #productInfo = product_config[productId]
    dt = Time.datetime()
    # 生成订单id
    order_info = Order.otherCreateOrder(gid, uid, productId, "weixin", "android")
    if order_info.is_error():
        return MsgPack.Error(0, 8, 'order create fail')

    order_id = order_info.get_param('orderId')

    Context.Log.debug('order_info:', order_info)

    tmp_kwargs = {
        "body": order_info.get_param('title'),
        "out_trade_no": order_id,
        "total_fee": int(order_info.get_param('price') * 100),
        "spbill_create_ip": request.getClientIP(),
        "notify_url": URL_NOTIFY_PAY,
        "trade_type": 'APP',
        #"sign" : "MD5",
        "nonce_str": Order.random_str(32),
        "mch_id": MCH_ID,
        "appid": APPID,
    }

    params = set_params(**tmp_kwargs)
    sign = calculate_sign(params, API_KEY)
    xml = dict_to_xml(params, sign)
    response = post_xml(URL_UNIFIEDORDER, xml)
    sign, result = xml_to_dict(response)
    if result:
        prepay_id = result.get("prepay_id", None)
        dictInfo = getUnifiedOrderInfo(prepay_id);
        dictInfo['pid'] = productId
        dictInfo['orderid'] = order_id
        dictInfo['paytype'] = payType
        kvs = {
            'thirdOrderId': prepay_id,
            'paytype': payType
        }
        Order.updateOrder(order_id, **kvs)
        return MsgPack(0, dictInfo)
    else:
        return MsgPack.Error(0, 1, 1)


#def __init__(self, appid, mch_id, api_key):
#    self.url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
#    self.trade_type = "NATIVE"



# =================登录相关=================
def login(mi, request):
    param = User.getParam(mi, 'accessToken', 'channelid')
    paramAccess = param['accessToken']
    if len(paramAccess) <= 1:
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)

    # 登录验证
    res = verify_login(paramAccess)
    if res.get('errcode') :
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
    openid = res.get('openid')
    access_token = res.get('access_token')
    gid = param['gameId']
    paramChannel = param['channelid']
    realChannel = paramChannel.split('_')[0]
    userId = Context.RedisMix.hash_get('%s.%s.uid' % (realChannel, gid), openid, None)

    headimgurl = ''
    if not userId:
        # 用户不存在，获取用户名
        res = get_userInfo(access_token, openid)
        if res.get('errcode'):
            return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
        nickName = res.get('nickname')
        headimgurl = res.get('headimgurl', '')

        Context.Log.report('%s,test11' %nickName)
        if type(nickName) == unicode:
            nickName = nickName.encode('utf8')
        param['nick'] = nickName

        channel = paramChannel
        idType = Const.IDTYPE_SDK
        userId = User.register(param, request, openid, idType, channel)
        if not userId:
            return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
        Context.RedisMix.hash_set('%s.%s.uid' % (realChannel, gid), openid, userId)
    else:  # 用户已存在，需要更新头像信息
        res = get_userInfo(access_token, openid)
        if res.get('errcode'):
            return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
        headimgurl = res.get('headimgurl', '')

    userId = int(userId)
    #if headimgurl != '':
    #    kvs = {}
    #    kvs['avatar'] = headimgurl
    #    Account.updateUserInfo(userId, **kvs)

    userInfo = Account.getUserInfo(userId)

    return User.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, True, openid=openid, loginChannelId=param['channelid'])


def verify_login(code):
    # 登录校验
    data = {'appid': APPID, 'secret': SECRET, 'code': code, 'grant_type': "authorization_code"}
    res = Context.WebPage.wait_for_json(URL_LOGIN, postdata=data)
    return res

def get_userInfo(access_token, openid):
    # 获取角色信息
    data = {'access_token': access_token, 'openid': openid }
    res = Context.WebPage.wait_for_json(URL_USERINFO, postdata=data)
    return res

def verify_order(orderId):
    Context.Log.report("verify_order:", orderId)
    data = {
        'appid': APPID,
        'mch_id': MCH_ID,
        'out_trade_no': orderId,
        'nonce_str': Order.random_str(32)
    }
    params = set_params(**data)
    sign = calculate_sign(params, API_KEY)

    xml = dict_to_xml(params, sign)
    response = post_xml(URL_ORDER_QUERY, xml)
    sign, result = xml_to_dict(response)
    if result:
        if 'return_code' not in result or result['return_code'] != 'SUCCESS':
            return order_wait
        else:
            if 'result_code' not in result or result['result_code'] != 'SUCCESS': # 订单异常
                if 'err_code' not in result or result['err_code'] != 'ORDERNOTEXIST':  #其他异常
                    return order_wait
                else:  #订单不存在
                    return order_fail
            else:  # 订单正常
                if 'trade_state' in result and result['trade_state'] == 'SUCCESS':
                    signNew = calculate_sign(result, API_KEY)
                    if sign == signNew:
                        return order_success
                    else:
                        return order_fail
                else:
                    return order_fail

    return order_wait

order_wait = 0   # 订单等待中，等待一段时间再次校验
order_fail = -1   # 订单不存在或者是失败订单
order_success = 1  # 订单成功

# 主动查询订单
def orderquery(orderId):
    res = verify_order(orderId)
    return res
