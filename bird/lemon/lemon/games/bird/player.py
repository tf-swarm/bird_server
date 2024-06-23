#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-12-04

from const import Enum
from props import BirdProps
from account import BirdAccount
from const import Message
from lemon.entity.player import Player
from framework.util.tool import Time, Tool
from framework.context import Context
from framework.entity.msgpack import MsgPack
import random
import time


class BirdPlayer(Player):
    def __init__(self, uid):
        super(BirdPlayer, self).__init__(uid)
        self._props_info = None
        self.bullet_number = 0          # 子弹计数器
        self.barrel_angle = 0           # 炮筒角度
        self._barrel_level = 1          # 炮筒等级
        self.barrel_multiple = 1        # 炮筒倍数
        self._match_barrel_multiple = None # 比赛炮倍
        self._weapon_id = 0             # 炮筒id
        self.state = Enum.user_state_free
        self.lock_state = 0             # 炮台锁定
        self.lock_bird = None           # 锁定的鸟
        self.identity = Enum.identity_type_unknown
        self.lock = {}
        self.violent = {}
        self.bullet_map = {}            # 记录子弹和倍数
        self.drill_info = {}            # 玩家的钻头信息
        self.around_bird = [None] * 3   # 围绕的鸟
        self.attack_timer = None
        self.call_bird_timer = None
        self.offline_timer = None
        self.cook_task_timer = None
        self.bounty_task = {}
        self.today_pay_total = 0
        self.blocked = None
        self.live_telecast_user = 0
        self.session_ver = '0.0.0'
        self.match_times = 1
        self._match_bullet = None
        self.match_score = 0
        self.match_task_101 = 0
        self.cook_task = {}
        self.cook_task_list = []
        self.cook_task_state = Enum.task_state_free
        self.create_time = None
        self.online_reward_ts = None
        self._recharge_buff = None
        self._vid = None
        self.shot_times = 1
        self._chip = None
        self.last_shot_bullet = 0  # 玩家最后发射子弹时间
        self._channel_id = None
        self._drop_coupon = None
        self._recharge_gift_cool_time = Time.current_ts()
        self.auto_shot_status = 0
        self.vip_protect_refresh_flag = False    #保护值刷新标志
        self.bullet = 0

        self.is_new_p = False       # 是否新玩家标记


    def leave_table(self):
        super(BirdPlayer, self).leave_table()
        self._props_info = None
        self.bullet_number = 0
        self.barrel_angle = 0
        self._barrel_level = 1
        self._match_barrel_multiple = None
        self.barrel_multiple = 1
        self.weapon_id = 0
        self.state = Enum.user_state_free
        self.identity = Enum.identity_type_unknown
        self.lock.clear()
        self.violent.clear()
        self.bullet_map.clear()
        self.bounty_task.clear()
        self.around_bird = [None] * 3  # 围绕的鸟
        self.today_pay_total = 0
        self.blocked = None
        self.live_telecast_user = 0
        self.session_ver = '0.0.0'
        self.match_times = 1
        self._match_bullet = None
        self.match_score = 0
        self.match_task_101 = 0
        self.cook_task = {}
        self.cook_task_list = []
        self.drill_info = {}
        self._channel_id = None
        self.auto_shot_status = 0
        self.cook_task_state = Enum.task_state_free
        if self.attack_timer:
            self.attack_timer.cancel()
            self.attack_timer = None

        if self.call_bird_timer:
            self.call_bird_timer.cancel()
            self.call_bird_timer = None

        if self.offline_timer:
            self.offline_timer.cancel()
            self.offline_timer = None

        if self.cook_task_timer:
            self.cook_task_timer.cancel()
            self.cook_task_timer = None

        self.create_time = None
        self.online_reward_ts = None
        self._recharge_buff = None
        self.last_shot_bullet = 0

    def switch_scene(self):
        self.lock.clear()
        self.violent.clear()
        if self.attack_timer:
            self.attack_timer.cancel()
            self.attack_timer = None

        if self.call_bird_timer:
            self.call_bird_timer.cancel()
            self.call_bird_timer = None

    def get_free_around_loc(self):
        for i in (0, 1, 2):
            if self.around_bird[i] is None:
                return i

    def get_around_loc(self, bird_id):
        for i in (0, 1, 2):
            if self.around_bird[i] == bird_id:
                return i

    def set_around_loc(self, loc, bird_id):
        self.around_bird[loc] = bird_id

    def del_around_bird(self, loc):
        self.around_bird[loc] = None

    def clear_around_bird(self):
        self.around_bird = [None] * 3

    def get_all_around_birds(self):
        l = []
        for i in (0, 1, 2):
            if self.around_bird[i]:
                l.append([i, self.around_bird[i]])
        return l

    def catch_bounty_bird(self, goal, bird_type, multi):
        if bird_type not in self.bounty_task:
            self.bounty_task[bird_type] = 1
        else:
            self.bounty_task[bird_type] += 1

        if 'count' not in self.bounty_task:
            self.bounty_task['count'] = 1
        else:
            self.bounty_task['count'] += 1

        self.bounty_task['ts'] = Time.current_ms()

        for _t, _cnt in goal.iteritems():
            if _cnt > self.bounty_task.get(_t, 0):
                return
        if multi not in self.bounty_task:
            self.bounty_task['multi'] = multi

    @property
    def props_info(self):
        return self._props_info

    @props_info.setter
    def props_info(self, props_list):
        self._props_info = dict(props_list)

    @property
    def props(self, pid):
        return self._props_info.get(pid, 0)

    @property
    def nick(self):
        return self.user_info['nick']

    @property
    def channel_id(self):
        if self._channel_id == None:
            self._channel_id = Context.Data.get_attr(self.uid, 'channelid', '1001_0')
        return self._channel_id

    @property
    def barrel_level(self):
        return self._barrel_level

    @property
    def weapon_id(self):
        self._weapon_id = Context.Data.get_game_attr_int(self.uid, self.gid, 'weapon_use_dict', 20000)
        return self._weapon_id

    @barrel_level.setter
    def barrel_level(self, level):
        self._barrel_level = level
        self.barrel_multiple = BirdAccount.trans_barrel_level(self.gid, level)

    @property
    def match_barrel_multiple(self):
        if not self._match_barrel_multiple:
            bullet_barrel = Context.Configure.get_game_item_json(self.gid, 'match.normal.config')
            self._match_barrel_multiple = bullet_barrel.get('barrel')[0]
        return self._match_barrel_multiple

    @match_barrel_multiple.setter
    def match_barrel_multiple(self, multiple):
        self._match_barrel_multiple = multiple

    @property
    def match_bullet(self):
        if self._match_bullet == None:
            self._match_bullet = Tool.to_int(Context.MatchDB.get_match_data('player', str(self.uid), 'bullet'))
        return self._match_bullet

    @match_bullet.setter
    def match_bullet(self, num):
        self._match_bullet = num

    @weapon_id.setter
    def weapon_id(self,idx):
        self._weapon_id = idx

    @property
    def max_barrel_level(self):
        return self.game_info['barrel_level']

    @max_barrel_level.setter
    def max_barrel_level(self, level):
        if self.game_info['barrel_level'] != level:
            self.game_info['barrel_level'] = level
            Context.Data.set_game_attr(self.uid, self.gid, 'barrel_level', level)

    @property
    def max_barrel_multi(self):
        return BirdAccount.trans_barrel_level(self.gid, self.game_info['barrel_level'])

    @property
    def barrel_skin(self):
        return self.game_info['barrel_skin']

    @barrel_skin.setter
    def barrel_skin(self, skin):
        if self.game_info['barrel_skin'] != skin:
            self.game_info['barrel_skin'] = skin
            Context.Data.set_game_attr(self.uid, self.gid, 'barrel_skin', skin)

    @property
    def chips(self):
        return self.chip

    @property
    def drop_coupon(self):
        if self._drop_coupon == None:
            self._drop_coupon = Context.Data.get_game_attr_int(self.uid, self.gid, 'drop_coupon', 0)
        return self._drop_coupon

    @drop_coupon.setter
    def drop_coupon(self, dc):
        self._drop_coupon = dc

    @property
    def exp(self):
        return self.game_info['exp']

    @exp.setter
    def exp(self, value):
        self.game_info['exp'] = value

    def in_locking(self, uptime):
        end = self.lock.get('end', 0)
        if end and end > uptime:
            return True

        self.lock.clear()
        return False

    def in_violent(self, uptime):
        end = self.violent.get('end', 0)
        if end and end > uptime:
            return True

        self.violent.clear()
        return False

    def can_shot(self):
        return self.game_info['barrel_level'] >= self._barrel_level

    def use_props(self, pid, roomtype):
        real, final = BirdProps.incr_props(self.uid, self.gid, pid, -1, 'game.use', roomtype=roomtype)
        if real == -1:
            self._props_info[pid] = final
            return True, final
        else:
            self._props_info[pid] = 0
            return False, 0

    def buy_props(self, pid):
        if self.game_info['diamond'] > 0:
            conf = BirdProps.get_config_by_id(self.gid, pid)
            price = conf['price']
            #  if self.game_info['diamond'] >= price:
            real, final = Context.UserAttr.incr_diamond(self.uid, self.gid, -price, 'table.buy.%d' % pid)
            self.game_info['diamond'] = final
            if real == -price:
                from newtask import NewTask
                NewTask.get_diamond_consume_task(self.uid, price)
                return final
        return None

    # 充值赠送冷却时间
    def get_recharge_gift_cool_time(self):
        return self._recharge_gift_cool_time

    def set_recharge_gift_cool_time(self, value):
        Context.Log.debug('set_recharge_gift_cool_time:', value)
        self._recharge_gift_cool_time = value

    @property
    def chip(self):
        #if self._chip is None:
        self._chip = Context.UserAttr.get_chip(self.uid, self.gid, 0)
        return self._chip

    def incr_chip(self, delta, event, **kwargs):
        real, final = Context.UserAttr.incr_chip(self.uid, self.gid, delta, event, **kwargs)
        self._chip = final
        self.game_info['chip'] = final
        return real, final, self.chips

    def incr_diamond(self, delta, event, **kwargs):
        real, final = Context.UserAttr.incr_diamond(self.uid, self.gid, delta, event, **kwargs)
        self.game_info['diamond'] = final
        return real, final

    def incr_coupon(self, delta, event, **kwargs):
        real, final = Context.UserAttr.incr_coupon(self.uid, self.gid, delta, event, **kwargs)
        self.game_info['coupon'] = final
        return real, final

    '''
      need_gift 是否是服务器赠送给玩家鸟蛋，如果是需要额外赠送额度
    '''
    def issue_rewards(self, rewards, event, need_gift=False, **kwargs):
        result = BirdProps.issue_rewards(self.uid, self.gid, rewards, event, need_gift, **kwargs)
        if result:
            if 'chip' in result:
                self.game_info['chip'] = result['chip']
            if 'coupon' in result:
                self.game_info['coupon'] = result['coupon']
            if 'diamond' in result:
                self.game_info['diamond'] = result['diamond']
            if 'props' in result:
                props = self._props_info
                for one in result['props']:
                    if one['id'] in props:
                        props[one['id']] += one['count']
                    else:
                        props[one['id']] = one['count']
        return result

    def check_bankrupt(self, leave=False):
        bankrupt = False
        if leave:
            if self.game_info['chip'] < 1:
                bankrupt = True
        else:
            if not self.bullet_map and self.game_info['chip'] < 1:
                bankrupt = True
        if bankrupt:
            chip = Context.UserAttr.get_chip(self.uid, self.gid, 0)
            if chip > 0:
                self.game_info['chip'] = chip
                bankrupt = False
        return bankrupt

    def check_match_bullet(self):
        return self.match_bullet <= 0 and not self.bullet_map

    @property
    def create_days(self):
        if not self.create_time:
            create_time = Context.Data.get_attr(self.uid, 'createTime')
            self.create_time = Time.str_to_timestamp(create_time[:19])
        return Time.between_days(self.create_time) + 1

    @property
    def recharge_buff(self):
        if self._recharge_buff is None:
            self._recharge_buff = Context.Data.get_game_attr_json(self.uid, self.gid, 'recharge_buff', {})
        return self._recharge_buff

    @recharge_buff.setter
    def recharge_buff(self, recharge_buff):
        self._recharge_buff = recharge_buff
        Context.Data.set_game_attr(self.uid, self.gid, 'recharge_buff', Context.json_dumps(recharge_buff))

    @property
    def vid(self):
        if self._vid is None:
            self._vid = Context.Data.get_game_attr_int(self.uid, self.gid, 'vid', 0)
        return self._vid

    def get_coupon_pool(self):
        pool_dict = {}
        pool_private = Context.UserAttr.get_coupon_private_pool(self.uid, self.gid, 0)
        pool_vip = Context.RedisMix.hash_get('game.2.share', 'coupon_pool_vip', default=0)
        pool_free = Context.RedisMix.hash_get('game.2.share', 'coupon_pool_free', default=0)
        vip_level = BirdAccount.get_vip_level(self.uid, self.gid)
        if int(pool_private) > 0:
            pool_dict['coupon_pool_private'] = int(pool_private)
        if int(pool_free) > 0:
            pool_dict['coupon_pool_free'] = int(pool_free)
        if int(pool_vip) > 0 and vip_level > 0:
            pool_dict['coupon_pool_vip'] = int(pool_vip)

        return pool_dict

