#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-08-04

from framework.util.tool import Tool, Time
from framework.context import Context
from framework.entity.const import Message
from framework.entity.msgpack import MsgPack
from mail import Mail
import copy


class BirdMatch(object):
    def __init__(self):
        return

    def get_config(self, gid):
        normal_config = Context.Configure.get_game_item_json(gid, 'match.normal.config')
        rank_reward = Context.Configure.get_game_item_json(gid, 'match.rank.reward')
        Context.Log.info('normal_config', normal_config, type(normal_config))
        conf = copy.deepcopy(normal_config)
        if conf.has_key('barrel'):
            del conf['barrel']
        if conf.has_key('bullet'):
            del conf['bullet']
        if conf.has_key('left_time'):
            del conf['left_time']

        for k,v in rank_reward.items():
            if k == '1':
                data = v
                if data.has_key('count'):
                    del data['count']
                if data.has_key('level'):
                    del data['level']
                conf['primary'] = data
            if k == '2':
                data = v
                if data.has_key('count'):
                    del data['count']
                if data.has_key('level'):
                    del data['level']
                conf['middle'] = data
            if k == '3':
                data = v
                if data.has_key('count'):
                    del data['count']
                if data.has_key('level'):
                    del data['level']
                conf['high'] = data
        if not conf.has_key('open'):
            conf['open'] = 1
        return conf

    #用于处理限时商城开启和关闭的定时器
    def on_match_room_timer(self, gid):
        normal_config = Context.Configure.get_game_item_json(gid, 'match.normal.config')
        open_time_1 = Tool.to_int(normal_config['start_1'])
        close_time_1 = Tool.to_int(normal_config['end_1'])
        open_time_2 = Tool.to_int(normal_config['start_2'])
        close_time_2 = Tool.to_int(normal_config['end_2'])
        open = Tool.to_int(normal_config.get('open'), 1)
        if open == 0:
            return
        now_ts = Time.datetime()
        led = u""
        if now_ts.hour in [open_time_1 - 1, open_time_2 - 1] and now_ts.minute >= 55: #竞技场开启前五分钟每分钟一个公告
            led = u'尊敬的各位玩家，<color=#00FF00FF>竞技场-快速赛</color>即将开启，请各位玩家做好战斗准备！'
        elif (((now_ts.hour > open_time_1 and now_ts.hour < close_time_1) or
                (now_ts.hour > open_time_2 and now_ts.hour < close_time_2)) and now_ts.minute in [0,30]) or \
                (now_ts.hour in [open_time_1, open_time_2] and now_ts.minute == 30): #竞技场开始后每半小时一个公告
            led = u'尊敬的各位玩家，当前<color=#00FF00FF>竞技场-快速赛</color>正火热开启中，快来加入到紧张刺激的比赛中吧！'
        elif now_ts.hour in [open_time_1, open_time_2] and now_ts.minute == 0 : #竞技场开启的公告
            led = u'尊敬的各位玩家，当前<color=#00FF00FF>竞技场-快速赛</color>已<color=#00FF00FF>开启</color>，快来加入到紧张刺激的比赛中吧！'
        elif now_ts.hour in [close_time_1, close_time_2] and now_ts.minute == 0: #竞技场结束公告,结算奖励
            self.deal_match_end_cache(gid)
            led = u'<color=#00FF00FF>竞技场-快速赛</color>已<color=#00FF00FF>关闭</color>，已报名但未参赛的玩家，<color=#FFFF00FF>报名费</color>会退还到各位的背包中，请注意查收！'
        if len(led) > 0:
            self.send_broadcast_to_system(led)

    def send_broadcast_to_system(self, led):
        bulletin = 3
        mo = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
        mo.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
        Context.GData.broadcast_to_system(mo)
        return

    def deal_match_end_cache(self, gid):
        for i in [1,2,3]:
            keys = 'match:%d'%i
            ret = Context.RedisMatch.hget_keys('%s:*'%keys)
            for j in ret:
                match_id = int(j.split('%s:'%keys)[1])
                status = Context.MatchDB.get_match_data(str(i), str(match_id), 'status')
                status = Tool.to_int(status,2)
                if status <= 1:
                    seat0, seat1, seat2, seat3, seat4, seat5, seat6, seat7 = Context.MatchDB.get_match_seat_info(i, match_id)
                    for k in [seat0, seat1, seat2, seat3, seat4, seat5, seat6, seat7]:
                        self.del_cache(k, gid, str(i))
                    Context.RedisMatch.delete('match:%d:%d' % (i, match_id))

    def deal_reboot_server(self, gid):
        for i in [1,2,3]:
            keys = 'match:%d'%i
            ret = Context.RedisMatch.hget_keys('%s:*'%keys)
            for j in ret:
                match_id = int(j.split('%s:'%keys)[1])
                seat0, seat1, seat2, seat3, seat4, seat5, seat6, seat7 = Context.MatchDB.get_match_seat_info(str(i), match_id)
                for k in [seat0, seat1, seat2, seat3, seat4, seat5, seat6, seat7]:
                    self.del_cache(k, gid, str(i))
                Context.RedisMatch.delete('match:%d:%d' % (i, match_id))

    def del_cache(self, uid, gid, level):
        if uid > 1000000:
            Context.RedisMatch.delete('match:player:%d' % (uid))
            match_rank_reward = Context.Configure.get_game_item_json(gid, 'match.rank.reward')
            cost = match_rank_reward[level]['cost']
            times = Time.current_ts()
            reward_p = {'chip': cost}
            ret = Mail.add_mail(uid, gid, times, 11, reward_p, -1)
            if ret:
                Mail.send_mail_list(uid, gid)

BirdMatch = BirdMatch()
