#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-03-24

from tester.HttpSdk import HttpSdk
from framework.context import Context
from framework.entity.manager import TaskManager


class BirdHttp(HttpSdk):
    gid = 2
    http_game = 'http://127.0.0.1:9006'

    def run_as_player(self):
        self.loginByGuest()
        if self.has_login:
            self.get_activity_list()
            # self.get_history()
            # self.get_rank_list()
            # self.upgrade_check()

    def send_to_http(self, path, param):
        url = self.http_game + path
        data = Context.json_dumps(param)
        return Context.WebPage.wait_for_json(url, postdata=data)

    def get_activity_list(self):
        param = {
            'userId': int(self.userId),
            'gameId': self.gid,
            'session': self.session,
        }
        self.send_to_http('/v1/game/activity_list', param)

    def consume_activity(self):
        param = {
            'userId': int(self.userId),
            'gameId': self.gid,
            'session': self.session,
            'id': 200,
        }
        self.send_to_http('/v1/game/consume_activity', param)

    def get_rank_list(self):
        param = {
            'userId': int(self.userId),
            'gameId': self.gid,
            'session': self.session,
            'rank': ['day']
        }
        self.send_to_http('/v1/game/rank_list', param)

    def get_history(self):
        param = {
            'userId': self.userId,
            'gameId': self.gid,
            'session': self.session,
            'which': 'fame'
        }
        self.send_to_http('/v1/game/history', param)

    def upgrade_check(self):
        param = {
            'gameId': self.gid,
            "version": "1.0.0",
            "channel": "qifan",
            "platform": "android"
        }
        self.send_to_sdk('/v1/upgrade/check', param)


if __name__ == '__main__':
    from tester.HttpSdk import main

    TaskManager.add_simple_task(main, BirdHttp)
    TaskManager.start_loop()
