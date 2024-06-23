#!/usr/bin/env python
# -*- coding=utf-8 -*-

from framework.interface import ICallable, IContext
from framework.util.tool import Time, Tool


class BuryingPointDB(ICallable, IContext):
    field = 'burying_point'
    format = '%Y-%m-%d'
    max_b = 14

    def set_new_player_gift(self, uid):
        return
        ks = 'new_player_gift'
        ts = Time.current_ts()
        key = '%s:%d:%s' % (self.field, uid, ks)
        self.ctx.RedisStat.list_rpush(key, ts)
        return

    def set_kill_bird_info(self, uid, bird_list, chip, cur_barrel, max_barrel):
        return
        if max_barrel >= self.max_b:
            return
        ks = 'kill_bird_info'
        ts = Time.current_ts()
        key = '%s:%d:%s' % (self.field, uid, ks)
        index = 0
        for i in bird_list:
            dat = {'b': i, 'cb': cur_barrel, 'c': chip, 'ts': ts}
            self.ctx.RedisStat.list_rpush(key, self.ctx.json_dumps(dat))
            index += 1
        return

    def set_user_upgrade_info(self, uid, level, max_barrel):
        return
        if max_barrel >= self.max_b:
            return
        ks = 'user_upgrade_info'
        ts = Time.current_ts()
        key = '%s:%d:%s' % (self.field, uid, ks)
        dat = {'l': level, 'ts': ts}
        self.ctx.RedisStat.list_rpush(key, self.ctx.json_dumps(dat))
        return

    def set_up_barrel_info(self, uid, barrel_level, chip, max_barrel):
        return
        if max_barrel >= self.max_b:
            return
        ks = 'up_barrel_info'
        ts = Time.current_ts()
        key = '%s:%d:%s' % (self.field, uid, ks)
        dat = {'l': barrel_level, 'ts': ts, 'c': chip}
        self.ctx.RedisStat.list_rpush(key, self.ctx.json_dumps(dat))
        return

    def set_skill_info(self, uid, skill, max_barrel):
        return
        if max_barrel >= self.max_b:
            return
        ks = 'skill_%s_info'%skill
        ts = Time.current_ts()
        key = '%s:%d:%s' % (self.field, uid, ks)
        self.ctx.RedisStat.list_rpush(key, ts)
        return

    def set_enter_primary_table_info(self, uid, chip, max_barrel):
        return
        if max_barrel >= self.max_b:
            return
        ks = 'enter_primary_table_info'
        ts = Time.current_ts()
        key = '%s:%d:%s' % (self.field, uid, ks)
        dat = {'ts': ts, 'c': chip}
        self.ctx.RedisStat.list_rpush(key, self.ctx.json_dumps(dat))
        return

    def set_daily_sign_info(self, uid, max_barrel):
        return
        if max_barrel >= self.max_b:
            return
        ks = 'daily_sign_info'
        ts = Time.current_ts()
        key = '%s:%d:%s' % (self.field, uid, ks)
        self.ctx.RedisStat.list_rpush(key, ts)
        return

    def set_lost_connect_info(self, uid):
        return
        barrel_level = self.ctx.Data.get_game_attr_int(uid, 2, 'barrel_level', 1)
        if barrel_level >= self.max_b:
            return
        ks = 'lost_connect_info'
        ts = Time.current_ts()

        conf = self.ctx.Configure.get_game_item_json(2, 'barrel.unlock.config')
        bl = conf[barrel_level - 1]['multiple']
        chip = self.ctx.Data.get_game_attr_int(uid, 2, 'chip', 0)
        dat = {'ts': ts, 'c': chip, 'b': bl}

        key = '%s:%d:%s' % (self.field, uid, ks)
        self.ctx.RedisStat.list_rpush(key, self.ctx.json_dumps(dat))
        return

    def set_user_bankrupt_info(self, uid):
        return
        barrel_level = self.ctx.Data.get_game_attr_int(uid, 2, 'barrel_level', 1)
        if barrel_level >= self.max_b:
            return
        ks = 'user_bankrupt_info'
        ts = Time.current_ts()
        key = '%s:%d:%s' % (self.field, uid, ks)
        self.ctx.RedisStat.list_rpush(key, ts)
        return

    def set_user_benefit_info(self, uid):
        return
        barrel_level = self.ctx.Data.get_game_attr_int(uid, 2, 'barrel_level', 1)
        if barrel_level >= self.max_b:
            return
        ks = 'user_benefit_info'
        ts = Time.current_ts()
        key = '%s:%d:%s' % (self.field, uid, ks)
        self.ctx.RedisStat.list_rpush(key, ts)
        return

    def set_receive_reward_info(self, uid, reward_str):
        return
        barrel_level = self.ctx.Data.get_game_attr_int(uid, 2, 'barrel_level', 1)
        if barrel_level >= self.max_b:
            return

        ks = 'receive_%s_info'%reward_str
        ts = Time.current_ts()
        key = '%s:%d:%s' % (self.field, uid, ks)
        self.ctx.RedisStat.list_rpush(key, ts)
        return

    def set_upper_bp_info(self, uid, m_str):
        return
        barrel_level = self.ctx.Data.get_game_attr_int(uid, 2, 'barrel_level', 1)
        if barrel_level >= self.max_b:
            return

        ts = Time.current_ts()
        key = '%s:%d:%s' % (self.field, uid, m_str)
        self.ctx.RedisStat.list_rpush(key, ts)
        return

BuryingPointDB = BuryingPointDB()