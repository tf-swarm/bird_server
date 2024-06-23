#!/usr/bin/env python
# -*- coding=utf-8 -*-

import random
from const import Message
from props import BirdProps
from account import BirdAccount
from framework.util.tool import Time, Tool
from framework.context import Context
from framework.entity.msgpack import MsgPack

class Const(object):
    MESSAGE_INFO = 0
    MESSAGE_START_GAME = 1
    MESSAGE_ROLL_THE_DICE = 2
    MESSAGE_END_GAME = 3

    EVENT_EMPTY = 0         #空事件
    EVENT_DICE_TWO = 1      #筛子*2
    EVENT_DICE_THREE = 2    #筛子*3
    EVENT_REWARD_TWO = 3    #奖励*2
    EVENT_NO_TICKET = 4     #免票


class RichMan(object):
    def __init__(self):
        self.game_name = 'rich_man'

    def get_config(self):
        cnf = Context.Configure.get_game_item_json(2, 'RichMan.config')
        return cnf

    def on_message(self, uid, gid, mi):
        total_cnf = self.get_config()

        mid = mi.get_param('mid')
        if mid == Const.MESSAGE_INFO:
            mo = MsgPack(Message.MSG_SYS_RICH_MAN | Message.ID_ACK)
            mo.set_param('mid', mid)
            mo.set_param('p', total_cnf.get(str(1)).get('ticket'))
            mo.set_param('m', total_cnf.get(str(2)).get('ticket'))
            mo.set_param('h', total_cnf.get(str(3)).get('ticket'))
            return mo

        level = mi.get_param('level', 1)
        cnf = total_cnf.get(str(level))
        if mid == Const.MESSAGE_START_GAME:
            mo = self.start_game(uid, gid, mid, level, cnf)
        elif mid == Const.MESSAGE_ROLL_THE_DICE:
            mo = self.roll_dice(uid, gid, mid, mi, cnf, level)
        elif mid == Const.MESSAGE_END_GAME:
            mo = self.end_game(uid, mid, cnf, level)
        else:
            mo = MsgPack(Message.MSG_SYS_RICH_MAN | Message.ID_ACK)
            return mo.set_error(0, 'no mid')
        return mo

    # 开始游戏
    def start_game(self, uid, gid, mid, level, cnf):
        mo = MsgPack(Message.MSG_SYS_RICH_MAN | Message.ID_ACK)
        status = Context.RedisCache.hash_get_int('smart_game:%d' % uid, 'status', 0)
        if status > 0:
            return mo.set_error(0, u"你正在进行第三方小游戏，无法开启大富翁")

        if cnf == None:
            return mo.set_error(1, u"配置出错")
        conf_dat = Context.RedisMix.hash_get_json('game.%d.background' % gid, 'rich_man.config', {})
        vip_level = BirdAccount.get_vip_level(uid, gid)
        if conf_dat:
            if conf_dat.get('open', 1) == 0:
                mo.set_error(4, u'活动已被关闭')
                Context.GData.send_to_connect(uid, mo)
                return
            if conf_dat.has_key('vip_limit'):
                vip_limit = conf_dat.get('vip_limit')
                if vip_level < vip_limit:
                    return mo.set_error(3, u"vip等级不足，无法开启游戏")
        else:
            vip_limit = cnf.get('vip_limit')
            if vip_level < vip_limit:
                return mo.set_error(3, u"vip等级不足，无法开启游戏")
        player_data = self.init_player_data(uid, cnf, level)
        level = player_data.get('level')
        total_cnf = self.get_config()
        cnf = total_cnf.get(str(level))

        mo.set_param('mid', mid)
        mo.set_param('level', level)
        mo.set_param('ticket', cnf.get('ticket', 100))
        mo.update_param(player_data)
        spacial_chip = cnf.get('spacial_reward').get('9').get('chip')
        spacial_coupon = cnf.get('spacial_reward').get('10').get('coupon')
        mo.set_param('sr', {'chip': spacial_chip, 'coupon': spacial_coupon})
        return mo

    # 完成游戏
    def end_game(self, uid, mid, cnf, level, end = False):
        pool = self.get_pool(level)
        keys = 'game:%s:%d' % (self.game_name, uid)
        mo = MsgPack(Message.MSG_SYS_RICH_MAN | Message.ID_ACK)
        mo.set_param('mid', mid)
        ticket = cnf.get('ticket')
        end_reward = {}
        if end == True:
            win_rate = self.get_win_rate(pool, cnf)
            P = random.random()
            if P < win_rate:
                interval = cnf.get('end_win')
            else:
                interval = cnf.get('end_lose')

            multiple = random.uniform(interval[0], interval[1])
            coupon = int(multiple * ticket / 10)
            end_reward['coupon'] = coupon

            nick = Context.Data.get_attr(uid, 'nick')
            nick = Context.hide_name(nick)
            led = u'赚翻了！玩家<color=#00FF00FF>%s</color>在<color=#FF0000FF>小游戏-大富翁</color>中获得<color=#FFFF00FF>%d</color>鸟券' % (
                nick, coupon)
            mou = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
            mou.set_param('game', {'msg': led, 'ts': Time.current_ts() + 3, 'bulletin': 3})
            Context.GData.broadcast_to_system(mou)

        mo.set_param('end_reward', end_reward)
        m_reward = Context.RedisActivity.hash_get_json(keys, 'reward')
        if not m_reward:
            return mo.set_param('final', {})

        if end_reward:
            m_reward = BirdProps.merge_reward(False, m_reward, end_reward)
            Context.RedisActivity.hash_set(keys, 'reward', Context.json_dumps(m_reward))
        rw = BirdProps.deal_none_reward(m_reward)

        dat = Context.RedisActivity.hash_getall(keys)
        dat_keys = "rich_man:%s:%d"%(Time.current_time('%Y-%m-%d') ,uid)
        Context.RedisStat.hash_set(dat_keys, Time.current_ms(), Context.json_dumps(dat))
        Context.RedisActivity.delete(keys)

        if len(rw) <= 0:
            return mo.set_param('final', {})

        final = BirdProps.issue_rewards(uid, 2, rw, 'rich.man.reward')

        mo.set_param('final', final)
        Context.GData.send_to_connect(uid, mo)
        channel_id = Context.Data.get_attr(uid, 'channelid')
        Context.Stat.incr_daily_data(channel_id, 'server_rich_man_play_times')
        nick = Context.Data.get_attr(uid, 'nick')
        nick = Context.hide_name(nick)
        desc_str = self.get_reward_str(rw)
        led = u'羡慕死了！玩家<color=#00FF00FF>%s</color>在<color=#FF0000FF>小游戏-大富翁</color>中获得<color=#FFFF00FF>%s</color>' % (
            nick, desc_str)
        mou = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
        mou.set_param('game', {'msg': led, 'ts': Time.current_ts() + 3, 'bulletin': 3})
        Context.GData.broadcast_to_system(mou)
        return

    # 色子roll点
    def roll_dice(self, uid, gid, mid, mi, cnf, level):
        event = self.pop_event(uid)
        keys = 'game:%s:%d' % (self.game_name, uid)
        ticket = cnf.get('ticket')
        mo = MsgPack(Message.MSG_SYS_RICH_MAN | Message.ID_ACK)
        if event != Const.EVENT_NO_TICKET:
            real, final = Context.UserAttr.incr_diamond(uid, gid, -ticket, 'rich.man.consume')
            if real != -ticket:
                return mo.set_error(4, u'钻石不足，无法购买')
            from newtask import NewTask
            NewTask.get_diamond_consume_task(uid, ticket)
            diamond_price = BirdProps.get_props_price({'diamond': ticket})
            pool = self.incr_pool(level, diamond_price)
            Context.RedisActivity.hash_incrby(keys, 'consume', ticket)
            mo.set_param('final', final)
        else:
            pool = self.get_pool(level)

        mo.set_param('mid', mid)
        mo.set_param('use_event', event)

        floor_count = Context.RedisActivity.hash_incrby(keys, 'floor_count', 1)
        mo.set_param('floor_count', floor_count)

        shake_num = random.randint(1, 6)
        if event == Const.EVENT_DICE_TWO:
            shake_num = shake_num*2
        if event == Const.EVENT_DICE_THREE:
            shake_num = shake_num*3
        mo.set_param('sn', shake_num)

        flag, floor_num, get_event, add_reward, reward = self.deal_reward(uid, event, cnf, shake_num, ticket, pool, level)
        if not flag:
            return

        mo.set_param('ft', floor_num)
        mo.set_param('get_event', get_event)
        mo.set_param('add_reward', add_reward)
        mo.set_param('t_reward', reward)
        return mo

    # 获取奖励玩家的奖励
    def deal_reward(self, uid, use_event, cnf, shake_num, ticket, pool, level):
        keys = 'game:%s:%d' % (self.game_name, uid)
        floor = Context.RedisActivity.hash_incrby(keys, 'floor', shake_num)
        map_list, reward = Context.RedisActivity.hash_mget(keys, 'map_list', 'reward')
        if not map_list:
            return False, 0, 0, None, None

        map_list = Context.json_loads(map_list)
        if floor >= len(map_list)-1:
            self.end_game(uid, 3, cnf, level, True)
            return False, 0, 0, None, None

        reward = Context.json_loads(reward)
        floor_num = Tool.to_int(map_list[floor], 0)
        get_event = 0
        add_reward = {}

        win_rate = self.get_win_rate(pool, cnf)
        P = random.random()
        if P < win_rate:
            interval = cnf.get('win')
        else:
            interval = cnf.get('lose')
        if floor_num == 1: # 鸟蛋
            multiple = random.uniform(interval[0], interval[1])
            chips = int(multiple * ticket * 500)
            if use_event == Const.EVENT_REWARD_TWO:
                chips *= 3
            add_reward['chip'] = chips
        elif floor_num == 2: # 鸟券
            multiple = random.uniform(interval[0], interval[1])
            coupon = int(multiple * ticket /10)
            if coupon < 1:
                coupon = 1
            if use_event == Const.EVENT_REWARD_TWO:
                coupon *= 3
            add_reward['coupon'] = coupon
        elif floor_num == 3: # 道具
            sp_rw = cnf.get('spacial_reward').get(str(floor_num))

            if interval[0] < 1.0:
                props = sp_rw.get('rw1').get('props')[0]
            else:
                props = sp_rw.get('rw2').get('props')[0]
            props_id = props.get('id')
            count = props.get('count')

            if use_event == Const.EVENT_REWARD_TWO:
                count *= 3
            add_reward['props'] = [{'id':props_id, 'count':count}]
        elif floor_num == 4: # 色子2倍
            get_event = Const.EVENT_DICE_TWO
            self.set_event(uid, get_event)
        elif floor_num == 5: # 色子3倍
            get_event = Const.EVENT_DICE_THREE
            self.set_event(uid, get_event)
        elif floor_num == 6: # 奖励两倍
            get_event = Const.EVENT_REWARD_TWO
            self.set_event(uid, get_event)
        elif floor_num == 7: # 门票免费
            get_event = Const.EVENT_NO_TICKET
            self.set_event(uid, get_event)
        elif floor_num == 9: # 固定鸟蛋
            chips = cnf.get('spacial_reward').get(str(floor_num)).get('chip')
            if use_event == Const.EVENT_REWARD_TWO:
                chips *= 3
            add_reward['chip'] = chips
        elif floor_num == 10: # 固定鸟券
            coupon = cnf.get('spacial_reward').get(str(floor_num)).get('coupon')
            if coupon < 1:
                coupon = 1
            if use_event == Const.EVENT_REWARD_TWO:
                coupon *= 3
            add_reward['coupon'] = coupon
        elif floor_num == 11: # 固定稀有道具
            props = Context.copy_obj(cnf.get('spacial_reward').get(str(floor_num)))
            if use_event == Const.EVENT_REWARD_TWO:
                count = props.get('props')[0].get('count')
                count *= 3
                props['props']['count'] = count
            add_reward = props
        if add_reward:
            reward_price = BirdProps.get_props_price(add_reward)
            self.incr_pool(level, -reward_price)
            reward = BirdProps.merge_reward(reward, add_reward)
            Context.RedisActivity.hash_set(keys, 'reward', Context.json_dumps(reward))

        return True, floor_num, get_event, add_reward, reward


    #获取池子的值
    def get_pool(self, level):
        primary_key = 'game.2.RichMan_pool'
        pool = Context.RedisMix.hash_get_int(primary_key, 'RichMan_pool_%d'%level, 0)
        return pool

    # 改变池子的值
    def incr_pool(self, level, diamond_price):
        primary_key = 'game.2.RichMan_pool'
        pool = Context.RedisMix.hash_incrby(primary_key, 'RichMan_pool_%d'%level, diamond_price)
        return pool

    # 取出上次色子获得的事件
    def pop_event(self, uid):
        keys = 'game:%s:%d' % (self.game_name, uid)
        event = Context.RedisActivity.hash_get_int(keys,'event', 0)
        if event != Const.EVENT_EMPTY:
            Context.RedisActivity.hash_set(keys, 'event', Const.EVENT_EMPTY)
        return event

    # 获取事件放入数据中
    def set_event(self, uid, event):
        keys = 'game:%s:%d' % (self.game_name, uid)
        Context.RedisActivity.hash_set(keys, 'event', event)
        return

    ## 新建地图
    def make_map(self, cnf):
        try:
            map_data = cnf.get('map')
            maps = []
            map_list = []
            event_list = []
            for k, v in map_data.items():
                num = random.randint(v[0], v[1])
                lst = num * [int(k)]
                if int(k) <= 3:
                    map_list.extend(lst)
                else:
                    event_list.extend(lst)

            chip_num = 98 - len(map_list) - len(event_list)
            chip_list = [1] * chip_num
            map_list.extend(chip_list)

            random.shuffle(map_list)
            random.shuffle(event_list)

            maps.extend(map_list[:10])
            map_list = map_list[10:]

            event_index_dict = []
            index_list = range(0, 82)

            for i in event_list:
                index = random.choice(index_list)
                index_list.remove(index)
                if index + 1 in index_list:
                    index_list.remove(index + 1)
                if index - 1 in index_list:
                    index_list.remove(index - 1)
                event_index_dict.append([i, index])

            d_list = sorted(event_index_dict, key=lambda x: int(x[1]), reverse=False)
            for i in d_list:
                map_list.insert(int(i[1]), int(i[0]))
            maps.extend(map_list)
            maps.insert(0, 0)
            maps.insert(len(maps), 0)
        except:
            return self.make_map(cnf)
        return maps

    # 进入大富翁初始化地图和玩家的数据
    def init_player_data(self, uid, cnf, level):
        ts = Time.current_ts()
        sp_rw = cnf.get('spacial_reward').get(str(3))
        props_rw1 = sp_rw.get('rw1').get('props')[0].get('id')
        props_rw2 = sp_rw.get('rw2').get('props')[0].get('id')
        reward = {
            'chip': 0,
            'coupon': 0,
            'props': [{'id': props_rw1, 'count': 0}, {'id': props_rw2, 'count': 0}]
        }
        dic = Context.RedisActivity.hash_getall('game:%s:%d' % (self.game_name, uid))
        if dic and dic.has_key('map_list'):
            player_data = {
                'map': Context.json_loads(dic.get('map_list')),
                'floor': dic.get('floor', 0),
                'eve': dic.get('event', Const.EVENT_EMPTY),
                'reward': Context.json_loads(dic.get('reward', '{}')),
                'start_ts': dic.get('start_ts',ts),
                'consume': dic.get('consume',0),
                'floor_count': dic.get('floor_count',0),
                'level': dic.get('level', 3),
            }
        else:
            map_list = self.make_map(cnf)
            Context.RedisActivity.hash_mset('game:%s:%d'%(self.game_name, uid),
                                         'map_list', Context.json_dumps(map_list),
                                         'floor', 0,
                                         'event', Const.EVENT_EMPTY,
                                         'reward', Context.json_dumps(reward),
                                         'start_ts', ts,
                                         'consume', 0,
                                         'floor_count', 0,
                                         'level', level)

            player_data = {
                'map':map_list,
                'floor': 0,
                'eve': Const.EVENT_EMPTY,
                'reward': reward,
                'start_ts': ts,
                'consume': 0,
                'floor_count': 0,
                'level':level
            }
        return player_data

    #获取赢率
    def get_win_rate(self, pool , cnf):
        average_line = cnf.get('average_line')
        range_line = cnf.get('range_line')
        average_rate = cnf.get('average_rate')
        range_rate = cnf.get('range_rate')

        win_rate = average_rate + range_rate * int((pool - average_line)/(range_line))
        if win_rate <= 0:
            win_rate = 0
        if win_rate >= 1:
            win_rate = 1
        return win_rate

    #获取奖励描述
    def get_reward_str(self, reward):
        desc = []
        keys = ['chip', 'diamond', 'coupon']
        names = [u'鸟蛋', u'钻石', u'鸟券']
        for key, name in zip(keys, names):
            if key in reward:
                desc.append(u'%d%s' % (reward[key], name))

        prop = reward.get('props')
        if prop:
            for one in prop:
                _ = BirdProps.get_props_desc(one['id']) + u'%d个' % one['count']
                desc.append(_)
        return u', '.join(desc)

Const = Const()
RichMan = RichMan()