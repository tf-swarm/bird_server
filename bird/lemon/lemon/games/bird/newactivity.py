#!/usr/bin/env python
# -*- coding=utf-8 -*-

import random, copy
from const import Message
import props
from framework.util.tool import Time, Tool
from framework.context import Context
from framework.entity.msgpack import MsgPack
import mail
import account
from mail import Mail
from shop import Shop
from giftactivity import *

def check_activity_in(start, end, show):
    if show:
        return True
    start_ts = Time.str_to_timestamp(start)
    end_ts = Time.str_to_timestamp(end)
    now_ts = Time.current_ts()
    if start_ts < now_ts < end_ts:
        return True
    return False

def random_reward(rw_list):
    R = int(random.random() * 10000)
    count = 10000
    l =  sorted(rw_list.keys(), reverse=False)
    for i in l:
        count -= int(rw_list[i]['rate'])
        if R >= count:
            return i, rw_list[i]['reward']
    return None, None

class Activity(object):
    def __get_into(self, conf):
        id = int(conf['id'].split('_')[0])
        model = int(conf['model'])
        name = conf['name']
        hot = int(conf['hot'])
        tips = conf.get('tips', 0)
        order = conf.get('order', 100)
        return {'id': id, 'model': model, 'name': name, 'hot': hot, 'tips': tips, 'order': order}

    def get_activity_list(self, uid):
        info = []
        mo = MsgPack(Message.MSG_SYS_NEW_ACTIVITY_LIST | Message.ID_ACK)
        if PayActivity.judge_pay_activity_open():
            cnf = PayActivity.activity_pay_config()
            data = self.__get_into(cnf)
            info.append(data)
        if TaskActivity.judge_task_activity_open():
            cnf = TaskActivity.activity_task_config()
            data = self.__get_into(cnf)
            info.append(data)
        if RankActivity.judge_rank_activity_open():
            cnf = RankActivity.activity_rank_config()
            data = self.__get_into(cnf)
            info.append(data)
        if LoginActivity.judge_login_activity_open():
            cnf = LoginActivity.activity_login_config()
            data = self.__get_into(cnf)
            info.append(data)
        if ShareActivity.judge_share_activity_open():
            cnf = ShareActivity.activity_share_config()
            data = self.__get_into(cnf)
            info.append(data)
        if DiscountActivity.judge_discount_activity_open():
            cnf = DiscountActivity.activity_discount_config()
            data = self.__get_into(cnf)
            info.append(data)
        if GiveActivity.judge_give_activity_open():
            cnf = GiveActivity.activity_give_config()
            data = self.__get_into(cnf)
            info.append(data)
        if DoubleActivity.judge_double_activity_open():
            cnf = DoubleActivity.activity_double_config()
            data = self.__get_into(cnf)
            info.append(data)
        if VipActivity.judge_vip_activity_open():
            cnf = VipActivity.activity_vip_config()
            data = self.__get_into(cnf)
            info.append(data)

        if WxNewPlayerActivity.judge_wx_new_player_activity_open():
            cnf = WxNewPlayerActivity.activity_wx_new_player_config()
            data = self.__get_into(cnf)
            info.append(data)

        if ShakeActivity.judge_shake_activity_open():
            cnf = ShakeActivity.activity_shake_config()
            switch = cnf.get('detail', {}).get('switch', 0)
            if switch > 0:
                data = self.__get_into(cnf)
                info.append(data)

        if PayRankActivity.judge_pay_rank_activity_open():
            cnf = PayRankActivity.activity_pay_rank_config()
            c_list = cnf.get('channel')
            cid = Context.Data.get_attr(uid, 'loginChannelId')
            if cid in c_list:
                data = self.__get_into(cnf)
                info.append(data)

        if GiftBox1Activity.judge_gift_box_activity_open():
            cnf = GiftBox1Activity.activity_gift_box_config()
            c_list = cnf.get('channel')
            cid = Context.Data.get_attr(uid, 'loginChannelId')
            if cid in c_list:
                data = self.__get_into(cnf)
                info.append(data)

        if GiftBox2Activity.judge_gift_box_activity_open():
            cnf = GiftBox2Activity.activity_gift_box_config()
            c_list = cnf.get('channel')
            cid = Context.Data.get_attr(uid, 'loginChannelId')
            if cid in c_list:
                data = self.__get_into(cnf)
                info.append(data)

        if PointShopActivity.judge_point_shop_activity_open():
            cnf = PointShopActivity.activity_point_shop_config()
            c_list = cnf.get('channel')
            cid = Context.Data.get_attr(uid, 'loginChannelId')
            if cid in c_list:
                data = self.__get_into(cnf)
                info.append(data)

        if SmashEggActivity.judge_smash_egg_activity_open():
            cnf = SmashEggActivity.activity_smash_egg_config()
            c_list = cnf.get('channel')
            cid = Context.Data.get_attr(uid, 'loginChannelId')
            if cid in c_list:
                data = self.__get_into(cnf)
                info.append(data)

        if GiftBox3Activity.judge_gift_box_activity_open():
            cnf = GiftBox3Activity.activity_gift_box_config()
            c_list = cnf.get('channel')
            cid = Context.Data.get_attr(uid, 'loginChannelId')
            if cid in c_list:
                create_day = cnf.get('create_day')
                day = Context.Data.get_uid_create_day(uid)
                if day <= create_day:
                    data = self.__get_into(cnf)
                    info.append(data)

        if GiftBox4Activity.judge_gift_box_activity_open():
            cnf = GiftBox4Activity.activity_gift_box_config()
            c_list = cnf.get('channel')
            cid = Context.Data.get_attr(uid, 'loginChannelId')
            if cid in c_list:
                vip_limit = cnf.get('vip_limit')
                vip_level = account.BirdAccount.get_vip_level(uid, 2)
                if vip_level >= vip_limit:
                    data = self.__get_into(cnf)
                    info.append(data)

        if DragonBoatActivity.judge_dragon_boat_activity_show():
            cnf = DragonBoatActivity.activity_dragon_boat_config()
            data = self.__get_into(cnf)
            info.append(data)

        version = TotalPayActivity.get_activity_version()
        conf = TotalPayActivity.activity_total_pay_config(version)
        if TotalPayActivity.judge_activity_open(conf):
            c_list = conf.get('channel')
            cid = Context.Data.get_attr(uid, 'loginChannelId')
            if cid in c_list:
                data = self.__get_into(conf)
                info.append(data)

        ret = sorted(info, key=lambda x: x['order'], reverse=True)
        mo.set_param('l', ret)
        return mo

    def get_activity_info(self, uid, gid, mi):
        model = mi.get_param('model')
        ac = {}
        if model == 1:
            ac = PayActivity.get_pay_activity_config(uid)
        elif model == 2:
            ac = TaskActivity.get_task_activity_config(uid)
        elif model == 3:
            ac = RankActivity.get_rank_activity_config(uid)
        elif model == 4:
            ac = LoginActivity.get_login_activity_config(uid)
        elif model == 5:
            ac = ShareActivity.get_share_activity_config(uid)
        elif model == 6:
            ac = DiscountActivity.get_discount_activity_config(uid)
        elif model == 7:
            ac = GiveActivity.get_give_activity_config(uid)
        elif model == 8:
            ac = DoubleActivity.get_double_activity_config(uid, gid)
        elif model == 9:
            ac = VipActivity.get_vip_activity_config(uid, gid)
        elif model == 10:
            ac = WxNewPlayerActivity.get_wx_new_player_activity_config(uid, gid)
        elif model == 11:
            ac = ShakeActivity.get_share_activity_config(uid, gid)
        elif model == 12:
            ac = PayRankActivity.get_pay_rank_activity_config(uid, gid)
        elif model == 13:
            ac = GiftBox1Activity.get_gift_box_1_activity_config(uid, gid)
        elif model == 14:
            ac = GiftBox2Activity.get_gift_box_2_activity_config(uid, gid)
        elif model == 15:
            ac = PointShopActivity.get_point_shop_activity_config(uid, gid)
        elif model == 16:
            ac = SmashEggActivity.get_smash_egg_activity_config(uid, gid)
        elif model == 17:
            ac = GiftBox3Activity.get_gift_box_3_activity_config(uid, gid)
        elif model == 18:
            ac = GiftBox4Activity.get_gift_box_4_activity_config(uid, gid)
        elif model == 19:
            ac = DragonBoatActivity.get_dragon_boat_activity_config(uid, gid)
        elif model == 20:
            ac = TotalPayActivity.get_pay_activity_config(uid, uid)
        mo = MsgPack(Message.MSG_SYS_NEW_ACTIVITY_CONFIG | Message.ID_ACK)
        info = {}
        info['model'] = model
        info['activity_info'] = ac
        mo.set_param('info', info)
        return mo

class PayActivity(object):
    def __init__(self):
        self.gid = 2

    def activity_pay_config(self):
        activity_pay_config = Context.Configure.get_game_item_json(self.gid, 'activity.pay.config')
        return activity_pay_config


    def judge_pay_activity_open(self):
        cnf = self.activity_pay_config()
        if not cnf:
            return False
        if not check_activity_in(cnf['start'], cnf['end'], 0):
            return False
        return True


    def get_user_activity_value(self, uid, start, end):
        ret = Context.Activity.get_activity_data_json(uid, 'pay', 'pay_times')
        if ret:
            if check_activity_in(ret['start'], ret['end'], 0)and Time.str_to_timestamp(start) <= Time.str_to_timestamp(ret['start']):
                return int(ret['value'])
        d = {'start': start, 'end': end, 'value': 0}
        Context.Activity.set_activity_data(uid, 'pay', 'pay_times', Context.json_dumps(d))
        return 0

    def pay_set(self, uid, pay_num):
        if not self.judge_pay_activity_open():
            return
        i = self.activity_pay_config()
        start = i['start']
        end = i['end']
        count = pay_num/i['need_pay']
        ret = Context.Activity.get_activity_data_json(uid, 'pay', 'pay_times')
        if ret:
            if check_activity_in(ret['start'], ret['end'], 0) and Time.str_to_timestamp(start) <= Time.str_to_timestamp(ret['start']):
                d = {'start': start, 'end': end, 'value': count + int(ret['value'])}
            else:
                d = {'start': start, 'end': end, 'value': count}
        else:
            d = {'start': start, 'end': end, 'value': count}
        Context.Activity.set_activity_data(uid, 'pay', 'pay_times', Context.json_dumps(d))
        return

    def get_pay_activity_config(self, uid):
        if not self.judge_pay_activity_open():
            return
        i = self.activity_pay_config()
        start = i['start']
        end = i['end']
        d = {}
        d['id'] = i['id']
        d['model'] = i['model']
        d['start'] = start
        d['end'] = end
        d['name'] = i['name']
        d['need_pay'] = i['need_pay']
        d['count'] = self.get_user_activity_value(uid, start, end)
        d['desc'] = i['desc']
        dt = []
        for k,v in i['rw_list'].items():
            dt.append(props.BirdProps.convert_reward(v['reward']))
        d['rwl'] = dt
        return d

    def on_raffle(self, uid):
        mo = MsgPack(Message.MSG_SYS_NEW_ACTIVITY_PAY_RAFFLE | Message.ID_ACK)
        if not self.judge_pay_activity_open():
            return mo.set_error(1, u"此活动已下架")
        i = self.activity_pay_config()
        aid = i['id']
        start = i['start']
        end = i['end']
        activity_value = self.get_user_activity_value(uid, i['start'], i['end'])
        if activity_value <= 0:
            return mo.set_error(1, u"可玩次数不够")
        index, rw = random_reward(i['rw_list'])
        if not rw or index == None:
            return mo.set_error(1, u"配置错误")
        activity_value -= 1
        info = {}
        final_info = props.BirdProps.issue_rewards(uid, self.gid, rw, 'activity.pay.raffle', True)
        d = {'start': start, 'end': end, 'value': activity_value}
        Context.Activity.set_activity_data(uid, 'pay', 'pay_times', Context.json_dumps(d))

        # 添加事件-------------
        record_data = {'ts':Time.current_ts(), 'uid':uid, 'rw': rw}
        ms = Time.current_ms()
        tmp = Time.current_time('%Y-%m-%d')
        Context.RedisStat.hash_set('pay_activity:%s:%d' % (tmp, uid), ms, Context.json_dumps(record_data))
        # -------------------

        self.add_raffle_record(uid, rw, Time.str_to_timestamp(start), aid)
        info['rw'] = final_info
        info['idx'] = index
        info['av'] = activity_value
        mo.set_param('info', info)
        return mo

    def add_raffle_record(self, uid, reward, start ,aid):
        end_ts = Context.Activity.get_activity_data(100, 'pay', 'end_ts')
        if end_ts:
            if int(end_ts) != start:
                ret = Context.Activity.get_activity_all_data(100, 'pay')
                for i in ret.keys():
                    Context.Activity.del_activity_data(100, 'pay', i)
                Context.save_cache('activity_pay', aid, ret)
                Context.Activity.set_activity_data(100, 'pay', 'end_ts', start)
            Context.Activity.set_activity_data(100, 'pay', Time.current_ms(), Context.json_dumps([uid, reward]))
        else:
            Context.Activity.set_activity_data(100, 'pay', 'end_ts', start)
            Context.Activity.set_activity_data(100, 'pay', Time.current_ms(), Context.json_dumps([uid, reward]))
        return

    def send_raffle_record(self, uid):
        mo = MsgPack(Message.MSG_SYS_NEW_ACTIVITY_PAY_SEND_RECORD | Message.ID_ACK)
        if not self.judge_pay_activity_open():
            return mo.set_error(1, u"此活动已下架")
        i = self.activity_pay_config()
        aid = i['id']
        start = Time.str_to_timestamp(i['start'])
        info = []
        end_ts = Context.Activity.get_activity_data(100, 'pay', 'end_ts')
        if end_ts:
            if int(end_ts) != start:
                ret = Context.Activity.get_activity_all_data(100, 'pay')
                for i in ret.keys():
                    Context.Activity.del_activity_data(100, 'pay', i)
                Context.save_cache('activity_pay', aid, ret)
                Context.Activity.set_activity_data(100, 'pay', 'end_ts', start)
            else:
                ret = Context.Activity.get_activity_all_data(100, 'pay')
                if ret.has_key('end_ts'):
                    del ret['end_ts']
                d_list = sorted(ret.items(), key=lambda x: int(x[0]), reverse=True)
                for i in d_list:
                    d = {}
                    data = Context.json_loads(i[1])
                    nick = Context.Data.get_attr(int(data[0]), 'nick')
                    d['n'] = nick
                    d['rw'] = props.BirdProps.convert_reward(data[1])
                    info.append(d)
        else:
            Context.Activity.set_activity_data(100, 'pay', 'end_ts', start)
        mo.set_param('info', info)
        return mo

class TaskActivity(object):
    def __init__(self):
        self.gid = 2

    def activity_task_config(self):
        activity_task_config = Context.Configure.get_game_item_json(self.gid, 'activity.task.config')
        return activity_task_config


    def judge_task_activity_open(self):
        cnf = self.activity_task_config()
        if not cnf:
            return False
        if not check_activity_in(cnf['start'], cnf['end'], 0):
            return False
        return True

    def get_task_activity_config(self, uid):
        if not self.judge_task_activity_open():
            return
        i = self.activity_task_config()
        start = i['start']
        end = i['end']
        d = {}
        d['id'] = i['id']
        d['model'] = i['model']
        d['start'] = start
        d['end'] = end
        d['name'] = i['name']
        d['desc'] = i['desc']
        d['reward'] = props.BirdProps.convert_reward(i['reward'])
        ret_task_list, task_day = self.get_activity_task_list(uid, i['task'], start, end)
        d['task_day'] = task_day
        lst = []
        for i in ret_task_list:
            l = {}
            l['tid'] = int(i[0])
            l['dt'] = i[1]
            l['tp'] = i[2]
            l['idx'] = i[3]
            l['c'] = i[4]
            l['cp'] = i[5]
            l['rz'] = i[6]
            l['at'] = i[7]
            l['rw'] = i[8]
            l['dc'] = i[9]
            lst.append(l)
        d['task_list'] = lst
        reward_total = Context.Activity.get_activity_data(uid, 'task', 'reward_total')
        if reward_total == None:
            reward_total = 0
        d['reward_total'] = reward_total
        return d

    def get_activity_task_list(self, uid, task, start, end):
        item_list = sorted(task.keys(), key=lambda x: int(x), reverse=False)
        task_time = Context.Activity.get_activity_data(uid, 'task', 'task_time')
        if not task_time:
            task_time = 0
        start_ts = Time.str_to_timestamp(start)
        end_ts = Time.str_to_timestamp(end)
        ret_task_list = []
        task_day = int((Time.current_ts() - start_ts) / (3600 * 24)) + 1
        lst = Context.Activity.get_activity_all_data(uid, 'task')
        if start_ts <= int(task_time) < end_ts:
            for i in item_list:
                if not lst.has_key(str(i)):
                    l = self.set_task_init(uid, i, task)
                    ret_task_list.append(l)
                else:
                    l = Context.json_loads(lst[str(i)])
                    ret_task_list.append([int(i), l[0], l[1], l[2], l[3], l[4], l[5], task[str(i)][4],
                                          props.BirdProps.convert_reward(task[str(i)][5]),
                                          task[str(i)][6]])
            # task_day = Context.Activity.get_activity_data(uid, 'task', 'task_day')
            # if not task_day:
            #    Context.Activity.set_activity_data(uid, 'task', 'task_day', 0)
            #    task_day = 1
        else:
            reward_total = Context.Activity.get_activity_data(uid, 'task', 'reward_total')
            if reward_total:
                Context.Activity.del_activity_data(uid, 'task', 'reward_total')
            for i in item_list:
                task_id = i
                l = self.set_task_init(uid, task_id, task)
                ret_task_list.append(l)
                Context.Activity.set_activity_data(uid, 'task', 'task_time', Time.str_to_timestamp(start))
            self.get_activity_task_list(uid, task, start, end)
        return ret_task_list, task_day

    def set_task_init(self, uid, task_id, task):
        l = [task[str(task_id)][0], task[str(task_id)][1], task[str(task_id)][2], task[str(task_id)][3], 0, 0]
        Context.Activity.set_activity_data(uid, 'task', int(task_id),Context.json_dumps(l))
        return [int(task_id), task[str(task_id)][0], task[str(task_id)][1], task[str(task_id)][2], task[str(task_id)][3], 0, 0,
                task[str(task_id)][4],
                props.BirdProps.convert_reward(task[str(task_id)][5]),
                task[str(task_id)][6]]

    def receive_reward_task(self, uid, mi):
        mo = MsgPack(Message.MSG_SYS_NEW_ACTIVITY_TASK_REWARD | Message.ID_ACK)
        if not self.judge_task_activity_open():
            return mo.set_error(1, u"此活动已下架")
        task_id = mi.get_param('tid')
        task_list = Context.Activity.get_activity_data_json(uid, 'task', task_id)
        reward = self.activity_task_config()['task'][str(task_id)][5]
        info = {}
        if task_list[4] >= task_list[3]:
            task_list[5] = 1
            final_info = props.BirdProps.issue_rewards(uid, self.gid, reward, 'activity.task.reward.receive', True)
            Context.Activity.set_activity_data(uid, 'task', int(task_id), Context.json_dumps(task_list))
            info['f'] = final_info
        else:
            ac = self.get_task_activity_config(uid)
            mo = MsgPack(Message.MSG_SYS_NEW_ACTIVITY_CONFIG | Message.ID_ACK)
            info = {}
            info['model'] = 2
            info['activity_info'] = ac
            mo.set_param('info', info)
            Context.GData.send_to_connect(uid, mo)
            return
        mo.set_param('info', info)
        return mo

    def receive_reward_total(self, uid):
        mo = MsgPack(Message.MSG_SYS_NEW_ACTIVITY_TASK_REWARD_TOTAL | Message.ID_ACK)
        if not self.judge_task_activity_open():
            return mo.set_error(1, u"此活动已下架")
        info = {}
        reward_total = Context.Activity.get_activity_data(uid, 'task', 'reward_total')
        if reward_total and int(reward_total) >= 1:
            return mo.set_error(2, u"你还不能领取最终奖励")
        task_day = int((Time.current_ts() - Time.str_to_timestamp(self.activity_task_config()['start'])) / (3600 * 24)) + 1
        if int(task_day):
            flag = True
            task_data = Context.Activity.get_activity_all_data(uid, 'task')
            for k,v in task_data.items():
                if k in ['task_time', 'reward_total']:
                    continue
                t = Context.json_loads(v)
                if t[3] > t[4]:
                    flag = False
            if flag:
                reward = self.activity_task_config()['reward']
                final_info = props.BirdProps.issue_rewards(uid, self.gid, reward, 'activity.task.reward.total', True)
                Context.Activity.set_activity_data(uid, 'task', 'reward_total', 1)
                info['f'] = final_info
        if len(info) <= 0:
            return mo.set_error(3, u"你还不能领取最终奖励")
        mo.set_param('info', info)
        return mo

class RankActivity(object):
    def __init__(self):
        self.gid = 2
        self.tid = 1000
        self.activity_rank_list = None

    def activity_rank_config(self):
        activity_rank_config = Context.Configure.get_game_item_json(self.gid, 'activity.rank.config')
        return activity_rank_config

    def judge_rank_activity_open(self):
        cnf = self.activity_rank_config()
        if not cnf:
            return False
        if not check_activity_in(cnf['start'], cnf['end'], 0):
            return False
        return True

    def incr_user_rank_value(self, uid, type, value):
        if not self.judge_rank_activity_open():
            return
        #if type != self.activity_rank_config()['type']:
        #    return
        Context.Activity.hincr_activity_data(self.tid, 'rank', uid, value)
        return

    def get_rank_activity_config(self, uid):
        if not self.judge_rank_activity_open():
            return
        i = self.activity_rank_config()
        start = i['start']
        end = i['end']
        d = {}
        d['id'] = i['id']
        d['t'] = i['model']
        d['s'] = start
        d['e'] = end
        d['n'] = i['name']
        d['d'] = i['desc']
        l, index, point = self.get_activity_rank_list(uid)
        if l != None and index != None and point != None:
            d['rl'] = l
            d['ix'] = index
            d['pnt'] = point
        return d

    def get_activity_rank_list(self, uid):
        if not self.judge_rank_activity_open():
            return None, None, None
        info = []
        index = -1
        point = Context.Activity.get_activity_data(self.tid, 'rank', uid, 0)
        conf = self.activity_rank_config()
        l = self.activity_rank_list
        if self.activity_rank_list == None:
            l = []
        for k, v in enumerate(l):
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
                vip_level = account.BirdAccount.get_vip_level(int(v[0]), self.gid)
            except:
                vip_level = 0
            level = -1
            for i, j in enumerate(conf['level']):
                if k + 1 in j:
                    level = i
            if level < 0:
                continue
            reward = props.BirdProps.convert_reward(conf['reward'][level])
            if int(v[0]) == uid:
                index = k
            rank = {
                'rank': int(k),
                'id': int(v[0]),
                'nick': nick,
                'sex': int(sex),
                'avatar': avatar,
                'vip': int(vip_level),
                'point': int(v[1]),
                'reward': reward
            }
            info.append(rank)
        return info, index, point

    #设置排行榜数据
    def set_rank_list(self):
        lst = Context.Activity.get_activity_all_data(self.tid, 'rank')
        if lst.has_key('refresh_time'):
            del lst['refresh_time']
        conf = self.activity_rank_config()
        if conf == None:
            return []
        count = conf['count']
        self.activity_rank_list = sorted(lst.items(), key=lambda x: int(x[1]), reverse=True)
        if len(self.activity_rank_list) >= count:
            self.activity_rank_list = self.activity_rank_list[:count]
        return self.activity_rank_list

    def deal_activity_rank(self):
        refresh_time = Context.Activity.get_activity_data(self.tid, 'rank', 'refresh_time')
        conf = self.activity_rank_config()
        if conf == None:
            return
        end = conf['end']
        end_ts = Time.str_to_timestamp(end)
        if refresh_time == None or int(refresh_time) != int(end_ts):
            Context.Activity.set_activity_data(self.tid, 'rank', 'refresh_time', end_ts)
            return
        ret_list = self.set_rank_list()
        now_ts = Time.current_ts()
        if now_ts > int(refresh_time):
            if ret_list != None and len(ret_list) > 0:
                # 发放奖励
                for k, v in enumerate(ret_list):
                    level = -1
                    for i, j in enumerate(conf['level']):
                        if k + 1 in j:
                            level = i
                    if level < 0:
                        continue
                    reward = conf['reward'][level]
                    ret = mail.Mail.add_mail(int(v[0]), self.gid, now_ts, 7, reward, -(k + 1))
                    if ret:
                        mail.Mail.send_mail_list(int(v[0]), self.gid)
                ret = Context.Activity.get_activity_all_data(self.tid, 'rank')
                for i in ret.keys():
                    Context.Activity.del_activity_data(self.tid, 'rank', i)
                if len(ret) > 0:
                    Context.save_cache('activity_rank', str(Time.current_ts()), ret)
                # if conf:
                #     end = conf['end']
                #     end_ts = Time.str_to_timestamp(end)
                #     Context.Activity.set_activity_data(self.tid, 'rank', 'refresh_time', end_ts)
                self.set_rank_list()
        return

    def on_rank_timer(self):
        self.deal_activity_rank()
        return

class LoginActivity(object):
    def __init__(self):
        self.gid = 2

    def activity_login_config(self):
        activity_login_config = Context.Configure.get_game_item_json(self.gid, 'activity.login.config')
        return activity_login_config


    def judge_login_activity_open(self):
        cnf = self.activity_login_config()
        if not cnf:
            return False
        if not check_activity_in(cnf['start'], cnf['end'], 0):
            return False
        return True

    def get_login_activity_config(self, uid):
        if not self.judge_login_activity_open():
            return
        i = self.activity_login_config()
        start = i['start']
        end = i['end']
        d = {}
        d['id'] = i['id']
        d['t'] = i['model']
        d['s'] = start
        d['e'] = end
        d['n'] = i['name']
        d['d'] = i['desc']
        l, index = self.activity_login_reward(uid)
        if l != None and index != None:
            d['rl'] = l
            d['ix'] = index
        return d

    def add_login_account(self, uid):
        if not self.judge_login_activity_open():
            return
        start_time = Context.Activity.get_activity_data(uid, 'login', 'start_time')
        refresh_time = Context.Activity.get_activity_data(uid, 'login', 'refresh_time')
        start = self.activity_login_config()['start']
        start = Time.str_to_timestamp(start)
        t = Time.current_ts()
        if refresh_time == None or start_time == None or start > int(start_time):
            Context.Activity.set_activity_data(uid, 'login', 'refresh_time', t)
            Context.Activity.set_activity_data(uid, 'login', 'start_time', start)
            Context.Activity.set_activity_data(uid, 'login', 'login_list', Context.json_dumps([0, 0, 0, 0, 0, 0, 0]))
            Context.Activity.set_activity_data(uid, 'login', 'login_count', 1)
            refresh_time = t
        if int(refresh_time) < Time.today_start_ts():
            Context.Activity.set_activity_data(uid, 'login', 'refresh_time', t)
            Context.Activity.hincr_activity_data(uid, 'login', 'login_count', 1)
        return

    def activity_login_reward(self, uid):
        #if not self.judge_login_activity_open():
        #    return None, None
        login_count = Context.Activity.get_activity_data(uid, 'login', 'login_count')
        login_list = Context.Activity.get_activity_data_json(uid, 'login', 'login_list')
        start_time = Context.Activity.get_activity_data(uid, 'login', 'start_time')
        refresh_time = Context.Activity.get_activity_data(uid, 'login', 'refresh_time')
        start = self.activity_login_config()['start']
        start = Time.str_to_timestamp(start)
        if (login_count == None or login_list == None or refresh_time == None
            or start_time == None or start > int(start_time)) and self.judge_login_activity_open():
            Context.Activity.set_activity_data(uid, 'login', 'refresh_time', Time.current_ts())
            Context.Activity.set_activity_data(uid, 'login', 'start_time', start)
            Context.Activity.set_activity_data(uid, 'login', 'login_count', 1)
            Context.Activity.set_activity_data(uid, 'login', 'login_count', Context.json_dumps([0, 0, 0, 0, 0, 0, 0]))
            login_count = 1
            login_list = [0,0,0,0,0,0,0]
        elif not self.judge_login_activity_open():
            Context.Activity.set_activity_data(uid, 'login', 'login_count', 0)
            Context.Activity.set_activity_data(uid, 'login', 'login_list', Context.json_dumps([0, 0, 0, 0, 0, 0, 0]))
            login_count = 0
            login_list = [0, 0, 0, 0, 0, 0, 0]
        l = []
        for k,v in enumerate(self.activity_login_config()['reward']):
            l.append({'recv': login_list[k], 'reward': props.BirdProps.convert_reward(v)})
        return l, login_count

    def receive_login_reward(self, uid, mi):
        mo = MsgPack(Message.MSG_SYS_NEW_ACTIVITY_LOGIN_REWARD | Message.ID_ACK)
        if not self.judge_login_activity_open():
            return mo.set_error(1, u"此活动已下架")
        count = int(mi.get_param('count'))
        if count > 7 or count <= 0:
            return mo.set_error(2, u"参数错误")
        login_count = Context.Activity.get_activity_data(uid, 'login', 'login_count')
        login_list = Context.Activity.get_activity_data_json(uid, 'login', 'login_list')
        if not login_count or login_list == None:
            Context.Activity.set_activity_data(uid, 'login', 'login_count', 1)
            Context.Activity.set_activity_data(uid, 'login', 'login_list', Context.json_dumps([0, 0, 0, 0, 0, 0, 0]))
            login_count = 1
            login_list = [0, 0, 0, 0, 0, 0, 0]
        if count > int(login_count):
            return mo.set_error(3, u"完成次数不够")
        if login_list[count - 1] > 0:
            return mo.set_error(4, u"你已经领取了该奖励")
        login_list[count - 1] = 1
        Context.Activity.set_activity_data(uid, 'login', 'login_list', Context.json_dumps(login_list))
        reward = self.activity_login_config()['reward'][count-1]
        final_info = props.BirdProps.issue_rewards(uid, self.gid, reward, 'activity.login.reward', True)
        info = {}
        info['f'] = final_info
        info['r'] = 1
        mo.set_param('info', info)
        return mo

class ShareActivity(object):
    def __init__(self):
        self.gid = 2

    def activity_share_config(self):
        activity_share_config = Context.Configure.get_game_item_json(self.gid, 'activity.share.config')
        return activity_share_config

    def judge_share_activity_open(self):
        cnf = self.activity_share_config()
        if not cnf:
            return False
        if not check_activity_in(cnf['start'], cnf['end'], 0):
            return False
        return True

    def get_share_activity_config(self, uid):
        if not self.judge_share_activity_open():
            return
        i = self.activity_share_config()
        start = i['start']
        end = i['end']
        d = {}
        d['id'] = i['id']
        d['t'] = i['model']
        d['s'] = start
        d['e'] = end
        d['n'] = i['name']
        d['d'] = i['desc']
        return d

class DiscountActivity(object):
    def __init__(self):
        self.gid = 2

    def activity_discount_config(self):
        activity_discount_config = Context.Configure.get_game_item_json(self.gid, 'activity.discount.config')
        return activity_discount_config

    def judge_discount_activity_open(self):
        cnf = self.activity_discount_config()
        if not cnf:
            return False
        if not check_activity_in(cnf['start'], cnf['end'], 0):
            return False
        return True

    def get_discount_activity_config(self, uid):
        if not self.judge_discount_activity_open():
            return
        i = self.activity_discount_config()
        start = i['start']
        end = i['end']
        show = i['show']
        if not check_activity_in(start, end, show):
            return None
        d = {}
        d['id'] = i['id']
        d['t'] = i['model']
        d['s'] = start
        d['e'] = end
        d['n'] = i['name']
        d['d'] = i['desc']
        p = self.get_discount_product()
        d['p'] = p
        return d

    def get_discount_product(self):
        info = []
        for i in self.activity_discount_config()['product']:
            info.append(i)
        return info

class GiveActivity(object):
    def __init__(self):
        self.gid = 2

    def activity_give_config(self):
        activity_give_config = Context.Configure.get_game_item_json(self.gid, 'activity.give.config')
        return activity_give_config

    def judge_give_activity_open(self):
        cnf = self.activity_give_config()
        if not cnf:
            return False
        if not check_activity_in(cnf['start'], cnf['end'], 0):
            return False
        return True

    def get_user_activity_value(self, uid, start, end):
        keys = ['start', 'end', 'count']
        start_d, end_d, count = Context.Activity.mget_activity_data(uid, 'give', keys)
        if start_d and end_d and count != None:
            if start == start_d and end == end_d:
                return int(count)
        d = {'start': start, 'end': end, 'count': 0}
        Context.Activity.mset_activity_data(uid, 'give', d)
        return 0

    def pay_set(self, uid, pay_num):
        if not self.judge_give_activity_open():
            return
        i = self.activity_give_config()
        start = i['start']
        end = i['end']
        start_d, end_d, count = Context.Activity.mget_activity_data(uid, 'give', ['start', 'end', 'count'])
        if start_d and end_d and count:
            if start == start_d and end == end_d:
                d = {'start': start, 'end': end, 'count': pay_num + int(count)}
            else:
                d = {'start': start, 'end': end, 'count': pay_num}
        else:
            d = {'start': start, 'end': end, 'count': pay_num}
        Context.Activity.mset_activity_data(uid, 'give', d)
        return

    def get_user_activity_receive(self, uid, count, key_list):
        receive = Context.Activity.get_activity_data_json(uid, 'give', 'receive')
        if receive == None:
            receive = [0 for _ in range(len(key_list))]
            Context.Activity.set_activity_data(uid, 'give', 'receive', Context.json_dumps(receive))
        l = []
        for k,v in zip(receive, key_list):
            if count >= int(v):
                if int(k) == 1:
                    l.append(2)
                else:
                    l.append(1)
            else:
                l.append(0)
        return l

    def get_give_activity_config(self, uid):
        if not self.judge_give_activity_open():
            return
        i = self.activity_give_config()
        start = i['start']
        end = i['end']
        count = self.get_user_activity_value(uid, start, end)
        d = {}
        d['id'] = i['id']
        d['model'] = i['model']
        d['start'] = start
        d['end'] = end
        d['name'] = i['name']
        d['count'] = count
        d['desc'] = i['desc']
        lt = []
        key_list = sorted(i['rw_list'].keys(), key=lambda x: int(x), reverse=False)
        receive = self.get_user_activity_receive(uid, count, key_list)
        for k,v in zip(key_list, receive):
            rw = props.BirdProps.convert_reward(i['rw_list'][str(k)])
            dt = {}
            dt['value'] = int(k)
            dt['reward'] = rw
            dt['receive'] = int(v)
            lt.append(dt)
        d['rwl'] = lt
        return d

    def on_receive_reward(self, uid, mi):
        mo = MsgPack(Message.MSG_SYS_NEW_ACTIVITY_GIVE_REWARD | Message.ID_ACK)
        if not self.judge_give_activity_open():
            return mo.set_error(1, u"此活动已下架")
        i = self.activity_give_config()
        cost = Tool.to_int(mi.get_param('cost'))
        start = i['start']
        end = i['end']
        pay_count = self.get_user_activity_value(uid, start, end)
        if cost > pay_count:
            return mo.set_error(2, u"你的充值还不足以领取此奖励")
        key_list = sorted(i['rw_list'].keys(), key=lambda x: int(x), reverse=False)
        receive = Context.Activity.get_activity_data_json(uid, 'give', 'receive')
        rw = None
        count = 0
        for k,v in zip(key_list, receive):
            if int(k) == cost and v == 0:
                receive[count] = 1
                rw = i['rw_list'][str(k)]
                Context.Activity.set_activity_data(uid, 'give', 'receive', Context.json_dumps(receive))
            count += 1
        if rw == None:
            return mo.set_error(2, u"你已经领取了该奖励")

        final_info = props.BirdProps.issue_rewards(uid, self.gid, rw, 'activity.give.reward', True)
        info = {}
        receive = self.get_user_activity_receive(uid, pay_count, key_list)
        info['f'] = final_info
        info['r'] = receive
        mo.set_param('info', info)
        return mo


class DoubleActivity(object):
    def __init__(self):
        self.gid = 2

    def activity_double_config(self):
        recharge_double_data = Context.RedisActivity.get('recharge.double.config')
        if recharge_double_data == None:
            recharge_double_data = None
        else:
            recharge_double_data = Context.json_loads(recharge_double_data)
        return recharge_double_data

    def judge_double_activity_open(self):
        cnf = self.activity_double_config()
        if not cnf:
            return False
        if not check_activity_in(cnf['start'], cnf['end'], 0):
            return False
        return True

    def get_double_activity_config(self, uid, gid):
        if not self.judge_double_activity_open():
            return {}
        i = self.activity_double_config()
        start = i['start']
        end = i['end']
        d = {}
        d['id'] = i['id']
        d['t'] = i['model']
        d['s'] = start
        d['e'] = end
        d['n'] = i['name']
        d['d'] = i['desc']
        pd = []

        for k,v in i['pd'].items():
            ret = self.get_product_buy_info(uid, k)
            if ret <= 0:
                pd.append([k,str(v)])
        d['pd'] = pd
        return d

    def get_recharge_date(self, gid):
        product_config = Context.Configure.get_game_item_json(gid, 'product.config')
        shop_config = Context.Configure.get_game_item_json(gid, 'shop.config')
        product_id_list = shop_config.get('chip')
        info = {}
        conf = {}
        for k,v in product_config.items():
            if k in product_id_list:
                conf[k] = v
        info['conf'] = conf

        recharge_double_data = Context.RedisActivity.get('recharge.double.config')
        if recharge_double_data == None:
            recharge_double_data = {}
        else:
            recharge_double_data = Context.json_loads(recharge_double_data)
        info['rdd'] = recharge_double_data
        return info

    def get_activity_can_buy_config(self, uid, gid):
        if not self.judge_double_activity_open():
            return False
        chip_product_config = Context.Configure.get_game_item_json(gid, 'chip.product.config')
        pid_list = []
        for k in chip_product_config:
            ret = self.get_product_buy_info(uid, k)
            if ret <= 0:
                pid_list.append(k)
        return pid_list

    def get_product_buy_info(self, uid, pid):
        channel_id = Context.Data.get_attr(uid, 'channelid')
        keys = 'user_daily:%s:%s:%d' % (channel_id, Time.current_time('%Y-%m-%d'), uid)
        fieds = 'product_%s' % str(pid)
        ret = Context.RedisStat.hash_get_int(keys, fieds, 0)
        return ret

    def get_activity_can_buy(self, uid, gid, product):
        if not self.judge_double_activity_open():
            return False, 0.0
        cnf = self.activity_double_config()
        pd = cnf.get('pd')
        double = 0.0
        if pd.has_key(str(product)):
            ret = self.get_product_buy_info(uid, str(product))
            if ret <= 0:
                double = pd.get(str(product))
                return True, double
        return False, double

class VipActivity(object):
    def __init__(self):
        self.gid = 2

    def activity_vip_config(self):
        vip_activity_data = Context.RedisActivity.get('vip.activity.config')
        if vip_activity_data == None:
            vip_activity_data = None
        else:
            vip_activity_data = Context.json_loads(vip_activity_data)
        return vip_activity_data

    def judge_vip_activity_open(self):
        cnf = self.activity_vip_config()
        if not cnf:
            return False
        if not check_activity_in(cnf['start'], cnf['end'], 0):
            return False
        return True

    def get_vip_activity_config(self, uid, gid):
        if not self.judge_vip_activity_open():
            return {}
        i = self.activity_vip_config()
        start = i['start']
        end = i['end']
        d = {}
        d['id'] = i['id']
        d['t'] = i['model']
        d['s'] = start
        d['e'] = end
        d['n'] = i['name']
        d['d'] = i['desc']
        ret = Context.Daily.get_daily_data(uid, gid, 'vip.activity.times')
        re = Tool.to_int(ret, 0)
        d['re'] = re
        return d

    def get_vip_activity_date(self, gid):
        vip_activity_data = Context.RedisActivity.get('vip.activity.config')
        if vip_activity_data == None:
            vip_activity_data = {}
        else:
            vip_activity_data = Context.json_loads(vip_activity_data)

        return vip_activity_data

    def vip_activity_recevie(self, uid, mi):
        mo = MsgPack(Message.MSG_SYS_NEW_ACTIVITY_VIP_RECEIVE | Message.ID_ACK)
        if not self.judge_vip_activity_open():
            return mo.set_error(1, u"此活动已下架")

        ret = Context.Daily.get_daily_data(uid, self.gid, 'vip.activity.times')
        re = Tool.to_int(ret, 0)
        if re > 0:
            return mo.set_error(2, u"你已经领取了vip奖励")
        cnf = self.activity_vip_config()
        rw_list = cnf.get('va')
        vip_level = account.BirdAccount.get_vip_level(uid, self.gid)
        if vip_level <= 0:
            return mo.set_error(3, u"你vip等级不足，无法领取")
        rw = rw_list.get(str(vip_level))
        rw_price = props.BirdProps.get_props_price(rw)
        if rw_price <= 0:
            return mo.set_error(4, u"你vip等级不足，无法领取")

        channel_id = Context.Data.get_attr(uid, 'channelid')
        keys = 'user_daily:%s:%s:%d'%(channel_id, Time.yesterday_time(), uid)
        fieds = '%s.pay.user.pay_total'%channel_id
        yesterday_recharge = Context.RedisStat.hash_get_int(keys, fieds, 0)
        if yesterday_recharge >= 10:
            double = cnf.get('double', 5)
            rw = props.BirdProps.reward_doubling(rw, double)
        final_info = props.BirdProps.issue_rewards(uid, self.gid, rw, 'vip.activity.reward', True)
        Context.Daily.incr_daily_data(uid, self.gid, 'vip.activity.times')
        mo.set_param('f', final_info)
        return mo

class SaveMoneyActivity(object):
    def __init__(self):
        self.gid = 2

    def save_money_activity_config(self):
        save_money_data = Context.RedisActivity.get('save.money.activity.config')
        if save_money_data == None:
            save_money_data = None
        else:
            save_money_data = Context.json_loads(save_money_data)
        return save_money_data

    def judge_save_money_open(self):
        cnf = self.save_money_activity_config()
        if not cnf:
            return False
        if not check_activity_in(cnf['start'], cnf['end'], 0):
            return False
        return True

    def get_save_money_activity_data(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_NEW_ACTIVITY_SAVE_MONEY_DATA | Message.ID_ACK)
        if not self.judge_save_money_open():
            return mo.set_param('open', 0)
        mo.set_param('open', 1)
        i = self.save_money_activity_config()
        start = i['start']
        save_value = i.get('save_chip')
        vip_level = account.BirdAccount.get_vip_level(uid, self.gid)
        vip_data = i.get('sp').get(str(vip_level))
        if vip_level == None:
            return mo.set_error(4, u"数据出错")
        times = Context.Daily.get_daily_data(uid, gid, 'save_money_activity_times')
        num, red = self.get_save_money_num(uid, start)
        num = Tool.to_int(num, 0)
        times = Tool.to_int(times, 0)
        chip = num / save_value
        max_chip = vip_data['chip']
        day_time = vip_data['day_time']
        if chip > max_chip:
            chip = max_chip
            if red <= 0:
                mo.set_param('r', 1)
            else:
                mo.set_param('r', 0)
            Context.Activity.set_activity_data(uid, 'save_money', 'red', 1)
        if times >= vip_data['day_time']:
            times = 0
        else:
            times = 1
        mo.set_param('c', chip)
        mo.set_param('t', times)
        mo.set_param('mc', max_chip)
        mo.set_param('mt', day_time)
        return mo

    def receive_save_money_reward(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_NEW_ACTIVITY_SAVE_MONEY_RECEIVE | Message.ID_ACK)
        if not self.judge_save_money_open():
            return mo.set_error(1, u"此活动已下架")
        i = self.save_money_activity_config()
        start = i['start']
        save_value = i.get('save_chip')
        vip_level = account.BirdAccount.get_vip_level(uid, self.gid)
        vip_data = i.get('sp').get(str(vip_level))
        if vip_level == None:
            return mo.set_error(4, u"数据出错")
        times = Context.Daily.get_daily_data(uid, gid, 'save_money_activity_times')
        num, red = self.get_save_money_num(uid, start)
        num = Tool.to_int(num, 0)
        times = Tool.to_int(times, 0)
        chip = num/save_value
        max_chip = vip_data['chip']
        day_time = vip_data['day_time']
        if chip > max_chip:
            chip = max_chip
        if times >= day_time:
            return mo.set_error(2, u"你已经领取完了存钱窝奖励")
        if chip <= 0:
            return mo.set_error(3, u"你的存钱窝还没有金币奖励，无法领取")
        rw = {'chip':chip}
        final_info = props.BirdProps.issue_rewards(uid, self.gid, rw, 'save.money.activity.reward', True)
        times = Context.Daily.incr_daily_data(uid, self.gid, 'save_money_activity_times')
        f = {'red': 1, 'save_money_num': 0}
        Context.Activity.mset_activity_data(uid, 'save_money', f)
        if times >= day_time:
            ts = 0
        else:
            ts = 1
        mo.set_param('f', final_info)
        mo.set_param('c', 0)
        mo.set_param('t', ts)
        return mo

    def incr_user_value(self, uid, gid, value):
        if not self.judge_save_money_open():
            return
        i = self.save_money_activity_config()
        start = i['start']
        num, red = self.get_save_money_num(uid, start)
        Context.Activity.hincr_activity_data(uid, 'save_money', 'save_money_num', value)
        save_value = i.get('save_chip')
        vip_level = account.BirdAccount.get_vip_level(uid, self.gid)
        vip_data = i.get('sp').get(str(vip_level))
        if vip_level == None:
            return
        mo = MsgPack(Message.MSG_SYS_NEW_ACTIVITY_SAVE_MONEY_DATA | Message.ID_ACK)
        times = Context.Daily.get_daily_data(uid, gid, 'save_money_activity_times')
        num = Tool.to_int(num, 0)
        times = Tool.to_int(times, 0)
        chip = num / save_value
        max_chip = vip_data['chip']
        day_time = vip_data['day_time']
        if chip > max_chip and red <= 0:
            chip = max_chip
            mo.set_param('r', 1)
            if times >= day_time:
                times = 0
            else:
                times = 1
            mo.set_param('c', chip)
            mo.set_param('t', times)
            mo.set_param('mc', max_chip)
            mo.set_param('mt', day_time)
            Context.GData.send_to_connect(uid, mo)
            Context.Activity.set_activity_data(uid, 'save_money', 'red', 1)
        return

    def get_save_money_num(self, uid, start):
        start_t, num, red = Context.Activity.mget_activity_data(uid, 'save_money', ['start', 'save_money_num', 'red'])
        if str(start) != str(start_t):
            d = {'start': start, 'save_money_num': 0}
            Context.Activity.mset_activity_data(uid, 'save_money', d)
            num = 0
        num = Tool.to_int(num , 0)
        red = Tool.to_int(red, 0)
        return num, red

class WxNewPlayerActivity(object):
    def __init__(self):
        self.gid = 2

    def activity_wx_new_player_config(self):
        wx_new_player_activity_data = Context.RedisActivity.get('wx_new_player.activity.config')
        if wx_new_player_activity_data == None:
            wx_new_player_activity_data = None
        else:
            wx_new_player_activity_data = Context.json_loads(wx_new_player_activity_data)
        return wx_new_player_activity_data

    def judge_wx_new_player_activity_open(self):
        cnf = self.activity_wx_new_player_config()
        if not cnf:
            return False
        if not check_activity_in(cnf['start'], cnf['end'], 0):
            return False
        return True

    def get_wx_new_player_activity_config(self, uid, gid):
        if not self.judge_wx_new_player_activity_open():
            return {}
        i = self.activity_wx_new_player_config()
        start = i['start']
        end = i['end']
        d = {}
        d['id'] = i['id']
        d['t'] = i['model']
        d['s'] = start
        d['e'] = end
        d['n'] = i['name']
        d['d'] = i['desc']
        re = i['re']
        d['re'] = re
        return d

    def get_wx_new_player_activity_date(self, gid):
        wx_new_player_activity_data = Context.RedisActivity.get('wx_new_player.activity.config')
        if wx_new_player_activity_data == None:
            wx_new_player_activity_data = {}
        else:
            wx_new_player_activity_data = Context.json_loads(wx_new_player_activity_data)
        return wx_new_player_activity_data

    def send_activity_mail(self, uid, gid):
        if self.judge_wx_new_player_activity_open():
            times = Time.current_ts()
            i = self.activity_wx_new_player_config()
            tips = i.get('det')
            reward_p = {'tips': tips}

            ret = Mail.add_mail(uid, gid, times, 12, reward_p, -1)
            if ret:
                Mail.send_mail_list(uid, gid)

    def activity_receive_new_player_gift(self, gid, uid):
        if not self.judge_wx_new_player_activity_open():
            return False
        i = self.activity_wx_new_player_config()
        start = i['start']
        end = i['end']
        createTime = str(Context.Data.get_attr(int(uid), "createTime"))[:19]
        start_ts = Time.str_to_timestamp(start)
        end_ts = Time.str_to_timestamp(end)
        create_ts = Time.str_to_timestamp(createTime)
        if start_ts < create_ts < end_ts:
            lingqu = Context.RedisActivity.hash_get('activity:wx:new_player_gift', uid, None)
            if lingqu:
                return False
            re = i['re']
            times = Time.current_ts()
            ret = Mail.add_mail(uid, gid, times, 13, re, -1)
            if ret:
                Mail.send_mail_list(uid, gid)
                Context.RedisActivity.hash_set('activity:wx:new_player_gift', uid, 1)
                return True
        return False

class ShakeActivity(object):
    def __init__(self):
        self.gid = 2

    def activity_shake_config(self):
        activity_shake_data = Context.RedisActivity.get('shake.activity.config')
        if activity_shake_data == None:
            activity_shake_data = None
        else:
            activity_shake_data = Context.json_loads(activity_shake_data)
        return activity_shake_data

    def judge_shake_activity_open(self):
        cnf = self.activity_shake_config()
        if not cnf:
            return False
        if not check_activity_in(cnf['start'], cnf['end'], 0):
            return False
        return True

    def get_share_activity_config(self, uid, gid):
        if not self.judge_shake_activity_open():
            return {}
        i = self.activity_shake_config()
        switch = i.get('detail', {}).get('switch', 0)
        if switch <= 0:
            return {}
        start = i['start']
        end = i['end']
        d = {}
        d['id'] = i['id']
        d['t'] = i['model']
        d['s'] = start
        d['e'] = end
        d['n'] = i['name']
        d['d'] = i['desc']
        return d

    def pay_set(self, uid, pay_num):
        if not self.judge_shake_activity_open():
            return
        i = self.activity_shake_config()
        switch = i.get('detail', {}).get('switch', 0)
        if switch <= 0:
            return
        start = i['start']
        end = i['end']
        start_d, end_d, count = Context.Activity.mget_activity_data(self.gid, 'shake', ['start', 'end', 'count'])
        pay_total = pay_num
        if start_d and end_d and count:
            if start == start_d and end == end_d:
                d = {'start': start, 'end': end, 'count': pay_num + int(count)}
                pay_total = pay_num + int(count)
            else:
                d = {'start': start, 'end': end, 'count': pay_num}
        else:
            d = {'start': start, 'end': end, 'count': pay_num}
        Context.Activity.mset_activity_data(self.gid, 'shake', d)
        self.start_shake(Tool.to_int(count, 0), pay_total)
        return

    def start_shake(self, last, next):
        i = self.activity_shake_config()
        dat = i.get('detail')
        start = i['start']
        end = i['end']
        way = dat.get('way')
        happy_dat = dat.get('happy')
        flag = False
        if way == 1:#循环
            h_dat = happy_dat[0]
            money = int(h_dat['money'])
            if int(last/money) != int(next/money):
                flag = True
                rebate = h_dat['rebate']
            pass
        elif way == 2:#手动
            for i in happy_dat:
                money = i['money']
                if last < money and next >= money:
                    flag = True
                    rebate = i['rebate']
                    break
        else:
            return
        if flag:
            room = dat.get('room')
            dtl = {'rebate': rebate, 'money': money, 'way': way, 'room': room, 'start':start, 'end':end}
            sid = Time.current_ms()

            Context.RedisActivity.hash_set('activity:shake:%d' % sid, 'detail', Context.json_dumps(dtl))
            mo = MsgPack(Message.BIRD_MSG_SEND_SHAKE_START | Message.ID_NTF)
            mo.set_param('sid', sid)
            mo.set_param('room', room)
            mo.set_param('tm', 8)
            Context.GData.broadcast_to_system(mo)
            from entity import BirdEntity
            BirdEntity.timer.setTimeout(15, {'sid': sid, 'gameId': self.gid, 'action': 'deal_shake'})
        return


    def deal_reward(self, msg):
        sid = msg.get_param('sid')
        shake_dat = Context.RedisActivity.hash_getall('activity:shake:%d'%sid)

        shake_detail = Context.json_loads(shake_dat.get('detail'))
        rebate = shake_detail.get('rebate') * 5000
        player_data = {}
        total_weight = 0
        for k, v in shake_dat.items():
            if k == 'detail':
                continue
            v = Context.json_loads(v)
            barrel_level = v.get('bl')
            shake_times = v.get('st')
            cdkey_pay = Context.Daily.get_daily_data(int(k), self.gid, 'cdkey_pay_total')
            recharge_pay = Context.Daily.get_daily_data(int(k), self.gid, 'pay_total')
            pay = Tool.to_int(cdkey_pay, 0) + Tool.to_int(recharge_pay, 0)
            weight_value = barrel_level * 10 + shake_times * 10 + pay * 2
            player_data[k] = weight_value
            total_weight += weight_value
        for k, v in player_data.items():
            dat = Context.RedisActivity.hash_get_json('activity:shake:%d' % sid, k)
            if total_weight > 0:
                rate = v / float(total_weight)
                if len(player_data) < 10 and rate > 0.1:
                    rate = 0.1
                chip_reward = int(rebate * rate)
                dat['reward'] = chip_reward
                Context.RedisActivity.hash_set('activity:shake:%d' % sid, k, Context.json_dumps(dat))

                shake_money = Context.RedisActivity.hash_incrby('activity:shake:%d' % 100, k, chip_reward)
                mo = MsgPack(Message.MSG_SYS_ACTIVITY_SHAKE_GET | Message.ID_ACK)
                mo.set_param('skm', shake_money)
                Context.GData.send_to_connect(int(k), mo)
        return

    def get_shake_money(self, uid, gid, mi):
        open = 1
        if not self.judge_shake_activity_open():
            open = 0
        shake_money = Context.RedisActivity.hash_get_int('activity:shake:%d' % 100, uid, 0)
        mo = MsgPack(Message.MSG_SYS_ACTIVITY_SHAKE_GET | Message.ID_ACK)
        mo.set_param('open', open)
        mo.set_param('skm', shake_money)
        return mo

    def recv_shake_money(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_ACTIVITY_SHAKE_RECV | Message.ID_ACK)
        if not self.judge_shake_activity_open():
            return mo.set_error(1, u"此活动已下架")
        shake_money = Context.RedisActivity.hash_get_int('activity:shake:%d' % 100, uid, 0)
        if shake_money > 0:
            reward = {'chip': shake_money}
            final_info = props.BirdProps.issue_rewards(uid, self.gid, reward, 'activity.shake.reward', True)
            Context.RedisActivity.hash_incrby('activity:shake:%d' % 100, uid, -shake_money)
            mo.set_param('ret', 0)
            mo.set_param('final', final_info)
        else:
            mo.set_param('ret', 1)
        return mo

    def query_shake_record(self, mi):
        start = str(mi.get_param('start'))
        end = str(mi.get_param('end'))

        start_day = Time.str_to_timestamp(start)
        end_day = Time.str_to_timestamp(end)

        keys = Context.RedisActivity.hget_keys('activity:shake:*')
        info = []
        for i in keys:
            sid = i.split('activity:shake:')[1]
            tmp = {}
            if start_day < int(sid)/1000 <= end_day:
                data = Context.RedisActivity.hash_getall(i)
                detail = Context.json_loads(data.get('detail'))
                tmp['sid'] = sid
                tmp['start'] = detail.get('start')
                tmp['end'] = detail.get('end')
                tmp['way'] = detail.get('way')
                tmp['money'] = detail.get('money')
                tmp['rebate'] = detail.get('rebate')
                player_data = {}
                for k, v in data.items():
                    if k == 'detail':
                        continue
                    v = Context.json_loads(v)
                    player_data[k] = v
                tmp['pd'] = player_data
                info.append(tmp)
        return info

class PayRankActivity(object):
    def __init__(self):
        self.gid = 2
        self.tid = 1000
        self.activity_pay_rank_list = []

    def activity_pay_rank_config(self):
        activity_pay_rank_data = Context.RedisActivity.get('pay_rank.activity.config')
        if activity_pay_rank_data == None:
            activity_pay_rank_data = None
        else:
            activity_pay_rank_data = Context.json_loads(activity_pay_rank_data)
        return activity_pay_rank_data

    def judge_pay_rank_activity_open(self):
        cnf = self.activity_pay_rank_config()
        if not cnf:
            return False
        if not check_activity_in(cnf['start'], cnf['end'], 0):
            return False
        return True

    def incr_user_pay_rank_value(self, uid, value):
        if not self.judge_pay_rank_activity_open():
            return
        cnf = self.activity_pay_rank_config()
        c_list = cnf.get('channel')
        cid = Context.Data.get_attr(uid, 'loginChannelId')
        if cid not in c_list:
            return
        # if type != self.activity_rank_config['type']:
        #     return
        start = cnf.get('start')
        key = 'activity:%s:%s' % ('pay_rank', start[:10])
        Context.RedisActivity.hash_incrby(key, uid, value)
        return

    def get_pay_rank_activity_config(self, uid, gid):
        if not self.judge_pay_rank_activity_open():
            return
        i = self.activity_pay_rank_config()
        c_list = i.get('channel')
        cid = Context.Data.get_attr(uid, 'loginChannelId')
        if cid not in c_list:
            return
        start = i['start']
        end = i['end']
        d = {}
        d['id'] = i['id']
        d['t'] = i['model']
        d['s'] = start
        d['e'] = end
        d['n'] = i['name']
        d['d'] = i['desc']
        l, index, point = self.get_activity_pay_rank_list(uid)
        if l != None and index != None and point != None:
            d['rl'] = l
            d['ix'] = index
            d['pnt'] = int(point)
        return d

    def get_activity_pay_rank_list(self, uid):
        if not self.judge_pay_rank_activity_open():
            return None, None, None
        info = []
        index = -1
        conf = self.activity_pay_rank_config()
        start = conf.get('start')
        key = 'activity:%s:%s' % ('pay_rank', start[:10])
        point = Context.RedisActivity.hash_get_int(key, uid, 0)
        l = self.activity_pay_rank_list
        if self.activity_pay_rank_list == None:
            l = []
        for k, v in enumerate(l):
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
                vip_level = account.BirdAccount.get_vip_level(int(v[0]), self.gid)
            except:
                vip_level = 0
            level = -1
            for i, j in enumerate(conf['level']):
                if k + 1 in j:
                    level = i
            if level < 0:
                continue
            r_data = conf['reward'][level]
            if r_data.has_key('product'):
                reward_type = 1
                reward = r_data.get('product')
            elif r_data.has_key('virtual'):
                reward_type = 2
                reward = props.BirdProps.convert_reward(r_data.get('virtual'))
            else:
                continue
            if int(v[0]) == uid:
                index = k
            rank = {
                'rank': int(k),
                'id': int(v[0]),
                'nick': nick,
                'sex': int(sex),
                'avatar': avatar,
                'vip': int(vip_level),
                'point': int(v[1]),
                'reward': reward,
                'retp':reward_type
            }
            info.append(rank)
        return info, index, point

    def query_background_pay_rank_record(self, s, e, c = None):
        key = 'activity:%s:*' % ('pay_rank')
        lst = Context.RedisActivity.hget_keys(key)
        ret = []
        for i in lst:
            start, refresh_time, channel = Context.RedisActivity.hash_mget(i, 'start', 'refresh_time', 'channel')
            if c != None and c not in channel:
                continue
            if int(start) < s or int(start) >= e:
                continue
            aid = i.split('activity:%s:'%('pay_rank'))[1]
            detail = self.query_background_pay_rank_detail(aid)
            info = {'start': start, 'end': refresh_time, 'channel':Context.json_loads(channel), 'detail': detail}
            ret.append(info)
        return ret

    def query_background_pay_rank_detail(self, aid):
        info = []
        conf = self.activity_pay_rank_config()
        count = conf.get('count')
        key = 'activity:%s:%s' % ('pay_rank', aid[:10])
        lst = Context.RedisActivity.hash_getall(key)
        if lst.has_key('refresh_time'):
            del lst['refresh_time']
        if lst.has_key('start'):
            del lst['start']
        if lst.has_key('channel'):
            del lst['channel']
        if lst.has_key('send_reward'):
            del lst['send_reward']
        if lst.has_key('conf'):
            conf = Context.json_loads(lst.get('conf'))
            count = conf.get('count')
            del lst['conf']

        l = sorted(lst.items(), key=lambda x: int(x[1]), reverse=True)
        if len(l) >= count:
            l = l[:count]

        for k, v in enumerate(l):
            try:
                nick = Context.Data.get_attr(int(v[0]), 'nick')
                if not nick:
                    nick = ''
                nick = Context.hide_name(nick)
            except:
                nick = ''
            try:
                phone = Context.Data.get_shop_attr(int(v[0]), 'shop:user', 'phone')
                if not phone:
                    idType = Context.Data.get_attr(int(v[0]), 'idType')
                    if idType == 13:
                        phone = Context.Data.get_attr(int(v[0]), 'userName')
                    else:
                        phone = ''
            except:
                phone = ''
            try:
                channel_id = Context.Data.get_attr(int(v[0]), 'loginChannelId')
            except:
                channel_id = ''
            try:
                vip_level = account.BirdAccount.get_vip_level(int(v[0]), self.gid)
            except:
                vip_level = 0
            level = -1
            for i, j in enumerate(conf['level']):
                if k + 1 in j:
                    level = i
            if level < 0:
                continue
            r_data = conf['reward'][level]
            if r_data.has_key('product'):
                reward_type = 1
                reward = r_data.get('product')
            elif r_data.has_key('virtual'):
                reward_type = 2
                reward = props.BirdProps.convert_reward(r_data.get('virtual'))
            else:
                continue
            rank = {
                'rank': int(k),
                'id': int(v[0]),
                'nick': nick,
                'vip': int(vip_level),
                'point': int(v[1]),
                'reward': reward,
                'retp':reward_type,
                'cid':channel_id,
                'phone': phone,
            }
            info.append(rank)
        ret = {'aid':aid, 'info':info}
        return ret

    #设置排行榜数据
    def set_rank_list(self):
        conf = self.activity_pay_rank_config()
        start = conf.get('start')
        key = 'activity:%s:%s' % ('pay_rank', start[:10])
        lst = Context.RedisActivity.hash_getall(key)
        if lst.has_key('refresh_time'):
            del lst['refresh_time']
        if lst.has_key('start'):
            del lst['start']
        if lst.has_key('channel'):
            del lst['channel']
        if lst.has_key('send_reward'):
            del lst['send_reward']
        if lst.has_key('conf'):
            del lst['conf']
        if conf == None:
            return []
        count = conf['count']
        self.activity_pay_rank_list = sorted(lst.items(), key=lambda x: int(x[1]), reverse=True)
        if len(self.activity_pay_rank_list) >= count:
            self.activity_pay_rank_list = self.activity_pay_rank_list[:count]
        return self.activity_pay_rank_list

    def deal_activity_pay_rank(self):
        conf = self.activity_pay_rank_config()
        if not conf:
            return
        start = conf.get('start')
        key = 'activity:%s:%s' % ('pay_rank', start[:10])
        start, refresh_time, channel, send_reward = Context.RedisActivity.hash_mget(key, 'start', 'refresh_time', 'channel', 'send_reward')
        end = conf['end']
        end_ts = Time.str_to_timestamp(end)
        if refresh_time == None or start == None or channel == None:
            start = conf['start']
            start_ts = Time.str_to_timestamp(start)
            channel = Context.json_dumps(conf['channel'])
            Context.RedisActivity.hash_mset(key, 'refresh_time', end_ts, 'start', start_ts, 'channel', channel)
            return

        now_ts = Time.current_ts()
        ret_list = []
        if send_reward == None:
            ret_list = self.set_rank_list()
        if now_ts > int(end_ts) and send_reward == None:
            if ret_list != None and len(ret_list) > 0 :
                # 发放奖励
                for k, v in enumerate(ret_list):
                    level = -1
                    for i, j in enumerate(conf['level']):
                        if k + 1 in j:
                            level = i
                    if level < 0:
                        continue
                    r_data = conf['reward'][level]
                    if r_data.has_key('product'):
                        reward = r_data.get('product')
                        reward_p = {'tips': u'%s，请联系客服领取奖励'%(reward['name'])}
                        ret = mail.Mail.add_mail(int(v[0]), self.gid, now_ts, 14, reward_p, -(k + 1))
                        if ret:
                            mail.Mail.send_mail_list(int(v[0]), self.gid)
                    elif r_data.has_key('virtual'):
                        reward = r_data.get('virtual')
                        ret = mail.Mail.add_mail(int(v[0]), self.gid, now_ts, 14, reward, -(k + 1))
                        if ret:
                            mail.Mail.send_mail_list(int(v[0]), self.gid)

                Context.RedisActivity.hash_set(key, 'send_reward', 1)
                Context.RedisActivity.hash_set(key, 'conf', Context.json_dumps(conf))
                self.activity_pay_rank_list = []

                # ret = Context.Activity.get_activity_all_data(self.tid, 'pay_rank')
                # for i in ret.keys():
                #     Context.Activity.del_activity_data(self.tid, 'pay_rank', i)
                # if len(ret) > 0:
                #     Context.save_cache('activity_pay_rank', str(Time.current_ts()), ret)
                # if conf:
                #     end = conf['end']
                #     end_ts = Time.str_to_timestamp(end)
                #     Context.Activity.set_activity_data(self.tid, 'rank', 'refresh_time', end_ts)

        return

    def on_pay_rank_timer(self):
        self.deal_activity_pay_rank()
        return

class PointShopActivity(object):
    def __init__(self):
        self.gid = 2
        self.activity_point_shop_list = []

    def activity_point_shop_config(self):
        activity_point_shop_data = Context.RedisActivity.get('point_shop.activity.config')
        if activity_point_shop_data == None:
            activity_point_shop_data = None
        else:
            activity_point_shop_data = Context.json_loads(activity_point_shop_data)
        return activity_point_shop_data

    def judge_point_shop_activity_open(self):
        cnf = self.activity_point_shop_config()
        if not cnf:
            return False
        if not check_activity_in(cnf['start'], cnf['end'], 0):
            return False
        return True

    def incr_user_point_shop_value(self, uid, value, cnf):
        start = cnf.get('start')
        key = 'activity:point_shop:%s:%s' % (start[:10], 'point_shop')
        Context.RedisActivity.hash_incrby(key, uid, value)
        return

    def incr_user_recharge(self, uid, value):
        if not self.judge_point_shop_activity_open():
            return
        cnf = self.activity_point_shop_config()
        c_list = cnf.get('channel')
        cid = Context.Data.get_attr(uid, 'loginChannelId')
        if cid not in c_list:
            return
        v = int(value*451/30)
        self.incr_user_point_shop_value(uid, v, cnf)
        return

    def incr_user_shot(self, uid, value):
        if not self.judge_point_shop_activity_open():
            return
        cnf = self.activity_point_shop_config()
        c_list = cnf.get('channel')
        cid = Context.Data.get_attr(uid, 'loginChannelId')
        if cid not in c_list:
            return
        start = cnf.get('start')
        key = 'activity:point_shop:%s:%s' % (start[:10], 'shot_point')
        curent_point = Context.RedisActivity.hash_get_int(key, uid, 0)
        shot_point = Context.RedisActivity.hash_incrby(key, uid, value)
        shot_value = cnf.get('shot_value')
        if curent_point/shot_value != shot_point/shot_value:
            v = cnf.get('shot_add')
            self.incr_user_point_shop_value(uid, v, cnf)
        return

    def get_point(self, uid):
        if not self.judge_point_shop_activity_open():
            return 0
        cnf = self.activity_point_shop_config()
        c_list = cnf.get('channel')
        cid = Context.Data.get_attr(uid, 'loginChannelId')
        if cid not in c_list:
            return 0
        start = cnf.get('start')
        key = 'activity:point_shop:%s:%s' % (start[:10], 'point_shop')
        key_use = 'activity:point_shop:%s:%s' % (start[:10], 'point_use')
        total_point = Context.RedisActivity.hash_get_int(key, uid, 0)
        use_point = Context.RedisActivity.hash_get_int(key_use, uid, 0)
        return total_point-use_point

    def incr_user_use_point(self, uid, point):
        if not self.judge_point_shop_activity_open():
            return 0
        cnf = self.activity_point_shop_config()
        c_list = cnf.get('channel')
        cid = Context.Data.get_attr(uid, 'loginChannelId')
        if cid not in c_list:
            return 0
        start = cnf.get('start')
        key_use = 'activity:point_shop:%s:%s' % (start[:10], 'point_use')
        point = Context.RedisActivity.hash_incrby(key_use, uid, point)
        return point

    def get_point_shop_activity_config(self, uid, gid):
        if not self.judge_point_shop_activity_open():
            return
        i = self.activity_point_shop_config()
        c_list = i.get('channel')
        cid = Context.Data.get_attr(uid, 'loginChannelId')
        if cid not in c_list:
            return
        start = i['start']
        end = i['end']
        d = {}
        d['id'] = i['id']
        d['t'] = i['model']
        d['s'] = start
        d['e'] = end
        d['n'] = i['name']
        d['d'] = i['desc']
        l, index, point = self.get_activity_point_shop_list(uid)
        if l != None and index != None and point != None:
            d['rl'] = l
            d['ix'] = index
            d['pnt'] = int(point)
        return d

    def get_activity_point_shop_list(self, uid):
        if not self.judge_point_shop_activity_open():
            return None, None, None
        info = []
        index = -1
        conf = self.activity_point_shop_config()
        start = conf.get('start')
        key = 'activity:point_shop:%s:%s' % (start[:10], 'point_shop')
        point = Context.RedisActivity.hash_get_int(key, uid, 0)
        l = self.activity_point_shop_list
        if self.activity_point_shop_list == None:
            l = []
        for k, v in enumerate(l):
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
                vip_level = account.BirdAccount.get_vip_level(int(v[0]), self.gid)
            except:
                vip_level = 0
            level = -1
            for i, j in enumerate(conf['level']):
                if k + 1 in j:
                    level = i
            if level < 0:
                continue
            r_data = conf['reward'][level]
            if r_data.has_key('product'):
                reward_type = 1
                reward = r_data.get('product')
            elif r_data.has_key('virtual'):
                reward_type = 2
                reward = props.BirdProps.convert_reward(r_data.get('virtual'))
            else:
                continue
            if int(v[0]) == uid:
                index = k
            rank = {
                'rank': int(k),
                'id': int(v[0]),
                'nick': nick,
                'sex': int(sex),
                'avatar': avatar,
                'vip': int(vip_level),
                'point': int(v[1]),
                'reward': reward,
                'retp':reward_type
            }
            info.append(rank)
        return info, index, point

    def query_background_point_shop_record(self, s, e, c = None):
        key = 'activity:point_shop:*:point_shop'
        lst = Context.RedisActivity.hget_keys(key)
        ret = []
        for i in lst:
            start, refresh_time, channel = Context.RedisActivity.hash_mget(i, 'start', 'refresh_time', 'channel')
            if c != None and c not in channel:
                continue
            if int(start) < s or int(start) >= e:
                continue
            aid = i.split(':')[2]
            detail = self.query_background_point_shop_detail(aid)
            info = {'start': start, 'end': refresh_time, 'channel':Context.json_loads(channel), 'detail': detail}
            ret.append(info)
        return ret

    def query_background_point_shop_detail(self, aid):
        info = []
        conf = self.activity_point_shop_config()
        count = 50#conf.get('count')
        key = 'activity:point_shop:%s:%s' % (aid[:10], 'point_shop')
        lst = Context.RedisActivity.hash_getall(key)
        if lst.has_key('refresh_time'):
            del lst['refresh_time']
        if lst.has_key('start'):
            del lst['start']
        if lst.has_key('channel'):
            del lst['channel']
        if lst.has_key('send_reward'):
            del lst['send_reward']
        if lst.has_key('conf'):
            conf = Context.json_loads(lst.get('conf'))
            count = 50#conf.get('count')
            del lst['conf']

        l = sorted(lst.items(), key=lambda x: int(x[1]), reverse=True)
        if len(l) >= count:
            l = l[:count]

        for k, v in enumerate(l):
            uid = int(v[0])
            try:
                nick = Context.Data.get_attr(uid, 'nick')
                if not nick:
                    nick = ''
                nick = Context.hide_name(nick)
            except:
                nick = ''
            try:
                phone = Context.Data.get_shop_attr(uid, 'shop:user', 'phone')
                if not phone:
                    idType = Context.Data.get_attr(uid, 'idType')
                    if idType == 13:
                        phone = Context.Data.get_attr(uid, 'userName')
                    else:
                        phone = ''
            except:
                phone = ''
            try:
                channel_id = Context.Data.get_attr(uid, 'loginChannelId')
            except:
                channel_id = ''
            try:
                vip_level = account.BirdAccount.get_vip_level(uid, self.gid)
            except:
                vip_level = 0
            level = -1
            for i, j in enumerate(conf['level']):
                if k + 1 in j:
                    level = i
            if level < 0:
                reward_type = 0
                reward = {}
            else:
                r_data = conf['reward'][level]
                if r_data.has_key('product'):
                    reward_type = 1
                    reward = r_data.get('product')
                elif r_data.has_key('virtual'):
                    reward_type = 2
                    reward = props.BirdProps.convert_reward(r_data.get('virtual'))
                else:
                    continue
            shot_key = 'activity:point_shop:%s:%s' % (aid[:10], 'shot_point')
            shot_p = Context.RedisActivity.hash_get_int(shot_key, uid, 0)
            shot_value = conf.get('shot_value')
            shot_point = int(shot_p/shot_value)
            key_use = 'activity:point_shop:%s:%s' % (aid[:10], 'point_use')
            use_point = Context.RedisActivity.hash_get_int(key_use, uid, 0)
            rank = {
                'rank': int(k),
                'id': uid,
                'nick': nick,
                'vip': int(vip_level),
                'point': int(v[1]),
                'shot_point': shot_point,
                'use_point': use_point,
                'reward': reward,
                'retp':reward_type,
                'cid':channel_id,
                'phone': phone,
            }
            info.append(rank)
        ret = {'aid':aid, 'info':info}
        return ret

    #设置排行榜数据
    def set_rank_list(self):
        conf = self.activity_point_shop_config()
        start = conf.get('start')
        key = 'activity:point_shop:%s:%s' % (start[:10], 'point_shop')
        lst = Context.RedisActivity.hash_getall(key)
        if lst.has_key('refresh_time'):
            del lst['refresh_time']
        if lst.has_key('start'):
            del lst['start']
        if lst.has_key('channel'):
            del lst['channel']
        if lst.has_key('send_reward'):
            del lst['send_reward']
        if lst.has_key('conf'):
            del lst['conf']
        if conf == None:
            return []
        count = conf['count']
        self.activity_point_shop_list = sorted(lst.items(), key=lambda x: int(x[1]), reverse=True)
        if len(self.activity_point_shop_list) >= count:
            self.activity_point_shop_list = self.activity_point_shop_list[:count]
        return self.activity_point_shop_list

    def deal_activity_point_shop(self):
        conf = self.activity_point_shop_config()
        if not conf:
            return
        start = conf.get('start')
        key = 'activity:point_shop:%s:%s' % (start[:10], 'point_shop')
        start, refresh_time, channel, send_reward = Context.RedisActivity.hash_mget(key, 'start', 'refresh_time', 'channel', 'send_reward')
        if refresh_time == None or start == None or channel == None:
            end = conf['end']
            end_ts = Time.str_to_timestamp(end)
            start = conf['start']
            start_ts = Time.str_to_timestamp(start)
            channel = Context.json_dumps(conf['channel'])
            Context.RedisActivity.hash_mset(key, 'refresh_time', end_ts, 'start', start_ts, 'channel', channel)
            return

        now_ts = Time.current_ts()
        ret_list = []
        if send_reward == None:
            ret_list = self.set_rank_list()
        if now_ts > int(refresh_time) and send_reward == None:
            if ret_list != None and len(ret_list) > 0 :
                # 发放奖励
                for k, v in enumerate(ret_list):
                    level = -1
                    for i, j in enumerate(conf['level']):
                        if k + 1 in j:
                            level = i
                    if level < 0:
                        continue
                    r_data = conf['reward'][level]
                    if r_data.has_key('product'):
                        reward = r_data.get('product')
                        reward_p = {'tips': u'%s，请联系客服领取奖励'%(reward['name'])}
                        ret = mail.Mail.add_mail(int(v[0]), self.gid, now_ts, 15, reward_p, -(k + 1))
                        if ret:
                            mail.Mail.send_mail_list(int(v[0]), self.gid)
                    elif r_data.has_key('virtual'):
                        reward = r_data.get('virtual')
                        ret = mail.Mail.add_mail(int(v[0]), self.gid, now_ts, 15, reward, -(k + 1))
                        if ret:
                            mail.Mail.send_mail_list(int(v[0]), self.gid)

                Context.RedisActivity.hash_set(key, 'send_reward', 1)
                Context.RedisActivity.hash_set(key, 'conf', Context.json_dumps(conf))
                self.activity_point_shop_list = []

        return

    def on_point_shop_timer(self):
        self.deal_activity_point_shop()
        return

    def get_point_shop_config(self, uid, gid):
        conf = Shop.get_point_shop_info(uid, gid)
        point = self.get_point(uid)
        mo = MsgPack(Message.MSG_SYS_GET_POINT_SHOP_CONFIG | Message.ID_ACK)
        mo.set_param('cnf', conf)
        mo.set_param('point', point)
        return mo

    def get_key(self):
        config = self.activity_point_shop_config()
        if not config:
            return
        start = config.get('start')
        return start[:10]

    def get_activity_point(self, uid, aid):
        key = 'activity:point_shop:%s:%s' % (aid, 'point_shop')
        key_use = 'activity:point_shop:%s:%s' % (aid, 'point_use')
        total_point = Context.RedisActivity.hash_get_int(key, uid, 0)
        use_point = Context.RedisActivity.hash_get_int(key_use, uid, 0)
        surplus_point = total_point-use_point
        return total_point, use_point, surplus_point

class SmashEggActivity(object):
    def __init__(self):
        self.gid = 2

    def activity_smash_egg_config(self):
        activity_smash_egg_data = Context.RedisActivity.get('smash_egg.activity.config')
        if activity_smash_egg_data == None:
            activity_smash_egg_data = None
        else:
            activity_smash_egg_data = Context.json_loads(activity_smash_egg_data)
        return activity_smash_egg_data

    def judge_smash_egg_activity_open(self):
        cnf = self.activity_smash_egg_config()
        if not cnf:
            return False
        if not check_activity_in(cnf['start'], cnf['end'], 0):
            return False
        return True

    def get_smash_egg_activity_config(self, uid, gid):
        if not self.judge_smash_egg_activity_open():
            return {}
        i = self.activity_smash_egg_config()
        # switch = i.get('detail', {}).get('switch', 0)
        # if switch <= 0:
        #     return {}
        start = i['start']
        end = i['end']
        d = {}
        d['id'] = i['id']
        d['t'] = i['model']
        d['s'] = start
        d['e'] = end
        d['n'] = i['name']
        d['d'] = i['desc']
        rw = i['reward']
        aid = start[:10]
        th = Context.RedisActivity.hash_get_int('game:smash_egg:%s:hammer' % aid, uid, 0)
        pt = Context.RedisActivity.hash_get_int('game:smash_egg:%s:pay' % aid, uid, 0)
        d['py'] = pt
        d['th'] = th
        d['pay'] = i['pay']
        d['add_hammer'] = i.get('add_hammer', 1)
        d['rw'] = self.get_reward_list(rw)
        return d

    def get_reward_list(self, rw):
        reward = []
        for k,v in rw.items():
            if int(k) == 9:
                continue
            rwd = self.get_reward(int(k), 1)
            reward.append(rwd)
        return reward

    def pay_set(self, uid, pay_num):
        if not self.judge_smash_egg_activity_open():
            return
        i = self.activity_smash_egg_config()
        # switch = i.get('detail', {}).get('switch', 0)
        # if switch <= 0:
        #     return
        c_list = i.get('channel')
        cid = Context.Data.get_attr(uid, 'loginChannelId')
        if cid not in c_list:
            return 0
        start = i['start']
        aid = start[:10]
        pay = i['pay']
        add_hammer = i.get('add_hammer', 1)
        pay_total_num = Context.RedisActivity.hash_incrby('game:smash_egg:%s:pay'%aid, uid, pay_num)
        hammer = (int(pay_total_num / pay) - int((pay_total_num - pay_num) / pay)) * add_hammer
        if hammer >= 1:
            total_hammer = Context.RedisActivity.hash_incrby('game:smash_egg:%s:hammer' % aid, uid, hammer)
        return

    def start_game(self, uid, gid, mi):
        if not self.judge_smash_egg_activity_open():
            return
        i = self.activity_smash_egg_config()
        c_list = i.get('channel')
        cid = Context.Data.get_attr(uid, 'loginChannelId')
        if cid not in c_list:
            return 0
        start = i['start']
        aid = start[:10]
        total_hammer = Context.RedisActivity.hash_get_int('game:smash_egg:%s:hammer' % aid, uid, 0)
        dat = Context.RedisActivity.hash_getall('game:smash_egg:%s:game:%d' %(aid, uid))
        mo = MsgPack(Message.MSG_SYS_ACTIVITY_SMASH_EGG_START | Message.ID_ACK)
        if dat == None:
            egg_list = []
            reward = []
            count = 0
            value = 0
            Context.RedisActivity.hash_mset('game:smash_egg:%s:game:%d' % (aid, uid), 'egg_list',
                                                           Context.json_dumps(egg_list), 'reward',
                                                           Context.json_dumps(reward), 'count', count, 'value', value)
            mo.set_param('th', total_hammer)
            mo.set_param('el', egg_list)
            mo.set_param('rw', reward)
            mo.set_param('c', count)
        else:
            egg_list = Context.json_loads(dat.get('egg_list', '[]'))
            reward = Context.json_loads(dat.get('reward', '[]'))
            count = dat.get('count', 0)
            mo.set_param('th', total_hammer)
            mo.set_param('el', egg_list)
            mo.set_param('rw', reward)
            mo.set_param('c', count)
        return mo

    def smash_egg(self, uid, gid, mi):
        i = self.activity_smash_egg_config()
        start = i['start']
        aid = start[:10]

        dat = Context.RedisActivity.hash_getall('game:smash_egg:%s:game:%d' % (aid, uid))
        total_hammer = Context.RedisActivity.hash_get_int('game:smash_egg:%s:hammer' % aid, uid, 0)
        mo = MsgPack(Message.MSG_SYS_ACTIVITY_SMASH_EGG_ACTION | Message.ID_ACK)
        if total_hammer <= 0:
            return mo.set_error(1, u"可玩次数不够")
        egg = mi.get_param('egg')

        egg_list = Context.json_loads(dat.get('egg_list', '[]'))
        if egg in egg_list:
            return mo.set_error(1, u"这个鸟蛋已经被砸开")
        egg_list.append(egg)
        index, min, max = self.random_egg(i['reward'])
        if index == None:
            return mo.set_error(1, u"配置错误")

        total_hammer = Context.RedisActivity.hash_incrby('game:smash_egg:%s:hammer' % aid, uid, -1)

        value = Tool.to_int(dat.get('value'), 0)
        pay = i.get('pay')
        ret = i.get('return')
        add_hammer = i.get('add_hammer', 1)

        pay_ret = int(pay * ret * 5000/100/add_hammer)
        pool = self.incr_pool(uid, pay_ret, i)
        if int(index) == 9:
            Context.RedisActivity.delete('game:smash_egg:%s:game:%d' % (aid, uid))
            mo.set_param('th', total_hammer)
            mo.set_param('egg', 9)
            return mo
        count = Tool.to_int(dat.get('count'), 0)
        if count >= 8:
            Context.RedisActivity.delete('game:smash_egg:%s:game:%d' % (aid, uid))
            mo.set_param('th', total_hammer)
            mo.set_param('egg', 9)
            return mo
        elif count == 0:
            rand = random.randint(min, max)
            rw = self.get_reward(index, rand)
        else:
            t_value = int(value*1.2)
            rw = self.get_reward_value(index,t_value)
        rw_price = props.BirdProps.get_props_price(rw)

        reward = Context.json_loads(dat.get('reward', '[]'))
        reward.append({'egg':egg, 'rw':rw})

        reward_total = {}
        for i in reward:
            rwd = i.get('rw')
            reward_total = props.BirdProps.merge_reward(False, reward_total, rwd)

        total_price = props.BirdProps.get_props_price(reward_total)
        if total_price >= pool:
            Context.RedisActivity.delete('game:smash_egg:%s:game:%d' % (aid, uid))
            mo.set_param('th', total_hammer)
            mo.set_param('egg', 9)
            return mo

        count += 1
        value = rw_price
        Context.RedisActivity.hash_mset('game:smash_egg:%s:game:%d' % (aid, uid), 'egg_list',
                                        Context.json_dumps(egg_list), 'reward',
                                        Context.json_dumps(reward), 'count', count, 'value', value)
        mo.set_param('egg', index)
        mo.set_param('get_rw', rw)
        mo.set_param('total_rw', reward)
        mo.set_param('el', egg_list)
        mo.set_param('th', total_hammer)
        return mo

    def get_reward(self, index, t_value):
        rw = {}
        if index == 1:
            rw['chip'] = t_value
        elif index ==2:
            rw['diamond'] = t_value
        elif index ==3:
            rw['coupon'] = t_value
        elif index ==4:
            rw['props'] = [{'id':202, 'count':t_value}]
        elif index ==5:
            rw['props'] = [{'id': 203, 'count': t_value}]
        elif index ==6:
            rw['props'] = [{'id': 204, 'count': t_value}]
        elif index ==7:
            rw['props'] = [{'id': 205, 'count': t_value}]
        elif index ==8:
            rw['props'] = [{'id': 220, 'count': t_value}]
        return rw

    def get_reward_value(self, index, t_value):
        rw = {}
        if index == 1:
            rw['chip'] = t_value
        elif index ==2:
            count = t_value / 500
            if count <= 0:
                count = 1
            rw['diamond'] = count
        elif index ==3:
            count = t_value / 5000
            if count <= 0:
                count = 1
            rw['coupon'] = count
        elif index ==4:
            count = t_value / 2500
            if count <= 0:
                count = 1
            rw['props'] = [{'id':202, 'count':count}]
        elif index ==5:
            count = t_value / 25000
            if count <= 0:
                count = 1
            rw['props'] = [{'id': 203, 'count': count}]
        elif index ==6:
            count = t_value / 100000
            if count <= 0:
                count = 1
            rw['props'] = [{'id': 204, 'count': count}]
        elif index ==7:
            count = t_value / 2500
            if count <= 0:
                count = 1
            rw['props'] = [{'id': 205, 'count': count}]
        elif index ==8:
            count = t_value / 5000
            if count <= 0:
                count = 1
            rw['props'] = [{'id': 220, 'count': count}]
        return rw

    def random_egg(self, rw_list):
        R = int(random.random() * 10000)
        count = 10000
        l = sorted(rw_list.keys(), reverse=False)
        for i in l:
            count -= int(rw_list[i]['rate'])
            if R >= count:
                return int(i), rw_list[i]['min'], rw_list[i]['max'],
        return None, None, None

    def get_pool(self, uid, cnf):
        aid = cnf.get('start')[:10]
        pool = Context.RedisActivity.hash_get_int('game:smash_egg:%s:pool' % aid, uid, 0)
        return pool

    def set_pool(self, uid, value, cnf):
        aid = cnf.get('start')[:10]
        pool = Context.RedisActivity.hash_set('game:smash_egg:%s:pool' % aid, uid, value)
        return pool

    def incr_pool(self, uid, value, cnf):
        aid = cnf.get('start')[:10]
        pool = Context.RedisActivity.hash_incrby('game:smash_egg:%s:pool' % aid, uid, value)
        return pool

    def deal_reward(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_ACTIVITY_SMASH_EGG_REWARD | Message.ID_ACK)
        conf = self.activity_smash_egg_config()
        start = conf['start']
        aid = start[:10]
        rw = Context.RedisActivity.hash_get_json('game:smash_egg:%s:game:%d' % (aid, uid), 'reward')
        if rw:
            reward_total = {}
            for i in rw:
                rwd = i.get('rw')
                reward_total = props.BirdProps.merge_reward(False, reward_total, rwd)
            total_price = props.BirdProps.get_props_price(reward_total)
            self.incr_pool(uid, -total_price, conf)
            final_info = props.BirdProps.issue_rewards(uid, self.gid, reward_total, 'activity.smash_egg.reward', True)

            nick = Context.Data.get_attr(uid, 'nick')
            nick = Context.hide_name(nick)
            desc_str = self.get_reward_str(reward_total)
            led = u'我的天呐！玩家<color=#00FF00FF>%s</color>在<color=#FF0000FF>活动-欢乐砸金蛋</color>中总共获得了<color=#FFFF00FF>%s</color>' % (
                nick, desc_str)
            mou = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
            mou.set_param('game', {'msg': led, 'ts': Time.current_ts() + 3, 'bulletin': 3})
            Context.GData.send_to_connect(uid, mou)

            Context.RedisActivity.delete('game:smash_egg:%s:game:%d' % (aid, uid))
            total_rw = Context.RedisActivity.hash_get_json('game:smash_egg:%s:reward' % aid, uid)
            reward = props.BirdProps.merge_reward(False, total_rw, reward_total)
            Context.RedisActivity.hash_set('game:smash_egg:%s:reward' % aid, uid, Context.json_dumps(reward))
            Context.RedisActivity.set('game:smash_egg:%s' % aid, Context.json_dumps(conf))
            mo.set_param('f', final_info)
            return mo
        else:
            return mo.set_error(1, u'你还没有开始游戏')

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
                _ = props.BirdProps.get_props_desc(one['id']) + u'%d个' % one['count']
                desc.append(_)
        return u', '.join(desc)

    def get_activity_detail(self, s, e, c=None):
        key = 'game:smash_egg:*:reward'
        lst = Context.RedisActivity.hget_keys(key)
        ret = []
        for i in lst:
            aid = i.split(':')[2]
            conf_key = 'game:smash_egg:%s'%aid
            conf = Context.RedisActivity.get(conf_key)
            conf = Context.json_loads(conf)
            channel = conf.get('channel')
            start = conf.get('start')
            start_ts = Time.str_to_timestamp(start)
            end = conf.get('end')
            pay = conf.get('pay')
            end_ts = Time.str_to_timestamp(end)
            if c != None and c not in channel:
                continue
            if int(start_ts) < s or int(start_ts) >= e:
                continue
            detail = self.query_background_detail(aid, conf)
            info = {'start': start_ts, 'end': end_ts, 'channel': channel, 'pay': pay, 'detail': detail}
            ret.append(info)
        return ret

    def query_background_detail(self, aid, conf):
        info = []
        key = 'game:smash_egg:%s:reward' % (aid)
        lst = Context.RedisActivity.hash_getall(key)
        for k, v in lst.items():
            uid = int(k)
            try:
                nick = Context.Data.get_attr(uid, 'nick')
                if not nick:
                    nick = ''
                nick = Context.hide_name(nick)
            except:
                nick = ''
            try:
                phone = Context.Data.get_shop_attr(uid, 'shop:user', 'phone')
                if not phone:
                    idType = Context.Data.get_attr(uid, 'idType')
                    if idType == 13:
                        phone = Context.Data.get_attr(uid, 'userName')
                    else:
                        phone = ''
            except:
                phone = ''
            try:
                vip_level = account.BirdAccount.get_vip_level(uid, self.gid)
            except:
                vip_level = 0
            reward = props.BirdProps.get_props_price(Context.json_loads(v))
            rank = {
                'id': uid,
                'nick': nick,
                'vip': int(vip_level),
                'chip': reward,
                'phone': phone,
            }
            info.append(rank)
        ret = {'aid':aid, 'info':info}
        return ret

class DragonBoatActivity(object):
    def __init__(self):
        self.table = 'game:dragon_boat'
        self.gid = 2

    def activity_dragon_boat_config(self):
        dragon_boat_config = Context.RedisActivity.get('dragon.boat.config')
        if dragon_boat_config == None:
            dragon_boat_config = None
        else:
            dragon_boat_config = Context.json_loads(dragon_boat_config)
        return dragon_boat_config

    def judge_dragon_boat_activity_open(self):
        cnf = self.activity_dragon_boat_config()
        if not cnf:
            return False
        if not check_activity_in(cnf['start'], cnf['end'], 0):
            return False
        return True

    def judge_dragon_boat_activity_show(self):
        cnf = self.activity_dragon_boat_config()
        if not cnf:
            return False
        if not check_activity_in(cnf['start'], cnf['show_end'], 0):
            return False
        return True

    def get_dragon_boat_activity_config(self, uid, gid, red= None):
        if not self.activity_dragon_boat_config():
            return
        conf = self.activity_dragon_boat_config()
        start = conf['start']
        end = conf['end']
        d = {}
        d['id'] = conf['id']
        d['t'] = conf['model']
        d['s'] = start
        d['e'] = end
        d['n'] = conf['name']
        d['d'] = conf['desc']
        info = self.get_user_activity_data(conf, uid, red)
        d.update(info)
        return d

    def get_user_activity_data(self, conf, uid, red):
        aid = conf['start'][:10]
        info = {}
        an, bn, cn, dn = Context.RedisActivity.hash_mget('%s:%s:data:%d' % (self.table, aid, uid), 'A',
                                                                  'B', 'C', 'D')
        info['A'] = Tool.to_int(an, 0)
        info['B'] = Tool.to_int(bn, 0)
        info['C'] = Tool.to_int(cn, 0)
        info['D'] = Tool.to_int(dn, 0)
        rw_list = conf.get('rw_list')
        rst = []
        for k, v in rw_list.items():
            dat = {}
            dat['rw_id'] = k
            dat['need'] = v.get('need')
            if v.has_key('limit'):
                dat['limit'] = v.get('limit')
                exchange = Context.RedisActivity.hash_get_int('%s:%s:record:%d' % (self.table, aid, uid), k, 0)
                dat['exchange'] = exchange
            dat['rw'] = v.get('reward')
            rst.append(dat)
        info['rst'] = rst
        red_hot = red
        if red_hot == None:
            flag, red_hot = self.set_red(conf, uid)
        info['red'] = red_hot
        return info

    def exchange_reward(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_DRAGON_BOAT_RECV | Message.ID_ACK)
        conf = self.activity_dragon_boat_config()
        if not conf:
            return mo.set_error(1, u"活动配置错误")
        keys = mi.get_param('k')
        dat = conf.get('rw_list').get(keys)
        if not dat:
            return mo.set_error(1, u"活动配置错误")
        start = conf['start']
        aid = start[:10]
        an, bn, cn, dn = Context.RedisActivity.hash_mget('%s:%s:data:%d' % (self.table, aid, uid), 'A',
                                                                  'B', 'C', 'D')
        zongzi_dict = {
            'A': Tool.to_int(an, 0),
            "B": Tool.to_int(bn, 0),
            "C": Tool.to_int(cn, 0),
            "D": Tool.to_int(dn, 0),
        }
        flag = True
        ret = self.get_result(zongzi_dict, dat.get('need'))
        if dat.has_key('limit') and ret:
            limit = dat.get('limit')
            exchange = Context.RedisActivity.hash_get_int('%s:%s:record:%d' % (self.table, aid, uid), keys, 0)
            if exchange >= limit:
                flag = False
        if not ret:
            flag = False

        if not flag:
            return mo.set_error(2, u"粽子不够哦，使用越高的炮倍击败端午龙舟，掉落的粽子品质越高数量越多")

        for k,v in dat.get('need').items():
            Context.RedisActivity.hash_incrby('%s:%s:data:%d' % (self.table, aid, uid), k, -v)
            Context.RedisActivity.hash_incrby('%s:%s:record:%d' % (self.table, aid, uid), k, v)

        rw_count = Context.RedisActivity.hash_incrby('%s:%s:record:%d' % (self.table, aid, uid), keys, 1)
        final_info = props.BirdProps.issue_rewards(uid, self.gid, dat.get('reward'), 'activity.dragon_boat.reward', True)
        mo.set_param('rw_id', keys)
        mo.set_param('rc', rw_count)
        mo.set_param('f', final_info)

        total_rw = Context.RedisActivity.hash_get_json('%s:%s:record:%d' % (self.table, aid, uid), 'reward', {})
        reward = dat.get('reward')
        result_reward = props.BirdProps.merge_reward(False, total_rw, reward)
        Context.RedisActivity.hash_set('%s:%s:record:%d' % (self.table, aid, uid), 'reward', Context.json_dumps(result_reward))

        flag, red_hot = self.set_red(conf, uid, get = True)
        if flag:
            self.update_user_activity(uid, gid, red_hot)

        return mo

    def add_zongzi(self, conf, uid, gid, multiple, chip):
        actv_conf = self.activity_dragon_boat_config()
        if not actv_conf:
            return None, None
        price_dict = actv_conf.get('price')
        rate_conf = conf.get('rate')
        add_rate = conf.get('add_rate')
        random_rate = conf.get('random_rate')
        D_rate = (rate_conf.get('D') + multiple*float(add_rate))/100.0
        R = random.random()
        rp = int((random.randint(random_rate[0], random_rate[1]) / 100.0) * chip)
        if R < D_rate:
            num = int(rp/price_dict.get('D'))
            if num < 1:
                num = 1
            self.deal_reward(actv_conf, uid, gid, 'D', num)
            return 'D', num
        C_rate = D_rate + rate_conf.get('C')/100.0
        if R < C_rate:
            num = int(rp/price_dict.get('C'))
            if num < 1:
                num = 1
            self.deal_reward(actv_conf, uid, gid, 'C', num)
            return 'C', num
        B_rate = C_rate + rate_conf.get('B')/100.0
        if R < B_rate:
            num = int(rp/price_dict.get('B'))
            if num < 1:
                num = 1
            self.deal_reward(actv_conf, uid, gid, 'B', num)
            return 'B', num
        num = int(rp / price_dict.get('B'))
        if num < 1:
            num = 1
        self.deal_reward(actv_conf, uid, gid, 'A', num)
        return 'A', num

    def deal_reward(self, conf, uid, gid, zongzi, count):
        start = conf['start']
        aid = start[:10]
        chip_pool = conf.get('price').get(zongzi)*count
        primary_key = 'game.2.year_monster'
        Context.RedisMix.hash_incrby(primary_key, 'dragon_boat_pool', -chip_pool)
        Context.RedisActivity.hash_incrby('%s:%s:data:%d'%(self.table, aid, uid), zongzi, count)
        Context.RedisActivity.hash_setnx('%s:%s:record:%d' % (self.table, aid, uid), 'start', aid)
        Context.RedisActivity.hash_setnx('%s:%s:record:%d' % (self.table, aid, uid), 'end', conf['end'][:10])
        flag, red_hot = self.set_red(conf, uid, get = True)
        if flag:
            self.update_user_activity(uid, gid, red_hot)
        return

    def set_red(self, conf, uid, get = False):
        start = conf['start']
        aid = start[:10]
        red_hot =  Context.RedisActivity.hash_get_int('%s:%s:data:%d' % (self.table, aid, uid), 'red_hot', 0)
        if red_hot > 0 and get:
            return False, red_hot
        an, bn, cn, dn = Context.RedisActivity.hash_mget('%s:%s:data:%d' % (self.table, aid, uid), 'A',
                                                                  'B', 'C', 'D')
        red_hot = Tool.to_int(red_hot, 0)
        zongzi_dict = {
            'A': Tool.to_int(an, 0),
            "B": Tool.to_int(bn, 0),
            "C": Tool.to_int(cn, 0),
            "D": Tool.to_int(dn, 0),
        }
        rw_list = conf.get('rw_list')
        flag = False
        for k, v in rw_list.items():
            ret = self.get_result(zongzi_dict, v.get('need'))
            if v.has_key('limit') and ret:
                limit = v.get('limit')
                exchange = Context.RedisActivity.hash_get_int('%s:%s:record:%d' % (self.table, aid, uid), k, 0)
                if exchange < limit:
                    flag = True
                    break
            elif not v.has_key('limit') and ret:
                flag = True
                break
        red_exchange = False
        if not flag and red_hot > 0:
            red_exchange = True
            red_hot = 0
        elif flag and red_hot <= 0:
            red_exchange = True
            red_hot = 1
        if red_exchange:
            Context.RedisActivity.hash_set('%s:%s:data:%d' % (self.table, aid, uid), 'red_hot', red_hot)
        return red_exchange, red_hot

    def get_result(self, d1, d2):
        for k, v in d2.items():
            if v > d1.get(k):
                return False
        return True

    def get_zongzi_name(self, zongzi):
        if 'A' == zongzi:
            return u'大枣粽子'
        elif 'B' == zongzi:
            return u'红豆粽子'
        elif 'C' == zongzi:
            return u'蛋黄粽子'
        elif 'D' == zongzi:
            return u'鲜肉粽子'
        return ''

    ##########   ------- 后台内容 -------    ########## start
    def update_user_activity(self, uid, gid, red):
        mo = MsgPack(Message.MSG_SYS_NEW_ACTIVITY_CONFIG | Message.ID_ACK)
        info = {}
        info['model'] = 19
        info['activity_info'] = self.get_dragon_boat_activity_config(uid, gid, red = red)
        mo.set_param('info', info)
        Context.GData.send_to_connect(uid, mo)
        return

    def query_dragon_boat(self, gid, mi, request):
        mo = MsgPack(0)
        cnf = self.activity_dragon_boat_config()
        if cnf == None:cnf = {}
        mo.set_param('ret', cnf)
        return mo

    def modify_dragon_boat(self, gid, mi, request):
        modify_cnf = mi.get_param('ret')

        if self.judge_dragon_boat_activity_open():
            cnf = self.activity_dragon_boat_config()
            if cnf.get('start') != modify_cnf.get('start'):
                return MsgPack.Error(0, 1, u'活动已开启，不可修改时间')

        Context.RedisActivity.set('dragon.boat.config', Context.json_dumps(modify_cnf))
        mou = MsgPack(Message.MSG_SYS_UPDATE_ACTIVITY_CONF | Message.ID_ACK)
        mou.set_param('model', 19)
        Context.GData.broadcast_to_system(mou)
        return MsgPack(0)

    def dragon_boat_pool_query(self, gid, mi, request):
        mo = MsgPack(0)
        primary_key = 'game.2.year_monster'
        pool_chip = Context.RedisMix.hash_get_int(primary_key, 'dragon_boat_pool', 0)
        mo.set_param("ret", pool_chip)
        return mo

    def dragon_boat_pool_modify(self, gid, mi, request):
        dt = mi.get_param('ret')
        primary_key = 'game.2.year_monster'
        pool_chip = Context.RedisMix.hash_incrby(primary_key, 'dragon_boat_pool', int(dt))
        mo = MsgPack(0)
        mo.set_param("ret", pool_chip)
        return mo

    def get_activity_detail(self, s, e):
        key = 'game:dragon_boat:*:data:*'
        lst = Context.RedisActivity.hget_keys(key)
        ret = {}

        date = set()

        for i in lst:
            aid = i.split(':')[2]
            start_ts = Time.str_to_timestamp(aid, '%Y-%m-%d')
            if int(start_ts) < s or int(start_ts) >= e:
                continue
            date.add(aid)
        for j in date:
            ks = 'game:dragon_boat:%s:data:*'%j
            lst = Context.RedisActivity.hget_keys(ks)
            date_data = {}
            for k in lst:
                inf = {}
                uid = Tool.to_int(k.split(':')[4])
                la, lb, lc, ld = Context.RedisActivity.hash_mget('%s:%s:data:%d'%(self.table, j, uid), 'A', 'B', 'C', 'D')
                ua, ub, uc, ud = Context.RedisActivity.hash_mget('%s:%s:record:%d' % (self.table, j, uid), 'A', 'B', 'C', 'D')
                reward, start, end = Context.RedisActivity.hash_mget('%s:%s:record:%d' % (self.table, j, uid), 'reward', 'start', 'end')
                inf['e'] = end
                if reward:
                    inf['rw'] = reward
                if la:
                    inf['la'] = la
                if lb:
                    inf['lb'] = lb
                if lc:
                    inf['lc'] = lc
                if ld:
                    inf['ld'] = ld
                if ua:
                    inf['ua'] = ua
                if ub:
                    inf['ub'] = ub
                if uc:
                    inf['uc'] = uc
                if ud:
                    inf['ud'] = ud

                try:
                    nick = Context.Data.get_attr(uid, 'nick')
                    if not nick:
                        nick = ''
                except:
                    nick = ''
                try:
                    phone = Context.Data.get_shop_attr(uid, 'shop:user', 'phone')
                    if not phone:
                        idType = Context.Data.get_attr(uid, 'idType')
                        if idType == 13:
                            phone = Context.Data.get_attr(uid, 'userName')
                        else:
                            phone = ''
                except:
                    phone = ''
                cid = Context.Data.get_attr(uid, 'loginChannelId')
                inf['c'] = cid
                inf['n'] = nick
                inf['p'] = phone
                date_data[uid] = inf
            ret[j] = date_data
        return ret


    ##########   ------- 后台内容 -------    ########## end

class TotalPayActivity(object):
    def __init__(self):
        self.gid = 2
        self.activity_key = 'total_pay'

    def get_activity_version(self):
        version = Context.RedisActivity.get('%s:current_version' % self.activity_key)
        version = Tool.to_int(version, 1000)
        return version

    def activity_total_pay_config(self, version):
        if not version:
            return
        activity_total_pay_data = Context.RedisActivity.get('%s:%d:config'%(self.activity_key, version))
        if activity_total_pay_data == None:
            activity_total_pay_data = None
        else:
            activity_total_pay_data = Context.json_loads(activity_total_pay_data)
        return activity_total_pay_data

    def get_config(self):
        version = self.get_activity_version()
        conf = self.activity_total_pay_config(version)
        mo = MsgPack(0)
        mo.set_param('c', conf)
        return mo

    def set_config(self, mi):
        version = Context.RedisActivity.get('%s:current_version' % self.activity_key)
        version = Tool.to_int(version, 1000)
        cg = mi.get_param('cg')
        if cg:
            version = version+1
        conf = mi.get_param('c')
        if conf:
            Context.RedisActivity.set('%s:current_version' % self.activity_key, version)
            Context.RedisActivity.set('%s:%d:config' % (self.activity_key, version), Context.json_dumps(conf))
        return MsgPack(0)

    def judge_activity_open(self, cnf):
        if not cnf:
            return False
        if not check_activity_in(cnf['start'], cnf['end'], 0):
            return False
        return True

    def get_user_activity_value(self, uid, version, conf):
        keys = '%s:%d:data:%d' % (self.activity_key, version, uid)
        pay_total, fresh_time= Context.RedisActivity.hash_mget(keys,'pay_total', 'fresh_time')
        current_ts = Time.current_ts()
        if not fresh_time:
            Context.RedisActivity.hash_mset(keys, 'pay_total', 0, 'fresh_time', current_ts)
            Context.RedisActivity.hash_set(keys, 'level', Context.json_dumps([0]*len(conf.get('info'))))
            return 0
        time_type = conf.get("time_type")
        flag = False
        if time_type == 1: #日刷新
            if time_type == 1:  # 开放类型为日开放
                rts = Time.timestamp_to_str(current_ts)
                if Time.is_today(rts):
                    flag = True

            elif time_type == 2:  # 开放类型为周开放
                wts = Time.current_week_start_ts()
                local_wts = Time.current_week_start_ts(current_ts)
                if wts == local_wts:
                    flag = True

            elif time_type == 3:
                lts = Time.current_localtime()
                local_wts = Time.current_localtime(current_ts)
                if lts.tm_year == local_wts.tm_year and lts.tm_mon == local_wts.tm_mon:
                    flag = True
        if not flag:
            Context.RedisActivity.hash_mset(keys, 'pay_total', 0, 'fresh_time', current_ts)
            Context.RedisActivity.hash_set(keys, 'level', Context.json_dumps([0]*len(conf.get('info'))))
            return 0

        pay_total = Tool.to_int(pay_total, 0)
        return pay_total

    def pay_set(self, uid, pay_num):
        version = self.get_activity_version()
        conf = self.activity_total_pay_config(version)
        if not self.judge_activity_open(conf):
            return
        channel = conf.get("channel")
        cid = Context.Data.get_attr(uid, 'loginChannelId')
        if cid not in channel:
            return
        pay_total = self.get_user_activity_value(uid, version, conf)
        pay = pay_total + pay_num
        Context.RedisActivity.hash_set('%s:%d:data:%d' % (self.activity_key, version, uid), 'pay_total', pay)
        return

    def get_pay_activity_config(self, uid, gid):
        version = self.get_activity_version()
        conf = self.activity_total_pay_config(version)
        if not self.judge_activity_open(conf):
            return
        keys = '%s:%d:data:%d' % (self.activity_key, version, uid)
        start = conf['start']
        end = conf['end']
        d = {}
        d['id'] = conf['id']
        d['model'] = conf['model']
        d['start'] = start
        d['end'] = end
        d['name'] = conf['name']
        d['desc'] = conf['desc']
        d['info'] = conf['info']
        pay_total = self.get_user_activity_value(uid, version, conf)
        level = Context.RedisActivity.hash_get_json(keys, 'level', [0]*len(conf.get('info')))
        red = 0
        for k,v in enumerate(conf['info']):
            if pay_total > v.get('pay') and level[k] <= 0:
                red = 1
                break
        d['pt'] = pay_total
        d['l'] = level
        d['r'] = red
        return d

    def on_recv_reward(self, uid, mi):
        mo = MsgPack(Message.MSG_SYS_ACTIVITY_TOTAL_PAY_RECV | Message.ID_ACK)
        version = self.get_activity_version()
        conf = self.activity_total_pay_config(version)
        if not self.judge_activity_open(conf):
            return mo.set_error(1, u'该活动已结束')
        level = mi.get_param('level')
        keys = '%s:%d:data:%d' % (self.activity_key, version, uid)
        pay_total = self.get_user_activity_value(uid, version, conf)
        level_list = Context.RedisActivity.hash_get_json(keys, 'level', [0]*len(conf.get('info')))

        info = conf['info'][level-1]

        if pay_total >= info.get('pay') and level_list[level - 1] <= 0:
            reward = info.get('re')
            final_info = props.BirdProps.issue_rewards(uid, self.gid, reward, 'activity.total_pay.recv', True)
            level_list[level-1] = 1
            Context.RedisActivity.hash_set(keys, 'level', Context.json_dumps(level_list))
            mo.set_param('f', final_info)
            mo.set_param('l', level_list)
            return mo
        return mo.set_error(2, u'未达到领取条件，无法领取')



DragonBoatActivity = DragonBoatActivity()
DiscountActivity = DiscountActivity()
ShareActivity = ShareActivity()
LoginActivity = LoginActivity()
RankActivity = RankActivity()
TaskActivity = TaskActivity()
PayActivity = PayActivity()
GiveActivity = GiveActivity()
DoubleActivity = DoubleActivity()
VipActivity = VipActivity()
SaveMoneyActivity = SaveMoneyActivity()
WxNewPlayerActivity = WxNewPlayerActivity()
ShakeActivity = ShakeActivity()
PayRankActivity = PayRankActivity()
PointShopActivity = PointShopActivity()
SmashEggActivity = SmashEggActivity()
TotalPayActivity = TotalPayActivity()
Activity = Activity()