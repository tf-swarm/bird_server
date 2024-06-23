# -*- coding:utf-8 -*-
"""
created by cui
"""

from sdk.modules.order import Order
from framework.context import Context
from framework.util.tool import Time
from framework.entity.msgpack import MsgPack
from framework.util.tool import Algorithm

import datetime
import json
import rsa
import base64
import urllib

APPID = '2018080160850004'
#sandAPPID = '2016091800541504'
SIGN_TYPE = "SHA-256"
URL_PAY_NOTIFY = 'http://39.103.150.106:8080/v2/third/callback/alipay/pay'

URL_PAY_QUERY = 'https://openapi.alipay.com/gateway.do'

RSA_ALIPAY_PUBLIC = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArt2Sv7OC9JRpiaTZq34NzdbSGXo9ZQH50ULCnOpMDYYz/apmpr/Vu3cxnWs98rgd0G6LMXErJYQTaTBYIDzALs0+xRtrTvGQX3XNBIPzEQ/nJwBMq96PeSWGjMeARg7sN+IIjVOsuJDxoVY28fDZEzY/su5SyKOcT/MwgJHB/2f6PjkjR50H462FnE4fev0VBGQ+xuAG7N9Ks8FBvZg4Nd1wy5B26DEHieEYNZlAq9YWZ0gWMGiUwhOwMZbY2g79jc4jgsMWw2ArGBDXegpgxpbqQwfaERuk2I3BpnkseD0K0yWzeqk215W7YBMkw2FHEpr+4JxbvqdkWZ7R7CsCkQIDAQAB
-----END PUBLIC KEY-----'''


RSA_PUBLIC = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuOiZyj5AQnEW/COqDLwx
+7CZwvEoM9Km1DUOL9hv4k46mmCh9jVqAlmZvvSaGa9dW7MAV0T21yu2ahLYIgiS
3+rnYlpULOlflZPrwna3tJU4VKtUW6otoJ1S/uxkEz5/CzAPWTsSac3fh3FbZez6
TYVd58tgG1NdXabdnVflnJ6qrJsAnWt/Bx/aJHlUGFA5JWcxj8cJjWXFLP9sQCm7
PG+WLhVysAyU5HLuA5XhQsJ7j+1ndGTU7FFu+p43jyaYCqVSjwO4vfP+aaR3aNwn
ih/fw4YwCBeDWDYjGENz5kxqnE1C6KOaiENHw04rlBVSCvzzt2ZwzE2h2dzZYeUq
EwIDAQAB
-----END PUBLIC KEY-----"""

RSA_PRIVATE ="""-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAuOiZyj5AQnEW/COqDLwx+7CZwvEoM9Km1DUOL9hv4k46mmCh
9jVqAlmZvvSaGa9dW7MAV0T21yu2ahLYIgiS3+rnYlpULOlflZPrwna3tJU4VKtU
W6otoJ1S/uxkEz5/CzAPWTsSac3fh3FbZez6TYVd58tgG1NdXabdnVflnJ6qrJsA
nWt/Bx/aJHlUGFA5JWcxj8cJjWXFLP9sQCm7PG+WLhVysAyU5HLuA5XhQsJ7j+1n
dGTU7FFu+p43jyaYCqVSjwO4vfP+aaR3aNwnih/fw4YwCBeDWDYjGENz5kxqnE1C
6KOaiENHw04rlBVSCvzzt2ZwzE2h2dzZYeUqEwIDAQABAoIBAQCn7SXt1AcL0CSt
q739ftRt3X5m2hhGqCI2SlCuBwPlJGJ4XRX5wZyascC8+OsSNH62jqPanZkG5H3v
a1m53st0a6LjYWFcwDy8XPAZVTOU3oef7VDZRn3VhcsgFJL2HyXFhUoLIWihigRc
vwfgUw0mZd5YagzIBDegm7Bb+r1eM/WIlQdyzW+eD4WG8VNzWQ0WN5xTD37KXt27
X4yERpjbmepzkgclJfHGeFKPC1bP7XfGoKPbQSjvFX6SAZl6XY50FpsBDOlDigjm
z4G+h0PJakk8tVS75UurGiu7MJ4e5pFcMk3bS7DMwmXWuu8Ht6U3Uxj2lVTY6BIp
RagzsLTBAoGBAO+oulZIDwKsMB9m+smxFgXuBrS9TN6RefedljmriC7pvUEGor1m
RGRYJEFohwDPeOCX3/dmw132oxng6NvOOuzVxXhmADItaofXzWpbsfPLjjrJ1Bzd
Me0fasvBu+0rwcvnTCo+IKi4r/4bP/0Lwky6ja0XdbuomaoHvoFcylajAoGBAMWE
MqEYW4ml7XgCU81Rlw2MpCtUEK1EwmqLiv0KLbhS21KyLXSXwifFlPpBCLWdBEnF
JmrHyHwK7Vr6YKtrwrWDh9PLvxm5fwbJNB5OydyvTtFge9SNwYTGPrJAV5rlFhB6
yM9z0bMSQZ0T/KR151BvZLyVMc3/3rEYJtqZY8XRAoGAUmzpiXtHDlhCRMqaPnwV
Yvy2ebsRkQrfs/YTEMqaD+h8Gr05g4KEyy41afmVVQYGQNh7Qw+o6cxF1ESyUcbg
JUxwmjQapSdRmF70WzwmO/8qb7Wyqiq5XSCNDn8XLz75bDOk0nKDsQO0I+UjYNiG
fvU6fOmwqFYYY44+Syeqv5kCgYBewRzIy7aeQku51uP9C7c7eM0JPDsD5IigNHFp
Ewj79EPjWDcWR/eMvOzLYYecGMeF3F6hu1Yiq9tSWesmUXwHOCJhKM10udiGmN+3
6nRMuo1FRNQjFB5SZAiP2u4sENqU7VKIszdWgNuZT41UGHvvyoC5N5m9CZL7wmph
VFTZAQKBgDJEtY8/nA9GU29tAqrlcB45HzKY67uo60MrI16/nhPO/yhF9Xs2Csps
DJqSbRL5UhX0DKBucFwH5IOa+3j8LFPD5m9Qx/nzNF5QdyiauG909muk/7IZ9pnc
ttC7wSQP5Mz96uw+gnhFeROpHClz3T6n88VJfukeHMZGNzT8Y20M
-----END RSA PRIVATE KEY-----"""



def check_sign(param):
    keys = param.keys()
    if 'sign' in keys:
        keys.remove('sign')
    if 'sign_type' in keys:
        keys.remove('sign_type')
    keys.sort()
    sign_data = ''
    for key in keys:
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
    Context.Log.report('sign_data:', sign_data)
    Context.Log.report('sign:', param['sign'])

    if Algorithm.verify_rsa(RSA_ALIPAY_PUBLIC, sign_data, param['sign']):
        Context.Log.report('suc', )
        return Order.state_verify_success
    return Order.state_verify_failed_sign


def pay_callback(request):
    # {'appid': 'wxdb9f9548f1418e81', 'attach': '20471', 'bank_type': 'CFT', 'cash_fee': '1', 'fee_type': 'CNY', 'is_subscribe': 'N', 'mch_id': '1359764502', 'nonce_str': 'w2bwfp9acxqm3zl9zxgl8bp9vc71qjwy', 'openid': 'o0z7Rv6m_wIPWEKPZ0JYIPeJjRKc', 'out_trade_no': '10020001BHUwF0EZ', 'result_code': 'SUCCESS', 'return_code': 'SUCCESS', 'sign': 'FB1AF3663CE0177C42998F519DE8371B', 'time_end': '20160908161743', 'total_fee': '1', 'trade_type': 'JSAPI', 'transaction_id': '4009362001201609083427120979'}
    param = request.get_args()
    Context.Log.debug(param)

    if 'trade_status' not in param or param['trade_status'] not in ['TRADE_SUCCESS', 'TRADE_FINISHED']:
        return 'fail1'
    orderId = param['out_trade_no']
    price = param['total_amount']

    if 'app_id' not in param or param['app_id'] != APPID:
        return 'fail2'

    parseInfo = Order.parse_order(orderId)
    if not parseInfo:
        return 'fail3'

    orderInfo = Order.getOrderInfo(orderId)
    Context.Log.debug('orderInfo-----', orderInfo)
    if not orderInfo:
        return 'fail4'

    state = int(orderInfo['state'])
    if state >= Order.state_pre_deliver:  # 可能并没有成功, 需要检查对单
        return 'success'

    cost = int(float(orderInfo['cost']) * 100)
    if int(float(price)*100) != cost:
        Context.Log.warn('price not equal', orderId, orderInfo, parseInfo)
        return 'fail5'

    userId = int(orderInfo['userId'])
    gameId = int(orderInfo['gameId'])
    productId = orderInfo['productId']

    if not Order.judge_exist_product_id(2, productId):
        Context.Log.error('productId not exist', orderId, productId)
        return 'fail6'

    result = check_sign(param)
    Order.updateOrder(orderId, state=result)
    if result != Order.state_verify_success:
        return 'fail7'

    Order.updateOrder(orderId, state=Order.state_pre_deliver)
    kvs = {
        'payTime': Time.current_time(),
        'deliverTime': Time.current_time(),
        'thirdOrderId': param['trade_no']
    }
    if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, orderInfo['paytype']):
        kvs['state'] = Order.state_deliver_success
    else:
        kvs['state'] = Order.state_deliver_failed

    Order.updateOrder(orderId, **kvs)
    key = 'ali.order.%s' % Time.current_time(fmt='%Y-%m')
    Context.RedisMix.hash_set(key, param['trade_no'], orderId)
    return 'success'

def make_payment_info(out_trade_no=None, subject=None, total_amount=None, body=None, passback_params=None):
    public = {  # public args
        "app_id": APPID,
        "method": "alipay.trade.app.pay",
        "charset": "utf-8",
        "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # 2014-07-24 03:07:50
        "version": "1.0",
        "notify_url": URL_PAY_NOTIFY,
        "sign_type": "RSA2"
    }

    # 业务参数
    order_info = {"product_code": "QUICK_MSECURITY_PAY",
                  "out_trade_no": None,
                  "subject": None,
                  "total_amount": total_amount,
                  "body": body,
                  }
    #if not passback_params:
    #    order_info['passback_params'] = passback_params
    order_info["out_trade_no"] = "%s" % (out_trade_no)
    order_info["subject"] = "%s" % (subject)
    if total_amount <= 0.0:
        total_amount = 0.01
    order_info["total_amount"] = "%s" % (total_amount)

    public['biz_content'] = json.dumps(order_info, ensure_ascii=False)
    return public

def params_to_query(params, quotes=False, reverse=False):
    """
        生成需要签名的字符串
    :param params:
    :return:
    """
    """
    :param params:
    :return:
    """
    query = ""
    for key in sorted(params.keys(), reverse=reverse):
        value = params[key]
        if quotes == True:
            query += str(key) + "=\"" + str(value) + "\"&"
        else:
            query += str(key) + "=" + str(value) + "&"
    query = query[0:-1]
    return query

def make_sign(message):
    """
    签名
    :param message:
    :return:
    """
    private_key = rsa.PrivateKey._load_pkcs1_pem(RSA_PRIVATE)
    sign = rsa.sign(message, private_key, SIGN_TYPE)
    b64sing = base64.b64encode(sign)
    return b64sing

def query_to_dict(query):
    """
    将query string转换成字典
    :param query:
    :return:
    """
    res = {}
    k_v_pairs = query.split("&")
    for item in k_v_pairs:
        sp_item = item.split("=", 1)  #注意这里，因为sign秘钥里面肯那个包含'='符号，所以splint一次就可以了
        key = sp_item[0]
        value = sp_item[1]
        res[key] = value

    return res

def params_escape(dict):
    escapedDict = {}
    for key, value in dict.items():
        str = urllib.quote_plus(value)
        escapedDict[key] = str
    return escapedDict

def query_to_dict(query):
    """
    将query string转换成字典
    :param query:
    :return:
    """
    res = {}
    k_v_pairs = query.split("&")
    for item in k_v_pairs:
        sp_item = item.split("=", 1)  #注意这里，因为sign秘钥里面肯那个包含'='符号，所以splint一次就可以了
        key = sp_item[0]
        value = sp_item[1]
        res[key] = value

    return res

def make_payment_request(params_dict):
    """
    构造一个支付请求的信息，包含最终结果里面包含签名
    :param params_dict:
    :return:
    """
    query_str = params_to_query(params_dict) #拼接签名字符串
    sign = make_sign(query_str) #生成签名
    res = "%s&sign=%s" % (query_str, sign)
    dict = query_to_dict(res)
    dict = params_escape(dict)
    res = params_to_query(dict)
    return res

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
    order_info = Order.otherCreateOrder(gid, uid, productId, "alipay", "android")
    if order_info.is_error():
        return MsgPack.Error(0, 8, 'order create fail')

    order_id = order_info.get_param('orderId')

    payment_info = make_payment_info(out_trade_no=order_id, subject=order_info.get_param('title'), total_amount=str(order_info.get_param('price')), body="", passback_params=None)
    Context.Log.report("payment_info:", payment_info)
    res = make_payment_request(payment_info)
    dictInfo = {}
    dictInfo['pid'] = productId
    dictInfo['orderid'] = order_id
    dictInfo['orderinfo'] = res
    dictInfo['paytype'] = payType
    kvs = {
        'thirdOrderId': "0",
        'paytype': payType,
    }
    Order.updateOrder(order_id, **kvs)
    return MsgPack(0, dictInfo)


order_wait = 0   # 订单等待中，等待一段时间再次校验
order_fail = -1   # 订单不存在或者是失败订单
order_success = 1  # 订单成功

def verify_order(orderId):
    public = {
        'app_id': APPID,
        'method': 'alipay.trade.query',
        'charset': 'utf-8',
        'sign_type': 'RSA2',
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'version': '1.0',
    }

    # 业务参数
    order_info = {
        'out_trade_no': orderId,
    }

    public['biz_content'] = json.dumps(order_info, ensure_ascii=False)
    query_str = params_to_query(public)  # 拼接签名字符串
    sign = make_sign(query_str)  # 生成签名
    requestStr = "%s&sign=%s" % (query_str, sign)
    dict = query_to_dict(requestStr)
    dict = params_escape(dict)
    requestStr = params_to_query(dict)
    response = Context.WebPage.wait_for_json(URL_PAY_QUERY, postdata=requestStr)

    #Context.Log.report('verify_order param:', response)
    query_response = response.get('alipay_trade_query_response')
    Context.Log.report('verify_order query_response:', query_response)
    if query_response.get('code') == '10000':   # 订单成功
        trade_status = query_response.get('trade_status')
        #Context.Log.report('verify_order trade_status:', trade_status)
        if trade_status == 'TRADE_SUCCESS':
            #Context.Log.report('verify_order trade_status2:', trade_status)
            #if Order.state_verify_success == check_sign(json.loads(response)):
            return order_success
            #else:
            #    return order_fail
        else:
            return order_fail
    else:
        return order_wait


# 主动查询订单
def orderquery(orderId):
    res = verify_order(orderId)
    return res
