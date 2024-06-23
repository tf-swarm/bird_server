#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-05-20

from sdk.modules.order import Order
from framework.context import Context
from framework.util.tool import Time
from framework.util.tool import Algorithm
from framework.entity.response import http_response_handle


class Youku(object):
    app_id = '2867'
    pay_key = '1f85c362a8c731c7732ac318055f8906'

    def parse(self, dt):
        Context.Log.debug(dt)
        param = {
            "apporderID": dt.get('apporderID'),
            "passthrough": dt.get('passthrough', ''),
            "price": dt.get('price', 0),
            "sign": dt.get('sign')
        }
        return param

    def check_sign(self, url, sign, param):
        if sign:
            full_url = Context.Global.http_sdk() + url
            s = '%s?apporderID=%s&price=%s' % (full_url, param['apporderID'], param['price'])
            _sign = Algorithm.hmac_encode(self.pay_key, s)
            if _sign == sign:
                return Order.state_verify_success
        return Order.state_verify_failed_sign

    @http_response_handle()
    def pay_callback(self, request):
        args = request.get_args()
        param = self.parse(args)

        orderId = param['apporderID']
        price = param['price']
        parseInfo = Order.parse_order(orderId)
        if not parseInfo:
            return {'status': 'failed', 'desc': u'未找到订单'}

        orderInfo = Order.getOrderInfo(orderId)
        Context.Log.debug('orderInfo-----', orderInfo)
        if not orderInfo:
            return {'status': 'failed', 'desc': u'未找到订单'}

        state = int(orderInfo['state'])
        if state >= Order.state_pre_deliver:  # 可能并没有成功, 需要检查对单
            return {'status': 'success', 'desc': u'通知成功'}

        cost = int(orderInfo['cost'])
        if int(price) / 100 != cost:
            Context.Log.warn('price not equal', orderId, orderInfo, parseInfo)
            return {'status': 'failed', 'desc': ''}

        userId = int(orderInfo['userId'])
        gameId = int(orderInfo['gameId'])
        channel = orderInfo['channel']
        productId = orderInfo['productId']

        if not Order.judge_exist_product_id(2, productId):
            Context.Log.error('productId not exist', orderId, productId)
            return {'status': 'failed', 'desc': ''}

        result = self.check_sign(request.uri, param['sign'], param)
        Order.updateOrder(orderId, state=result)
        if result != Order.state_verify_success:
            return {'status': 'failed', 'desc': u'数字签名错误'}

        Order.updateOrder(orderId, state=Order.state_pre_deliver)
        kvs = {
            'payTime': Time.current_time(),
            'deliverTime': Time.current_time(),
            'thirdOrderId': param['passthrough']
        }
        if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, 'NaN'):
            kvs['state'] = Order.state_deliver_success
        else:
            kvs['state'] = Order.state_deliver_failed

        Order.updateOrder(orderId, **kvs)
        return {'status': 'success', 'desc': u'通知成功'}


Youku = Youku()
