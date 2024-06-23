#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-06-08

from framework.context import Context
from framework.util.tool import Time


class Share(object):
    def get_invitee(self, uid, gid):
        key = 'share:%d:%d' % (gid, uid)
        kvs = Context.RedisCluster.hash_getall(uid, key)
        _kvs = {}
        for k, v in kvs.iteritems():
            _kvs[int(k)] = Context.json_loads(v)
        return _kvs

    def get_invitee_by_uid(self, uid, gid, invitee):
        key = 'share:%d:%d' % (gid, uid)
        return Context.RedisCluster.hash_get_json(uid, key, invitee)

    def add_invitee(self, uid, gid, invitee, *args):
        v = self.get_invitee_by_uid(uid, gid, invitee)
        if not v:
            v = {'ts': Time.current_ts(), 'ids': []}
        for arg in args:
            if arg not in v['ids']:
                v['ids'].append(arg)
        key = 'share:%d:%d' % (gid, uid)
        Context.RedisCluster.hash_set(uid, key, invitee, Context.json_dumps(v))
        return v
