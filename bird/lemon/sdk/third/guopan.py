#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-05-19

from sdk.const import Const
from sdk.modules.user import User
from sdk.modules.order import Order
from sdk.modules.account import Account
from framework.context import Context
from framework.util.tool import Time
from framework.util.tool import Algorithm
from framework.entity.msgpack import MsgPack


class Guopan(object):
    app_id = '104183'
    login_url = 'http://userapi.guopan.cn/gamesdk/verify/'
    server_key = 'WW4KANH3HL86T89R7Q2UJASRGLJ690OA0EGEDLJDK6GZG79MZ5S2B7LOEI1UXV2T'

    def verify_login(self, uin, token):
        now_ts = str(Time.current_ts())
        param = {
            'game_uin': uin,
            'appid': self.app_id,
            'token': token,
            't': now_ts
        }
        sign = Algorithm.md5_encode(uin + self.app_id + now_ts + self.server_key)
        param['sign'] = sign
        response = Context.WebPage.wait_for_page(self.login_url, query=param, method='GET')
        if response == 'true':
            return True
        else:  # false:失败, -1:加密验证失败, -2:appid错误
            return False

    def parse(self, dt):
        Context.Log.debug(dt)
        param = {
            "trade_no": str(dt.get('trade_no', '')),
            "serialNumber": dt.get('serialNumber', ''),
            "money": dt.get('money', 0),
            "status": int(dt.get('status', 0)),
            "t": int(dt.get('t', 0)),
            "sign": str(dt.get('sign', '')),
            "appid": dt.get('appid'),
            "item_id": dt.get('item_id'),
            "item_price": dt.get('item_price'),
            "item_count": dt.get('item_count'),
            'reserved': dt.get('reserved')
        }
        return param

    def check_sign(self, sign, param):
        if sign:
            s = param['serialNumber'] + param['money'] + str(param['status']) + str(param['t']) + self.server_key
            _sign = Algorithm.md5_encode(s)
            if _sign == sign:
                return Order.state_verify_success
        return Order.state_verify_failed_sign

    def login(self, mi, request):
        param = User.getParam(mi, 'accessToken', 'uid', 'devName', 'nickName')
        result = self.verify_login(param['uid'], param['accessToken'])
        if not result:
            return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)

        gid = param['gameId']
        openid = param['uid']
        userId = Context.RedisMix.hash_get('guopan.%s.uid' % gid, openid)
        if not userId:
            channel = 'guopan'
            idType = Const.IDTYPE_GUOPAN
            userId = User.register(param, request, openid, idType, channel)
            if not userId:
                return MsgPack.Error(0, User.error_invalid_access_token, User.desc_invalid_access_token)
            Context.RedisMix.hash_set('guopan.%s.uid' % gid, openid, userId)
        userId = int(userId)
        userInfo = Account.getUserInfo(userId)

        return User.getLoginInfo(request, 0, userId, param['gameId'], param, userInfo, False, openid=openid, loginChannelId=param['channelid'])

    def pay_callback(self, request):
        args = request.get_args()
        param = self.parse(args)
        if int(param['status']) != 1:  # 0=失败；1=成功；2=失败，原因是余额不足
            return 'success'

        orderId = param['serialNumber']
        price = param['money']
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
            'payTime': param['t'],
            'deliverTime': Time.current_time(),
            'thirdOrderId': param['trade_no']
        }
        if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, 'NaN'):
            kvs['state'] = Order.state_deliver_success
        else:
            kvs['state'] = Order.state_deliver_failed

        Order.updateOrder(orderId, **kvs)
        return 'success'


Guopan = Guopan()
