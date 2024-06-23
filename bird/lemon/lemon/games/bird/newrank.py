#!/usr/bin/env python
# -*- coding=utf-8 -*-



import time
import datetime
from const import Message
from framework.entity.msgpack import MsgPack
from framework.context import Context
from framework.util.tool import Time, Tool
from props import BirdProps
from account import BirdAccount
from mail import Mail

table_dict = {
    1:1001,
    2:1002,
    3:1003,
    4:1004,
}

date_dict = {
    1:'pay.rank.reward',
    2:'primary.rank.reward',
    3:'middle.rank.reward',
    4:'high.rank.reward',
}

class NewRank(object):
    def __init__(self):
        self.pay_rank_list = None
        self.primary_rank_list = None
        self.middle_rank_list = None
        self.high_rank_list = None

    def deal_pay_rank(self, gid, nType):
        ret_list = self.set_rank_list(gid, nType)
        refresh_time = Context.Data.get_rank_attr(table_dict[nType], gid, 'refresh_time')
        if not refresh_time:
            Context.Data.set_rank_attr(table_dict[nType], gid, 'refresh_time', time.time())
        now_ts = Time.datetime()
        if now_ts.minute == 0 and now_ts.hour == 0  or self.judge_refresh(1, refresh_time):
            if (ret_list != None and len(ret_list) > 0):
                # 发放奖励
                conf = Context.Configure.get_game_item_json(gid, date_dict[nType])
                for k, v in enumerate(ret_list):
                    level = -1
                    for i, j in enumerate(conf['level']):
                        if k + 1 in j:
                            level = i
                    if level < 0:
                        continue
                    reward = conf['reward'][level]
                    times = time.time()
                    ret = Mail.add_mail(int(v[0]), gid, times, nType+2, reward, -(k + 1))
                    if ret:
                        Mail.send_mail_list(int(v[0]), gid)
                ret = Context.Data.get_rank_all(table_dict[nType], gid)
                for i in ret.keys():
                    Context.Data.del_rank_attrs(table_dict[nType], gid, i)
                if len(ret) > 1:
                    file_name = 'pay_rank'
                    Context.save_cache(file_name, str(Time.current_ts()), ret)
                self.set_rank_list(gid, nType)
            Context.Data.set_rank_attr(table_dict[nType], gid, 'refresh_time', time.time())
        return

    def deal_fight_rank(self, gid, nType):
        ret_list = self.set_rank_list(gid, nType)
        refresh_time = Context.Data.get_rank_attr(table_dict[nType], gid, 'refresh_time')
        if not refresh_time:
            Context.Data.set_rank_attr(table_dict[nType], gid, 'refresh_time', time.time())
        now_ts = Time.datetime()
        if (now_ts.minute == 0 and now_ts.hour == 0 and datetime.datetime.now().weekday() == 5) or self.judge_refresh(2, refresh_time):
            if ret_list != None and len(ret_list) > 0:
                # 发放奖励
                conf = Context.Configure.get_game_item_json(gid, date_dict[nType])
                first_id = None
                for k, v in enumerate(ret_list):
                    level = -1
                    for i, j in enumerate(conf['level']):
                        if k + 1 in j:
                            level = i
                    if level < 0:
                        continue
                    reward = conf['reward'][level]
                    times = time.time()
                    ret = Mail.add_mail(int(v[0]), gid, times, nType+2, reward, -(k + 1))
                    if ret:
                        first_id = int(v[0])
                        Mail.send_mail_list(int(v[0]), gid)
                if table_dict[nType] == 1002:
                    file_name = 'primary_rank'
                    if first_id:
                        bulletin = 3
                        nick = Context.Data.get_attr(first_id, 'nick')
                        nick = Context.hide_name(nick)
                        led = u'恭喜<color=#00FF00FF>%s</color>获得了新手海岛排行榜第一名，赢得了无与伦比的丰厚奖励！' % (nick)
                        mo = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
                        mo.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
                        Context.GData.broadcast_to_system(mo)
                elif table_dict[nType] == 1003:
                    file_name = 'middle_rank'
                    if first_id:
                        bulletin = 3
                        nick = Context.Data.get_attr(first_id, 'nick')
                        nick = Context.hide_name(nick)
                        led = u'恭喜<color=#00FF00FF>%s</color>获得了林海雪原排行榜第一名，赢得了无与伦比的丰厚奖励！' % (nick)
                        mo = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
                        mo.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
                elif table_dict[nType] == 1004:
                    file_name = 'high_rank'
                    if first_id:
                        bulletin = 3
                        nick = Context.Data.get_attr(first_id, 'nick')
                        nick = Context.hide_name(nick)
                        led = u'恭喜<color=#00FF00FF>%s</color>获得了猎龙峡谷排行榜第一名，赢得了无与伦比的丰厚奖励！' % (nick)
                        mo = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
                        mo.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
                else:
                    file_name = 'rank'
                ret = Context.Data.get_rank_all(table_dict[nType], gid)
                for i in ret.keys():
                    Context.Data.del_rank_attrs(table_dict[nType], gid, i)
                if len(ret) > 1:
                    Context.save_cache(file_name, str(Time.current_ts()), ret)
                self.set_rank_list(gid, nType)
            Context.Data.set_rank_attr(table_dict[nType], gid, 'refresh_time', time.time())
        return

    #防止服务器更新时排行榜的刷新
    def judge_refresh(self, type, times): #type = 1 日刷新，2 周五刷新
        if times == None:
            return False
        if type == 1:
            today = Time.today_start_ts()
            if today > float(times):
                return True
        elif type == 2:
            tm = time.localtime(int(time.time()))
            ts = Time.current_ts()
            if (tm.tm_wday / 5) > 0:
                week = ts - (tm.tm_wday - 5) * 86400 - tm.tm_hour * 3600 - tm.tm_min * 60 - tm.tm_sec
            else:
                week = ts - (tm.tm_wday + 2) * 86400 - tm.tm_hour * 3600 - tm.tm_min * 60 - tm.tm_sec #周六
            if week > float(times):
                return True
        return False


    #设置排行榜数据
    def set_rank_list(self, gid, type):
        lst = Context.Data.get_rank_all(table_dict[type], gid)
        if lst.has_key('refresh_time'):
            del lst['refresh_time']
        conf = Context.Configure.get_game_item_json(gid, date_dict[type])
        count = Tool.to_int(conf['count'])
        if type == 1:
            limit = Tool.to_int(conf['limit'])
            for k,v in lst.items():
                if int(v) < limit:
                    del lst[k]
            self.pay_rank_list = sorted(lst.items(), key=lambda x: int(x[1]), reverse=True)
            if len(self.pay_rank_list) >= count:
                self.pay_rank_list = self.pay_rank_list[:count]
            return self.pay_rank_list
        elif type == 2:
            self.primary_rank_list = sorted(lst.items(), key=lambda x: int(x[1]), reverse=True)
            if len(self.primary_rank_list) >= count:
                self.primary_rank_list = self.primary_rank_list[:count]
            return self.primary_rank_list
        elif type == 3:
            self.middle_rank_list = sorted(lst.items(), key=lambda x: int(x[1]), reverse=True)
            if len(self.middle_rank_list) >= count:
                self.middle_rank_list = self.middle_rank_list[:count]
            return self.middle_rank_list
        elif type == 4:
            self.high_rank_list = sorted(lst.items(), key=lambda x: int(x[1]), reverse=True)
            if len(self.high_rank_list) >= count:
                self.high_rank_list = self.high_rank_list[:count]
            return self.high_rank_list

    #处理世界boss的排行榜
    def deal_rank(self, gid):
        Week = datetime.datetime.now().weekday()
        if Week not in [5, 6]:
            return
        now_ts = Time.datetime()
        world_boss_config = Context.Configure.get_game_item_json(gid, 'world.boss.201.config')
        life_hour = world_boss_config.get('reward_list').keys()
        if (str(now_ts.hour+1) in life_hour and now_ts.minute >= 50) or (str(now_ts.hour) in life_hour and now_ts.minute == 10):
            delta_time = Context.Data.get_rank_attr(1000, gid, 'delta_time')
            if delta_time != None:
                if str(now_ts.hour) in life_hour and now_ts.minute == 10:
                    if int(delta_time) == 0:
                        return
                    self.deal_world_boss_reward(gid)

                #删除排行榜
                if int(delta_time) == 0:
                    ret = Context.Data.get_rank_all(1000, gid)
                    for i in ret.keys():
                        Context.Data.del_rank_attrs(1000, gid, i)
                    Context.save_cache('world_boss_rank', str(Time.current_ts()), ret)
                    Context.Data.set_rank_attr(1000, gid, 'delta_time', -1)
            #初始化排行榜
            else:
                Context.Data.set_rank_attr(1000, gid, 'delta_time', -1)
        return

    #boss离场或者boss被击杀时触发
    def deal_world_boss_reward(self,gid):
        ret = Context.Data.get_rank_all(1000, gid)
        if ret.has_key('delta_time'):
            del ret['delta_time']
        conf = Context.Configure.get_game_item_json(gid, 'world_boss.reward')
        count = conf['count'] #排行榜显示的数量
        rank_ret = sorted(ret.items(), key=lambda x: int(x[1]), reverse=True)
        if len(rank_ret) >= count:
            rank_ret = rank_ret[:count]
        mo = MsgPack(Message.MSG_SYS_WBRANK_CAST | Message.ID_NTF)
        Context.GData.broadcast_to_system(mo)
        # 发放奖励
        flag = False
        blood = Context.Data.get_game_attr_int(100, gid, 'blood', 0)
        if blood <= 0:
            flag = True
        for k, v in enumerate(rank_ret):
            level = -1
            for i, j in enumerate(conf['level']):
                if k + 1 in j:
                    level = i
            if level < 0:
                continue
            reward = conf['reward'][level]
            #boss被击杀排行榜奖励翻倍
            if flag:
                reward = BirdProps.reward_doubling(reward, 2)
            times = time.time()
            ret = Mail.add_mail(int(v[0]), gid, times, 2, reward, -(k + 1))
            if ret:
                Mail.send_mail_list(int(v[0]), gid)
        Context.Data.set_rank_attr(1000, gid, 'delta_time', 0)
        return

    #发送排行榜数据
    def send_rank(self, gid, uid, mi):
        # info = []
        # mo = MsgPack(Message.MSG_SYS_RANK | Message.ID_ACK)
        # mo.set_param('rank_list', info)
        # return mo

        mo = MsgPack(Message.MSG_SYS_RANK | Message.ID_ACK)
        nType = mi.get_param('type')
        rank_list = None
        conf = Context.Configure.get_game_item_json(gid, date_dict[nType])
        point = Context.Data.get_rank_attr_int(table_dict[nType], gid, str(uid), 0)
        if nType == 1:
            rank_list = self.pay_rank_list
        elif nType == 2:
            rank_list = self.primary_rank_list
        elif nType == 3:
            rank_list = self.middle_rank_list
        elif nType == 4:
            rank_list = self.high_rank_list
        if conf == None:
            return
        mo.set_param('type', nType)
        if point != None:
            mo.set_param('my_point', point)
        if rank_list == None:
            rank_list = []
        info = []
        for k, v in enumerate(rank_list):
            try:
                nick = Context.Data.get_attr(int(v[0]), 'nick')
                if not nick:
                    nick = ''
                nick = Context.hide_name(nick)
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
                vip_level = BirdAccount.get_vip_level(int(v[0]), gid)
            except:
                vip_level = 0
            level = -1
            for i, j in enumerate(conf['level']):
                if k + 1 in j:
                    level = i
            if level < 0:
                continue
            reward = BirdProps.convert_reward(conf['reward'][level])
            rank = {
                'rank': int(k),
                'id':int(v[0]),
                'nick':nick,
                'sex':int(sex),
                'avatar':avatar,
                'vip':int(vip_level),
                'point':int(v[1]),
                'reward':reward
            }
            info.append(rank)
        mo.set_param('rank_list', info)
        return mo

    # 发送世界boss排行榜数据
    def send_world_boss_rank_list(self, uid, gid):
        mo = MsgPack(Message.MSG_SYS_WBRANK_LIST | Message.ID_ACK)
        point = Context.Data.get_rank_attr_int(1000, gid, str(uid), 0)
        conf = Context.Configure.get_game_item_json(gid, 'world_boss.reward')
        if conf == None:
            return
        count = conf['count']
        ret = Context.Data.get_rank_all(1000, gid)
        if ret.has_key('delta_time'):
            del ret['delta_time']
        rank_list = sorted(ret.items(), key=lambda x: int(x[1]), reverse=True)
        if len(rank_list) >= count:
            rank_list = rank_list[:count]

        mo.set_param('my_point', point)
        blood = Context.Data.get_game_attr_int(100, gid, 'blood', 0)
        mo.set_param('blood', blood)
        if rank_list == None:
            rank_list = []
        info = []
        for k, v in enumerate(rank_list):
            try:
                nick = Context.Data.get_attr(int(v[0]), 'nick')
                if not nick:
                    nick = ''
                nick = Context.hide_name(nick)
            except:
                nick = ''
            try:
                avatar = Context.Data.get_attr(int(v[0]), 'avatar', '2')
            except:
                avatar = '2'
            try:
                vip_level = BirdAccount.get_vip_level(int(v[0]), gid)
            except:
                vip_level = 0
            level = -1
            for i, j in enumerate(conf['level']):
                if k + 1 in j:
                    level = i
            if level < 0:
                continue

            if blood <= 0:#boss被击杀 奖励需要翻倍
                reward_info = BirdProps.reward_doubling(conf['reward'][level], 2)
            else:
                reward_info = conf['reward'][level]
            reward = BirdProps.convert_reward(reward_info)
            rank = {
                'rank': int(k),
                'id': int(v[0]),
                'nick': nick,
                'avatar': avatar,
                'vip': int(vip_level),
                'point': int(v[1]),
                'reward': reward
            }
            info.append(rank)
        mo.set_param('rank_list', info)
        return mo

    def on_rank_timer(self, gid):
        #self.deal_rank(gid)
        self.deal_pay_rank(gid, 1)
        self.deal_fight_rank(gid, 2)
        self.deal_fight_rank(gid, 3)
        self.deal_fight_rank(gid, 4)
        return

NewRank = NewRank()