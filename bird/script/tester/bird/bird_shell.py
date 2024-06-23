#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-03-24

from framework.context import Context
from framework.entity.manager import TaskManager
from framework.util.tool import Time
from framework.util.tool import Algorithm


class BirdShell(object):
    gid = 2
    http_shell = 'http://127.0.0.1:9000'

    def __init__(self):
        self.access_key = Context.Configure.get_global_item('shell.access_key')

    def send_to_http(self, path, param):
        url = self.http_shell + path
        ts = Time.current_ts()
        s = 'gameId=%d&token=%s&ts=%d' % (self.gid, self.access_key, ts)
        sign = Algorithm.md5_encode(s)
        param['ts'] = ts
        param['sign'] = sign
        param['gameId'] = self.gid
        data = Context.json_dumps(param)
        return Context.WebPage.wait_for_json(url, postdata=data)

    def run_as_tester(self):
        # self.query_overview()
        # self.query_summary()
        # self.query_pay_detail()
        # self.query_chip_consume()
        # self.query_chip_produce()
        # self.query_diamond_consume()
        # self.query_diamond_produce()
        # self.query_egg_fall()
        # self.query_shot()
        # self.query_raffle()
        # self.query_room_211()
        # self.query_chip_carrying()
        # self.query_user_info()
        # self.query_history_phone()
        # self.gm_reward_chip()
        # self.gm_reward_diamond()
        # self.gm_reward_vip()
        # self.gm_reward_card()
        # self.gm_reward_egg()
        # self.gm_freeze_account()
        # self.gm_disable_account()
        # self.gm_exchange_phone()
        # self.gm_push_led()
        # self.gm_version_upgrade()
        # self.gm_reward_coupon_pool()
        self.gm_query_coupon_pool()

    def query_overview(self):
        param = {
        }
        self.send_to_http('/v1/shell/query/overview', param)

    def query_summary(self):
        param = {
            'start': '2016-03-30',
            'end': '2016-03-30',
        }
        self.send_to_http('/v1/shell/query/summary', param)

    def query_pay_detail(self):
        param = {
            'start': '2016-03-23',
            'end': '2016-03-24',
        }
        self.send_to_http('/v1/shell/query/pay/detail', param)

    def query_chip_consume(self):
        param = {
            'start': '2016-03-29',
            'end': '2016-03-29',
        }
        self.send_to_http('/v1/shell/query/chip/consume', param)

    def query_chip_produce(self):
        param = {
            'start': '2016-03-29',
            'end': '2016-03-29',
        }
        self.send_to_http('/v1/shell/query/chip/produce', param)

    def query_diamond_consume(self):
        param = {
            'start': '2016-03-29',
            'end': '2016-03-29',
        }
        self.send_to_http('/v1/shell/query/diamond/consume', param)

    def query_diamond_produce(self):
        param = {
            'start': '2016-03-29',
            'end': '2016-03-29',
        }
        self.send_to_http('/v1/shell/query/diamond/produce', param)

    def query_egg_fall(self):
        param = {
            'start': '2016-03-28',
            'end': '2016-03-29',
        }
        self.send_to_http('/v1/shell/query/props/egg/fall', param)

    def query_shot(self):
        param = {
            'start': '2016-03-29',
            'end': '2016-03-29',
        }
        self.send_to_http('/v1/shell/query/shot', param)

    def query_raffle(self):
        param = {
            'start': '2016-09-01',
            'end': '2016-09-04',
        }
        self.send_to_http('/v1/shell/query/raffle', param)

    def query_room_211(self):
        param = {
            'start': '2016-09-01',
            'end': '2016-09-04',
        }
        self.send_to_http('/v1/shell/query/room/211', param)

    def query_chip_carrying(self):
        param = {
            'start': '2016-03-29',
            'end': '2016-03-29',
        }
        self.send_to_http('/v1/shell/query/chip/carrying', param)

    def query_user_info(self):
        param = {
            'userId': 20201,
        }
        self.send_to_http('/v1/shell/query/user/info', param)

    def gm_reward_chip(self):
        param = {
            'userId': 20002,
            'chip': 1000,
        }
        self.send_to_http('/v1/shell/gm/reward/chip', param)

    def gm_reward_diamond(self):
        param = {
            'userId': 20001,
            'diamond': 1000,
        }
        self.send_to_http('/v1/shell/gm/reward/diamond', param)

    def gm_reward_vip(self):
        param = {
            'userId': 20002,
            'rmb': 100,
        }
        self.send_to_http('/v1/shell/gm/reward/vip', param)

    def gm_reward_card(self):
        param = {
            'userId': 66863,
            'days': 30,
        }
        self.send_to_http('/v1/shell/gm/reward/card', param)

    def gm_reward_egg(self):
        param = {
            'userId': 20002,
            'id': 214,
            'count': 2,
        }
        self.send_to_http('/v1/shell/gm/reward/egg', param)

    def gm_freeze_account(self):
        param = {
            'userId': 20003,
            'days': 10,
        }
        self.send_to_http('/v1/shell/gm/account/freeze', param)

    def gm_disable_account(self):
        param = {
            'userId': 20003,
        }
        self.send_to_http('/v1/shell/gm/account/disable', param)

    def gm_exchange_phone(self):
        param = {
            'userId': 20277,
            'seq': 12,
        }
        self.send_to_http('/v1/shell/gm/exchange/phone', param)

    def query_history_phone(self):
        param = {
            'userId': 20003,
            'start': '2016-04-08',
            'end': '2016-04-08',
        }
        self.send_to_http('/v1/shell/query/history/phone', param)

    def gm_push_led(self):
        param = {
            'msg': 'I am led'
        }
        self.send_to_http('/v1/shell/gm/push/led', param)

    def gm_version_upgrade(self):
        param = {
            "version": "1.0.1",
            "changelog": "fix bug",
            "size": "24.4M",
            "bytes": 25611070,
            "md5": "8401ae3be6d9b6052a57716f7e81f7b2",
            "url": "http://cdn-p3.gtestin.cn/41eb50e6f94345988372bcd1c161b579.apk",
            "channel": "qifan",
            "platform": "android",
            "prompt": "1.0.1",
            "force": "1.0.0",
        }
        self.send_to_http('/v1/shell/gm/version/upgrade', param)

    def gm_reward_coupon_pool(self):
        param = {
            'userId': 20002,
            'coupon_pool': 20,
        }
        self.send_to_http('/v1/shell/gm/reward/coupon_buff', param)

    def gm_query_coupon_pool(self):
        param = {
            'userId': 20002,
        }
        self.send_to_http('/v1/shell/gm/query/coupon_buff', param)

def main():
    redis_key = '127.0.0.1:6379:0'
    Context.init_with_redis_key(redis_key)
    Context.Log.open_std_log()
    shell = BirdShell()
    shell.run_as_tester()
    TaskManager.end_loop()


if __name__ == '__main__':
    TaskManager.add_simple_task(main)
    TaskManager.start_loop()
