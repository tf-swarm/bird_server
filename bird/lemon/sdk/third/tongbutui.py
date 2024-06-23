#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-08-30

from sdk.const import Const
from sdk.modules.user import User
from sdk.modules.order import Order
from sdk.modules.account import Account
from framework.context import Context
from framework.util.tool import Time
from framework.util.tool import Algorithm
from framework.entity.msgpack import MsgPack


class TongBuTui(object):
    app_id = '160804'
    login_url = 'http://tgi.tongbu.com/api/LoginCheck.ashx'
    app_key = 'F6q3anM#m2UrzAkElmtZQ9mDlIM*AzI1'

    def verify_login(self, uid, session):
        param = {
            'session': session,
            'appid': self.app_id
        }
        response = Context.WebPage.wait_for_page(self.login_url, query=param, method='GET')
        code = int(response)
        if code > 0:
            if code == int(uid):
                return True

        return False

    def parse(self, dt):
        Context.Log.debug(dt)
        param = {
            'source': dt.get('source'),
            'trade_no': dt.get('trade_no'),
            'amount': dt.get('amount'),
            'partner': dt.get('partner'),
            'paydes': dt.get('paydes'),
            'debug': dt.get('debug'),
            'tborder': dt.get('tborder'),
            'sign': dt.get('sign')
        }
        return param

    def check_sign(self, sign, param):
        if sign:
            line = 'source=tongbu&trade_no=%s&amount=%s&partner=%s&paydes=%s&debug=%s&tborder=%s&key=%s' % (
                                            param['trade_no'], param['amount'], param['partner'],
                                            param['paydes'], param['debug'], param['tborder'], self.app_key)
            _sign = Algorithm.md5_encode(line)
            if _sign == sign:
                return Order.state_verify_success
        return Order.state_verify_failed_sign

    def login(self, mi, request):
        param = User.getParam(mi, 'session', 'uid', 'devName', 'nickName')
        result = self.verify_login(param['uid'], param['session'])
        if not result:
            return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)

        gid = param['gameId']
        openid = param['uid']
        userId = Context.RedisMix.hash_get('tongbutui.%s.uid' % gid, openid)
        if not userId:
            channel = 'tongbutui'
            idType = Const.IDTYPE_TONGBUTUI
            userId = User.register(param, request, openid, idType, channel)
            if not userId:
                return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
            Context.RedisMix.hash_set('tongbutui.%s.uid' % gid, openid, userId)
        userId = int(userId)
        userInfo = Account.getUserInfo(userId)

        return User.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, False, openid=openid, loginChannelId=param['channelid'])

    def pay_callback(self, request):
        args = request.get_args()
        param = self.parse(args)
        orderId = param['trade_no']
        price = param['amount']
        parseInfo = Order.parse_order(orderId)
        if not parseInfo:
            return '{"status":"failed"}'

        orderInfo = Order.getOrderInfo(orderId)
        Context.Log.debug('orderInfo-----', orderInfo)
        if not orderInfo:
            return '{"status":"failed"}'

        state = int(orderInfo['state'])
        if state >= Order.state_pre_deliver:  # 可能并没有成功, 需要检查对单
            return '{"status":"success"}'

        cost = int(orderInfo['cost'])
        if int(float(price)) / 100 != cost:
            Context.Log.warn('price not equal', orderId, orderInfo, parseInfo)
            return '{"status":"failed"}'

        userId = int(orderInfo['userId'])
        gameId = int(orderInfo['gameId'])
        channel = orderInfo['channel']
        productId = orderInfo['productId']

        if not Order.judge_exist_product_id(2, productId):
            Context.Log.error('productId not exist', orderId, productId)
            return '{"status":"failed"}'

        result = self.check_sign(param['sign'], param)
        Order.updateOrder(orderId, state=result)
        if result != Order.state_verify_success:
            return '{"status":"failed"}'

        Order.updateOrder(orderId, state=Order.state_pre_deliver)
        kvs = {
            'payTime': Time.current_time(),
            'deliverTime': Time.current_time(),
            'thirdOrderId': param['tborder']
        }
        if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, 'NaN'):
            kvs['state'] = Order.state_deliver_success
        else:
            kvs['state'] = Order.state_deliver_failed

        Order.updateOrder(orderId, **kvs)
        return '{"status":"success"}'


TongBuTui = TongBuTui()
