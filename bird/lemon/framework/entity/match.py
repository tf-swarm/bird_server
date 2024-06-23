#!/usr/bin/env python
# -*- coding=utf-8 -*-

from framework.interface import ICallable, IContext
from framework.util.tool import Time, Tool


class MatchDB(ICallable, IContext):
    player_field = 'match'
    format = '%Y-%m-%d'

    def get_match_data(self, table_name, table_key, *field):
        key = '%s:%s:%s' % (self.player_field, table_name, table_key)
        if not field:
            return self.ctx.RedisMatch.hash_getall(key)
        elif len(field) == 1:
            return self.ctx.RedisMatch.hash_get(key, *field)
        else:
            return self.ctx.RedisMatch.hash_mget(key, *field)

    def set_match_data(self, table_name, table_key, field, value):
        key = '%s:%s:%s' % (self.player_field, table_name, table_key)
        return self.ctx.RedisMatch.hash_set(key, field, value)

    def incr_match_data(self, table_name, table_key, field, delta=1):
        key = '%s:%s:%s' % (self.player_field, table_name, table_key)
        return self.ctx.RedisMatch.hash_incrby(key, field, delta)

    def mincr_match_data(self, table_name, table_key, *args, **kwargs):
        key = '%s:%s:%s' % (self.player_field, table_name, table_key)
        return self.ctx.RedisMatch.hash_incrby(key, *args, **kwargs)

    def get_match_seat_info(self, level, match_id):
        seat0, seat1, seat2, seat3, seat4, seat5, seat6, seat7 = \
            self.get_match_data(str(level), match_id, 'seat0', 'seat1', 'seat2', 'seat3',
                                              'seat4', 'seat5', 'seat6', 'seat7')
        seat0 = Tool.to_int(seat0, 0)
        seat1 = Tool.to_int(seat1, 0)
        seat2 = Tool.to_int(seat2, 0)
        seat3 = Tool.to_int(seat3, 0)
        seat4 = Tool.to_int(seat4, 0)
        seat5 = Tool.to_int(seat5, 0)
        seat6 = Tool.to_int(seat6, 0)
        seat7 = Tool.to_int(seat7, 0)
        return seat0,seat1,seat2,seat3,seat4,seat5,seat6,seat7

    def get_match_player_status(self, uid):
        level , match_id = self.ctx.MatchDB.get_match_data('player', uid, 'level', 'match_id')
        if level == None or match_id == None:
            return False
        status, table_id = self.ctx.MatchDB.get_match_data(str(level), match_id, 'status', 'table_id')
        status = Tool.to_int(status, 0)
        table_id = Tool.to_int(table_id, 0)
        if status >= 1 and table_id > 1000:
            return True
        return False

MatchDB = MatchDB()
