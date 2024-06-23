#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-05-20

from sdk.const import Const
from sdk.modules.user import User
from sdk.modules.order import Order
from sdk.modules.account import Account
from framework.context import Context
from framework.util.tool import Time
from framework.util.tool import Algorithm
from framework.entity.msgpack import MsgPack


class Ccpay(object):
    app_id = '106124'
    login_url = 'http://android-api.ccplay.com.cn/api/v2/payment/checkUser/'
    developer_key = 'b8e5939d9f6042519b4f7d8c91d0cefd'
    sign_key = '4b5f43e855b1477b8b3bda1619f77f8b'

    def verify_login(self, token):
        param = {
            'token': token
        }
        response = Context.WebPage.wait_for_page(self.login_url, query=param, method='GET')
        if response == 'success':
            return True
        else:
            return False

    def parse(self, dt):
        Context.Log.debug(dt)
        param = {
            "transactionNo": dt.get('transactionNo'),
            "partnerTransactionNo": dt.get('partnerTransactionNo', ''),
            "statusCode": dt.get('statusCode', 0),
            "productId": dt.get('productId', 0),
            "orderPrice": dt.get('orderPrice', 0),
            "packageId": dt.get('packageId', ''),
            "sign": dt.get('sign')
        }
        return param

    def check_sign(self, sign, param):
        if sign:
            copy_param = Context.copy_json_obj(param)
            del copy_param['sign']
            query_param = copy_param.items()
            query_param.sort(key=lambda item: item[0])
            s = Context.Strutil.url_encode(query_param) + '&' + self.sign_key
            _sign = Algorithm.md5_encode(s)
            if _sign == sign:
                return Order.state_verify_success
        return Order.state_verify_failed_sign

    def login(self, mi, request):
        param = User.getParam(mi, 'accessToken', 'uid', 'devName', 'nickName')
        result = self.verify_login(param['accessToken'])
        if not result:
            return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)

        gid = param['gameId']
        openid = param['uid']
        userId = Context.RedisMix.hash_get('ccpay.%s.uid' % gid, openid)
        if not userId:
            channel = 'ccpay'
            idType = Const.IDTYPE_CCPAY
            userId = User.register(param, request, openid, idType, channel)
            if not userId:
                return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
            Context.RedisMix.hash_set('ccpay.%s.uid' % gid, openid, userId)
        userId = int(userId)
        userInfo = Account.getUserInfo(userId)

        return User.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, False, openid=openid, loginChannelId=param['channelid'])

    def pay_callback(self, request):
        args = request.get_args()
        param = self.parse(args)
        if param['statusCode'] != '0000':  # 0000表示支付成功，0002表示支付失败
            return 'success'

        orderId = param['partnerTransactionNo']
        price = param['orderPrice']
        parseInfo = Order.parse_order(orderId)
        if not parseInfo:
            return 'failed'

        orderInfo = Order.getOrderInfo(orderId)
        Context.Log.debug('orderInfo-----', orderInfo)
        if not orderInfo:
            return 'failed'

        state = int(orderInfo['state'])
        if state >= Order.state_pre_deliver:  # 可能并没有成功, 需要检查对单
            return 'success'

        cost = int(orderInfo['cost'])
        if int(float(price)) != cost:
            Context.Log.warn('price not equal', orderId, orderInfo, parseInfo)
            return 'failed'

        userId = int(orderInfo['userId'])
        gameId = int(orderInfo['gameId'])
        channel = orderInfo['channel']
        productId = orderInfo['productId']

        if not Order.judge_exist_product_id(2, productId):
            Context.Log.error('productId not exist', orderId, productId)
            return 'failed'

        result = self.check_sign(param['sign'], param)
        Order.updateOrder(orderId, state=result)
        if result != Order.state_verify_success:
            return 'failed'

        Order.updateOrder(orderId, state=Order.state_pre_deliver)
        kvs = {
            'payTime': Time.current_time(),
            'deliverTime': Time.current_time(),
            'thirdOrderId': param['transactionNo']
        }
        if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, 'NaN'):
            kvs['state'] = Order.state_deliver_success
        else:
            kvs['state'] = Order.state_deliver_failed

        Order.updateOrder(orderId, **kvs)
        return 'success'


Ccpay = Ccpay()
