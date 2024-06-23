# -*- coding:utf-8 -*-
"""
created by xq
"""

import sys
import urllib
import json

from framework.context import Context
from framework.entity.msgpack import MsgPack
from framework.util.tool import Time

from sdk.const import Const
from sdk.modules.account import Account
from sdk.modules.user import User
from sdk.modules.order import Order
from sdk.lib.yeshen.client.NoxSDKServer import NoxSDKServer
from sdk.lib.yeshen.utils.NoxConstant import NoxConstant

reload(sys)
sys.setdefaultencoding("utf-8")

APPKEY = '866754a82b9049a0af61f3a1c8adb6f3'
APPID = '1c12d520dd7b49938d2545b6f0948d21'
PRIVATE_KEY = 'MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCVjxb9btfMz8WFejbNuPKSDHi+COVT/nlgsabXgdbpw6GWOvadj3ODfxdd5uxoOjgZBafI12d2DQTQALSmpbkKMhhv0hJP7ppUjGcD7UoCG60opMRv8dmtFzb846UWQuwSc9e1M/iJ05l4joEJFAZE0Hhl38WImbwSafRLWD0YORmiXXEZ3yILhdvB7HVnPVzDLIfenFAhvXbnicJkkmKEw4Cn6yZWRZLj8m4yoNaGquzlA8pbQ9Qxxu1872E5PLxfoq1whFesgq2t/1ZwjYn1K06f4hZWJsqKmhLNLbSymGarNDZiAo2uPo2qNvA9xc8tYnOBi4sq9qbRgJx2VKPTAgMBAAECggEBAJPbRbhBl/k0w6rlGz8hBDcdO1VsiAQVBbxxhWdzRpwOuzZBjsRQKLwsrlY4USntvL4IGEt3oSJVVpeoyvAh0KDiy8Po5A+/7TV/JOz973fMEtGmq0mcyT3VQJidGf27JZZMjknnWmQwHH7SK4FlGZl4nD7jDm+wxP1TYKAIWUYSzOz1ivlFNrwZ6/GA3J/6vq8WOqcO9ZlosxZaafMVD90lFXe6QTXi/sjFovxzOTkMMDIODmsVKtR3nZQ3gLx8c4+d3jEyY3YvECkeHEwKjefBhNHQOvHn9NdqZxARZLjoQvED5T7LK2z++w5tgiR9A2u5H1nI1Ee5sAaIbf4To0ECgYEA59D3HicVgAgGUqDYHWKfch7EumGCUgAnH5zXaTU4L8LfH2krmeL/sFCfZ6y69qaP3PFs7k0IG/qo0aawmkSzsAz0Hi3Qd11nBs1UaglVEAq8LrQmTVEOpgqZH/SntUiz5zq5vYjvAjlEkOEpnMqV3BkrqiGLOAJo5UlWim0UNrMCgYEApSlOrjWOwatOOZUpWwmP8E0Kpabh+HCoJZ0Skuna8HfFu3FtTy7VguEQ2Cro3+8BAeJom/yk8ogxm4kJAIIIpJjBDURWDJltaHTU1PLP24MlHPXI/K5Mp5IRRd+tXCyJ9yCC6ysTw+EB9/WZZoSutQ36F6vzKs2O+lZBX1KpbmECgYAcGXBa71Hj2xUpHuYTacj6BFDEZt1tIyea5WAXGKRe5bg2DoGCfcmQjbVE0+M10qrNlVYm7J93BMNB5nqxuHIvfOJ6ZgNG9MNwR6Nb1xXAhAybfKrH5HNqHQ7CmN1bVBy6gpvRJbATDO4KwcBRiRzxOPvZ+4bsmx4r7N/Yl7BDkQKBgGIXPWaT4nw9jJEAePZboIQ8jWVCzxRpfEQSnLRqdaC50dL4k84iZ6Z6mzF3kqVk4nlHCZATJbfxkVzpr1IA6LcxDf8eJekHuoX+VWU/7JlXs1QW2c7QijA/vUh9hw2mWi5OvdKD3BJK8Ytd70SG6ugXLAChHCPAv/kH/31or74hAoGAMDjJsRukyYeLguNmXhTA6hWSLBoNfI6/73DJW3BAYTk6WfR5BvUBuSdCymkh6F+3MdAXes5c2Ww9lfdRX2ckA9JOccU2boayCZgBvW8We33ZSl6DKYYu32ZcbNguqJG2MrpeePjOE/byQ7X6o1d2z5SRtly/jMGnZehp47eqo6g='

def verify_login(accessToken, uid):
    noxSDKServer = NoxSDKServer(APPID, APPKEY)
    validateResult = noxSDKServer.validate(accessToken, uid)
    if str(validateResult.getErrNum()) == NoxConstant.SUCCESS and str(validateResult.getTransdata().get('isValidate')) == NoxConstant.MSG_PASSPORT_VALID:  # 正确接收到数据
        return True
    Context.Log.debug('yeshen-verify-----', validateResult.getErrNum(), str(validateResult.getTransdata()))
    return False

def login(mi, request):
    param = User.getParam(mi, 'accessToken', 'uid', 'devName')
    if len(param['accessToken']) <= 1:
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)

    result = verify_login(param['accessToken'], param['uid'])
    if not result:
        return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)

    gid = param['gameId']
    # openid = data.get('uid')
    openid = param['uid']
    # user_name = result.get('name')
    userId = Context.RedisMix.hash_get('yeshen.%s.uid' % gid, openid, None)
    if not userId:
        channel = 'yeshen'
        idType = Const.IDTYPE_YESSHEN
        userId = User.register(param, request, openid, idType, channel)
        if not userId:
            return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
        Context.RedisMix.hash_set('yeshen.%s.uid' % gid, openid, userId)
    userId = int(userId)
    userInfo = Account.getUserInfo(userId)

    return User.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, False, openid=openid, loginChannelId=param['channelid'])

def pay_callback(request):
    url_data = request.raw_data()
    data = urllib.unquote(url_data)
    req = json.loads(data)

    Context.Log.debug('yeshen-callback-----', req.get('goodsOrderId'), req.get('orderId'))

    noxSDKServer = NoxSDKServer(APPID, APPKEY)
    payResult = noxSDKServer.getNotifyResult(req)

    # 验证请求状态码
    if str(payResult.getErrNum()) != NoxConstant.SUCCESS:
        return NoxConstant.MSG_FAILURE

    if req.get('payStatus') != '2':
        return NoxConstant.MSG_FAILURE

    # 验证业务数据
    orderId = req.get('goodsOrderId')

    orderInfo = Order.getOrderInfo(orderId)
    Context.Log.debug('yeshen-orderInfo-----', orderInfo)
    if not orderInfo:
        return NoxConstant.MSG_FAILURE

    parseInfo = Order.parse_order(orderId)
    if not parseInfo:
        return NoxConstant.MSG_FAILURE

    productId = orderInfo['productId']

    cost = float(orderInfo['cost'])
    money = req.get('orderMoney')
    if int(money) != int(cost*100):
        Context.Log.warn('price not equal', orderId, orderInfo, parseInfo)
        return NoxConstant.MSG_FAILURE

    state = int(orderInfo['state'])
    if state >= Order.state_pre_deliver:        # 可能并没有成功, 需要检查对单
        return NoxConstant.MSG_SUCCESS

    userId = int(orderInfo['userId'])
    gameId = int(orderInfo['gameId'])
    productId = orderInfo['productId']

    Order.updateOrder(orderId, state=Order.state_pre_deliver)
    kvs = {
        'payTime': Time.current_time(),
        'deliverTime': Time.current_time(),
        'thirdOrderId': req.get('orderId')
    }
    if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, 'NaN'):
        kvs['state'] = Order.state_deliver_success
    else:
        kvs['state'] = Order.state_deliver_failed

    Order.updateOrder(orderId, **kvs)
    Context.Log.debug('yeshen-orderInfo-----success')
    return NoxConstant.MSG_SUCCESS
