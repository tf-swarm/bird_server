#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-05-04

from framework.context import Context
from framework.util.tool import Tool
from framework.entity.manager import TaskManager
from lemon.games.bird.account import BirdProps
from lemon.games.bird.account import BirdAccount

redis_config = {
    "config": {"host": "10.44.167.229", "port": 16379, "db": 0},
    "cluster": [
        {"host": "10.44.167.229", "port": 16380, "db": 0},
        {"host": "10.44.167.229", "port": 16381, "db": 0},
        {"host": "10.44.167.229", "port": 16382, "db": 0},
        {"host": "10.44.167.229", "port": 16383, "db": 0},
        {"host": "10.44.167.229", "port": 16384, "db": 0},
        {"host": "10.44.167.229", "port": 16385, "db": 0},
        {"host": "10.44.167.229", "port": 16386, "db": 0},
        {"host": "10.44.167.229", "port": 16387, "db": 0}
    ],
    "mix": {"host": "10.44.167.229", "port": 16400, "db": 0},
    "pay": {"host": "10.44.167.229", "port": 16401, "db": 0},
    "stat": {"host": "10.44.167.229", "port": 16402, "db": 0},
    "cache": {"host": "10.44.167.229", "port": 16403, "db": 0}
}


def main():
    Context.Log.open_std_log()
    Context.init_with_redis_json(redis_config)
    Context.load_lua_script()
    max_uid = Context.RedisMix.hash_get_int('global.info.hash', 'max.user.id', 0)
    total_user[0] = max_uid + 1 - 1000000
    for uid in xrange(1000000, max_uid + 1):
        TaskManager.add_simple_task(query_one, uid)


def query_one(uid):
    # barrel_level, pay_total = Context.Data.get_game_attrs(uid, gid, ['barrel_level', 'pay_total'])
    # if barrel_level == '54':
    #    pay_total = Tool.to_int(pay_total, 0)
    #    vip = BirdAccount.get_vip_level(uid, gid, pay_total)
    #    gem = BirdProps.get_props(uid, gid, 219)
    #    user_cache.append('%d %d %d' % (uid, vip, gem))
    gem = BirdProps.get_props(uid, gid, 219)
    user_cache.append('%d %d' % (uid, gem))
    total_user[0] -= 1
    if total_user[0] <= 0:
        TaskManager.end_loop()


if __name__ == '__main__':
    import sys

    gid = int(sys.argv[1])
    cache_file = sys.argv[2]
    fd_cache = open(cache_file, 'w')
    user_cache = []
    total_user = [0]

    TaskManager.add_simple_task(main)
    TaskManager.start_loop()
    fd_cache.write('\n'.join(user_cache))
