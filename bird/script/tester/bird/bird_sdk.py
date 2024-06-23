#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-04-10

from tester.HttpSdk import HttpSdk
from sdk.modules.order import Order
from framework.context import Context
from framework.util.tool import Time
from framework.util.tool import Algorithm
from framework.entity.manager import TaskManager


class BirdSdk(HttpSdk):
    gid = 2

    def __init__(self, *args):
        super(BirdSdk, self).__init__(*args)
        self.qifan_app_info = Context.Configure.get_game_item_json(self.gid, 'qifan.app.info')

    def run_as_player(self):
        self.loginByGuest()
        if self.has_login:
            result = self.get_order_id('100633')
            if 'error' not in result:
                # self.query_order(result['orderId'])
                # self.qifan_pay_callback(self.userId, result['orderId'], result['productId'], result['cost'])
                self.qifan_replacement_order('10020001BBMAS003')

    def query_order(self, *order):
        param = {
            'gameId': self.gid,
            'orders': order
        }
        self.send_to_sdk('/v1/order/deliver', param)

    def qifan_pay_callback(self, uid, orderId, productId, price):
        param = {
            'appId': self.qifan_app_info['appId'],
            'userId': uid,
            'order': 'qifan_callback_order_id',
            'price': price,
            'payType': 10,
            'payCode': productId,
            'state': 'success',
            'time': Time.current_time(),
            'gameOrder': orderId,
            'sign': ''
        }
        self_info = Context.Configure.get_game_item_json(self.gid, 'qifan.app.info')
        data = '%s%s%s%s' % (param['userId'], param['payCode'], param['order'], self_info['appKey'])
        param['sign'] = Algorithm.md5_encode(data)
        data = Context.json_dumps(param)
        data = Algorithm.base64_encode(data)
        self.simulate_callback('/v1/third/callback/qifan/pay', data)

    def qifan_replacement_order(self, orderId):
        info = Order.getOrderInfo(orderId)
        if info:
            uid = int(info['userId'])
            pid = info['productId']
            price = int(info['cost'])
            self.qifan_pay_callback(uid, orderId, pid, price)


if __name__ == '__main__':
    from tester.HttpSdk import main

    TaskManager.add_simple_task(main, BirdSdk)
    TaskManager.start_loop()
