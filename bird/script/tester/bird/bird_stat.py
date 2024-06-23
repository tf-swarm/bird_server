#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-03-25

import sys
from framework.context import Context
from framework.entity.manager import TaskManager


def main(start, end):
    redis_key = '127.0.0.1:6379:0'
    Context.init_with_redis_key(redis_key)
    fields = ['pool.shot.202', 'pool.reward.202']
    shot, reward = Context.RedisMix.hash_mget('game.2.info.hash', *fields)
    print shot, reward
    while start <= end:
        chip = Context.UserAttr.get_chip(start, 2, 0)
        print start, chip
        start += 1
    TaskManager.end_loop()


if __name__ == '__main__':
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    TaskManager.add_simple_task(main, start, end)
    TaskManager.start_loop()
