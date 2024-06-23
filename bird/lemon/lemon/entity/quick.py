#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-12-17

from framework.context import Context
from framework.util.tool import Time, Tool

class Quick(object):
    @classmethod
    def get_free_table(cls, gid):
        key = 'cache.%d.relax_info.hash' % gid
        Context.RedisCache.hash_setnx(key, 'max.relax_table.id', 1000)
        table_id = Context.RedisCache.hash_incrby(key, 'max.relax_table.id', 1)
        return table_id

    def get_free_vip_table(cls, gid):
        key = 'cache.%d.info.hash' % gid
        Context.RedisCache.hash_setnx(key, 'max.table.id', 1000)
        table_id = Context.RedisCache.hash_incrby(key, 'max.table.id', 1)
        return table_id

    @classmethod
    def get_match_free_table(cls, gid):
        key = 'cache.%d.info.hash' % gid
        Context.RedisCache.hash_setnx(key, 'max.table.id', 1000)
        table_id = Context.RedisCache.hash_incrby(key, 'max.table.id', 1)
        return table_id

    @classmethod
    def get_free_match(cls, gid, level):
        key = 'match:%d:'%level
        match_list = Context.RedisMatch.hget_keys(key+'*')
        for i in match_list:
            match_id = str(i.split(key)[1])
            seat0, seat1, seat2, seat3, seat4, seat5, seat6, seat7 = \
                Context.MatchDB.get_match_seat_info(level, match_id)
            status = Context.MatchDB.get_match_data(str(level), str(match_id), 'status')
            if (seat0 <= 0 or seat1 <= 0 or seat2 <= 0 or seat3 <= 0 or seat4 <= 0
                 or seat5 <= 0 or seat6 <= 0 or seat7 <= 0) and Tool.to_int(status, 0) == 1:
                return int(match_id)

        key_1 = 'cache.%d.info.hash' % gid
        Context.RedisCache.hash_setnx(key_1, 'max.match.id', 10000)
        match_id = Context.RedisCache.hash_incrby(key_1, 'max.match.id', 1)

        keys = key + str(match_id)
        kvs = {
            'seat0': 0,
            'seat1': 0,
            'seat2': 0,
            'seat3': 0,
            'seat4': 0,
            'seat5': 0,
            'seat6': 0,
            'seat7': 0,
            'status': 1, #竞技场创建时是准备状态
            'table_id_0': 0,
            'table_id_1': 0,
            'table_status_0': 0,
            'table_status_1': 0,
            'send_reward': 0,
            'match_start_ts': 0,
        }
        Context.RedisMatch.hash_mset(keys, **kvs)
        return match_id

