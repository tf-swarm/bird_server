#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-07-15

from framework.context import Context
from framework.entity.manager import TaskManager


class HttpSdk(object):
    def __init__(self, gid, http_sdk, devId, version, devName):
        self.gid = gid
        self.http_sdk = http_sdk
        self.devId = devId
        self.version = version
        self.devName = devName
        self.has_login = False
        self.cookies = {}
        self.roomType = None
        self.tableId = None
        self.seatId = None
        self.userId = None
        self.session = None
        self.host = None
        self.port = None

    def send_to_sdk(self, path, param, **kwargs):
        url = self.http_sdk + path
        if isinstance(param, dict):
            data = Context.json_dumps(param)
        else:
            data = param
        return Context.WebPage.wait_for_json(url, postdata=data, cookies=self.cookies, **kwargs)

    def simulate_callback(self, path, param, **kwargs):
        url = self.http_sdk + path
        if isinstance(param, dict):
            data = Context.json_dumps(param)
        else:
            data = param
        return Context.WebPage.wait_for_page(url, postdata=data, **kwargs)

    def loginByGuest(self):
        if not self.gid:
            raise Exception('gid must be right')

        params = {
            'gameId': self.gid,
            'deviceId': self.devId,
            'devName': self.devName,
            'releaseVer': self.version
        }
        try:
            mi = self.send_to_sdk('/v1/user/loginByGuest', params)
            if 'error' not in mi:
                for k, v in mi.iteritems():
                    setattr(self, k, v)
                self.has_login = True
        except Exception, e:
            Context.Log.exception()

    def registerByUserName(self, username, password):
        if not self.gid:
            raise Exception('gid must be right')

        params = {
            'gameId': self.gid,
            'userName': username,
            'passwd': password,
            'releaseVer': self.version
        }
        try:
            mi = self.send_to_sdk('/v1/user/registerByUserName', params)
            if 'error' not in mi:
                for k, v in mi.iteritems():
                    setattr(self, k, v)
                self.has_login = True
        except Exception, e:
            Context.Log.exception()

    def get_order_id(self, productId, channel='qifan', platform='android'):
        params = {
            'gameId': self.gid,
            'channel': channel,
            'platform': platform,
            'productId': productId,
        }
        return self.send_to_sdk('/v1/order/create', params)

    def run_as_player(self):
        return self.loginByGuest()


def main(httpClient):
    redis_key = '127.0.0.1:6379:0'
    Context.init_with_redis_key(redis_key)
    params = Context.Configure.get_global_item_json('params')
    Context.Log.open_std_log()
    http_sdk = params['server']['http.sdk']
    http = httpClient(2, http_sdk, 'test', 'test', 'test')
    http.run_as_player()
    # http.registerByUserName('测试1', '111111')
    TaskManager.end_loop()


if __name__ == '__main__':
    TaskManager.add_simple_task(main, HttpSdk)
    TaskManager.start_loop()
