#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-08-05

from framework.util.tool import Tool
from framework.util.tool import Time
from framework.interface import IContext

class Stat(IContext):
    prefix = 'stat'
    format = '%Y-%m-%d'
    online = 'online'

    def get_daily_data(self, channel_id, *field):
        return self.get_day_data(channel_id, Time.current_time(self.format), *field)

    def get_day_data(self, channel_id, fmt, *field):
        key = '%s:%s:%s' % (self.prefix, channel_id, fmt)
        if not field:
            return self.ctx.RedisStat.hash_getall(key)
        elif len(field) == 1:
            return self.ctx.RedisStat.hash_get(key, *field)
        else:
            return self.ctx.RedisStat.hash_mget(key, *field)

    def setnx_daily_data(self, channel_id, field, value):
        key = '%s:%s:%s' % (self.prefix, channel_id, Time.current_time(self.format))
        return self.ctx.RedisStat.hash_setnx(key, field, value)

    def set_daily_data(self, channel_id, fmt, field, value):
        key = '%s:%s:%s' % (self.prefix, channel_id, fmt)
        return self.ctx.RedisStat.hash_set(key, field, value)

    def incr_daily_data(self, channel_id, field, delta=1):
        key = '%s:%s:%s' % (self.prefix, channel_id, Time.current_time(self.format))
        return self.ctx.RedisStat.hash_incrby(key, field, delta)

    def incr_daily_time_data(self, channel_id, times, field, delta=1):
        key = '%s:%s:%s' % (self.prefix, channel_id, times)
        return self.ctx.RedisStat.hash_incrby(key, field, delta)

    def incr_user_data(self, uid, gid, field, delta=1):
        key = 'user:%s:%s' % (gid, uid)
        return self.ctx.RedisStat.hash_incrby(key, field, delta)

    def mincr_user_data(self, uid, gid, *args, **kwargs):
        key = 'user:%s:%s' % (gid, uid)
        return self.ctx.RedisStat.hash_mincrby(key, *args, **kwargs)

    def get_user_data(self, gid, uid, *field):
        key = 'user:%s:%s' % (gid, uid)
        if not field:
            return self.ctx.RedisStat.hash_getall(key)
        elif len(field) == 1:
            return self.ctx.RedisStat.hash_get(key, *field)
        else:
            return self.ctx.RedisStat.hash_mget(key, *field)

    def mincr_daily_data(self, channel_id, *args, **kwargs):
        key = '%s:%s:%s' % (self.prefix, channel_id, Time.current_time(self.format))
        return self.ctx.RedisStat.hash_mincrby(key, *args, **kwargs)

    def incr_daily_user_data(self, channel_id, uid, field, delta=1):
        key = 'user_daily:%s:%s:%s' % (channel_id, Time.current_time(self.format), str(uid))
        return self.ctx.RedisStat.hash_incrby(key, field, delta)

    def mincr_daily_user_data(self, channel_id, uid, *args, **kwargs):
        key = 'user_daily:%s:%s:%s' % (channel_id, Time.current_time(self.format) , str(uid))
        return self.ctx.RedisStat.hash_mincrby(key, *args, **kwargs)

    def get_daily_user_data(self, channel_id, uid, fmt, *field):
        key = 'user_daily:%s:%s:%s' % (channel_id, fmt, str(uid))
        if not field:
            return self.ctx.RedisStat.hash_getall(key)
        elif len(field) == 1:
            return self.ctx.RedisStat.hash_get(key, *field)
        else:
            return self.ctx.RedisStat.hash_mget(key, *field)

    def on_online_timer(self, gid):
        game_room = self.ctx.GData.map_room_type.get(gid)
        room_types = sorted(game_room.keys())
        online = self.ctx.Online.get_online(gid, *room_types)
        online_list = []
        for _online in online:
            _online = Tool.to_int(_online, 0)
            online_list.append(_online)
        if len(room_types) <= 0 or len(online_list) <=0 or len(room_types) != len(online_list):
            return
        for k, v in enumerate(room_types):
            rdb = '%s:%s:%s' % (self.online+str(v), gid, Time.current_time(self.format))
            now_ts = Time.datetime()
            now_hours = now_ts.hour
            now_node = int(now_ts.minute/10)
            key = '%d_%d'%(now_hours,now_node)
            value = online_list[k]
            self.ctx.RedisStat.hash_setnx(rdb, key, value)

    def get_online_data(self, gid, fmt, room):
        self.ctx.Log.info(gid, fmt, room)
        key = '%s:%s:%s' % (self.online + str(room), gid, fmt)
        return self.ctx.RedisStat.hash_getall(key)

Stat = Stat()
