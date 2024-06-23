#!/usr/bin/env python
# -*- coding=utf-8 -*-

import random
import datetime
import copy
from const import Enum
from pet import BirdPet
from const import Message
from props import BirdProps
from builder import MapBuilder
from account import BirdAccount
from registry import BirdRegistry
from framework.context import Context
from framework.util.tool import Time
from framework.util.tool import Tool
from lemon.entity.table import Table
from framework.entity.msgpack import MsgPack
from lemon.entity.gametimer import GameTimer
from entity import BirdEntity
from comm import BirdComm
from newtask import NewTask
from red_packet import Red_Packet
from framework.entity.userattr import SuperWeaponEvent

class BirdTable(Table):
    MAX_PLAYER_CNT = 4

    def __init__(self, gid, tid, playMode):
        super(BirdTable, self).__init__(gid, tid, playMode)
        self.players = [None] * self.MAX_PLAYER_CNT
        self.bird_config = {}
        self.vip_config = {}
        self.flush_config = {}
        self.fall_config = {}
        self.super_weapon_config = {}   # 超级武器配置
        self.weapon_config = {}
        self.switch_timer = GameTimer()
        self.delta_timer = GameTimer()

        self.loop_flush_timer = GameTimer()
        self.lasted_freeze = {}
        self.total_freeze = 0
        self.map = None
        self.special_birds = {}         # 暂存的等待report的鸟, type:uid
        self.weapon_eff_birds = {}      # 存入武器特性report的鸟
        self.builder_info = None
        self.loop_shot_times = 0

        self.barrel_unlock_use = 3      # 解锁要求

        self.dict_pinfo = {}               # 玩家信息

        self.drill_bomb_uid = 0
        self.coupon_target_num = 0

        self._pool_level = 0
        self._table_pool = 0
        self.cd_loop = 0


    def reset_param(self, empty=True):
        self.switch_timer.cancel()
        self.delta_timer.cancel()
        self.lasted_freeze = {}
        self.total_freeze = 0
        self.map = None
        self.special_birds = {}

        if empty:
            self.builder_info = None
            self.loop_shot_times = 0
            self.coupon_target_num = 0
            self.loop_flush_timer.cancel()
            self.cd_loop = 0

            self.dict_pinfo = {}

    def fetch_table_info(self):
        key = 'relax_table:%d:%d' % (self.gid, self.tid)
        attrs = ['room_type', 'seat0', 'seat1', 'seat2', 'seat3']
        kvs = Context.RedisCache.hash_mget_as_dict(key, *attrs)
        if len(kvs) != len(attrs):
            self._error('miss field', kvs)
            return False
        self.table_info = dict([(k, int(v)) for k, v in kvs.iteritems()])
        for i in range(self.MAX_PLAYER_CNT):
            k = 'seat' + str(i)
            v = self.table_info[k]
            if v > 0:
                self.table_info[v] = i

        room_type = int(self.table_info['room_type'])
        config = Context.Configure.get_room_config(self.gid, room_type)
        if not config:
            self._error('miss room config')
            return False

        room_config = Context.copy_json_obj(config)

        config = Context.Configure.get_game_item_json(self.gid, 'bird.config')
        if not config:
            self._error('miss bird config')
            return False

        bird_config = {}
        for bird in config['all']:
            bird_config[bird['type']] = bird

        config = Context.Configure.get_game_item_json(self.gid, 'flush.%d.config' % room_type)
        flush_config = {}
        for one in config:
            flush_config[one['type']] = one

        config = Context.Configure.get_game_item_json(self.gid, 'fall.%d.config' % room_type) # fall.201.config
        fall_config = {}
        for one in config:
            fall_config[one['id']] = one

        config = Context.Configure.get_game_item_json(self.gid, 'super.weapon.%d.config' % room_type)
        if not config:
            self._error('miss super weapon config')
            return False

        coupon_config = Context.Configure.get_game_item_json(self.gid, 'coupon.%d.config'%room_type)

        vip_config = Context.Configure.get_game_item_json(self.gid, 'vip.config')
        self.hit_bird_addition_config = Context.Configure.get_game_item_json(self.gid, 'hit_bird.addition.config')
        self.barrel_unlock_config = Context.Configure.get_game_item_json(self.gid, 'barrel.unlock.config')
        self.online_reward_config = Context.Configure.get_game_item_json(self.gid, 'online_reward.config')
        self.boom_conf = Context.Configure.get_game_item_json(self.gid, 'boom.%d.config' % room_type)
        self.exp_level_reward_conf = Context.Configure.get_game_item_json(self.gid, 'exp.level.reward')
        self.barrel_unlock_use = Tool.to_int(Context.Configure.get_game_item_json(self.gid, 'barrel.unlock.use'), 3)

        self.barrel_max_level = Context.Configure.get_game_item_json(self.gid, 'barrel.max.level')
        self.drill_kill_rate =  Context.Configure.get_game_item_json(self.gid, 'drill.kill.rate')
        self.type_bird_config = Context.Configure.get_game_item_json(self.gid, 'type_bird.%d.config'%(room_type))
        self.not_flush_config = Context.Configure.get_game_item_json(self.gid, 'not_flush.%d.config'%(room_type))

        weapon_config = Context.Configure.get_game_item_json(self.gid, 'weapon.config')
        for i in weapon_config:
            self.weapon_config[int(i['id'])] = i

        self.vip_config = vip_config
        self.bird_config = bird_config
        self.flush_config = flush_config
        self.fall_config = fall_config
        self.room_config = room_config
        self.super_weapon_config = config
        self.coupon_config = coupon_config

        self._pool_level = self.room_config['barrel_max1'] * 3000

        self.level_min1 = room_config['level_min1']
        self.barrel_min1 = room_config['barrel_min1']
        # vip房有玩家设置的炮倍限制
        if self.play_mode == Enum.play_mode_vip:
            keys = ('table:2:%d')%self.table_id
            multi = Context.RedisCache.hash_get_int(keys, 'multi', 0)
            barrel_level = BirdAccount.trans_barrel_multi(self.gid, multi)
            if not barrel_level:
                barrel_level = 1
                multi = 1
            self.barrel_min1 = multi
            self.level_min1 = barrel_level
        return True

    @property
    def table_pool(self):
        if self._table_pool is None:
            key = 'relax_table:%d:%d' % (self.gid, self.tid)
            self._table_pool = Context.RedisCache.hash_get_int(key, 'table_pool', 0)
        return self._table_pool

    def incr_table_pool(self, delta):
        key = 'relax_table:%d:%d' % (self.gid, self.tid)
        self._table_pool = Context.RedisCache.hash_incrby(key, 'table_pool', delta)
        return self._table_pool

    def incr_table_profit(self, delta):
        key = 'relax_table:%d:%d' % (self.gid, self.tid)
        Context.RedisCache.hash_incrby(key, 'table_profit', delta)


    def leave_limit(self, uid):
        tid = Context.RedisCache.hash_get('location:%d:%d' % (self.gid, uid), 'table_id')
        times = Time.current_ts()
        leave_limit = Context.Data.get_game_attr_json(uid, self.gid, 'leave_limit')
        if not leave_limit or not isinstance(leave_limit, dict):
            leave_limit = {str(tid): times}
        else:
            leave_limit[str(tid)] = times
        Context.Data.set_game_attr(uid, self.gid, 'leave_limit', Context.json_dumps(leave_limit))
        return

    def player_leave(self, uid):
        if uid in self.all_user:
            player = self.all_user[uid]
            del self.all_user[uid]
            if player.sid is not None:
                self.players[player.sid] = None
            self.leave_limit(uid)
            self.remove_player(uid)
            self._check_bankrupt(player, True)
            now_ts = Time.current_ts()

            # 在线奖励结束计时
            config = self.online_reward_config
            if str(player.create_days) in config['cd']:
                today_start_ts = Time.today_start_ts(now_ts)
                start_ts = player.online_reward_ts
                if start_ts < today_start_ts:
                    add_t = now_ts - today_start_ts
                else:
                    add_t = now_ts - start_ts
                Context.Daily.incr_daily_data(uid, self.gid, 'online.reward.long', add_t)

            if uid in self.dict_pinfo:
                del self.dict_pinfo[uid]
                Context.Log.debug('clear p data')

            player.leave_table()

        if not self.all_user:
            if self.play_mode == Enum.play_mode_village:
                self._village_room_close()
            self._info('table empty, recycle it')
            self.reset_param(True)
            self.set_recycle_flag()

    #初始化地图
    def init_map_info(self, old_map=None):
        if not self.map:
            if old_map:
                for player in self.players:
                    if player:
                        player.switch_scene()
            self.map = MapBuilder(self.room_type)
            self.map.listener = self
            next_img = old_map.next_img if old_map else None
            self.update_builder_info()
            hunter = self.get_by_state(Enum.user_state_playing)
            duration, _, _ = self.map.new_map(self.builder_info, hunter, next_img)
            self.set_timer('switch', self.map.total_ts + 0.5)
            self.set_timer('delta', duration - 6)

    def delta_update(self):
        uptime = self.real_uptime()
        self.__map_as_delta(uptime)
        return 0

    def update_builder_info(self):
        self.cd_loop += 1
        self._info('-----------', self.cd_loop)
        if self.builder_info is None:
            self.builder_info = self.map.get_default_builder_info(self.room_type)
        elif self.cd_loop < self.builder_info['cd']:
            return
        else:
            self.cd_loop = 0
            G = self.builder_info['G']
            Xg = self.builder_info['Xg']
            Zmin = self.builder_info['Zmin']
            Zmax = self.builder_info['Zmax']
            Bg1 = self.builder_info['Bg']
            Bg2 = Zmin + (G / (G + Xg)) * (Zmax - Zmin)
            self.builder_info['Bg'] = Bg2
            self.builder_info['Xg'] = Xg

        info_map = self.builder_info['map']
        total = float(sum([v['ratio'] for _, v in info_map.iteritems()]))
        odds_list = []
        for bird in self.builder_info['birds']:
            odds_list.append(info_map[bird]['ratio'] / total)
        self.builder_info['odds'] = odds_list

    def map_as_tide(self, uptime, hunter, which):
        info = self.map.get_tide_map(uptime, hunter, which)
        duration = None
        if info:
            duration, ev_list, tide = info
            if self.map.has_more_map():
                self.set_timer('delta', duration)
            mo = MsgPack(Message.BIRD_MSG_DELTA_SCENE | Message.ID_NTF)
            mo.set_param('tide', tide)
            mo.set_param('events', ev_list)
            mo.set_param('uptime', uptime)
            self.table_broadcast(mo)
        return duration, which, None

    def __map_as_delta(self, uptime):
        self.update_builder_info()
        hunter = self.get_by_state(Enum.user_state_playing)
        count = 0
        for p in self.players:
            if p and p.state == Enum.user_state_playing:
                count += 1

        info = self.map.delta_map(self.builder_info, hunter, count=count)
        if not info:
            self.set_timer('delta', 30)
            return False

        start, duration, ev_list, birds = info
        if self.map.has_more_map():
            self.set_timer('delta', duration)

        mo = MsgPack(Message.BIRD_MSG_DELTA_SCENE | Message.ID_NTF)
        if birds:
            mo.set_param('birds', birds)
        if ev_list:
            mo.set_param('events', ev_list)
        mo.set_param('uptime', uptime)
        self.table_broadcast(mo)
        return True

    def set_timer(self, action, tm, **kwargs):
        param = kwargs
        param['action'] = action
        param['gameId'] = self.gid
        param['tableId'] = self.tid

        self._info(action, tm, param)
        if action == 'delta':
            self.delta_timer.cancel()
            self.delta_timer.setTimeout(tm, param)
        elif action == 'switch':
            self.switch_timer.cancel()
            self.switch_timer.setTimeout(tm, param)
        elif action == 'call_bird':
            uid = kwargs['userId']
            player = self.all_user.get(uid)
            if player:
                if player.call_bird_timer:
                    player.call_bird_timer.cancel()
                else:
                    player.call_bird_timer = GameTimer()
                player.call_bird_timer.setTimeout(tm, param)
        elif action == 'offline':
            uid = kwargs['userId']
            player = self.all_user.get(uid)
            if player:
                if player.offline_timer:
                    player.offline_timer.cancel()
                else:
                    player.offline_timer = GameTimer()
                player.offline_timer.setTimeout(tm, param)
        elif action == 'loop_timer':
            self.loop_flush_timer.cancel()
            self.loop_flush_timer.setTimeout(tm, param)

        return param

    def real_uptime(self):
        return Time.current_ms() - self.map.start_ms

    def relative_time(self):
        uptime = self.real_uptime()
        self.__check_freeze(uptime)
        total = self.total_freeze
        left_ms = 0
        if self.lasted_freeze:
            left_ms = self.lasted_freeze['end'] - uptime
            total += uptime - self.lasted_freeze['start']

        return uptime - total, uptime, left_ms

    def onTimer(self, cmd, gid, msg):
        # TODO: sometime maybe can not cancel
        self._info('-------------', msg)
        action = msg.get_param('action')
        if action == 'delta':
            self.delta_update()
        elif action == 'switch':
            self.delta_timer.cancel()
            old_map = self.map
            self.reset_param(False)
            self.init_map_info(old_map)
            self.notify_next_scene()
        elif action == 'offline':
            self.__handle_user_offline(msg)
        elif action == 'loop_flush':
            self.__handle_loop_flush(msg)

    def __handle_user_offline(self, msg):
        uid = msg.get_param('userId')
        self._info(uid, 'offline timer begin')
        player = self.all_user.get(uid)
        # TODO 为什么player有时是None
        if player and player.offline_timer:
            player.offline_timer.cancel()
            player.offline_timer = None
            if player.state == Enum.user_state_offline:
                self.player_leave(uid)
                left_player = self.get_by_identity_type(Enum.identity_type_player)
                if not left_player:
                    self.update_table_status(Enum.table_status_free)

                Context.Online.incr_online(self.gid, self.room_type, False)
        self._info(uid, 'offline timer end')

    def on_join(self, uid):

        self._info(uid, 'req to join')
        if uid in self.all_user:
            player = self.all_user[uid]
            if player.state == Enum.user_state_offline:
                player.state = Enum.user_state_free
            self._info('the user is already here, maybe reconnect')
            return 0

        player = BirdRegistry.get_player(uid)
        if not player:
            self._warn('not found player', uid)
            return Enum.join_table_failed_unknown

        if not self.fetch_table_info():
            return Enum.join_table_failed_unknown

        if not self.is_join_legal(uid):
            self._warn('player is not distributed here')
            return Enum.join_table_failed_unknown

        user_info = BirdAccount.get_user_info(uid, self.gid)
        _, game_info = BirdAccount.get_game_info(uid, self.gid)
        chip_min = self.room_config.get('chip_min', -1)
        if chip_min != -1 and chip_min > game_info['chip']:
            self._warn('%d chip %d < %d' % (uid, game_info['chip'], chip_min))
            return Enum.join_table_failed_limit_min

        chip_max = self.room_config.get('chip_max', -1)
        if chip_max != -1 and chip_max < game_info['chip']:
            self._warn('%d chip %d > %d' % (uid, game_info['chip'], chip_max))
            return Enum.join_table_failed_limit_max

        props_list = BirdProps.get_props_list(uid, self.gid)

        player.gid = self.gid
        player.user_info = user_info
        player.game_info = game_info
        player.props_info = props_list
        player.identity = Enum.identity_type_player
        player.state = Enum.user_state_free
        player.auto_shot_status = 0

        fileds = ['pay_total', 'ganga']
        values = Context.Daily.get_daily_data(uid, self.gid, *fileds)
        kvs = Tool.make_dict(fileds, values)
        if kvs['pay_total']:
            player.today_pay_total = int(kvs['pay_total'])

        blocked = Context.Data.get_game_attr(uid, self.gid, 'block')
        if blocked:
            player.blocked = float(blocked)
        player.live_telecast_user = Context.RedisMix.set_ismember('game.%d.live.telecast.user' % self.gid, uid)
        player.session_ver = Context.Data.get_game_attr(uid, self.gid, 'session_ver')

        if self.room_config['level_max1'] > player.max_barrel_level:
            player.barrel_level = player.max_barrel_level
        else:
            player.barrel_level = self.room_config['level_max1']
        self.all_user[uid] = player

        # 玩家入场
        Context.Online.set_location_status(uid, self.gid, Enum.location_status_join)  # 标记玩家来了
        Context.Online.incr_online(self.gid, self.room_type, True)

        self._info(uid, 'join success')

        return 0

    def on_sit_down(self, uid, sid):
        self._info(uid, 'req to sit', sid)
        if sid < 0 or sid >= self.MAX_PLAYER_CNT:
            self._error(uid, 'error seat id', sid)
            return Enum.sit_down_failed_error_seat_id

        if uid not in self.all_user:
            self._warn(uid, 'not join table') # 用户不在桌子中
            return Enum.sit_down_failed_error_not_join

        player = self.all_user[uid]
        if player.identity != Enum.identity_type_player: #用户身份错误
            self._warn(uid, 'error identity', player.identity)
            return Enum.sit_down_failed_error_identity

        if player.sid == sid:
            player.state = Enum.user_state_playing
            self._info(uid, 'already sit here, maybe reconnect', sid)
            return 0

        if self.players[sid]: #座位已经有人
            key = 'relax_table:%d:%d' % (self.gid, self.tid)
            attr = 'seat%d' % sid
            sid_uid = Context.RedisCache.hash_get_int(key, attr, 0)
            if sid_uid <= 0 or sid_uid != uid:
                self._warn(self.players[sid].uid, 'is already here', sid)
                return Enum.sit_down_failed_other_here

        if uid not in self.table_info or self.table_info[uid] != sid:
            self._warn(uid, 'is not assigned to here', sid)
            return Enum.sit_down_failed_other_here

        player.state = Enum.user_state_playing
        player.sid = sid
        self.players[sid] = player

        if self.play_mode == Enum.play_mode_village:
            count = 0
            for p in self.players:
                if p and p.state == Enum.user_state_playing:
                    count += 1
            if count == 4:
                self._village_room_start()

        now_ts = Time.current_ts()
        player.online_reward_ts = now_ts

        self._info(uid, 'sit %d success' % sid)
        return 0

    def on_ready(self, uid):
        return 0

    def on_cancel_ready(self, uid):
        pass

    def on_stand_up(self, uid):
        pass

    def on_leave(self, uid):
        self._info(uid, 'leave')
        if uid not in self.all_user:
            self._warn(uid, 'not here')
            return Enum.leave_table_failed_not_join

        player = self.all_user[uid]
        if player.identity != Enum.identity_type_player:
            self._warn(uid, 'error identity', player.identity)
            return Enum.leave_table_failed_error_identity

        self.player_leave(uid)
        left_player = self.get_by_identity_type(Enum.identity_type_player)
        if not left_player:
            self.update_table_status(Enum.table_status_free)

        Context.Online.incr_online(self.gid, self.room_type, False)
        self._info(uid, 'leave success')
        return 0

    def on_force_quit(self, uid):
        pass

    def on_viewer_join(self, uid, sid):
        return 0

    def on_viewer_leave(self, uid):
        return 0

    def on_offline(self, uid):
        self._info(uid, 'offline')
        if uid not in self.all_user:
            self._warn(uid, 'not here')
            return Enum.leave_table_failed_not_join

        player = self.all_user[uid]
        player.state = Enum.user_state_offline
        self.set_timer('offline', 10, userId=uid)
        return 0

    def on_reconnect(self, uid):
        player = self.all_user.get(uid)
        if player:
            player.state = Enum.user_state_playing
        return 0

    def on_broadcast(self, uid, msg):
        pass

    def on_flush(self, uid, msg):
        pass

    def on_trustee(self, uid):
        pass

    def on_cancel_trustee(self, uid):
        pass

    def on_timeout(self, uid):
        pass

    def on_game_start(self):
        pass

    def on_client_message(self, uid, cmd, mi):
        player = self.all_user.get(uid)
        if not player or player.sid is None:
            self._error(uid, 'illegal seat id')
            return -1

        mo = None
        if cmd == Message.BIRD_MSG_BOARD_INFO | Message.ID_REQ:
            mo = self.on_board_info(uid, player, mi)
        elif cmd == Message.BIRD_MSG_BANKRUPT | Message.ID_REQ:
            mo = self.on_check_bankrupt(uid, player, mi)
        elif cmd == Message.BIRD_MSG_SHOT_BULLET | Message.ID_REQ:
            mo = self.on_shot_bullet(uid, player, mi)
        elif cmd == Message.BIRD_MSG_MOVE_BARREL | Message.ID_REQ:
            mo = self.on_move_barrel(uid, player, mi)
        elif cmd == Message.BIRD_MSG_HIT_BIRD | Message.ID_REQ:
            mo = self.on_hit_bird(uid, player, mi)
        elif cmd == Message.BIRD_MSG_UNLOCK_BARREL | Message.ID_REQ:
            mo = self.on_unlock_barrel(uid, player, mi)
        elif cmd == Message.BIRD_MSG_SWITCH_BARREL | Message.ID_REQ:
            mo = self.on_switch_barrel(uid, player, mi)
        elif cmd == Message.BIRD_MSG_SKILL_LOCK | Message.ID_REQ:
            mo = self.on_skill_lock(uid, player, mi)
        elif cmd == Message.BIRD_MSG_SKILL_FREEZE | Message.ID_REQ:
            mo = self.on_skill_freeze(uid, player, mi)
        elif cmd == Message.BIRD_MSG_SKILL_VIOLENT | Message.ID_REQ:
            mo = self.on_skill_violent(uid, player, mi)
        elif cmd == Message.BIRD_MSG_SKILL_SUPER_WEAPON | Message.ID_REQ:
            mo = self.on_skill_super_weapon(uid, player, mi)
        elif cmd == Message.BIRD_MSG_SKILL_PORTAL | Message.ID_REQ:
            mo = self.on_skill_portal(uid, player, mi)
        elif cmd == Message.BIRD_MSG_LOCK_BIRD | Message.ID_REQ:
            mo = self.on_lock_bird(uid, player, mi)
        elif cmd == Message.BIRD_MSG_REPORT_BIRDS | Message.ID_REQ:
            mo = self.on_report_birds(uid, player, mi)
        elif cmd == Message.MSG_SYS_ONLINE_REWARD_INFO | Message.ID_REQ:
            mo = self.on_online_reward_info(uid, player, mi)
        elif cmd == Message.MSG_SYS_GET_ONLINE_REWARD | Message.ID_REQ:
            mo = self.on_get_online_reward(uid, player, mi)
        elif cmd == Message.BIRD_MSG_RED_ENVELOPE | Message.ID_REQ: #发红包的信息
            pass

            return
        elif cmd == Message.BIRD_MSG_RANDOM_RED_ENVELOPE | Message.ID_REQ:  # 打开普通红包
            mo = Red_Packet.open_general_envelope(uid, player, mi)
        elif cmd == Message.BIRD_MSG_RED_ENVELOPE_RECORD | Message.ID_REQ:  # 普通红包记录
            mo = Red_Packet.general_envelope_record(uid, player, mi)
        elif cmd == Message.BIRD_MSG_WEAPON_REPORT_BIRD | Message.ID_REQ:
            mo = self.on_weapon_report_birds(uid, player, mi)
        elif cmd == Message.BIRD_MSG_WEAPON_LIGHT | Message.ID_REQ:
            mo = self.on_light_hit_bird(uid, player, mi)

        elif cmd == Message.BIRD_MSG_TABLE_UP_BARREL | Message.ID_REQ:          #战斗中强化炮消息
            mo = self.on_table_up_barrel(uid, player, mi)

        elif cmd == Message.BIRD_MSG_SKILL_SUPER_WEAPON_READY | Message.ID_REQ:     #准备发射超级武器
            mo = self.on_skill_super_weapon_ready(uid, player, mi)
        elif cmd == Message.BIRD_MSG_SEND_EMOJI | Message.ID_REQ:     #发送表情
            mo = self.on_send_emoji(uid, mi)
        elif cmd == Message.BIRD_MSG_SEND_SHAKE_END | Message.ID_REQ:           #开心摇一摇的结果
            mo = self.on_set_shake_data(uid, player, mi)
        elif cmd == Message.BIRD_MSG_CLOSE_SHAKE | Message.ID_REQ:           #开心摇一摇的结果
            mo = self.on_close_shake(uid, player, mi)

        elif cmd == Message.BIRD_MSG_DRILL_SHOT | Message.ID_REQ:
            mo = self.on_shot_drill(uid, player, mi)
        elif cmd == Message.BIRD_MSG_DRILL_HIT_BIRD | Message.ID_REQ:
            mo = self.on_drill_hit_bird(uid, player, mi)
        elif cmd == Message.BIRD_MSG_DRILL_BOOM | Message.ID_REQ:
            mo = self.on_drill_boom(uid, player, mi)
        elif cmd == Message.BIRD_MSG_AUTO_SHOT_STATUS | Message.ID_REQ:
            mo = self.on_auto_shot_status(player, mi)

        if isinstance(mo, MsgPack):
            Context.GData.send_to_connect(uid, mo)

        return 0

    def on_auto_shot_status(self, player, mi):
        return

    def on_set_shake_data(self, uid, player, mi):
        shake_id = mi.get_param('sid')
        detail = Context.RedisActivity.hash_get_json('activity:shake:%d' % shake_id, 'detail')
        room = detail.get('room', [])
        if str(self.room_type) in room:
            shake_times = mi.get_param('t')
            if shake_times <= 0:
                return
            barrel_level = player.barrel_multiple
            dat = {'st': shake_times, 'bl': barrel_level}
            Context.RedisActivity.hash_set('activity:shake:%d' % shake_id, uid, Context.json_dumps(dat))

        return

    def on_close_shake(self, uid, player, mi):
        mo = MsgPack(Message.BIRD_MSG_CLOSE_SHAKE | Message.ID_NTF)
        mo.set_param('uid', uid)
        self.table_broadcast(mo)

    def on_send_emoji(self, uid, mi):
        emoji_id = mi.get_param('id')
        mo = MsgPack(Message.BIRD_MSG_SEND_EMOJI | Message.ID_NTF)
        mo.set_param('id', emoji_id)
        mo.set_param('uid', uid)
        self.table_broadcast(mo)

    def on_table_up_barrel(self, uid, player, mi):
        ret = BirdEntity.on_up_barrel(uid, self.gid, mi)
        if isinstance(ret, int):
            if ret > 0:
                mo = MsgPack(Message.BIRD_MSG_SWITCH_BARREL | Message.ID_NTF)
                player.max_barrel_level = ret
                player.barrel_level = ret
                mo.set_param('lv', ret)
                mo.set_param('mt', player.barrel_multiple)
                mo.set_param('u', uid)
                self.table_broadcast(mo)

    def on_check_bankrupt(self, uid, player, mi):
        Context.Log.report('on_check_bankrupt:', uid)
        self._check_bankrupt(player)

        return 0

    def on_board_info(self, uid, player, mi):
        self.init_map_info()  #初始化地图
        mo = MsgPack(Message.BIRD_MSG_BOARD_INFO | Message.ID_NTF) #桌面信息, 游戏初始化数据
        # 桌面信息
        mo.set_param('start', self.map.start_ms)
        uptime = self.real_uptime()
        mo.set_param('uptime', uptime)
        self.__check_freeze(uptime)
        freeze = {'total': self.total_freeze}
        if self.lasted_freeze:
            freeze['start'] = self.lasted_freeze['start']
        mo.set_param('freeze', freeze)
        board_info, rank_info = [], []
        for player in self.players:
            if player and player.state != Enum.user_state_offline:
                info = self.get_broad_info(player)
                board_info.append(info)

        mo.set_param('board', board_info)
        # 向其他人广播
        self.table_broadcast(mo, exclude=uid)

        # 地图信息
        rel_uptime, rea_uptime, left = self.relative_time()
        self.map.adjust_map_info(rel_uptime)
        mo.set_cmd(Message.BIRD_MSG_BOARD_INFO | Message.ID_ACK)
        mo.set_param('map', self.map.get_map_info())
        Context.GData.send_to_connect(uid, mo)

        for player in self.players:
            if player and player.lock_state == 1:
                mo = MsgPack(Message.BIRD_MSG_SKILL_LOCK | Message.ID_ACK)
                mo.set_param('u', player.uid)
                mo.set_param('state', 1)
                Context.GData.send_to_connect(uid, mo)

                if player.lock_bird:
                    mo = MsgPack(Message.BIRD_MSG_LOCK_BIRD | Message.ID_NTF)
                    bird = player.lock_bird
                    mo.set_param('u', player.uid)
                    mo.set_param('i', bird)
                    Context.GData.send_to_connect(uid, mo)
        return 0

    def get_broad_info(self, player):
        vip = BirdAccount.get_vip_level(player.uid, self.gid)
        info = {
            'u': player.uid,
            'a': player.barrel_angle,
            'b': player.bullet_number,
            'mt': player.barrel_multiple,
            'lv': player.barrel_level,
            'sid': player.sid,
            'wid': player.weapon_id,
            'vip': vip,
        }
        pet_id, _, _ = BirdPet.use_info(player.uid, self.gid)
        if pet_id:
            info['p'] = pet_id
        return info

    def adjust_barrel(self, player, cost):
        bm = self.barrel_min1
        lv = self.level_min1
        if cost < bm:
            chip = Context.Data.get_game_attr_int(player.uid, self.gid, 'chip', 0)
            if chip >= bm:
                mo = MsgPack(Message.BIRD_MSG_SWITCH_BARREL | Message.ID_NTF)
                player.barrel_level = lv
                mo.set_param('lv', lv)
                mo.set_param('mt', player.barrel_multiple)
                mo.set_param('u', player.uid)
                self.table_broadcast(mo)
                return True
        else:
            return False

    def on_shot_drill(self, uid, player, mi):
        if player.uid != self.drill_bomb_uid:
            self._warn(' not real player')
            return 1

        angle = mi.get_param('a')

        if not self.map:
            self._warn('maybe not req map')
            return 1

        if len(player.drill_info) < 0:
            self._warn('can not shot')
            return 2

        mo = MsgPack(Message.BIRD_MSG_DRILL_SHOT | Message.ID_ACK)
        mo.set_param('u', uid)
        mo.set_param('a', angle)
        player.drill_info['angle'] = angle
        self.table_broadcast(mo)
        return 0

    def on_shot_bullet(self, uid, player, mi):
        bullet = mi.get_param('b')
        angle = mi.get_param('a')

        if not self.map:
            self._warn('maybe not req map')
            return 1

        if not player.can_shot() or len(player.drill_info) > 0:
            self._warn('can not shot', player.drill_info)
            return 2

        # 限制玩家用加速器，125毫秒一发子弹
        current_shot_bullet = Time.current_ms()
        ms = int(1000/(self.weapon_config[int(player.weapon_id)]['speed'] + 1))
        if player.last_shot_bullet and player.last_shot_bullet + ms > current_shot_bullet :
            return 4
        player.last_shot_bullet = current_shot_bullet

        uptime = self.real_uptime()
        in_violent = False
        if player.in_violent(uptime):
            in_violent = True
            cost = player.barrel_multiple * 2
            if self.adjust_barrel(player, cost):
                cost = player.barrel_multiple * 2
        else:
            cost = player.barrel_multiple
            if self.adjust_barrel(player, cost):
                cost = player.barrel_multiple

        # 子弹改为全金 dz
        shot_type = 1

        _all = Context.UserAttr.get_chip(player.uid, player.gid, 0)
        if shot_type:
            if _all <= 0:
                self._warn(uid, 'have no enough chip')
                return 3
            elif  _all < cost:
                cost = _all
            real, final, _all = player.incr_chip(-cost, 'game.shot.bullet', roomtype=self.room_type)
            from newactivity import RankActivity, SaveMoneyActivity, PointShopActivity
            RankActivity.incr_user_rank_value(player.uid, 1, cost)
            SaveMoneyActivity.incr_user_value(player.uid, self.gid, cost)
            PointShopActivity.incr_user_shot(player.uid, cost)

        _pool_shot = 'pool.shot.%d' % self.room_type
        _shot_times = 'shot.times.%d' % self.room_type
        Context.Stat.mincr_daily_data(self.gid, _shot_times, 1, _pool_shot, cost)

        mo = MsgPack(Message.BIRD_MSG_SHOT_BULLET | Message.ID_NTF)
        mo.set_param('u', uid)
        mo.set_param('b', bullet)
        player.bullet_number = bullet

        r_shot_type = 1
        player.shot_times += 1
        weapon_id = player.weapon_id
        # dz 增加狂暴子弹
        player.bullet_map[bullet] = {'in_violent': in_violent, 'multi': player.barrel_multiple, 'cost': cost, 'wid':weapon_id,
                                     'shot_type': r_shot_type, 'r_shot_type': r_shot_type}        # dz 增加狂暴子弹

        # 去掉抽成等剩余的额度
        #pool_cost, normal_cost = self.get_pool_cost(player, cost, player.barrel_multiple)
        self.incr_table_pool(cost)
        #self.incr_table_profit(normal_cost)
        if angle is not None:
            mo.set_param('a', angle)
            player.barrel_angle = angle
        mo.set_param('c', _all)
        if self.play_mode == Enum.play_mode_match:
            mo.set_param('l', player.match_bullet)
        # mo.set_param('ts', uptime)
        self._reduce_bullet(uid, player, cost, _all, in_violent)
        self.flush_coupon_bird(player.barrel_multiple)
        self.table_broadcast(mo)
        return 0

    def flush_coupon_bird(self, barrel_multiple):
        if barrel_multiple < 2000:
            return
        self.loop_shot_times += 1
        if self.map.get_tide_state() or self.room_type not in [203, 209]:
            return

        need = (self.coupon_target_num+1)*3000*len(self.all_user)
        if need <= self.loop_shot_times:
            self.loop_shot_times = 0
            R = random.choice([1,2])
            rel_uptime, _, _ = self.relative_time()
            hunter = self.get_by_state(Enum.user_state_playing)
            start = int(rel_uptime) / 100
            if R == 1:
                _, birds, _ = self.map.make_coupon(start, hunter)
            else:
                _, birds, _ = self.map.make_target(start, hunter)
            if birds:
                mo = MsgPack(Message.BIRD_MSG_NEW_BIRD | Message.ID_NTF)
                mo.set_param('birds', [birds])
                self.table_broadcast(mo)
            return

    #  玩家鸟蛋不足自动降低炮倍
    def _reduce_bullet(self, uid, player, cost, _all, in_violent):
        lv = self.level_min1
        bm = self.barrel_min1
        if (0 < _all <= cost) or (bm > cost and _all > cost):
            conf = self.barrel_unlock_config

            if in_violent:
                _all = int(_all/2)
            for k,v in enumerate(conf):
                if v['multiple'] > _all:
                    if k <= 0:
                        break
                    lv = conf[k - 1]['level']
                    break
            if player.barrel_level != lv:
                mo = MsgPack(Message.BIRD_MSG_SWITCH_BARREL | Message.ID_NTF)
                player.barrel_level = lv
                mo.set_param('lv', lv)
                mo.set_param('mt', player.barrel_multiple)
                mo.set_param('u', uid)
                self.table_broadcast(mo)
        return

    def on_move_barrel(self, uid, player, mi):
        angle = mi.get_param('a')
        mo = MsgPack(Message.BIRD_MSG_MOVE_BARREL | Message.ID_NTF)
        mo.set_param('u', uid)
        mo.set_param('a', angle)
        player.barrel_angle = angle
        self.table_broadcast(mo)
        return 0


    def get_all_online_chip(self):
        refresh_time = Context.RedisMix.hash_get('game.2.share', 'refresh_time')
        ts = Time.current_ts()
        if refresh_time and ts <= int(refresh_time) + 1*60:
            total_chip = Context.RedisMix.hash_get('game.2.share', 'total_chip', default = 0)
            return int(total_chip)
        else:
            Context.RedisMix.hash_set('game.2.share', 'refresh_time', ts)
            total_chip = 0
            ret = Context.RedisCluster.hget_keys('game:2:*')
            for i in ret:
                uid = int(i.split('game:2:')[1])
                if uid <= 1000000:
                    continue
                p_chip = Context.Data.get_game_attr_int(uid, self.gid, 'chip', 0)
                total_chip += (p_chip)
            Context.RedisMix.hash_set('game.2.share', 'total_chip', total_chip)
            return total_chip


    def get_fall_coupon_xg(self):
        return 0.03

    def fall_coupon_logic(self, player, bird_id, cost):
        fall_num = 1
        total_cost = self.get_self_fall_coupon_total_cost(player.uid)
        drop_xg = self.get_fall_coupon_xg()
        total_cost += cost * drop_xg
        need_cost = fall_num * 1250
        if total_cost >= need_cost:   # 掉落鸟券
            self.set_self_fall_coupon_total_cost(player.uid, total_cost - need_cost)
            self.incr_table_pool(-need_cost)
            self.incr_table_profit(need_cost)
            pool_name = 'coupon_pool'
            mo = MsgPack(Message.MSG_SYS_DROP_COUPON | Message.ID_NTF)
            c_real, c_final = Context.UserAttr.incr_coupon(player.uid, self.gid, fall_num, pool_name + '.hit.bird')
            mo.set_param('uid', player.uid)
            mo.set_param('drop', 1)
            mo.set_param('bird', bird_id)
            mo.set_param('final', c_final)
            self.table_broadcast(mo)
            return fall_num
        else:       # 未掉落
            self.set_self_fall_coupon_total_cost(player.uid, total_cost)
            mo = MsgPack(Message.MSG_SYS_DROP_COUPON_SLIDER | Message.ID_ACK)
            mo.set_param('uid', player.uid)
            mo.set_param('need', need_cost)
            mo.set_param('cost', total_cost)
            Context.GData.send_to_connect(player.uid, mo)
            return 0

    def on_drill_hit_bird(self, uid, player, mi):
        if player.uid != self.drill_bomb_uid:
            return 1

        if len(player.drill_info) < 0:
            self._warn('bullet maybe hit already' )
            return 1

        multi = player.drill_info['multiple']
        total_point = player.drill_info.get('total_point', 0)
        bird = mi.get_param('i')
        bird_type = self.map.bird_type(bird)

        if bird_type is None:
            return 0
        else:
            bird_config = self.bird_config[bird_type]

        bird_t = mi.get_param('t')
        if bird_t == 452:
            return 0

        big_bird_type = bird_type % 1000
        if big_bird_type == 451:
            return 0

        catched_list = []
        bird_point = bird_config['point']
        bird_class = bird_config['class']
        success = True
        if bird_point + total_point > 300 or bird_class in ['boss', 'worldBoss', 'special']:
            success = False
        else:
            rate = self.drill_kill_rate.get(bird_class)
            rand = random.random()
            if rand > rate:
                success = False
        if success:
            player.drill_info['total_point'] = total_point + bird_point
            catched_list.append(bird)
        self.process_hit_bird(multi, bird, player, catched_list)
        mo = MsgPack(Message.BIRD_MSG_DRILL_HIT_BIRD | Message.ID_ACK)
        mo.set_param('i', bird)
        mo.set_param('u', uid)
        self.table_broadcast(mo)
        return 0

    # 击杀鸟
    def set_kill_bird_info(self, player, catched_list, cur_barrel):
        return

    def get_trans_barrel_level(self, player):
        return player.max_barrel_level

    def on_hit_bird(self, uid, player, mi):
        bullet = mi.get_param('b')
        if bullet not in player.bullet_map:
            self._warn('bullet %d maybe hit already' % bullet)
            return 1

        # 穿透处理
        double = 1
        info = player.bullet_map[bullet]

        bullet_multiple = player.bullet_map[bullet]['multi']
        in_violent = player.bullet_map[bullet]['in_violent']

        del player.bullet_map[bullet]

        bird = mi.get_param('i')
        bird_type = self.map.bird_type(bird)

        if bird_type is None:
            # 房间池处理
            self._info('bird %d maybe caught already' % bird)
            self._check_bankrupt(player)
            success, _ = self.check_catch_bird(player, bird_type, bird, bullet_multiple, in_violent)
            return 0

        big_bird_type = bird_type % 1000

        catched_list = []
        success, _ = self.check_catch_bird(player, bird_type, bird, bullet_multiple, in_violent)

        if success:
            if bird_type in (551, 552, 553):    # 击杀炸弹怪处理
                task_bird = bird_type
                if bird_type == 551:
                    task_bird = self.map.bird_map[bird]['sk']
                self.hit_bird_task(player.uid, task_bird, self.room_type)
                uptime = self.real_uptime()
                boom_conf = self.boom_conf
                area = 0
                if boom_conf.has_key(str(bird_type)): # 转为十六进制
                    if boom_conf[str(bird_type)].has_key('a'):
                        area = boom_conf[str(bird_type)]['a']
                self.special_birds[bird_type] = {'uid': uid, 'ts': uptime + self.map.start_ms,
                                                 'multiple': info['multi']}
                ack = MsgPack(Message.BIRD_MSG_HIT_BIRD | Message.ID_ACK)
                ack.set_param('i', bird)
                ack.set_param('ts', uptime)
                ack.set_param('a', area)
                ack.set_param('multi', bullet_multiple)
                return ack
            elif self.catch_is_6jg(big_bird_type):  # 一网打尽
                _birds = self.map.get_all_wipe_bird()
                catched_list.extend(_birds)
                self.map.clear_wipe_bird()
            elif big_bird_type == 555:
                uptime = self.real_uptime()
                player.drill_info = {'ts': uptime + self.map.start_ms, 'multiple': info['multi']}
                ou = MsgPack(Message.BIRD_MSG_DRILL_KILL | Message.ID_ACK)
                self.drill_bomb_uid = uid
                ou.set_param('uid', uid)
                ou.set_param('b', bird)
                self.table_broadcast(ou)
                self.map.remove_bird(bird)
            else:
                catched_list.append(bird)

        self.process_hit_bird(info['multi'], bird, player, catched_list)
        return 0

    # 激光扫射鸟
    def on_light_hit_bird(self, uid, player, mi):
        bullet = mi.get_param('b')
        if bullet not in player.bullet_map:
            self._warn('bullet %d maybe hit already' % bullet)
            return 1
        info = player.bullet_map[bullet]
        bullet_multiple = player.bullet_map[bullet]['multi']
        in_violent = player.bullet_map[bullet]['in_violent']
        del player.bullet_map[bullet]
        birds = mi.get_param('birds')
        if birds == None or len(birds) <= 0:
            self._warn('light not hit birds?')
            return 1
        b_cost = True

        for bird in birds:
            if int(bird) <= 0:
                return 0

            bird_type = self.map.bird_type(bird)
            if bird_type is None:
                self._info('bird %d maybe caught already' % bird)
                self._check_bankrupt(player)
                return 0

            bird_config = self.bird_config[bird_type]
            big_bird_type = bird_type % 1000

            # 统计个人击杀
            if b_cost:
                if bird_config['Lj'] != 0:
                    stat_cost = info['cost']
                else:
                    stat_cost = None
                if bird_config['Ln'] != 0 and bird_config['Lg'] != 0:
                    unit_W = (float(info['multi']) / bird_config['Ln']) * bird_config['Lg']
                else:
                    unit_W = None
                self.map.update_bird_stat(uid, bird, stat_cost, unit_W)

            catched_list = []
            success = False
            if info['shot_type']:
                if b_cost == False:
                    spacial = {'wid': info['wid'], 'len': len(birds)}
                else:
                    spacial = None
                    b_cost = False
                success, _ = self.check_catch_bird(player, bird_type, bird, bullet_multiple, in_violent)

            if success:
                if bird_type in (551, 552, 553):  # 炸弹怪
                    self.hit_bird_task(player.uid, bird_type, self.room_type)
                    uptime = self.real_uptime()
                    boom_conf = self.boom_conf
                    area = 0
                    if boom_conf.has_key(str(bird_type)):  # 转为十六进制
                        if boom_conf[str(bird_type)].has_key('a'):
                            area = boom_conf[str(bird_type)]['a']
                    self.special_birds[bird_type] = {'uid': uid, 'ts': uptime + self.map.start_ms,
                                                     'multiple': info['multi']}
                    ack = MsgPack(Message.BIRD_MSG_HIT_BIRD | Message.ID_ACK)
                    ack.set_param('i', bird)
                    ack.set_param('ts', uptime)
                    ack.set_param('a', area)
                    return ack
                elif self.catch_is_6jg(big_bird_type):  # 一网打尽
                    _birds = self.map.get_all_wipe_bird()
                    catched_list.extend(_birds)
                    self.map.clear_wipe_bird()
                else:
                    catched_list.append(bird)
                self.set_kill_bird_info(player, catched_list, info['multi'])
            self.process_hit_bird(info['multi'], bird, player, catched_list)
        return

    #获取闪电炮打到的鸟
    def get_table_birds(self):
        ts = (self.real_uptime() - self.total_freeze) / 1000  # 10000
        bird_list = []

        map_info = self.map.get_map_info()
        for i in map_info['birds']:
            if i.has_key('n') and i.has_key('s'):
                bs = i['n'] / 10
                if ts < bs or ts > bs + i['s']:
                    continue
                bird_list.append(i['i'])
        return bird_list

    def process_hit_bird(self, multi, bird, player, catched_list):
        # 处理打到鸟 不包括 炸弹 孙悟空 . 如果是一网打尽 就是多只鸟
        if catched_list:
            final_info, catch_bird_list, up_reward_list, critM = self.process_catch_birds(player, catched_list, multi)
            mo = MsgPack(Message.BIRD_MSG_CATCH_BIRD | Message.ID_NTF)
            mo.set_param('u', player.uid)
            mo.set_param('i', bird)
            if not up_reward_list:
                exp = Context.Data.get_game_attr_int(player.uid, self.gid, 'exp', 0)
                mo.set_param('exp', exp)
            if final_info:
                mo.update_param(final_info)
            if catch_bird_list:
                mo.set_param('r', catch_bird_list)
            if self.play_mode == Enum.play_mode_match:
                mo.set_param('s', player.match_score)
            if len(critM) >= 1:
                l = []
                for k, v in enumerate(critM):
                    info = {}
                    info['bird'] = v[0]
                    info['double'] = v[1]
                    l.append(info)
                mo.set_param('critM', l)
            #Context.Log.debug('=====_cpr3:', mo)
            self.broadcast_notify_with_filter(player, mo)
            if up_reward_list:
                self._notify_exp_upgrade(player, up_reward_list)

        self._check_bankrupt(player)

    def _check_bankrupt(self, player, leave=False):
        if player.check_bankrupt(leave):
            mo = BirdAccount.check_bankrupt(player.uid, self.gid)
            if leave:
                Context.GData.send_to_connect(player.uid, mo)
            else:
                self.table_broadcast(mo)

    def _notify_exp_upgrade(self, player, up_reward_list):
        mo = MsgPack(Message.BIRD_MSG_EXP_UPGRADE | Message.ID_NTF)
        level, diff = BirdAccount.get_exp_info(player.uid, self.gid, player.exp)
        mo.set_param('exp', player.exp)
        mo.set_param('lv', level)
        if diff:
            mo.set_param('df', diff)
        final_reward = BirdProps.merge_reward_result(True, *up_reward_list)
        final_reward = BirdProps.convert_reward(final_reward)
        mo.update_param(final_reward)
        Context.GData.send_to_connect(player.uid, mo)
        return 0

    def catch_is_6jg(self, bird_type):  # 惊弓之鸟
        if 161 <= bird_type <= 168:
            return True
        return False

    def catch_is_6jg_or_bomb(self, bird_type):
        if self.catch_is_6jg(bird_type) or 551 == bird_type:  # 惊弓之鸟 * 6 或同类炸弹怪
            return True
        else:
            return False

    def catch_get_point(self, bird_type, bird_id):
        if self.catch_is_same_bomb(bird_type):
            real_type = self.map.bird_map[bird_id]['sk']
            bird_config = self.bird_config[real_type]
            point = bird_config.get('point', 0)
            point *= 6
        else:
            bird_config = self.bird_config[bird_type]
            point = bird_config.get('point', 0)  # 当前鸟的分数倍率
        if self.catch_is_6jg(bird_type):
            point = 60
        return point

    def set_self_fall_coupon_total_cost(self, uid, value):
        Context.UserAttr.set_fall_coupon_total_cost(uid, self.gid, value, 'hit.bird')  # 存到数据库

    def get_self_fall_coupon_total_cost(self, uid):
        value = float(Context.UserAttr.get_fall_coupon_total_cost(uid, self.gid, 0))
        return value

    def catch_is_boom_need_delay(self, bird_type):
        if bird_type in [551, 552, 553, 555]:
            return True

        return False

    def catch_is_same_bomb(self, bird_type):
        if bird_type == 551:
            return True

        return False

    def get_catch_win_chip(self, bird_type, bird_id, barrel_multiple):
        win_chip = 0
        point = self.catch_get_point(bird_type, bird_id)
        if self.catch_is_coupon(bird_type):
            coupon_count = self.map.bird_map[bird_id]['number']
            win_chip = -coupon_count * 5000
        elif self.catch_is_target(bird_type):
            coupon_count = self.map.bird_map[bird_id]['number'] * 4
            win_chip = -coupon_count * 5000
        elif self.catch_is_diamond(bird_type):
            diamond_count = self.map.bird_map[bird_id]['number']
            win_chip = -diamond_count * 500

        elif point == 0:
            win_chip = -self.bird_config[bird_type].get('need_cost', 0)
        else:
            win_chip = -barrel_multiple * point
        return win_chip

    '''
    击杀成功处理
    bird_type   击杀的鸟的类型
    barrel_multiple 使用的炮倍倍率
    pool_id    当前池子id
    player  玩家数据类
    total_cost  全服总消耗
    self_total_cost   个人总消耗
    #cost 本次子弹消耗
    '''
    def catch_suc_pro(self, bird_type, bird_id, barrel_multiple):
        win_chip = self.get_catch_win_chip(bird_type, bird_id, barrel_multiple)

    # 鸟券怪
    def catch_is_coupon(self, bird_type):
        if bird_type == 501:
            return True
        return False

    # 靶券怪
    def catch_is_target(self, bird_type):
        if bird_type == 511:
            return True
        return False

    # 靶券怪
    def catch_is_diamond(self, bird_type):
        if bird_type == 521:
            return True
        return False

    # 子弹进池子处理
    def normal_shot_in_pool(self, cost, pool_id):
        in_pool_chip = cost

    def get_add_random(self, player, point):
        total_add = 0.0

        # ------------------------power table addition-------------------------------end
        if self.table_pool > self._pool_level * 1.15:
            if point >= 100:   # 如果
                Context.Log.debug("池子满概率加成")
                total_add += 5

        # ------------------------pool addition-------------------------------end

        # ------------------------vip  addition-------------------------------start
        vip_level = BirdAccount.get_vip_level(player.uid, self.gid)
        vip_add = self.hit_bird_addition_config.get('vip').get(str(vip_level))
        total_add += vip_add
        # ------------------------vip addition-------------------------------end

        Context.Log.debug('vip_add', vip_add, total_add)
        return total_add

    def get_bird_point(self, bird_id, bird):
        real_bird_type = bird % 1000
        bird_config = self.bird_config[real_bird_type]
        point = bird_config.get('point', 0)
        if real_bird_type >= 161 and real_bird_type <= 168:
            point *= 6
        if real_bird_type == 551:
            boom_type = self.map.bird_map[bird_id]['sk']
            bird_config = self.bird_config[boom_type]
            point = bird_config.get('point', 0)
            point *= 5
        return point

    # 检测捕鸟是否成功
    '''
    player 玩家数据
    bird_type_old 击中鸟的类型
    bird_id 鸟的实例id
    barrel_multiple 当前子弹的倍数
    in_violent 是否开启狂暴
    '''
    def check_catch_bird(self, player, bird_type, bird_id, barrel_multiple, in_violent=False):
        cost = barrel_multiple
        if in_violent:
            cost *= 2
        fall_coupon_num = self.fall_coupon_logic(player, bird_id, cost)
        if bird_type is None:
            return False, fall_coupon_num

        R = random.random()
        bird_type = int(bird_type)
        point = self.get_bird_point(bird_id, bird_type)
        if point == 0:
            wChip = self.get_catch_win_chip(bird_type, bird_id, barrel_multiple)
            point = float(-wChip) / barrel_multiple

        r = 1 / float(point)
        addition = self.get_add_random(player, point)
        rand = r * float(1 + addition - 0.03)
        if in_violent: rand *= 2
        Context.Log.debug('point:', point, 'r:', r, 'addition:', addition, 'rand:', rand, R)
        if R <= rand:
            Context.Log.debug('击杀鸟成功')
            wChip = self.get_catch_win_chip(bird_type, bird_id, barrel_multiple)
            if self.table_pool < -wChip:
                return False, fall_coupon_num

            return True, fall_coupon_num


        return False, fall_coupon_num

    def __issue_catch_reward(self, player, bird, bird_config, multiple):
        if 'class' in bird_config:
            bird_class = bird_config['class']
        else:
            bird_class = 'other'
        bird_type = bird_config['type']
        big_bird_type = bird_type % 1000
        if not self.map.bird_map[bird].has_key('cs'):
            self.new_flush(bird_type)
        reward_info = {}
        critM = None
        bonus_pool, bonus_count = None, None
        pipe_args = ['bird.' + str(big_bird_type), 1, 'class.' + str(bird_class), 1]

        Context.Daily.mincr_daily_data(player.uid, self.gid, *pipe_args)
        numbers = 0
        if big_bird_type in [511, 501, 521]:#记录鸟（靶）卷怪掉鸟（靶）卷的数量
            numbers = self.map.bird_map[bird]['number']
        point = 0
        if self.catch_is_same_bomb(big_bird_type):
            real_type = self.map.bird_map[bird]['sk']
            bird_config = self.bird_config[real_type]
            point = bird_config['point']
        elif self.catch_is_boom_need_delay(big_bird_type):
            point = 10   # 默认给炸弹自带10的倍率
        elif big_bird_type not in [601, 602, 603, 451, 452]: # 宝箱怪和世界boss是不掉鸟蛋的
            point = bird_config.get('point', 0)

        self.map.remove_bird(bird)  # 已经被捕获从map中删除

        if big_bird_type in [601, 602, 603]: # 宝箱怪掉落宝箱
            box_fall_conf = self.fall_config[big_bird_type]
            _rewards = box_fall_conf['p']
            _rewards = player.issue_rewards(_rewards, 'bird.fall', roomtype=self.room_type)
            # 打到宝箱需要从池子里面吧金币扣掉
            needCoin = box_fall_conf['needCoin']
            # 打到宝箱发公告
            if _rewards:
                props_id = _rewards['props'][0]['id']
                props_name = BirdProps.get_props_desc(props_id)
                bird_name = bird_config['name']
                bulletin = 2
                nick = Context.hide_name(player.nick)
                led = u'手起刀落！玩家<color=#00FF00FF>%s</color>在<color=#00FF00FF>%s</color>击杀<color=#00FF00FF>%s</color>获得<color=#FFFF00FF>%s</color>！' % (
                    nick, self.room_name, bird_name, props_name)
                mo = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
                mo.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
                Context.GData.broadcast_to_system(mo)
                reward_info = BirdProps.merge_reward_result(True, reward_info, _rewards)

        elif big_bird_type in [501, 511]:
            # 掉鸟券，根据概率判断是否掉
            pool = 'coupon_pool'
            if big_bird_type == 501:
                event_name = pool + '.coupon.bird.fall'
                Context.RedisMix.hash_incrby('game.2.share', 'coupon_pool', -numbers)
                rw = player.issue_rewards({'coupon': numbers}, event_name)
                reward_info = BirdProps.merge_reward_result(True, reward_info, rw)
                # 发放公告
                nick = Context.hide_name(player.nick)
                bulletin = 2
                bird_name = bird_config['name']
                led = u'强势围观，<color=#00FF00FF>%s</color>在<color=#00FF00FF>%s</color>击杀<color=#00FF00FF>%s</color>获得<color=#FFFF00FF>%d</color>鸟券！' % (
                    nick, self.room_name, bird_name, numbers)
                mo = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
                mo.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
                Context.GData.broadcast_to_system(mo)
            elif big_bird_type == 511:
                Context.RedisMix.hash_incrby('game.%d.target_pool' % self.gid, 'target_number', -numbers)
                Context.RedisMix.hash_incrby('game.2.share', 'coupon_pool', -numbers * 4)
                rw = player.issue_rewards({'target': numbers}, 'target.bird.fall')
                reward_info = BirdProps.merge_reward_result(True, reward_info, rw)

                # 发放公告
                nick = Context.hide_name(player.nick)
                bulletin = 2
                bird_name = bird_config['name']
                led = u'强势围观，<color=#00FF00FF>%s</color>在<color=#00FF00FF>%s</color>击杀<color=#00FF00FF>%s</color>获得<color=#FFFF00FF>%d</color>靶场券！' % (
                    nick, self.room_name, bird_name, numbers)
                mo = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
                mo.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
                Context.GData.broadcast_to_system(mo)

        elif big_bird_type == 521:
            # Context.RedisMix.hash_incrby('game.%d.target_pool' % self.gid, 'target_number', -numbers)
            # Context.RedisMix.hash_incrby('game.2.share', 'coupon_pool', -numbers * 4)
            rw = player.issue_rewards({'diamond': numbers}, 'diamond.bird.fall')
            reward_info = BirdProps.merge_reward_result(True, reward_info, rw)
            # 发放公告
            nick = Context.hide_name(player.nick)
            bulletin = 2
            bird_name = bird_config['name']
            led = u'强势围观，<color=#00FF00FF>%s</color>在<color=#00FF00FF>%s</color>击杀<color=#00FF00FF>%s</color>获得<color=#FFFF00FF>%d</color>钻石！' % (
                nick, self.room_name, bird_name, numbers)
            mo = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
            mo.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
            Context.GData.broadcast_to_system(mo)

        if point > 0:
            if isinstance(point, list):
                point = random.choice(point)

            chip = point * multiple
            fake_chip = chip

            if big_bird_type in [501,511,601,602,603]:    #鸟券怪是不掉鸟蛋的
                chip = 0

            reward_info['reward'] = {'chip': chip}

            if chip > 0:
                player.incr_chip(chip, 'catch.bird', roomtype=self.room_type)
                NewTask.get_chip_task(player.uid, chip, 'catch.bird', self.room_type)
            Context.Daily.incr_daily_data(player.uid, self.gid, 'win.chip', chip)
            reward_info['chip'] = player.chips
            if fake_chip != chip:
                reward_info['reward']['fake_chip'] = fake_chip
        if 'chip' in reward_info:
            chg_chip = reward_info['reward']['chip']
            if chg_chip > 0:
                Context.Data.hincr_rank(self.room_type, self.gid, '%d' % player.uid, chg_chip)

            if bird_class == 'boss':    # boss或者超级boss
                nick = Context.hide_name(player.nick)
                bulletin = 2
                bird_name = bird_config['name']
                led = u'强势围观，<color=#00FF00FF>%s</color>在<color=#00FF00FF>%s</color>击杀<color=#00FF00FF>%s</color>获得<color=#FFFF00FF>%d</color>鸟蛋！' % (
                nick, self.room_name, bird_name, chg_chip)
                mo = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
                mo.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
                Context.GData.broadcast_to_system(mo)
        return reward_info, bonus_pool, bonus_count, critM

    def notify_next_scene(self):
        mo = MsgPack(Message.BIRD_MSG_NEXT_SCENE | Message.ID_NTF)
        mo.set_param('start', self.map.start_ms)
        uptime = self.real_uptime()
        mo.set_param('uptime', uptime)
        mo.set_param('map', self.map.get_map_info())
        self.table_broadcast(mo)
        return 0

    def on_unlock_barrel(self, uid, player, mi):
        mo = MsgPack(Message.BIRD_MSG_UNLOCK_BARREL | Message.ID_ACK)
        conf = self.barrel_unlock_config
        if not conf:
            self._error('miss barrel.unlock.config')
            return mo.set_error(1, 'system error')

        next_level = player.max_barrel_level + 1
        strong_conf = Context.Configure.get_game_item_json(self.gid, 'barrel.unlock.strong')
        if next_level >= strong_conf[0]:
            return mo.set_error(2, 'max level')

        level_conf = conf[next_level - 1]
        cost = -level_conf['diamond']
        real, final = player.incr_diamond(cost, 'unlock.barrel')
        if real != cost:
            return mo.set_error(3, 'lack diamond')
        NewTask.get_diamond_consume_task(uid, -cost, self.room_type)

        player.max_barrel_level = next_level
        multiple = BirdAccount.trans_barrel_level(self.gid, next_level)
        reward = player.issue_rewards(level_conf['reward'], 'unlock.barrel', True)
        reward = BirdProps.convert_reward(reward)

        mo = MsgPack(Message.BIRD_MSG_UNLOCK_BARREL | Message.ID_NTF)
        mo.set_param('u', uid)
        mo.update_param(reward)
        final = reward.get('d', final)
        mo.set_param('d', final)
        mo.set_param('lv', next_level)
        mo.set_param('mt', multiple)
        self.table_broadcast(mo)
        return

    def on_switch_barrel(self, uid, player, mi):
        mo = MsgPack(Message.BIRD_MSG_SWITCH_BARREL | Message.ID_NTF)
        delta = mi.get_param('da')
        switch_skin = mi.get_param('si')
        level = mi.get_param('lv', 0)
        if level > 0:
            if level > self.room_config['level_max1'] or level > player.max_barrel_level:
                return -1

            player.barrel_level = level
            mo.set_param('lv', level)
            mo.set_param('mt', player.barrel_multiple)
        elif delta in (-1, 1):    # 切换炮台
            if uid not in self.dict_pinfo:
                self.dict_pinfo[uid] = {}
            self.dict_pinfo[uid]['last_switch_timer'] = Time.current_ts()
            switch_level = player.barrel_level + delta
            max_barrel_level = player.max_barrel_level
            if switch_level == max_barrel_level + 2:                # 当前已经是等级预览
                switch_level = self.level_min1
            elif switch_level > self.room_config['level_max1']:     # 最高限制
                switch_level = self.level_min1
            elif switch_level < self.level_min1:     # 最低限制
                switch_level = self.room_config['level_max1']

            if switch_level > max_barrel_level:
                switch_level = max_barrel_level + 1  # 等级预览
                if switch_level > self.barrel_max_level:
                    if delta == -1:
                        switch_level = max_barrel_level
                    else:
                        switch_level = self.level_min1

            player.barrel_level = switch_level
            mo.set_param('lv', switch_level)
            mo.set_param('mt', player.barrel_multiple)

        if switch_skin is not None:
            player.barrel_skin = switch_skin
            mo.set_param('si', switch_skin)
            mo.set_param('lv', player.barrel_level)
            mo.set_param('mt', player.barrel_multiple)

        mo.set_param('u', uid)
        self.table_broadcast(mo)
        return 0

    def on_skill_lock(self, uid, player, mi):
        """
        锁定
        """
        if self.map is None:
            return

        mo = MsgPack(Message.BIRD_MSG_SKILL_LOCK | Message.ID_NTF)

        if player.lock_state == 1:
            player.lock_state = 0
            player.lock_bird = None
        else:
            player.lock_state = 1

        mo.set_param('u', uid)
        mo.set_param('state', player.lock_state)
        self.table_broadcast(mo)
        return 0

    def on_lock_bird(self, uid, player, mi):
        if self.map is None:
            return

        uptime = self.real_uptime()
        mo = MsgPack(Message.BIRD_MSG_LOCK_BIRD | Message.ID_NTF)
        if player.lock_state == 1:
            bird = mi.get_param('i')
            mo.set_param('u', uid)
            mo.set_param('i', bird)
            player.lock_bird = bird
            self.table_broadcast(mo)
            return 0
        return mo.set_error(1, 'not in locking')

    def on_skill_freeze(self, uid, player, mi):
        if self.map is None:
            return

        mo = MsgPack(Message.BIRD_MSG_SKILL_FREEZE | Message.ID_NTF)

        res, final = player.use_props(BirdProps.PROP_FREEZE, self.room_type)
        if not res:
            if player.max_barrel_level < self.barrel_unlock_use:
                return mo.set_error(4, u'解锁10倍炮才能购买')
            diamond = player.buy_props(BirdProps.PROP_FREEZE)
            if diamond is None:
                return mo.set_error(2, 'no more')
            mo.set_param('d', diamond)

        uptime = self.real_uptime()
        self.__check_freeze(uptime)
        if self.lasted_freeze:
            left_ms = self.lasted_freeze['end'] - uptime
            delay_timer = 15000 - left_ms
            self.total_freeze += delay_timer
        else:
            delay_timer = 15000

        # delay scene switch timer
        delay_second = delay_timer / 1000.0
        if self.delta_timer.IsActive():
            self.delta_timer.delay(delay_second)
            self._info('freeze, delay delta_timer', delay_second)
        if self.switch_timer.IsActive():
            self.switch_timer.delay(delay_second)
            self._info('freeze, delay switch_timer', delay_second)
        if self.loop_flush_timer.IsActive():
            self.loop_flush_timer.delay(delay_second)
            self._info('freeze, delay loop_flush_timer', delay_second)

        NewTask.get_freeze_task(player.uid, self.room_type)

        self.lasted_freeze['start'] = uptime
        self.lasted_freeze['end'] = uptime + 15000
        mo.set_param('u', uid)
        mo.set_param('ts', uptime)
        mo.set_param('lt', final)
        self.table_broadcast(mo)
        return 0

    def __check_freeze(self, uptime):
        if self.lasted_freeze:
            end_ms = self.lasted_freeze['end']
            if end_ms <= uptime:  # expired
                self.total_freeze += 15000
                self.lasted_freeze.clear()

    def on_skill_violent(self, uid, player, mi):
        """
        双倍击杀概率, 30秒内击杀获得双倍鸟蛋, vipx以上使用
        """
        if self.map is None:
            return

        mo = MsgPack(Message.BIRD_MSG_SKILL_VIOLENT | Message.ID_NTF)

        res, final = player.use_props(BirdProps.PROP_VIOLENT, self.room_type)
        if not res:
            if player.max_barrel_level < self.barrel_unlock_use:
                return mo.set_error(4, u'解锁10倍炮才能购买')
            diamond = player.buy_props(BirdProps.PROP_VIOLENT)
            if diamond is None:
                return mo.set_error(2, 'no more')
            mo.set_param('d', diamond)

        NewTask.get_violent_task(player.uid, self.room_type)

        uptime = self.real_uptime()
        player.violent['start'] = uptime
        player.violent['end'] = uptime + 30000
        mo.set_param('u', uid)
        mo.set_param('ts', uptime)
        mo.set_param('lt', final)
        self.table_broadcast(mo)
        return 0

    def get_super_weapon_pool_chip(self):
        key = 'game.%d.info.super_weapon_pool' % self.gid
        key2 = 'pool.barrel_level_chip'
        pool_chip = Context.RedisMix.hash_get(key, key2, 0)
        return Tool.to_int(pool_chip)

    def incr_super_weapon_pool_chip(self, value):
        key = 'game.%d.info.super_weapon_pool' % self.gid
        key2 = 'pool.barrel_level_chip'
        Context.RedisMix.hash_incrby(key, key2, value)

    def get_super_weapon_pool_baseline(self):
        baseReward = self.super_weapon_config['baseReward']
        maxR = self.super_weapon_config['maxR']
        return baseReward * maxR

    def get_super_weapon_reward_rate(self):
        retRate = 0
        pool_chip = self.get_super_weapon_pool_chip()
        if pool_chip >= self.get_super_weapon_pool_baseline():      # 超过水线放水
            maxR = self.super_weapon_config['maxR']
            retRate = random.uniform(1, maxR)
        else:           # 蓄水
            minR = self.super_weapon_config['minR']
            retRate = random.uniform(minR, 1)

        return retRate

    def cmp_point(self, bird_id_1, bird_id_2):
        bird_type = self.map.bird_type(bird_id_1)
        if bird_type is None:
            return -1
        bird_config = self.bird_config[bird_type]
        if 'class' in bird_config and bird_config['class'] in ['boss', 'worldBoss']:  # boss无效
            return -1
        point_1 = bird_config['point']

        bird_type = self.map.bird_type(bird_id_2)
        if bird_type is None:
            return 1
        bird_config = self.bird_config[bird_type]
        if 'class' in bird_config and bird_config['class'] in ['boss', 'worldBoss']:  # boss无效
            return 1
        point_2 = bird_config['point']
        return Tool.to_int(point_1) - Tool.to_int(point_2)

    def sort_bird_list_by_point(self, bird_list):
        return sorted(bird_list, cmp=self.cmp_point)

    def on_skill_super_weapon_ready(self, uid, player, mi):
        mo = MsgPack(Message.BIRD_MSG_SKILL_SUPER_WEAPON_READY | Message.ID_NTF)
        mo.set_param('u', uid)
        self.table_broadcast(mo)
        return

    def on_skill_super_weapon(self, uid, player, mi):
        """
        vip2以上使用, 辐射一块
        """
        if self.map is None:
            return

        mo = MsgPack(Message.BIRD_MSG_SKILL_SUPER_WEAPON | Message.ID_NTF)
        pt = mi.get_param('pt')
        res, final = player.use_props(BirdProps.PROP_SUPER_WEAPON, self.room_type)
        if not res:
            if player.max_barrel_level < self.barrel_unlock_use:
                return mo.set_error(4, u'解锁10倍炮才能购买')
            diamond = player.buy_props(BirdProps.PROP_SUPER_WEAPON)
            if diamond is None:
                # if can:
                #     Context.Data.del_game_attrs(uid, self.gid, 'try_super_weapon')
                return mo.set_error(2, 'no more')
            mo.set_param('d', diamond)

        uptime = self.real_uptime()
        birds = mi.get_param('birds')
        birds = set(birds)
        catched_list = []

        multiple = self.super_weapon_config['multi']
        baseReward = self.super_weapon_config['baseReward']
        rewardRate = self.get_super_weapon_reward_rate()
        c_rewardChip = baseReward * rewardRate
        Context.Log.debug('超级武器，本次最多获取：', c_rewardChip)
        # 武器使用成功应该把对应钱数存进池中
        self.incr_super_weapon_pool_chip(baseReward)

        bird_list = self.sort_bird_list_by_point(birds)
        allReward = 0
        for bird in bird_list:
            bird_type = self.map.bird_type(bird)
            if bird_type is None:
                continue
            bird_config = self.bird_config[bird_type]
            if bird_config['Bomc'] == 0:    # 判断是否可以被爆炸击杀
                continue

            point = bird_config['point']

            bird_reward = point*multiple
            if allReward + bird_reward > c_rewardChip:
                continue
            else:
                if bird not in catched_list:
                    catched_list.append(bird)
                    allReward += bird_reward

        mo.set_param('u', uid)
        mo.set_param('pt', pt)
        mo.set_param('ts', uptime)
        mo.set_param('lt', final)
        # 扣除武器池中钱数
        self.incr_super_weapon_pool_chip(-allReward)

        k, v = SuperWeaponEvent.get_super_weapon_event_dict(self.gid, -allReward, 'super_weapon_bomb')  # 使用超级武器
        SuperWeaponEvent.add_event(uid, k, v)

        # 固定鸟蛋获得
        NewTask.get_super_weapon_task(player.uid, self.room_type)

        mo.set_param('fc', 0)
        mo.set_param('c', player.chip)

        if allReward > 20000:
            bulletin = 3
            nick = Context.Data.get_attr(uid, 'nick')
            nick = Context.hide_name(nick)
            led = u'真乃军事奇才！恭喜玩家<color=#00FF00FF>%s</color>使用<color=#00FF00FF>超级武器</color>获得<color=#FFFF00FF>%d</color>鸟蛋！' % (
                nick, allReward)
            mou = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
            mou.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
            Context.GData.broadcast_to_system(mou)

        if catched_list:    # 有鸟挂
            final_info, catch_bird_list, up_reward_list, critM = self.process_catch_birds(player, catched_list, multiple)
            mo.update_param(final_info)
            if not up_reward_list:
                exp = Context.Data.get_game_attr_int(player.uid, self.gid, 'exp', 0)
                mo.set_param('exp', exp)
            if catch_bird_list:
                mo.set_param('r', catch_bird_list)
            if len(critM) >= 1:
                l = []
                for k, v in enumerate(critM):
                    info = {}
                    info['bird'] = v[0]
                    info['double'] = v[1]
                    l.append(info)
                mo.set_param('critM', l)
            self.broadcast_notify_with_filter(player, mo)

            if up_reward_list:  # 等级升级提醒
                self._notify_exp_upgrade(player, up_reward_list)
        else:
            self.table_broadcast(mo)
        return 0

    def on_skill_portal(self, uid, player, mi):
        """
        随机召唤一只鸟
        """
        if self.map is None:
            return

        mo = MsgPack(Message.BIRD_MSG_SKILL_PORTAL | Message.ID_NTF)

        res, final = player.use_props(BirdProps.PROP_PORTAL, self.room_type)
        if not res:
            if player.max_barrel_level < self.barrel_unlock_use:
                return mo.set_error(4, u'解锁10倍炮才能购买')
            diamond = player.buy_props(BirdProps.PROP_PORTAL)
            if diamond is None:
                return mo.set_error(2, 'no more')
            mo.set_param('d', diamond)

        rel_uptime, _, _ = self.relative_time()
        hunter = self.get_by_state(Enum.user_state_playing)
        bird = self.map.make_bonus(int(rel_uptime) / 100, hunter)

        NewTask.get_call_task(player.uid, self.room_type)

        mo.set_param('u', uid)
        mo.set_param('bird', bird)
        mo.set_param('ts', rel_uptime)
        mo.set_param('lt', final)
        self.table_broadcast(mo)
        return 0

    def check_exp_level(self, player, gid, exp, delta):
        prev_level, prev_diff = BirdAccount.get_exp_info(player.uid, gid, exp)
        player.exp = Context.Data.hincr_game(player.uid, gid, 'exp', delta)
        now_level, now_diff = BirdAccount.get_exp_info(player.uid, gid, player.exp)

        up_reward_list = []
        while prev_level < now_level:
            # 升级礼包
            conf = self.exp_level_reward_conf
            rewards = conf[prev_level]
            rewards_info = player.issue_rewards(rewards, 'exp.upgrade', True)

            prev_level += 1
            up_reward_list.append(rewards_info)
        return up_reward_list

    def on_drill_boom(self, uid, player, mi):
        if player.uid != self.drill_bomb_uid:
            return 1
        # bird = mi.get_param('bird')
        # bird_type = self.map.bird_type(bird)
        # if not bird_type:
        #     self._warn('bird %d maybe caught already' % bird)
        #     return 0
        owner = player.drill_info

        multiple = owner.get('multiple')
        shot_total_point = owner.get('total_point', 0)
        birds = mi.get_param('birds')
        birds = set(birds)
        catched_list = []
        if not multiple or multiple == 0:
            Context.Log.debug('error; bomb report not has multi')
            multiple = player.barrel_multiple
            return

        allReward = multiple * 10   # 全屏，区域炸弹怪默认自带10倍
        total_point = 10
        for bird in birds:
            bird_types = self.map.bird_type(bird)
            if bird_types is None:
                continue
            bird_config = self.bird_config[bird_types]
            if bird_config['Bomc'] == 0:
                continue
            else:
                point = bird_config['point']
                bird_reward = point * multiple
                if bird_reward == 0:
                    continue
                if total_point + point > 300:
                    continue
                else:
                    if bird not in catched_list:
                        catched_list.append(bird)
                        total_point += point
                        allReward += bird_reward

        mo = MsgPack(Message.BIRD_MSG_CATCH_BIRD | Message.ID_NTF)
        mo.set_param('u', uid)
        final_info, catch_bird_list, up_reward_list, critM = self.process_catch_birds(player, catched_list, multiple)
        chip_total = shot_total_point * multiple
        for i in catch_bird_list:
            if i.has_key('w'):
                if i['w'].has_key('c'):
                    chip_total += i['w']['c']
        if chip_total > 20000:
            nick = Context.hide_name(player.nick)
            bulletin = 2
            bird_config = self.bird_config[555]
            bird_name = bird_config['name']
            led = u'人品爆发，<color=#00FF00FF>%s</color>在<color=#00FF00FF>%s</color>击杀<color=#00FF00FF>%s</color>获得<color=#FFFF00FF>%d</color>鸟蛋！' % (
            nick, self.room_name, bird_name, chip_total)
            mou = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
            mou.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
            Context.GData.broadcast_to_system(mou)

        if final_info:
            mo.update_param(final_info)
        if catch_bird_list:
            mo.set_param('r', catch_bird_list)
        if self.play_mode == Enum.play_mode_match:
            mo.set_param('s', player.match_score)

        if not up_reward_list:
            exp = Context.Data.get_game_attr_int(player.uid, self.gid, 'exp', 0)
            mo.set_param('exp', exp)
        self.broadcast_notify_with_filter(player, mo)
        player.drill_info = {}
        if up_reward_list:  # 等级升级提醒
            self._notify_exp_upgrade(player, up_reward_list)

        mo = MsgPack(Message.BIRD_MSG_DRILL_BOOM | Message.ID_ACK)
        mo.set_param('w', chip_total)
        mo.set_param('u', uid)
        self.table_broadcast(mo)

        return 0

    def on_report_birds(self, uid, player, mi):
        # 炸弹辐射到鸟
        bird = mi.get_param('bird')
        ts = mi.get_param('ts')
        bullet_multiple = mi.get_param('multi', 0)
        bird_type = self.map.bird_type(bird)
        if not bird_type:
            self._warn('bird %d maybe caught already' % bird)
            return 0
        owner = self.special_birds.get(bird_type)
        if not owner or owner['uid'] != uid:
            self._warn('uid not match')
            return 0

        del self.special_birds[bird_type]
        if owner['ts'] - self.map.start_ms != ts:
            self._warn('ts not match')
            return 0

        uptime = self.real_uptime()
        if owner['ts'] + 500 < uptime:
            self._info('report expired, pass')
            return 0

        multiple = owner['multiple']
        birds = mi.get_param('birds')
        birds = set(birds)
        catched_list = []
        if bird_type == 551:
            boom_type = self.map.bird_map[bird]['sk']
            bird_id = bird
            catched_list.append(bird)
            for bird in birds:
                bird_types = self.map.bird_type(bird)
                if bird_types is None:
                    continue
                if bird_types == boom_type:
                    if bird not in catched_list:
                        if len(catched_list) > 5:
                            break
                        catched_list.append(bird)

            # 同类炸弹怪问题处理 水池延时处理
            if bullet_multiple == 0:
                Context.Log.debug('error; bomb report not has multi')
                bullet_multiple = player.barrel_multiple
            point = self.bird_config[boom_type].get('point', 0)
            total = len(catched_list) * point * bullet_multiple   #

            self.map.clear_boom_birds_type()
        else:

            if bullet_multiple == 0:
                Context.Log.debug('error; bomb report not has multi')
                bullet_multiple = player.barrel_multiple
            point = self.bird_config[bird_type].get('point', 0)
            c_total = point * bullet_multiple   #

            catched_list.append(bird)
            allReward = bullet_multiple * 10   # 全屏，区域炸弹怪默认自带10倍
            for bird in birds:
                bird_types = self.map.bird_type(bird)
                if bird_types is None:
                    continue
                bird_config = self.bird_config[bird_types]
                if bird_config['Bomc'] == 0:
                    continue
                else:
                    point = bird_config['point']
                    bird_reward = point * multiple
                    if bird_reward == 0:
                        continue
                    if allReward + bird_reward > c_total:
                        continue
                    else:
                        if bird not in catched_list:
                            catched_list.append(bird)
                            allReward += bird_reward
            #Context.Log.debug('炸弹怪：', bird_type, ',c_total:', c_total, ',allReward:', allReward)

        mo = MsgPack(Message.BIRD_MSG_CATCH_BIRD | Message.ID_NTF)
        mo.set_param('u', uid)
        mo.set_param('b', bird)
        final_info, catch_bird_list, up_reward_list, critM = self.process_catch_birds(player, catched_list, multiple)
        if bird_type in [553, 552, 551]:
            chip_total = 0
            for i in catch_bird_list:
                if i.has_key('w'):
                    if i['w'].has_key('c'):
                        chip_total += i['w']['c']
            if chip_total > 20000:
                nick = Context.hide_name(player.nick)
                bulletin = 2
                bird_config = self.bird_config[bird_type]
                bird_name = bird_config['name']
                led = u'人品爆发，<color=#00FF00FF>%s</color>在<color=#00FF00FF>%s</color>击杀<color=#00FF00FF>%s</color>获得<color=#FFFF00FF>%d</color>鸟蛋！' % (
                nick, self.room_name, bird_name, chip_total)
                mou = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
                mou.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
                Context.GData.broadcast_to_system(mou)
        if final_info:
            mo.update_param(final_info)
        if catch_bird_list:
            mo.set_param('r', catch_bird_list)
        if self.play_mode == Enum.play_mode_match:
            mo.set_param('s', player.match_score)
        if len(critM) >= 1:
            l = []
            for k, v in enumerate(critM):
                info = {}
                info['bird'] = v[0]
                info['double'] = v[1]
                l.append(info)
            mo.set_param('critM', l)
        if not up_reward_list:
            exp = Context.Data.get_game_attr_int(player.uid, self.gid, 'exp', 0)
            mo.set_param('exp', exp)
        self.broadcast_notify_with_filter(player, mo)

        if up_reward_list:  # 等级升级提醒
            self._notify_exp_upgrade(player, up_reward_list)
        return 0

    def on_weapon_report_birds(self, uid, player, mi):
        t = mi.get_param('t')
        bird = mi.get_param('bird')

        owner = self.weapon_eff_birds.get(bird)
        if not owner or owner['uid'] != uid:
            self._warn('uid not match')
            return 0
        if owner['ts'] - 1 <= 0:
            del self.weapon_eff_birds[bird]
        else:
            self.weapon_eff_birds[bird]['ts'] -= 1
        pene = self.weapon_config[int(owner['wid'])]['pene']
        if t not in pene:
            self._warn('your weapon is spacial effect, pass')
            return 0

    def get_reward_coin(self, catch_bird_list, player):
        chip_total = 0
        for i in catch_bird_list:
            if i.has_key('w'):
                if i['w'].has_key('c'):
                    chip_total += i['w']['c']
                elif i['w'].has_key('tg'):
                    chip_total += i['w']['tg'] * 5000
                elif i['w'].has_key('d'):
                    chip_total += i['w']['d'] * 500
                elif i['w'].has_key('o'):
                    chip_total += i['w']['o'] * 1250
        if chip_total > 0:
            self.incr_table_pool(-chip_total)
        return

    def process_catch_birds(self, player, birds, multiple):
        # 处理捕获到的鸟
        catch_reward_list, catch_bird_list = [], []
        bonus_pool, bonus_count = 0, 0
        birds_exp = 0
        critM = []
        for bird in birds:
            bird_type = self.map.bird_type(bird)
            if not bird_type:
                continue
            real_bird_type = bird_type % 1000
            bird_config = self.bird_config[real_bird_type]
            catch_reward, bonus_pool, bonus_count, vio = self.__issue_catch_reward(player, bird, bird_config, multiple)
            if vio != None:
                critM.append(vio)
            catch_reward_list.append(catch_reward)
            catch_reward = BirdProps.convert_reward(catch_reward)
            catch_bird_list.append({'i': bird, 'w': catch_reward['w']})

            self.hit_bird_task(player.uid, bird_type, self.room_type)

            exp = bird_config['Exp']
            birds_exp += exp
            
        if len(catch_reward_list) == 1:
            final_info = BirdProps.convert_reward(catch_reward_list[0])
            del final_info['w']
        else:
            final_info = BirdProps.merge_reward_result(False, *catch_reward_list)
            final_info = BirdProps.convert_reward(final_info)

        if bonus_pool > 0:
            final_info['bonus_pool'] = bonus_pool
        if bonus_count > 0:
            final_info['bonus_count'] = bonus_count

        up_reward_list = self.check_exp_level(player, self.gid, player.exp, birds_exp)
        if final_info:
            self.__stat_fall_info(player, catch_bird_list)
        self.get_reward_coin(catch_bird_list, player)
        return final_info, catch_bird_list, up_reward_list, critM

    def broadcast_notify_with_filter(self, player, mo):
        self.__filter_plt_ver(mo)

    def __filter_plt_ver(self, mo):
        self.table_broadcast(mo)


    def new_flush(self, bird_type):
        if not self.map.has_more_map():
            return

        if self.map.get_tide_state():
            return

        flush_bird = None
        for k,v in self.type_bird_config.items():
            if bird_type in v:
                if k in self.not_flush_config:
                    flush_bird = random.choice(v)
        if not flush_bird:
            return

        rel_uptime, _, _ = self.relative_time()
        hunter = self.get_by_state(Enum.user_state_playing)
        start = int(rel_uptime) / 100

        bird = self.map.flush_new_bird(start, flush_bird, hunter)
        birds = [bird]
        if birds:
            mo = MsgPack(Message.BIRD_MSG_NEW_BIRD | Message.ID_NTF)
            mo.set_param('birds', birds)
            self.table_broadcast(mo)

    def flush_new_bird(self, conf):
        if not self.map.has_more_map():
            return

        if self.map.get_tide_state():
            return
        birds = []
        rel_uptime, _, _ = self.relative_time()
        hunter = self.get_by_state(Enum.user_state_playing)
        start = int(rel_uptime) / 100
        # 必出
        if 'a' in conf:
            for bird_type, count in conf['a']:
                for i in range(count):
                    bird = self.map.flush_new_bird(start, bird_type, hunter)
                    if bird:
                        if isinstance(bird, list):
                            birds.extend(bird)
                        else:
                            birds.append(bird)
        # 多选1
        if 'b' in conf:
            accumulator = 0
            rand = random.randint(1, 10000)
            for bird_type, count, odd in conf['b']:
                accumulator += int(odd * 10000)
                if rand <= accumulator:
                    for i in range(count):
                        bird = self.map.flush_new_bird(start, bird_type, hunter)
                        if bird:
                            if isinstance(bird, list):
                                birds.extend(bird)
                            else:
                                birds.append(bird)
                    break
        # 多选多
        if 'c' in conf:
            for bird_type, count, odd in conf['c']:
                if random.random() <= odd:
                    for i in range(count):
                        bird = self.map.flush_new_bird(start, bird_type, hunter)
                        if bird:
                            if isinstance(bird, list):
                                birds.extend(bird)
                            else:
                                birds.append(bird)
        if birds:
            mo = MsgPack(Message.BIRD_MSG_NEW_BIRD | Message.ID_NTF)
            mo.set_param('birds', birds)
            self.table_broadcast(mo)

    def __handle_loop_flush(self, msg):
        conf = self.flush_config.get(6)
        if conf:
            self.set_timer('loop_flush', conf['var'])
            if not self.map.has_more_map():
                self.flush_new_bird(conf)


    def __stat_fall_info(self, player, catch_bird_list):
        if catch_bird_list:
            stat_info = {}
            for one in catch_bird_list:
                if 'c' in one['w']:
                    stat_info[BirdProps.PROP_CHIP] = stat_info.get(BirdProps.PROP_CHIP, 0) + one['w']['c']
                if 'd' in one['w']:
                    stat_info[BirdProps.PROP_DIAMOND] = stat_info.get(BirdProps.PROP_DIAMOND, 0) + one['w']['d']
                if 'o' in one['w']:
                    stat_info[BirdProps.PROP_COUPON] = stat_info.get(BirdProps.PROP_COUPON, 0) + one['w']['o']
                props = one['w'].get('p')
                if props:
                    for _t, _c in props:
                        stat_info[_t] = stat_info.get(_t, 0) + _c

            if stat_info:
                list_params = []
                for k, v in stat_info.iteritems():
                    list_params.append('barrel_limit_prop_' + str(k))
                    list_params.append(v)
                if len(list_params) == 2:
                    Context.Data.hincr_game(player.uid, self.gid, *list_params)
                else:
                    Context.Data.hmincr_game(player.uid, self.gid, *list_params)

    def get_online_reward_t(self, player, config, times, uid):
        now_ts = Time.current_ts()
        today_start_ts = Time.today_start_ts()
        # if player.online_reward_ts:
        #     start_ts = player.online_reward_ts
        # else:
        #     start_ts = player.online_ts
        start_ts = player.online_reward_ts
        if start_ts < today_start_ts:
            add_t = now_ts - today_start_ts
        else:
            add_t = now_ts - start_ts
        l = Context.Daily.get_daily_data(uid, self.gid, 'online.reward.long')
        l = Tool.to_int(l, 0) + add_t
        # ll = 0
        # for i, v in enumerate(config['cd'][str(player.create_days)]):
        #     if i == times:
        #         break
        #     ll += v[0]
        # t = config['cd'][str(player.create_days)][times][0] - (l - ll)
        t = config['cd'][str(player.create_days)][times][0] - l
        return t

    def on_get_online_reward(self, uid, player, mi):
        ack = MsgPack(Message.MSG_SYS_GET_ONLINE_REWARD | Message.ID_ACK)
        config = self.online_reward_config
        times = Context.Daily.get_daily_data(uid, self.gid, 'online.reward.times')
        times = Tool.to_int(times, 0)
        if str(player.create_days) not in config['cd'] or times == len(config['cd'][str(player.create_days)]):
            return ack.set_error(1, 'is over')
        t = self.get_online_reward_t(player, config, times, uid)
        if t > 2:
            return ack.set_error(2, u'时间还没到')
        # 处理概率
        pool_id = config['cd'][str(player.create_days)][times][1]
        r = random.random()
        odd = 0
        i = None
        for _i, _odd in enumerate(config['odds'][str(pool_id)]):
            if not _odd:
                continue
            odd += _odd
            if r <= odd:
                i = _i
                break
        # 处理掉落
        vip_level_form = BirdAccount.get_vip_level(uid, self.gid)
        _reward = config['pool_reward'][str(pool_id)][i]
        if _reward:
            player.issue_rewards(_reward, 'online.reward', True)
        # 处理抽奖次数
        Context.Daily.incr_daily_data(uid, self.gid, 'online.reward.times', 1)
        Context.Daily.set_daily_data(uid, self.gid, 'online.reward.long', 0)
        now_ts = Time.current_ts()
        player.online_reward_ts = now_ts
        new_times = times + 1
        if str(player.create_days) in config['cd'] and new_times <= (len(config['cd'][str(player.create_days)])-1):
            pool = config['cd'][str(player.create_days)][new_times][1]
            conf = config['pool_info'][str(pool)]
            ack.set_param('conf', conf)

            t = self.get_online_reward_t(player, config, new_times, uid)
            t = 0 if t < 0 else t
            ack.set_param('t', t)

        elif str(player.create_days+1) in config['cd']:
            pool = config['cd'][str(player.create_days+1)][0][1]
            conf = config['pool_info'][str(pool)]
            ack.set_param('conf', conf)
            ack.set_param('is_t', 1)

        # 处理LED
        if 'vip_exp' in _reward:
            vip_exp = _reward.get('vip_exp')
            vip_level = BirdAccount.get_vip_level(uid, self.gid, vip_exp)
            if vip_level >= 4 and vip_level > vip_level_form:
                bulletin = 3
                nick = Context.hide_name(player.nick)
                led = u'玩家<color=#00FF00FF>%s</color>VIP等级晋升到<color=#FFFF00FF>%d</color>，羡煞众人！' % (nick, vip_level)
                mo = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
                mo.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
                Context.GData.broadcast_to_system(mo)
        ack.set_param('i', i)
        return ack

    def on_online_reward_info(self, uid, player, mi):
        ack = MsgPack(Message.MSG_SYS_ONLINE_REWARD_INFO | Message.ID_ACK)
        config = self.online_reward_config
        times = Context.Daily.get_daily_data(uid, self.gid, 'online.reward.times')
        times = Tool.to_int(times, 0)
        if str(player.create_days) not in config['cd'] or times == len(config['cd'][str(player.create_days)]):
            if str(player.create_days+1) in config['cd']:
                pool = config['cd'][str(player.create_days+1)][0][1]
                conf = config['pool_info'][str(pool)]
                ack.set_param('conf', conf)
                ack.set_param('is_t', 1)
                return ack
            return ack.set_error(1, 'is over')
        t = self.get_online_reward_t(player, config, times, uid)
        t = 0 if t < 0 else t
        ack.set_param('t', t)
        if mi.get_param('type') == 1:
            pool = config['cd'][str(player.create_days)][times][1]
            conf = config['pool_info'][str(pool)]
            ack.set_param('conf', conf)
        return ack

    def hit_bird_task(self, uid, bird_id, room):
        NewTask.in_room_task(uid, 0, bird_id, 1, room)
        NewTask.in_room_task(uid, 1, bird_id, 1, room)
        NewTask.in_task(uid, 0, bird_id, 1)
        NewTask.in_task(uid, 1, bird_id, 1)
        return
