#!/usr/bin/env python
# -*- coding=utf-8 -*-



import time
from time import strftime
import json
import random
import datetime
import sys
from const import Message
from framework.entity.msgpack import MsgPack
from framework.context import Context
from framework.util.tool import Time
from sdk.modules.mobile import Mobile
from props import BirdProps
from account import BirdAccount


if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf8')

class Red_Packet(object):
    general_list = []
    special_list = []

    @classmethod
    def set_general_list(cls):
        cls.general_list = []

    @classmethod
    def set_special_list(cls):
        cls.special_list = []

    @classmethod
    def add_general_list(cls, arr, info):
        arr.append(info)
        arr = sorted(arr, key=lambda e: e.__getitem__('times'), reverse=True)
        if len(arr) == 7:
            arr.pop(len(cls.general_list) - 1)
        return arr

    @classmethod
    def add_special_list(cls, arr, info):
        arr.append(info)
        arr = sorted(arr, key=lambda e: e.__getitem__('packet'), reverse=True)
        if len(arr) == 7:
            arr.pop(len(arr) - 1)
        return arr

    def red_packet(self, uid, mi): #普通红包
        conf = Context.Configure.get_game_item_json(2, 'red_packet.config')
        min_cost = conf['min_cost']
        recharge = mi.get_param('reg')
        if 'chip' in recharge:
            #if min_cost <= recharge['chip']:
                send_gold = recharge['chip'] * conf['percentage'] / 100

                now = Time.current_ts()
                Red_Packet.set_general_list()
                Context.Data.set_red_packet_attr(uid, 'red_packet:general', now, 'send_id', uid)

                mo = MsgPack(Message.BIRD_MSG_RED_ENVELOPE | Message.ID_ACK)

                random_packet = 5
                # random_packet = send_gold / conf['average_chip_count']  # 红包个数
                # random_packet = random.randint(random_packet / 2, int(random_packet * 1.5))

                Context.Data.set_red_packet_attrs(uid, 'red_packet:general', now, ['packet_sum', 'send_gold', 'get_money', 'surplus'], [random_packet, send_gold, 0, random_packet])
                mins = 1
                red_packet_list, surplus_list = Context.randBonus(mins, send_gold, random_packet)
                if not red_packet_list and not surplus_list:
                    Context.Log.debug('充值红包生成异常！')
                    red_packet_list, surplus_list = Context.randBonus(mins, send_gold, random_packet)
                    Context.Data.set_red_packet_attrs(uid, 'red_packet:general', now, ['packet_list', 'surplus_list'],
                                                  [red_packet_list, surplus_list])
                else:
                    Context.Data.set_red_packet_attrs(uid, 'red_packet:general', now, ['packet_list', 'surplus_list'],
                                                  [red_packet_list, surplus_list])
                nick = Context.Data.get_attr(uid, 'nick')
                user_vip = BirdAccount.get_vip_level(uid, 2)
                red_packet = {
                    'times_tamp': now,  # 时间戳
                    'packet_sum': random_packet,  # 红包个数
                    'send_gold': send_gold,  # 发的金币
                    'packet_type': 'general',  # 普通红包
                    'get_money': 0,  # 领取红包个数
                    'surplus': random_packet,  # 剩余
                    'nick': nick,
                    'vip': user_vip,
                }
                mo.set_param('red_packet', red_packet)
                return True, mo
        return False, 0

    def open_general_envelope(self, uid, player, mi): #打开普通红包
        mo = MsgPack(Message.BIRD_MSG_RANDOM_RED_ENVELOPE | Message.ID_ACK)
        info_dict = {}
        now = mi.get_param('times_tamp')
        nick = mi.get_param('mynick')
        packet_type = mi.get_param('packet_type')
        user_vip = BirdAccount.get_vip_level(uid, 2)
        if user_vip < 1:
            vip = 1
        else:
            vipConfig = Context.Configure.get_game_item_json(2, 'vip.config')
            vip_level = vipConfig[user_vip - 1].get('red_packets_general')
            vip = vip_level
        money, packet_sum, red_packet, surplus= Context.Data.get_red_packet_attrs(uid, 'red_packet:{}'.format(packet_type), now, ['get_money', 'packet_sum', 'packet_list', 'surplus_list'])
        index = int(money)
        number = int(packet_sum)
        if index >= number:
            return mo.set_error(1, '红包数量已发完')
        red_packet_list = Context.json_loads(red_packet)
        surplus_list = Context.json_loads(surplus)
        packet = red_packet_list[index]
        surplus = surplus_list[index]
        specials = Context.Daily.get_daily_data(uid, 2, 'red_packets_{}'.format(packet_type))
        if not specials:
            numbers = 1
            Context.Daily.set_daily_data(uid, 2, 'red_packets_{}'.format(packet_type), numbers)
        else:
            if int(specials) >= vip:
                return mo.set_error(2, '今日的抢红包次数已用完，升级VIP可提高每日可抢红包次数')
            else:
                numbers = 1
                Context.Daily.mincr_daily_data(uid, 2, 'red_packets_{}'.format(packet_type), numbers)

        date_now = strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        info_dict = {'uid': uid, 'nick': nick, 'packet': packet, 'times': date_now}
        users = Context.Data.get_red_packet_attr(uid, 'red_packet:{}'.format(packet_type), now, uid, 0)
        if users:
            return mo.set_error(3, '红包已经领取')

        sorted_list = Context.Data.get_red_packet_attr(uid, 'red_packet:{}'.format(packet_type), now, 'rank_money', 0)
        if sorted_list != 0:
            sorted_list = Context.json_loads(sorted_list)
        else:
            sorted_list = []
        sorted_list = self.add_general_list(sorted_list, info_dict)
        index = index + 1
        sort_info = sorted(sorted_list, key=lambda x: x['packet'], reverse=True)
        sorted_lists =Context.json_dumps(sort_info)

        info_dicts = Context.json_dumps(info_dict)
        Context.Data.set_red_packet_attrs(uid, 'red_packet:{}'.format(packet_type), now, ['rank_money', 'get_money', 'surplus', uid],[sorted_lists, index, surplus, info_dicts])
        reward = {'chip': packet}
        final = BirdProps.issue_rewards(uid, 2, reward, 'red_packet.reward', True)
        mo.set_param('packet_type', packet_type)
        mo.set_param('packet', packet)
        mo.set_param('chip', final)
        return mo

    def general_envelope_record(self, uid, player, mi): #普通红包记录
        mo = MsgPack(Message.BIRD_MSG_RED_ENVELOPE_RECORD | Message.ID_ACK)
        now = mi.get_param('times_tamp')
        packet_type = mi.get_param('packet_type')
        sorted_list = Context.Data.get_red_packet_attr(uid, 'red_packet:{}'.format(packet_type), now, 'rank_money',0)
        sorted_list = Context.json_loads(sorted_list)
        info = []
        for k in sorted_list:
            info.append(k)
        mo.set_param('get_record', info)
        return mo


    def special_red_packet(self, gid):
        ret = Context.RedisCluster.hget_keys('red_packet:special_timer:*')
        if not ret:
            return
        now = Time.current_ts()
        for item in ret:
            stamp = item.split(':')[2]
            start_today, end_today, start_hours, end_hours, interval_ts,stop_state = Context.Data.get_red_packet_attrs(100,'red_packet:special_timer',stamp, ['start_today','end_today','start_hours','end_hours','interval_time','stop_state'])
            today_start = int(start_today) + int(start_hours)
            today_end = int(end_today) + int(end_hours)
            if now >= today_start and now <=today_end and int(stop_state) != 2:
                ts = (now - today_start)%int(interval_ts)
                if ts <= 3:
                    self.special_packets(uid=1000001, now=stamp)
            else:
                continue

    def special_packet_timer(self, today_times): #特殊红包公告
        led = u'红包活动{}开始'.format(today_times)
        mo = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
        mo.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': 2})
        Context.GData.broadcast_to_system(mo)


    def bulletin_info(self): # 1大厅 2 战斗显示 3 大厅和战斗显示
        today = int(''.join(str(datetime.date.today()).split('-')))
        bul_info = Context.RedisCache.hash_getall('game.led.%d' % today)
        for k, v in bul_info.items():
            v = Context.json_loads(v)
            bull = {}
            if v['cycle'] > 0:
                interval_red_list = []
                today_start = v['start_hour']
                i = 0
                while i < v['cycle']:
                    interval_red_list.append(Time.timestamp_to_datetime(today_start))
                    today_start = today_start + int(v['interval'])
                    i = i + 1
                for start_hours in interval_red_list:
                    now_ts = Time.datetime()
                    if now_ts.year == start_hours.year and now_ts.month == start_hours.month and now_ts.day == start_hours.day:
                        if now_ts.hour == start_hours.hour and now_ts.minute == start_hours.minute:
                            bull['bulletin'] = v['bulletin']
                            bull['msg'] = v['msg']
                            bull['ts'] = Time.datetime_to_timestamp(start_hours)
                            mo = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
                            mo.set_param('game', bull)
                            Context.GData.broadcast_to_system(mo)
            else:
                now_ts = Time.datetime()
                start_hours = Time.timestamp_to_datetime(v['start_hour'])
                if now_ts.year == start_hours.year and now_ts.month == start_hours.month and now_ts.day == start_hours.day:
                    if now_ts.hour == start_hours.hour and now_ts.minute == start_hours.minute:
                        bull['bulletin'] = v['bulletin']
                        bull['msg'] = v['msg']
                        bull['ts'] = Time.datetime_to_timestamp(start_hours)
                        mo = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
                        mo.set_param('game', bull)
                        Context.GData.broadcast_to_system(mo)


    def special_packets(self, uid,now,red_type=None): #特殊红包
        mo = MsgPack(Message.MSG_SYS_SPECIAL_RED_ENVELOPE | Message.ID_NTF)
        Red_Packet.set_special_list()
        mins = 1
        # maxs = send_gold / random_packet
        packet_type = "special"
        if red_type:
            number, total_price = Context.Data.get_red_packet_attrs(100, 'red_packet:special', now,
                                                                    ['packet_sum', 'send_gold'])
            random_packet = int(number)
            send_gold = int(total_price)

            red_packet_list, surplus_list = Context.randBonus(mins, send_gold, random_packet)
            if not red_packet_list and not surplus_list:#普通全服红包
                red_packet_list, surplus_list = Context.randBonus(mins, send_gold, random_packet)
                Context.Data.set_red_packet_attrs(uid, 'red_packet:{}'.format(packet_type), now,['packet_list', 'surplus_list'],[red_packet_list, surplus_list])
            else:
                Context.Data.set_red_packet_attrs(uid, 'red_packet:{}'.format(packet_type), now, ['packet_list', 'surplus_list'],[red_packet_list, surplus_list])
            new_now = now

        else:
            number, total_price,send_packet_list = Context.Data.get_red_packet_attrs(100, 'red_packet:special_timer', now,['packet_sum', 'send_gold','send_packet_list'])
            packet_list = Context.json_loads(send_packet_list)
            random_packet = int(number)
            send_gold = int(total_price)
            timer_now = Time.current_ts()
            Context.Data.set_red_packet_dict(100, 'red_packet:{}'.format(packet_type), timer_now,{'red_packet_type': 1, 'packet_sum': random_packet, 'send_gold': send_gold,
                                              'get_money': 0, 'surplus': send_gold,"receive_packet_id":now})
            packet_list.append(timer_now)
            Context.Data.set_red_packet_dict(100, 'red_packet:special_timer', now, {"send_packet_list":packet_list})

            red_packet_list, surplus_list = Context.randBonus(mins, send_gold, random_packet)
            if not red_packet_list and not surplus_list:#定时全服红包
                red_packet_list, surplus_list = Context.randBonus(mins, send_gold, random_packet)
                Context.Data.set_red_packet_attrs(uid, 'red_packet:{}'.format(packet_type), timer_now,['packet_list', 'surplus_list'],[red_packet_list, surplus_list])
            else:
                Context.Data.set_red_packet_attrs(uid, 'red_packet:{}'.format(packet_type), timer_now, ['packet_list', 'surplus_list'],[red_packet_list, surplus_list])
            new_now = timer_now

        red_packet = {
            'times_tamp': new_now,  # 时间戳
            'packet_sum': random_packet,  # 红包个数
            'send_gold': send_gold,  # 发的金币
            'packet_type': packet_type,  # 全服红包类型
            'get_money': 0,  # 领取红包个数
            'surplus': random_packet,  # 剩余
            'nick': u'红包活动',
        }

        mo.set_param('red_packet', red_packet)
        Context.GData.broadcast_to_system(mo)
        return


    def open_special_envelope(self, uid, mi): #打开特殊红包
        mo = MsgPack(Message.MSG_SYS_OPEN_SPECIAL_ENVELOPE | Message.ID_ACK)
        info_dict = {}
        now = mi.get_param('times_tamp')
        nick = mi.get_param('mynick')
        packet_type = mi.get_param('packet_type')
        money, packet_sum, red_packet, surplus_list,surplus = Context.Data.get_red_packet_attrs(uid, 'red_packet:{}'.format(packet_type), now, ['get_money', 'packet_sum', 'packet_list', 'surplus_list','surplus'])
        index = int(money)
        number = int(packet_sum)
        if index >= number:
            return mo.set_error(1, '红包数量已发完')
        red_packet_list = Context.json_loads(red_packet)
        # surplus_list = Context.json_loads(surplus_list)
        packet = red_packet_list[index]
        surplus = int(surplus) - packet
        # today = str(''.join(str(datetime.date.today()).split('-')))
        #get_time = Context.Data.get_red_packet_attr(uid, 'red_packet:{}_conf'.format(packet_type), today, 'get_time')
        #vip = int(get_time)
        user_vip = BirdAccount.get_vip_level(uid, 2)
        if user_vip < 1:
            vip = 1
        else:
            vipConfig = Context.Configure.get_game_item_json(2, 'vip.config')
            vip_level = vipConfig[user_vip - 1].get('red_packets_general')
            vip = vip_level

        specials = Context.Daily.get_daily_data(uid, 2, 'red_packets_{}'.format(packet_type))
        if not specials:
            number = 1
            Context.Daily.set_daily_data(uid, 2, 'red_packets_{}'.format(packet_type), number)
        else:
            if int(specials) >= vip:
                return mo.set_error(2, '今日的抢红包次数已用完，升级VIP可提高每日可抢红包次数')
            else:
                number = 1
                Context.Daily.mincr_daily_data(uid, 2, 'red_packets_{}'.format(packet_type), number)
        date_now = strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        info_dict = {'uid': uid, 'nick': nick, 'packet': packet, 'times': date_now}
        users = Context.Data.get_red_packet_attr(uid, 'red_packet:{}'.format(packet_type), now, uid, 0)
        if users:
            return mo.set_error(3, '红包已经领取')

        sorted_list = Context.Data.get_red_packet_attr(uid, 'red_packet:{}'.format(packet_type), now, 'rank_money',0)
        if sorted_list != 0:
            sorted_list = Context.json_loads(sorted_list)
        else:
            sorted_list = []
        sorted_list = self.add_special_list(sorted_list, info_dict)

        index = index + 1
        sorted_lists = Context.json_dumps(sorted_list)
        info_dicts = Context.json_dumps(info_dict)
        Context.Data.set_red_packet_attrs(uid, 'red_packet:{}'.format(packet_type), now,
                                          ['rank_money', 'get_money', 'surplus', uid],
                                          [sorted_lists, index, surplus, info_dicts])

        reward = {'chip': packet}
        final = BirdProps.issue_rewards(uid, 2, reward, 'red_packet.reward', True)
        mo.set_param('packet_type', packet_type)
        mo.set_param('packet', packet)
        mo.set_param('chip', final)
        return mo


    def special_envelope_record(self, uid, mi): #特殊红包记录
        mo = MsgPack(Message.MSG_SYS_SPECIAL_ENVELOPE_RECORD | Message.ID_ACK)
        now = mi.get_param('times_tamp')
        packet_type = mi.get_param('packet_type')

        sorted_json = Context.Data.get_red_packet_attr(uid, 'red_packet:{}'.format(packet_type), now, 'rank_money',0)
        sorted_list = Context.json_loads(sorted_json)
        info = []
        for k in sorted_list:
            info.append(k)
        mo.set_param('get_record', info)
        return mo

Red_Packet = Red_Packet()