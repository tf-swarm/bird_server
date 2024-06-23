#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: cui

from props import BirdProps
from framework.util.tool import Time
from framework.util.tool import Tool
from framework.context import Context
from framework.entity.msgpack import MsgPack
from framework.entity.const import Message


class BirdGroupBuy(object):
    def on_buy(self, uid, gid):
        now_dt = Time.datetime()
        prefix = Time.datetime_to_str(now_dt, '%Y-%m-%d')
        conf = Context.Configure.get_game_item_json(gid, 'group_buy.config')
        # 更新购买信息
        key = 'group_buy:%d:%s' % (gid, prefix)
        Context.RedisMix.hash_incrby(key, 'total', 1)
        Context.RedisMix.hash_incrby(key, uid, 1)
        return True

    '''def get_group_buy_reward(self, uid, gid, mi):
        reward_id = mi.get_param('id')
        mo = MsgPack(Message.MSG_SYS_GROUP_BUY_REWARD | Message.ID_ACK)
        conf = Context.Configure.get_game_item_json(gid, 'group_buy.config')
        if type(reward_id) != int or reward_id <0 or reward_id > len(conf['reward_info']):
            return mo.set_error(1, 'error id')
        reward_conf = conf['reward_info'][reward_id-1]

        prefix = Time.datetime_now('%Y-%m-%d')
        key = 'group_buy:%d:%s' % (gid, prefix)
        total, ids, buy_count = Context.RedisMix.hash_mget(key, 'total', '%s.ids' % uid, uid)
        if not buy_count:
            return mo.set_error(2, 'can not')
        total = Tool.to_int(total, 0)
        if total < reward_conf['num']:
            return mo.set_error(3, 'not done')
        if ids:
            ids = Context.json_loads(ids)
        else:
            ids = []
        if reward_id in ids:
            return mo.set_error(4, 'already')

        ids.append(reward_id)
        Context.RedisMix.hash_set(key, '%s.ids' % uid, Context.json_dumps(ids))
        Context.RedisMix.hash_incrby(key, 'reward.' + str(reward_id), 1)
        BirdProps.issue_rewards(uid, gid, reward_conf['reward'], 'group_buy', rid=reward_id)
        return mo
        '''

    def get_group_buy_info(self, uid, gid, mi):
        conf = Context.Configure.get_game_item_json(gid, 'group_buy.config')
        now_dt = Time.datetime()
        prefix = Time.datetime_to_str(now_dt, '%Y-%m-%d')
        now_ts = Time.current_ts(now_dt)
        start_ts = Time.str_to_timestamp('%s %s' % (prefix, conf['start']))
        if now_ts < start_ts:
            now_dt = Time.next_days(days=-1)
            prefix = Time.datetime_to_str(now_dt, '%Y-%m-%d')

        mo = MsgPack(Message.MSG_SYS_GROUP_BUY_INFO | Message.ID_ACK)
        key = 'group_buy:%d:%s' % (gid, prefix)
        total, ids, buy_count = Context.RedisMix.hash_mget(key, 'total', '%d.ids' % uid, uid)
        total = Tool.to_int(total, 0)
        mo.set_param('count', total)
        if not buy_count:
            buy_state = 0
        else:
            buy_state = 1
        mo.set_param('buy_state', buy_state)
        if ids:
            ids = Context.json_loads(ids)
            mo.set_param('ids', ids)
        return mo


BirdGroupBuy = BirdGroupBuy()
