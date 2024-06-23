#!/usr/bin/env python
# -*- coding=utf-8 -*-



import time
import json
import random
import sys
from const import Message
from framework.entity.msgpack import MsgPack
from framework.context import Context
from framework.util.tool import Time
from sdk.modules.mobile import Mobile
from props import BirdProps
from account import BirdAccount
from framework.util.tool import Tool

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf8')

class Target(object):
    def get_target_config(self, uid, gid):
        conf = {}
        room_Dict = {}
        target_time = {}
        room_type = [201, 202, 203]
        vip_level = range(0,9)
        vipConfig = Context.Configure.get_game_item_json(gid, 'vip.config')
        user_vip = BirdAccount.get_vip_level(uid, gid)
        for room in room_type:
            target_room = Context.Configure.get_game_item_json(gid, 'target_range.{0}.config'.format(room))
            room_Dict[room] = target_room
        conf['room_config'] = room_Dict

        conf['coupon'] = Context.Data.get_game_attr_int(uid, gid, 'target_coupon', 0)
        if user_vip > 0:
            for n in room_type:
                times = Context.Daily.get_daily_data(uid, gid, 'target_%d' %n)
                if user_vip == 1 and int(n) == 202 or user_vip == 1 and int(n) == 203 :
                    break
                if user_vip == 2 and int(n) == 203:
                    break
                if not times:
                    if vipConfig[user_vip - 1].has_key('target_range'):
                        vip_info = vipConfig[user_vip - 1].get('target_range')
                        for info in vip_info:
                            room = info['room_type']
                            count = info['count']
                            target_time[room] = count
                            Context.Daily.set_daily_data(uid, gid, 'target_%d' % room, count)
                        Context.Daily.set_daily_data(uid, gid, 'before_vip', user_vip)
                        break

                else:
                    before_vip = int(Context.Daily.get_daily_data(uid, gid, 'before_vip'))
                    if user_vip != before_vip:
                        if vipConfig[user_vip - 1].has_key('target_range'):
                            vip_info = vipConfig[user_vip - 1].get('target_range')
                            for info in vip_info:
                                room = info['room_type']
                                count = info['count']
                                target_time[room] = count
                                Context.Daily.set_daily_data(uid, gid, 'target_%d' % room, count)
                    else:
                        target_time[n] = times
                        conf['target_times'] = target_time
            conf['target_times'] = target_time
            Context.Daily.set_daily_data(uid, gid, 'before_vip', user_vip)
        else:
            conf['target_times'] = 0
        for vip in vip_level:
            vip_date = vipConfig[vip].get('target_range', 0)
            conf[vip+1] = vip_date
        return conf

    def incr_target_consume_target(self, value):
        key1 = 'game.2.target_pool'
        key2 = 'consume_target'  # 消耗靶场券
        Context.RedisMix.hash_incrby(key1, key2, value)

    def get_target_consume_target(self, default=None):
        key1 = 'game.2.target_pool'
        key2 = 'consume_target'   # 消耗靶场券
        ret = Context.RedisMix.hash_get(key1, key2, default)
        return Tool.to_int(ret)

    def incr_target_reward_coupon(self, value):
        key1 = 'game.2.target_pool'
        key2 = 'reward_coupon'  # 产出鸟券
        Context.RedisMix.hash_incrby(key1, key2, value)

    def get_target_reward_coupon(self, default=None):
        key1 = 'game.2.target_pool'
        key2 = 'reward_coupon'   # 产出鸟券
        ret = Context.RedisMix.hash_get(key1, key2, default)
        return Tool.to_int(ret)

    def target_room_date(self, uid, gid, mi):
        room_type = mi.get_param('room_type')
        mo = MsgPack(Message.MSG_SYS_TARGET_RANGE | Message.ID_ACK)
        daily = {}
        # 验证vip等级
        conf_dat = Context.RedisMix.hash_get_json('game.%d.background' % gid, 'target.config', {})
        if conf_dat.get('open', 1) == 0:
            mo.set_error(4, u'活动已被关闭')
            Context.GData.send_to_connect(uid, mo)
            return

        status = Context.RedisCache.hash_get_int('smart_game:%d' % uid, 'status', 0)
        if status > 0:
            return mo.set_error(0, u"你正在进行第三方小游戏，无法开启靶场")

        vip_limit = 0
        if room_type == 201:
            vip_limit = conf_dat.get('vlp')
        if room_type == 202:
            vip_limit = conf_dat.get('vlm')
        if room_type == 203:
            vip_limit = conf_dat.get('vlh')
        user_vip = BirdAccount.get_vip_level(uid, gid)
        vipConfig = Context.Configure.get_game_item_json(gid, 'vip.config')
        if user_vip <= vip_limit:
            return mo.set_error(1, 'level limit')

        target_room = Context.Configure.get_game_item_json(gid, 'target_range.%d.config'%room_type)

        consume = target_room['consume']
        owner_target = Context.UserAttr.get_target(uid, gid, 0)
        if owner_target < consume:
            return mo.set_error(2, u'您的靶场券不足，请前往商城购买靶场券')

        vip_info = vipConfig[user_vip - 1].get('target_range')
        #验证打靶的次数
        if user_vip < 5:
            times = Context.Daily.get_daily_data(uid, gid, 'target_{}'.format(room_type))
            if not times:
                if vipConfig[user_vip - 1].has_key('target_range'):
                    for inf in vip_info:
                        if inf['room_type'] == room_type:
                            daily[room_type] = inf['count']
            else:
                if int(times) <= 0:
                    return mo.set_error(3, u'今日打靶次数用完了，请明日再战')
                number = 1
                count = Context.Daily.incr_daily_data(uid, gid, 'target_{}'.format(room_type), -number)
                daily[room_type] = count
        else:
            for inf in vip_info:
                if inf['room_type'] == room_type:
                    daily[room_type] = inf['count']

        # 扣除靶卷
        real, final = Context.UserAttr.incr_target(uid, gid, -consume, 'target.room.consume')
        channel_id = Context.Data.get_attr(uid, 'channelid')
        Context.Stat.incr_daily_data(channel_id, 'server_target_play_times')

        # 随机打靶的环数
        total_consume_target = self.get_target_consume_target(0)
        total_reward_coupon = self.get_target_reward_coupon(0)
        if total_reward_coupon > total_consume_target * 4 + 500:   # 靶场游戏最多庄家输500处理
            roll_number = self.random_reward(target_room['rw_list']) # 环数
        else:
            roll_number = self.random_reward(target_room['rw_all'])

        # 奖励鸟倦
        award = target_room['g_award'][roll_number]
        # 池子记录靶场游戏
        self.incr_target_consume_target(consume)
        self.incr_target_reward_coupon(award)

        match_status = Context.MatchDB.get_match_player_status(uid)
        if match_status:
            mo.set_error(2, u'您正在竞技场中')
            Context.GData.send_to_connect(uid, mo)

        target_pool = Context.RedisMix.hash_get('game.2.share', 'target_pool', default=0)
        inf = {'cost': consume, 'reward': {'coupon': award}, 'target_pool': target_pool}
        tmp = Time.current_time('%Y-%m-%d')
        Context.RedisStat.hash_set('target:%s:%d' % (tmp, uid), Time.current_ms(), Context.json_dumps(inf))
        c_real, c_final = Context.UserAttr.incr_coupon(uid, gid, award, 'target.room.get')

        bulletin = 3
        nick = Context.Data.get_attr(uid, 'nick')
        nick = Context.hide_name(nick)
        led = u'运气爆棚！玩家<color=#00FF00FF>%s</color>在<color=#FF0000FF>小游戏-靶场</color>中获得<color=#FFFF00FF>%d</color>个鸟券' % (
            nick, award)
        mou = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
        mou.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
        Context.GData.broadcast_to_system(mou)

        target = {
            'loop': int(roll_number),
            'bird_roll': award,
            'coupon': c_final,
            'target_coupon': final,
            'target_times': daily,
            }
        mo.set_param('target', target)
        return mo


    def random_reward(self, rw_list):
        ran = int(random.random() * 10000)
        count = 10000
        for index, item in enumerate(rw_list):
            count -= int(rw_list[index][1])
            if ran >= count:
                return rw_list[index][0]
        return None

Target = Target()