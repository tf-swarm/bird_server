# -*- coding:utf-8 -*-
"""
created by cui
"""
from sdk.lib.xiaomi.XMHttpClient import XMHttpClient
from sdk.lib.xiaomi.XMUtils import XMUtils

import hmac
import hashlib
from sdk.const import Const
from sdk.modules.user import User
from sdk.modules.order import Order
from framework.context import Context
from framework.util.tool import Time
from sdk.modules.account import Account
from framework.entity.msgpack import MsgPack

AppId = '2882303761517467497'
AppKey = '5741746710497'
AppSecret = 'CN4PTjrwbmiXhCQZA12oOg=='
VerifySession_URL = 'http://mis.migc.xiaomi.com/api/biz/service/verifySession.do'


def verify_login(uid, session):
    xm_utils = XMUtils()
    client = XMHttpClient(VerifySession_URL)
    params = dict(appId=AppId, session=session, uid=uid)
    sign = xm_utils.buildSignature(params, AppSecret)
    # headers = xm_utils.buildMacRequestHead(User.accessToken, nonce, sign)
    params["signature"] = sign
    res = client.request("", "GET", params)
    jsonObject = client.safeJsonLoad(res.read())
    return jsonObject


def login_xiaomi(mi, request):
    param = User.getParam(mi, 'uid', 'accessToken', 'devName')
    result = verify_login(param['uid'], param['accessToken'])

    if result.get('errcode') != 200:
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)

    gid = param['gameId']
    openid = param['uid']
    userId = Context.RedisMix.hash_get('xiaomi.%s.uid' % gid, openid, None)
    if not userId:
        channel = 'xiaomi'
        idType = Const.IDTYPE_XIAOMI
        userId = User.register(param, request, openid, idType, channel)
        if not userId:
            return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
        Context.RedisMix.hash_set('xiaomi.%s.uid' % gid, openid, userId)
    userId = int(userId)
    userInfo = Account.getUserInfo(userId)

    return User.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, False, openid=openid, loginChannelId=param['channelid'])


def pay_callback(request):
    appId = ''
    cpOrderId = ''
    cpUserInfo = ''
    uid = ''
    orderId = ''
    orderStatus = ''
    payFee = ''
    productCode = ''
    productName = ''
    productCount = ''
    payTime = ''
    orderConsumeType = ''
    signature = ''

    if request.args.get('appId'):
        appId = request.args.get('appId')[0]
    if request.args.get('cpOrderId'):
        cpOrderId = request.args.get('cpOrderId')[0]
    if request.args.get('cpUserInfo'):
        cpUserInfo = request.args.get('cpUserInfo')[0]
    if request.args.get('uid'):
        uid = request.args.get('uid')[0]
    if request.args.get('orderId'):
        orderId = request.args.get('orderId')[0]
    if request.args.get('orderStatus'):
        orderStatus = request.args.get('orderStatus')[0]
    if request.args.get('payFee'):
        payFee = request.args.get('payFee')[0]
    if request.args.get('productCode'):
        productCode = request.args.get('productCode')[0]
    if request.args.get('productName'):
        productName = request.args.get('productName')[0]
    if request.args.get('productCount'):
        productCount = request.args.get('productCount')[0]
    if request.args.get('payTime'):
        payTime = request.args.get('payTime')[0]
    if request.args.get('orderConsumeType'):
        orderConsumeType = request.args.get('orderConsumeType')[0]
    if request.args.get('signature'):
        signature = request.args.get('signature')[0]

    orderInfo = Order.getOrderInfo(cpOrderId)
    if not orderInfo:
        return return_data(1515)

    parseInfo = Order.parse_order(cpOrderId)
    if not parseInfo:
        return return_data(1515)
    productId = orderInfo['productId']
    gameId = int(orderInfo['gameId'])
    state = int(orderInfo['state'])
    if state >= Order.state_pre_deliver:  # 可能并没有成功, 需要检查对单
        return return_data(200)

    userId = Context.RedisMix.hash_get_int('xiaomi.%s.uid' % gameId, uid, 0)
    if userId <= 0:
        return return_data(1515)

    cost = int(orderInfo['cost'])
    if int(payFee) != cost * 100:
        Context.Log.warn('price not equal', cpOrderId, orderInfo, parseInfo)
        return return_data(1515)

    if orderStatus != 'TRADE_SUCCESS':
        return return_data(1515)

    # 验证签名
    sign_data = ''
    for [k, v] in (['appId', appId], ['cpOrderId', cpOrderId], ['cpUserInfo', cpUserInfo],
                   ['orderConsumeType', orderConsumeType], ['orderId', orderId],
                   ['orderStatus', orderStatus], ['payFee', payFee], ['payTime', payTime],
                   ['productCode', productCode], ['productCount', productCount],
                   ['productName', productName], ['uid', uid]):
        if not v:
            continue
        if sign_data:
            sign_data += '&'
        sign_data += k
        sign_data += '='
        sign_data += v

    h = hmac.new(str(AppSecret), str(sign_data), hashlib.sha1)
    s = h.digest()
    _signature = s.encode("hex")

    if _signature != signature:
        return return_data(1515)

    Order.updateOrder(cpOrderId, state=Order.state_pre_deliver)
    kvs = {
        'payTime': Time.current_time(),
        'deliverTime': Time.current_time(),
        'thirdOrderId': orderId
    }
    if Order.deliver_product(userId, gameId, cpOrderId, orderInfo, productId, 'NaN'):
        kvs['state'] = Order.state_deliver_success
    else:
        kvs['state'] = Order.state_deliver_failed

    Order.updateOrder(cpOrderId, **kvs)
    return return_data(200)


def return_data(code):
    return Context.json_dumps({'errcode': code})
