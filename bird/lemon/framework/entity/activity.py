#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-08-03

from framework.interface import ICallable
from framework.interface import IContext
from framework.util.tool import Tool
from framework.util.tool import Time


class Activity(ICallable, IContext):
    def get_activity_data(self, uid, gid, attr, default = None):
        key = 'activity:%s:%d' % (gid, uid)
        return self.ctx.RedisActivity.hash_get(key, attr, default)

    def set_activity_data(self, uid, gid, attr, value):
        key = 'activity:%s:%d' % (gid, uid)
        return self.ctx.RedisActivity.hash_set(key, attr, value)

    def get_activity_data_json(self, uid, gid, attr, default=None):
        key = 'activity:%s:%d' % (gid, uid)
        return self.ctx.RedisActivity.hash_get_json(key, attr, default)

    def get_activity_all_data(self, uid, gid):
        key = 'activity:%s:%d' % (gid, uid)
        return self.ctx.RedisActivity.hash_getall(key)

    def del_activity_data(self, uid, gid, *attrs):
        key = 'activity:%s:%d' % (gid, uid)
        return self.ctx.RedisActivity.hash_del(key, *attrs)

    def hincr_activity_data(self, uid, gid, attr, delta):
        key = 'activity:%s:%d' % (gid, uid)
        return self.ctx.RedisActivity.hash_incrby(key, attr, delta)

    def mget_activity_data(self, uid, gid, attr):
        key = 'activity:%s:%d' % (gid, uid)
        return self.ctx.RedisActivity.hash_mget(key, *attr)

    def mset_activity_data(self, uid, gid, attr):
        key = 'activity:%s:%d' % (gid, uid)
        return self.ctx.RedisActivity.hash_mset(key, **attr)


Activity = Activity()
