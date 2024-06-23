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

URL = 'http://f_signin.bppstore.com/loginCheck.php'

APPID = '104077'
APPKEY = '11c7359591b77ba4688f5a3cf346d07b'
PUBLICKEY = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDIBfUX8toHvKcEsll4yLQKuCtw
NHtWBTrKVWjdgdH1z9wLzpnbAUiGetN3xgDhEOucGGWWEonA9e+1OHKgi8Q5a0Wp
s2H/TozwJZi/q3e2AkLFaW2riQFcid/PBbhcyqutQhk6B895NTG1a2q9Wbfn4+MF
2rM8IrQNq2RyF/z6FQIDAQAB
-----END PUBLIC KEY-----'''
SECRETKEY = 'a37d3108e983fff44d680b50ffb7d5ee'


def rsa_decrypt_with_pub_key(pub_key, data):
    lib, ffi = Context.CFFILoader.load_framework_cffi()
    pub_str = ffi.new("char[]", 256)
    lib.rsa_decrypt(data, pub_key, 1, pub_str)
    pystr = ffi.string(pub_str)
    Context.Log.debug(pystr, len(pystr))
    return pystr


def verify_login(token):
    sign_data = APPKEY + token
    sign = Algorithm.md5_encode(sign_data)
    data = {'tokenKey': token, 'sign': sign}
    res = Context.WebPage.wait_for_json(URL, postdata=data)
    code = res.get('code')
    if code == 0:
        return 1, res.get('data')
    else:
        Context.Log.debug('7659 login error', res.get('msg'))
        return 0, res.get('msg')


def login(mi, request):
    param = User.getParam(mi, 'accessToken', 'devName')
    if len(param['accessToken']) <= 1:
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)

    result, data = verify_login(param['accessToken'])
    if not result or not data:
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)

    gid = param['gameId']
    openid = data.get('guid')
    # user_name = result.get('name')
    userId = Context.RedisMix.hash_get('7659.%s.uid' % gid, openid, None)
    if not userId:
        channel = '7659'
        idType = Const.IDTYPE_7659
        userId = User.register(param, request, openid, idType, channel)
        if not userId:
            return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
        Context.RedisMix.hash_set('7659.%s.uid' % gid, openid, userId)
    userId = int(userId)
    userInfo = Account.getUserInfo(userId)

    return User.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, False, openid=openid, loginChannelId=param['channelid'])


def parse(dt):
    Context.Log.debug(dt)

    param = {
        "notify_data": dt.get('notify_data', ''),
        "orderid": dt.get('orderid', ''),
        "dealseq": dt.get('dealseq', ''),
        "uid": dt.get('uid', ''),
        "subject": dt.get('subject', ''),
        "v": dt.get('v', ''),
        "sign": dt.get('sign', ''),
    }
    return param


def verify_sign(param):
    keys = param.keys()
    keys.sort()
    if 'sign' in keys:
        keys.remove('sign')
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
        sign_data += v
    return Algorithm.verify_rsa(PUBLICKEY, sign_data, param['sign'])


def check_sign(param):
    if verify_sign(param):
        return Order.state_verify_success
    return Order.state_verify_failed_sign


def pay_callback(request):
    args = request.get_args()
    # args = {'sign': 'WOOW3qUgvmTE0XNRhME3boqXheCBkwBo3FVpVNwFgkJPlu2ZlE9x5ltCJveScmoB6PZNNDVoMDWxCco9/acM3hExJ9fIIKD8pXpq0ZyH3GG1g3nLkAr4+lJ1d37XtcNAoaJey2b3nmG/E0twAh22+vTV5mtwHOTzLGkYaBuxhhg=', 'uid': 's57d90ecc884d4', 'v': '1.0', 'notify_data': 'FkL3vYFXxz8XnWKDt5DL3W4YsKMjDNO+aBPbb5ulPrVofvSmnF/k0lR+VcDkyQy1wpkYRtUZVNxgPysEge36sSzWJsVoI3CIij8877rbpJw9PQgctonRGGgZWhKtkbap/QD6NP8GTFTYoFGKMmm5GR2YD1YN12JXX76zwyd9Nr4=', 'dealseq': '10020001BLxbk0II', 'subject': u'首充礼包', 'orderid': '16091810407716103544917'}
    param = parse(args)

    result = check_sign(param)
    # Order.updateOrder(orderId, state=result)
    if result != Order.state_verify_success:
        Context.Log.debug('7659 pay_callback err 1')
        return 'failed'

    data = rsa_decrypt_with_pub_key(PUBLICKEY, param['notify_data'])
    res = dict((l.split('=') for l in data.split('&')))
    payresult = res.get('payresult')
    orderId = res.get('dealseq')
    price = res.get('fee')
    if not orderId:
        Context.Log.debug('7659 pay_callback err 2')
        return 'failed'

    parseInfo = Order.parse_order(orderId)
    if not parseInfo:
        Context.Log.debug('7659 pay_callback err 3')
        return 'failed'

    orderInfo = Order.getOrderInfo(orderId)
    Context.Log.debug('orderInfo-----', orderInfo)
    if not orderInfo:
        Context.Log.debug('7659 pay_callback err 4')
        return 'failed'

    state = int(orderInfo['state'])
    if state >= Order.state_pre_deliver:  # 可能并没有成功, 需要检查对单
        Context.Log.debug('7659 pay_callback 5')
        return 'success'

    if payresult != '0':
        Context.Log.debug('7659 pay_callback err 6')
        return 'failed'

    cost = int(orderInfo['cost'])
    if int(float(price)) != cost:
        Context.Log.warn('price not equal', orderId, orderInfo, parseInfo)
        return 'failed'

    userId = int(orderInfo['userId'])
    gameId = int(orderInfo['gameId'])
    productId = orderInfo['productId']

    if not Order.judge_exist_product_id(2, productId):
        Context.Log.error('productId not exist', orderId, productId)
        return 'failed'

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
