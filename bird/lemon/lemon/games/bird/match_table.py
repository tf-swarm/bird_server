#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-08-02

import random
from const import Enum
import copy
from pet import BirdPet
from const import Message
from rank import BirdRank
from table import BirdTable
from mail import Mail
from props import BirdProps
from account import BirdAccount
from framework.util.tool import Time, Tool
from framework.context import Context
from framework.entity.msgpack import MsgPack
from lemon.entity.gametimer import GameTimer



class MatchBirdTable(BirdTable):
    def __init__(self, gid, tid, level, match_id, table_index):
        super(MatchBirdTable, self).__init__(gid, tid)
        self.match_end_timer = GameTimer()
        self.match_rank_timer = GameTimer()
        self.match_level = level
        self.match_id = match_id
        self.table_index = table_index
        self.start_ts = 0
        self.end_ts = 0
        self._player_list = []
        match_rank_reward = Context.Configure.get_game_item_json(self.gid, 'match.rank.reward')
        self.match_rank_reward = match_rank_reward[str(self.match_level)]
        self.match_level_cost = self.match_rank_reward.get('cost')
        bullet_barrel = Context.Configure.get_game_item_json(self.gid, 'match.normal.config')
        self.barrel_config = bullet_barrel.get('barrel')
        self.bullet_config = bullet_barrel.get('bullet')
        self.left_time = Tool.to_int(bullet_barrel.get('left_time'))
        self.match_start_ts = 0
        self.match_end_ts = 0

    def reset_param(self, empty=True):
        BirdTable.reset_param(self, empty)
        if empty:
            self.start_ts = 0
            self.end_ts = 0

    def set_timer(self, action, tm, **kwargs):
        param = BirdTable.set_timer(self, action, tm, **kwargs)

        if action == 'match_end':
            self.match_end_timer.cancel()
            self.match_end_timer.setTimeout(tm, param)
        if action == 'match_rank':
            self.match_rank_timer.cancel()
            self.match_rank_timer.setTimeout(tm, param)

        return param

    def onTimer(self, cmd, gid, msg):
        BirdTable.onTimer(self, cmd, gid, msg)
        action = msg.get_param('action')

        if action == 'match_end':
            self.__handle_match_end()
        if action == 'match_rank':
            self.send_rank_to_player(timer = True)

    def switch_barrel(self, player):
        barrel = self.barrel_config
        bullet = self.bullet_config
        if player.match_bullet in bullet:
            index = bullet.index(player.match_bullet)
            player.match_barrel_multiple = barrel[index]
            mo = MsgPack(Message.BIRD_MSG_SWITCH_BARREL | Message.ID_NTF)
            mo.set_param('mt', player.match_barrel_multiple)
            mo.set_param('u', player.uid)
            self.table_broadcast(mo)
        return 0

    def on_shot_bullet(self, uid, player, mi):
        bullet = mi.get_param('b')
        angle = mi.get_param('a')
        now_ts = Time.current_ts()
        if self.match_start_ts > now_ts or self.match_end_ts < now_ts:
            return
        match_bullet = Context.MatchDB.get_match_data('player', str(uid), 'bullet')
        if player.match_bullet <= 0 or match_bullet == None:
            return
        player.match_bullet = Context.MatchDB.incr_match_data('player', str(uid), 'bullet', -1)
        mo = MsgPack(Message.BIRD_MSG_SHOT_BULLET | Message.ID_NTF)
        mo.set_param('u', uid)
        mo.set_param('b', bullet)
        player.bullet_number = bullet
        # dz 增加狂暴子弹
        player.bullet_map[bullet] = {'multi': player.match_barrel_multiple}  # dz 增加狂暴子弹
        if angle is not None:
            mo.set_param('a', angle)
            player.barrel_angle = angle
        self.switch_barrel(player)
        mo.set_param('n', player.match_bullet)
        self.table_broadcast(mo)

    def on_hit_bird(self, uid, player, mi):
        ts = Time.current_ts()
        if ts >= self.match_end_ts:
            return 6
        bullet = mi.get_param('b')
        if bullet not in player.bullet_map:
            self._warn('bullet %d maybe hit already' % bullet)
            return 1
        info = player.bullet_map[bullet]
        del player.bullet_map[bullet]

        bird = mi.get_param('i')
        bird_type = self.map.bird_type(bird)

        if bird_type is None:
            self._info('bird %d maybe caught already' % bird)
            return 0

        bullet_multiple = info['multi']
        self.map.update_bird_stat(uid, bird)
        self.check_catch_bird(player, bird_type, bird, bullet_multiple)
        return 0

    def check_catch_bird(self, player, bird_type, bird, bullet_multiple, in_violent=False):
        hit = self.map.bird_hit(bird, player.uid)
        bird_config = self.bird_config[bird_type]
        point = bird_config['point']
        rate = pow(hit/float(point), 2)
        get_point = int(point)*bullet_multiple/4
        P = random.random()
        if P < rate:
            self.loop_die_fish += 1
            player.match_score = Context.MatchDB.incr_match_data('player', str(player.uid), 'point', get_point)
            mo = MsgPack(Message.BIRD_MSG_CATCH_BIRD | Message.ID_NTF)
            mo.set_param('u', player.uid)
            mo.set_param('i', bird)
            mo.set_param('gp', get_point)
            mo.set_param('tp', player.match_score)
            self.table_broadcast(mo)

    def on_skill_super_weapon(self, uid, player, mi):
        return

    def on_skill_freeze(self, uid, player, mi):
        return

    def on_skill_portal(self, uid, player, mi):
        return

    def on_skill_violent(self, uid, player, mi):
        return

    def on_switch_barrel(self, uid, player, mi):
        return

    def get_broad_info(self, player):
        info = BirdTable.get_broad_info(self, player)
        if not player.match_score:
            player.match_score = Context.MatchDB.get_match_data('player', str(player.uid), 'point')
        info['tp'] = player.match_score
        info['l'] = player.match_bullet
        info['mb'] = player.match_barrel_multiple
        return info

    def fetch_table_info(self):
        success = BirdTable.fetch_table_info(self)
        return success

    def update_gamedata(self, player):
        BirdTable.update_gamedata(self, player)
        if player.match_bullet <= 0 and player.bullet_map:  # 退出或者断线的时候子弹没有碰撞完
            player.bullet_map.clear()
            try:
                self.process_match_result(player.uid, player)
            except Exception, e:
                Context.Log.exception(player.uid)

    def player_leave(self, uid):
        BirdTable.player_leave(self, uid)
        ts = Time.current_ts()
        nums = int(len(self.all_user))
        if ts < self.match_end_ts and nums <= 0:
            key1 = 'table_status_%d'%self.table_index
            key2 = 'table_status_%d' % (1 - self.table_index)
            Context.MatchDB.set_match_data(str(self.match_level), str(self.match_id), key1, Enum.match_table_end)
            other_status = Context.MatchDB.get_match_data(str(self.match_level), str(self.match_id), key2)
            other_status = Tool.to_int(other_status, 0)
            if other_status == Enum.match_table_end:
                self.__handle_match_end()

    def send_reward_to_all(self, player_list):
        send_reward = Context.MatchDB.get_match_data(str(self.match_level), str(self.match_id), 'send_reward')
        if send_reward == None or Tool.to_int(send_reward, 0):
            return
        count = self.match_rank_reward.get('count')
        reward_level = self.match_rank_reward.get('level')
        reward = self.match_rank_reward.get('reward')
        ret_list = copy.deepcopy(player_list)
        Context.Stat.incr_daily_data(2, 'match_ticket_chip', self.match_level_cost * len(ret_list))
        if count < len(ret_list):
            ret_list = ret_list[:count]
        Context.MatchDB.set_match_data(str(self.match_level), str(self.match_id), 'send_reward', 1)
        for k, v in enumerate(ret_list):
            level = -1
            for i, j in enumerate(reward_level):
                if k + 1 in j:
                    level = i
            if level < 0:
                continue
            reward_p = reward[level]
            chip = reward_p.get('chip')
            if level < 1:
                bulletin = 3
                mo = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
                nick = Context.Data.get_attr(int(v[0]), 'nick')
                nick = Context.hide_name(nick)
                led = u'恭喜<color=#00FF00FF>%s</color>在<color=#00FF00FF>竞技场-快速赛</color>中获得<color=#FFFF00FF>第%d名</color>奖励<color=#FFFF00FF>%d</color>鸟蛋！'%(nick, k+1, chip)
                mo.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
                Context.GData.broadcast_to_system(mo)

            Context.Stat.incr_daily_data(2, 'match_reward_chip', chip)
            times = Time.current_ts()
            ret = Mail.add_mail(int(v[0]), self.gid, times, 10, reward_p, -(k + 1))
            if ret:
                Mail.send_mail_list(int(v[0]), self.gid)
        return

    def get_player_list(self):
        if not self._player_list:
            seat0, seat1, seat2, seat3, seat4, seat5, seat6, seat7 = \
                Context.MatchDB.get_match_seat_info(self.match_level, self.match_id)
            self._player_list = [seat0, seat1, seat2, seat3, seat4, seat5, seat6, seat7]
        return self._player_list

    def get_players_point(self):
        player_point_dict = self.get_players_point_dict()
        match_rank_list = sorted(player_point_dict.items(), key=lambda x: int(x[1]), reverse=True)
        return match_rank_list

    def get_players_point_dict(self):
        player_list = self.get_player_list()
        player_point_dict = {}
        for i in player_list:
            if i <= 0:
                continue
            match_score = Tool.to_int(Context.MatchDB.get_match_data('player', str(i), 'point'), 0)
            player_point_dict[i] = match_score
        return player_point_dict

    def send_reward_to_player(self, player_list):
        mo = MsgPack(Message.MSG_SYS_MATCH_SEND_REWARD | Message.ID_ACK)
        reward_level = self.match_rank_reward.get('level')
        reward = self.match_rank_reward.get('reward')
        ret_list = player_list
        info = []
        for k, v in enumerate(ret_list):
            try:
                nick = Context.Data.get_attr(int(v[0]), 'nick')
                if not nick:
                    nick = ''
            except:
                nick = ''
            try:
                avatar = Context.Data.get_attr(int(v[0]), 'avatar', '1')
            except:
                avatar = '1'
            try:
                sex = Context.Data.get_attr_int(int(v[0]), 'sex', 0)
            except:
                sex = 0
            try:
                vip_level = BirdAccount.get_vip_level(int(v[0]), self.gid)
            except:
                vip_level = 0
            level = -1
            for i, j in enumerate(reward_level):
                if k + 1 in j:
                    level = i
            reward_p = {}
            if level >= 0:
                reward_p = BirdProps.convert_reward(reward[level])
            rank = {
                'rank': int(k),
                'id': int(v[0]),
                'nick': nick,
                'sex': int(sex),
                'avatar': avatar,
                'vip': int(vip_level),
                'point': int(v[1]),
                'reward': reward_p
            }
            info.append(rank)
        mo.set_param('rank_list', info)
        for k, v in enumerate(player_list):
            Context.GData.send_to_connect(v[0], mo)
        return

    def send_rank_to_player(self, uid = None, timer = False):
        ts = Time.current_ts()
        if ts >= self.match_end_ts:
            return
        mo = MsgPack(Message.MSG_SYS_MATCH_SEND_RANK | Message.ID_ACK)
        ret_list = self.get_players_point()
        info = []
        for k, v in enumerate(ret_list):
            try:
                nick = Context.Data.get_attr(int(v[0]), 'nick')
                if not nick:
                    nick = ''
            except:
                nick = ''
            try:
                avatar = Context.Data.get_attr(int(v[0]), 'avatar', '1')
            except:
                avatar = '1'
            try:
                sex = Context.Data.get_attr_int(int(v[0]), 'sex', 0)
            except:
                sex = 0
            try:
                vip_level = BirdAccount.get_vip_level(int(v[0]), self.gid)
            except:
                vip_level = 0

            rank = {
                'rank': int(k),
                'id': int(v[0]),
                'nick': nick,
                'sex': int(sex),
                'avatar': avatar,
                'vip': int(vip_level),
                'point': int(v[1]),
            }
            info.append(rank)
        mo.set_param('rank_list', info)
        if uid:
            Context.GData.send_to_connect(uid, mo)
        else:
            self.table_broadcast(mo)
        if timer:
            self.set_timer('match_rank', 10)

    def on_sit_down(self, uid, sid):
        BirdTable.on_sit_down(self, uid, sid)
        if self.play_mode == Enum.play_mode_match:
            ts = Time.current_ts()
            match_start_ts = Tool.to_int(Context.MatchDB.get_match_data(str(self.match_level),
                                                                        str(self.match_id), 'match_start_ts'), 0)
            if match_start_ts == 0 or self.match_start_ts == 0:
                if match_start_ts == 0:
                    self.match_start_ts = ts
                    Context.MatchDB.set_match_data(str(self.match_level), str(self.match_id), 'match_start_ts', ts)
                else:
                    self.match_start_ts = match_start_ts
                self.set_timer('match_rank', 10)
                self.set_timer('match_end', self.left_time + 15)
            else:
                self.match_start_ts = match_start_ts
            self.match_end_ts = self.match_start_ts + self.left_time + 15
            key = 'table_status_%d'%self.table_index
            table_status = Tool.to_int(Context.MatchDB.get_match_data(str(self.match_level), str(self.match_id), key), 0)
            if table_status != Enum.match_table_start:
                Context.MatchDB.set_match_data(str(self.match_level), str(self.match_id), key, Enum.match_table_start)

            left_time = self.left_time - (ts - self.match_start_ts) + 15
            mo = MsgPack(Message.MSG_SYS_MATCH_LEFT_TIME | Message.ID_ACK)
            mo.set_param('lt', left_time)
            mo.set_param('left_time', self.left_time)
            Context.GData.send_to_connect(uid, mo)
            self.send_rank_to_player(uid = uid)


    def __handle_match_end(self):
        status = Context.MatchDB.get_match_data(str(self.match_level), str(self.match_id), 'status')
        if not status:
            return
        player_list = self.get_players_point()
        self.send_reward_to_player(player_list)
        self.send_reward_to_all(player_list)

        # 添加事件-------------
        ms = Time.current_ms()
        tmp = Time.current_time('%Y-%m-%d')
        player_dict = self.get_players_point_dict()
        player_count = len(player_dict)
        player_dict['times'] = Time.current_ts()
        player_dict['rw'] = self.match_rank_reward.get('reward')

        Context.RedisStat.hash_set('match_table_data:%d:%s' % (self.match_level, tmp), ms,
                                   Context.json_dumps(player_dict))
        Context.Stat.incr_daily_data(2, 'match_quick_player', player_count)
        Context.Stat.incr_daily_data(2, 'match_quick_%d'%self.match_level)
        # --------------------

        Context.RedisMatch.delete('match:%d:%d'%(self.match_level, self.match_id))
        mo = MsgPack(Message.MSG_SYS_MATCH_END | Message.ID_ACK)
        for i in player_list:
            uid = i[0]
            Context.RedisMatch.delete('match:player:%d' % (uid))
            Context.GData.send_to_connect(uid, mo)

        return