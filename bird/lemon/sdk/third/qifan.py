#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-18

from sdk.modules.order import Order
from framework.context import Context
from framework.util.tool import Time
from framework.util.tool import Algorithm


class QiFan(object):
    def parse(self, data):
        data = Algorithm.base64_decode(data)
        dt = Context.json_loads(data)
        Context.Log.debug(dt)
        param = {
            "appId": str(dt.get('appId', '')),
            "userId": dt.get('userId', ''),
            "order": dt.get('order', ''),
            "price": int(dt.get('price', 0)),
            "paytype": int(dt.get('payType', '')),
            "payCode": str(dt.get('payCode', '')),
            "state": dt.get('state', ''),
            "time": dt.get('time', ''),
            "gameOrder": dt.get('gameOrder', ''),
            "sign": dt.get('sign', ''),
        }
        return param

    def check_app_info(self, self_info, param):
        if self_info['appId'] != param['appId']:
            Context.Log.error('appId not match', self_info, param)
            return Order.state_verify_failed_id
        data = '%s%s%s%s' % (param['userId'], param['payCode'], param['order'], self_info['appKey'])
        sign = Algorithm.md5_encode(data)
        if sign != param['sign']:
            Context.Log.error('sign not match', sign, param)
            return Order.state_verify_failed_sign
        return Order.state_verify_success

    def pay_callback(self, request):
        data = request.raw_data()
        param = self.parse(data)
        if param['state'] != 'success':
            return 'failed'

        orderId = param['gameOrder']
        payType = param['paytype']
        price = param['price']
        parseInfo = Order.parse_order(orderId)
        if not parseInfo:
            return 'failed'

        orderInfo = Order.getOrderInfo(orderId)
        Context.Log.debug('orderInfo-----', orderInfo)
        if not orderInfo:
            return 'failed'

        state = int(orderInfo['state'])
        if state >= Order.state_pre_deliver:        # 可能并没有成功, 需要检查对单
            return 'success'

        cost = int(orderInfo['cost'])
        if price != cost:
            Context.Log.warn('price not equal', orderId, orderInfo, parseInfo)
            return 'failed'

        userId = int(orderInfo['userId'])
        gameId = int(orderInfo['gameId'])
        channel = orderInfo['channel']
        productId = orderInfo['productId']

        if not Order.judge_exist_product_id(2, productId):
            Context.Log.error('productId not exist', orderId, productId)
            return 'failed'

        qifan_app_info = Context.Configure.get_game_item_json(gameId, 'qifan.app.info')
        if not qifan_app_info:
            Context.Log.warn('qifan.app.info miss', orderId, orderInfo, parseInfo)
            return 'failed'

        result = self.check_app_info(qifan_app_info, param)
        Order.updateOrder(orderId, state=result)
        if result != Order.state_verify_success:
            return 'failed'

        Order.updateOrder(orderId, state=Order.state_pre_deliver, payType=payType)
        kvs = {
            'payTime': param['time'],
            'deliverTime': Time.current_time(),
            'thirdOrderId': param['order']
        }
        if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, payType):
            kvs['state'] = Order.state_deliver_success
        else:
            kvs['state'] = Order.state_deliver_failed

        Order.updateOrder(orderId, **kvs)
        return 'success'


QiFan = QiFan()
