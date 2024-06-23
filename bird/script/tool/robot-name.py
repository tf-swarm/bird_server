#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-08-28

import sys
from framework.context import Context

redis_key = sys.argv[1]
fname = sys.argv[2]

robot_names = []
with open(fname) as f:
    for line in f.readlines():
        robot_names.append(line[:-1])

Context.init_with_redis_key(redis_key)
Context.load_lua_script()

robot_range = Context.Configure.get_game_item_json(1, 'robot.list')
robot_range = range(robot_range[0], robot_range[1])
step = len(robot_range) / 500
Context.Log.info('robot list:[%d, %d], phone type: %d, step: %d' % (robot_range[0], robot_range[-1], len(robot_names), step))

for i, uid in enumerate(robot_range[::step]):
    old = Context.Data.get_attr(uid, 'nick')
    robot_name = robot_names[i % len(robot_names)]
    Context.Log.info(uid, 'set nick name %s to %s' % (old, robot_name))
    Context.Data.set_attr(uid, 'nick', robot_name)
