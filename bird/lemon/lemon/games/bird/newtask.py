#!/usr/bin/env python
# -*- coding=utf-8 -*-

import random
from const import Message
import props
from framework.util.tool import Time
from framework.context import Context
from framework.entity.msgpack import MsgPack
import newactivity


class NewTask(object):
    def __init__(self):
        self.gid = 2
        self._task_201_config = None
        self._task_202_config = None
        self._task_203_config = None
        self._task_day_config = None
        self._task_week_config = None
        self._day_activity_config = None
        self._week_activity_config = None

    @property
    def task_201_config(self):
        if self._task_201_config is None:
            self._task_201_config = Context.Configure.get_game_item_json(self.gid, 'task.201.config')
        return self._task_201_config

    @property
    def task_202_config(self):
        if self._task_202_config is None:
            self._task_202_config = Context.Configure.get_game_item_json(self.gid, 'task.202.config')
        return self._task_202_config

    @property
    def task_203_config(self):
        if self._task_203_config is None:
            self._task_203_config = Context.Configure.get_game_item_json(self.gid, 'task.203.config')
        return self._task_203_config

    @property
    def task_day_config(self):
        if self._task_day_config is None:
            self._task_day_config = Context.Configure.get_game_item_json(self.gid, 'task.daily.config')
        return self._task_day_config

    @property
    def task_week_config(self):
        if self._task_week_config is None:
            self._task_week_config = Context.Configure.get_game_item_json(self.gid, 'task.week.config')
        return self._task_week_config

    @property
    def day_activity_config(self):
        if self._day_activity_config is None:
            self._day_activity_config = Context.Configure.get_game_item_json(self.gid, 'day.activity.config')
        return self._day_activity_config

    @property
    def week_activity_config(self):
        if self._week_activity_config is None:
            self._week_activity_config = Context.Configure.get_game_item_json(self.gid, 'week.activity.config')
        return self._week_activity_config

    def complete_task(self, uid, mi):
        mo = MsgPack(Message.MSG_SYS_RECEIVE_TASK_REWARD | Message.ID_ACK)
        task_id = mi.get_param('idx')
        task_type = int(mi.get_param('t'))
        info = {}
        if task_type == 1:
            l = self.get_day_task_list()
            m_l = self.get_user_day_task_list(uid)
            if str(task_id) not in l or not m_l.has_key(int(task_id)):
                return mo.set_error(1, u"该任务已失效")
            elif m_l[int(task_id)][3] > m_l[int(task_id)][4]:
                return mo.set_error(2, u"该任务还未完成")
            if not self.task_day_config.has_key(str(task_id)):
                return mo.set_error(3, u'没有该任务')
            if m_l[task_id][5] == 1:
                return mo.set_error(4, u'你已领取了该任务的奖励，无法再次领取')
            reward = self.task_day_config[str(task_id)][5]
            activity_value = int(self.task_day_config[str(task_id)][4])
            final_info = props.BirdProps.issue_rewards(uid, self.gid, reward, 'task.get', True)
            final = Context.Data.hincr_task_attr(uid, 'day', 'activity_value', activity_value)
            m_l[task_id][5] = 1
            Context.Data.set_task_attr(uid, 'day', str(task_id), Context.json_dumps(m_l[task_id]))
            info['tid'] = task_id
            info['rw'] = final_info
            info['av_d'] = final
            info['t'] = task_type

        elif task_type == 2:
            l = self.get_week_task_list()
            m_l = self.get_user_week_task_list(uid)
            if str(task_id) not in l or not m_l.has_key(int(task_id)):
                return mo.set_error(1, u"该任务已失效")
            elif m_l[int(task_id)][3] > m_l[int(task_id)][4]:
                return mo.set_error(2, u"该任务还未完成")
            if not self.task_week_config.has_key(str(task_id)):
                return mo.set_error(3, u'没有该任务')
            if m_l[task_id][5] == 1:
                return mo.set_error(4, u'你已领取了该任务的奖励，无法再次领取')
            reward = self.task_week_config[str(task_id)][5]
            activity_value = int(self.task_week_config[str(task_id)][4])
            final_info = props.BirdProps.issue_rewards(uid, self.gid, reward, 'task.get', True)
            final = Context.Data.hincr_task_attr(uid, 'week', 'activity_value', activity_value)
            # Context.Data.set_task_attr(100, 'week', 'week_time', Time.current_ts())
            m_l[task_id][5] = 1
            Context.Data.set_task_attr(uid, 'week', str(task_id), Context.json_dumps(m_l[task_id]))
            info['tid'] = task_id
            info['rw'] = final_info
            info['av_w'] = final
            info['t'] = task_type

        elif task_type in [3,4,5]:
            room_task = self.get_user_table_task(uid, 198 + task_type)
            if not room_task.has_key(int(task_id)):
                return mo.set_error(1, u"该任务已失效")
            elif room_task[int(task_id)][3] > room_task[int(task_id)][4]:
                return mo.set_error(2, u"该任务还未完成")
            if task_type == 3:
                task_config = self.task_201_config
            elif task_type == 4:
                task_config = self.task_202_config
            else:
                task_config = self.task_203_config

            reward = task_config[str(task_id)][5]
            final_info = props.BirdProps.issue_rewards(uid, self.gid, reward, 'task.get', True)
            Context.Data.del_task_attr(uid, 'room_%d'%(198 + task_type), str(task_id))

            l = task_config.keys()
            l.remove(str(task_id))
            room_task_id = random.choice(l)
            room_data = task_config[str(room_task_id)]
            room_task[int(room_task_id)] = [room_data[0], room_data[1], room_data[2], room_data[3], 0, 0]
            Context.Data.set_task_attr(uid, 'room_%d' % (198 + task_type), int(room_task_id),
                                       Context.json_dumps(room_task[int(room_task_id)]))
            info['tid'] = task_id
            info['rw'] = final_info
            self.send_task_room(uid, 198 + task_type)
        elif task_type == 6:
            pass

        mo.set_param('complete', info)
        return mo

    def activity_value_receive(self, uid, mi):
        mo = MsgPack(Message.MSG_SYS_ACTIVITY_RECEIVE | Message.ID_ACK)
        _type = int(mi.get_param('t'))
        index = int(mi.get_param('index'))
        info = {}
        if _type == 1:
            activity_value = self.get_user_day_activity_value(uid)
            activity_receive = self.get_user_day_activity_receive(uid)
            item_list = sorted(self.day_activity_config.items(), key=lambda x: int(x[0]), reverse=False)
            v = index - 1
            ac = item_list[v]
            if int(ac[0]) <= activity_value and activity_receive[v] <= 0:
                final_info = props.BirdProps.issue_rewards(uid, self.gid, ac[1], 'day.activity.value.receive', True)
                activity_receive[v] = 1
                Context.Data.set_task_attr(uid, 'day', 'activity_receive', Context.json_dumps(activity_receive))
                info['ar'] = activity_receive
                info['rw'] = final_info
        else:
            activity_value = self.get_user_week_activity_value(uid)
            activity_receive = self.get_user_week_activity_receive(uid)
            item_list = sorted(self.week_activity_config.items(), key=lambda x: int(x[0]), reverse=False)
            v = index - 1
            ac = item_list[v]
            if int(ac[0]) <= activity_value and activity_receive[v] <= 0:
                final_info = props.BirdProps.issue_rewards(uid, self.gid, ac[1], 'week.activity.value.receive', True)
                activity_receive[v] = 1
                Context.Data.set_task_attr(uid, 'week', 'activity_receive', Context.json_dumps(activity_receive))
                info['ar'] = activity_receive
                info['rw'] = final_info
        if len(info) <= 0:
            return mo.set_error(1, u"活跃度不足")
        mo.set_param('reward', info)
        return mo

    def get_user_day_activity_value(self, uid):
        day_activity_time = Context.Data.get_task_attr(uid, 'day', 'day_time', None)
        activity_value = Context.Data.get_task_attr(uid, 'day', 'activity_value')
        if activity_value == None or not day_activity_time or int(day_activity_time) < Time.today_start_ts():
            self.get_user_day_task_list(uid)
            Context.Data.set_task_attr(uid, 'day', 'activity_value', 0)
            activity_receive = [0] * len(self.day_activity_config)
            Context.Data.set_task_attr(uid, 'day', 'activity_receive', Context.json_dumps(activity_receive))
            Context.Data.set_task_attr(uid, 'day', 'day_time', int(Time.current_ts()))
            activity_value = 0

        return int(activity_value)

    def get_user_day_activity_receive(self, uid):
        day_activity_time = Context.Data.get_task_attr(uid, 'day', 'day_time', None)
        activity_receive = Context.Data.get_task_attr_json(uid, 'day', 'activity_receive')
        if activity_receive == None or not day_activity_time or int(day_activity_time) < Time.today_start_ts():
            self.get_user_day_task_list(uid)
            activity_receive = [0] * len(self.day_activity_config)
            Context.Data.set_task_attr(uid, 'day', 'activity_receive', Context.json_dumps(activity_receive))
            Context.Data.set_task_attr(uid, 'day', 'activity_value', 0)
            Context.Data.set_task_attr(uid, 'day', 'day_time', int(Time.current_ts()))
        return activity_receive

    def get_user_week_activity_value(self, uid):
        week_activity_time = Context.Data.get_task_attr(uid, 'week', 'week_time', None)
        activity_value = Context.Data.get_task_attr(uid, 'week', 'activity_value')
        if activity_value == None or not week_activity_time or int(week_activity_time) < Time.current_week_start_ts():
            self.get_user_week_task_list(uid)
            Context.Data.set_task_attr(uid, 'week', 'activity_value', 0)
            activity_receive = [0] * len(self.week_activity_config)
            Context.Data.set_task_attr(uid, 'week', 'activity_receive', Context.json_dumps(activity_receive))
            Context.Data.set_task_attr(uid, 'week', 'week_time', int(Time.current_ts()))
            activity_value = 0
        return int(activity_value)

    def get_user_week_activity_receive(self, uid):
        week_activity_time = Context.Data.get_task_attr(uid, 'week', 'week_time', None)
        activity_receive = Context.Data.get_task_attr_json(uid, 'week', 'activity_receive')
        if activity_receive == None or not week_activity_time or int(week_activity_time) < Time.current_week_start_ts():
            self.get_user_week_task_list(uid)
            Context.Data.set_task_attr(uid, 'week', 'activity_value', 0)
            activity_receive = [0] * len(self.week_activity_config)
            Context.Data.set_task_attr(uid, 'week', 'activity_receive', Context.json_dumps(activity_receive))
            Context.Data.set_task_attr(uid, 'week', 'week_time', int(Time.current_ts()))
        return activity_receive

    def send_task_list(self, uid):
        mo = MsgPack(Message.MSG_SYS_NEW_TASK_LIST | Message.ID_ACK)
        task_day = self.get_user_day_task_list(uid)
        task_week = self.get_user_week_task_list(uid)
        activity_day_value = self.get_user_day_activity_value(uid)
        activity_week_value = self.get_user_week_activity_value(uid)
        info = {}
        task_day_list = []
        for k,v in task_day.items():
            d = self.get_task_send_dict(k, v, self.task_day_config)
            task_day_list.append(d)
        task_week_list = []
        for k,v in task_week.items():
            d = self.get_task_send_dict(k, v, self.task_week_config)
            task_week_list.append(d)
        ar_d = self.get_user_day_activity_receive(uid)
        ar_w = self.get_user_week_activity_receive(uid)
        info['td'] = task_day_list
        info['tw'] = task_week_list
        info['av_d'] = activity_day_value
        info['av_w'] = activity_week_value
        info['ar_d'] = ar_d
        info['ar_w'] = ar_w
        mo.set_param('task', info)
        return mo

    def send_task_room(self, uid, mi):
        if isinstance(mi, MsgPack):
            room = mi.get_param('room')
        else:
            room = mi
        mo = MsgPack(Message.MSG_SYS_TABLE_TASK_LIST | Message.ID_ACK)
        table_task = self.get_user_table_task(uid, room)
        info = {}
        if room == 201:
            task_config = self.task_201_config
        elif room == 202:
            task_config = self.task_202_config
        elif room == 203:
            task_config = self.task_203_config
        else:
            return None
        task_table_list = []
        for k, v in table_task.items():
            d = self.get_task_send_dict(k, v, task_config)
            task_table_list.append(d)

        info['tt'] = task_table_list
        mo.set_param('task', info)
        Context.GData.send_to_connect(uid, mo)
        return

    def get_task_send_dict(self, tid, t_list, c_config):
        d = {}
        d['tid'] = int(tid)
        d['dt'] = t_list[0]
        d['tp'] = t_list[1]
        d['idx'] = t_list[2]
        d['c'] = t_list[3]
        d['cp'] = t_list[4]
        d['rz'] = t_list[5]
        d['at'] = c_config[str(tid)][4]
        d['rw'] = props.BirdProps.convert_reward(c_config[str(tid)][5])
        d['dc'] = c_config[str(tid)][6]
        return d

    def get_day_time(self, uid):
        return Context.Data.get_task_attr(uid, 'day', 'day_time', None)

    def get_week_time(self, uid):
        return Context.Data.get_task_attr(uid, 'week', 'week_time', None)

    def get_user_table_task(self, uid, room):
        if room == 201:
            task_config = self.task_201_config
        elif room == 202:
            task_config = self.task_202_config
        elif room == 203:
            task_config = self.task_203_config
        else:
            return None
        room_task_list = Context.Data.get_task_all(uid, 'room_%d'%room)
        room_task = {}
        if not room_task_list:
            room_task_id = random.choice(task_config.keys())
            room_data = task_config[str(room_task_id)]
            room_task[int(room_task_id)] = [room_data[0], room_data[1], room_data[2], room_data[3], 0, 0]
            Context.Data.set_task_attr(uid, 'room_%d'%room, int(room_task_id), Context.json_dumps(room_task[int(room_task_id)]))
        else:
            l = room_task_list.items()
            for k, v in enumerate(l):
                if k == 0:
                    room_task[int(v[0])] = Context.json_loads(v[1])
                else:
                    Context.Data.del_task_attr(uid, 'room_%d'%room, v[0])
        return room_task

    def get_user_week_task_list(self, uid):
        week_time = self.get_week_time(uid)
        week_list = {}
        if not week_time or int(week_time) < Time.current_week_start_ts():
            task_all_list = Context.Data.get_task_all(uid, 'week')
            if task_all_list:
                for k, v in task_all_list.items():
                    Context.Data.del_task_attr(uid, 'week', k)
            taskList = self.get_week_task_list()
            for i in taskList:
                week_data = self.task_week_config[str(i)]
                week_list[int(i)] = [week_data[0], week_data[1], week_data[2], week_data[3], 0, 0]
                Context.Data.set_task_attr(uid, 'week', int(i), Context.json_dumps(week_list[int(i)]))
            Context.Data.set_task_attr(uid, 'week', 'week_time', Time.current_ts())
            activity_receive = [0] * len(self.week_activity_config)
            Context.Data.set_task_attr(uid, 'week', 'activity_receive', Context.json_dumps(activity_receive))
            Context.Data.set_task_attr(uid, 'week', 'activity_value', 0)
        else:
            task_all_list = Context.Data.get_task_all(uid, 'week')
            for k, v in task_all_list.items():
                if k in ['week_time', 'activity_value', 'activity_receive']:
                    continue
                week_list[int(k)] = Context.json_loads(v)
        return week_list

    def get_week_task_list(self):
        week_time = self.get_week_time(100)
        week_task = Context.Data.get_task_attr(100, 'week', 'task_list', None)
        if not week_time or not week_task or int(week_time) < Time.current_week_start_ts():
            week_task = self.task_week_config.keys()
            week_task = random.sample(week_task, 10)
            Context.Data.set_task_attr(100, 'week', 'task_list', Context.json_dumps(week_task))
            Context.Data.set_task_attr(100, 'week', 'week_time', Time.current_ts())
        else:
            week_task = Context.json_loads(week_task)
        return week_task

    def get_user_day_task_list(self, uid):
        day_time = self.get_day_time(uid)
        day_list = {}
        if not day_time or int(day_time) < Time.today_start_ts():
            task_all_list = Context.Data.get_task_all(uid, 'day')
            if task_all_list:
                for k, v in task_all_list.items():
                    Context.Data.del_task_attr(uid, 'day', k)
            taskList = self.get_day_task_list()
            for i in taskList:
                day_data = self.task_day_config[str(i)]
                day_list[int(i)] = [day_data[0], day_data[1], day_data[2], day_data[3], 0, 0]
                Context.Data.set_task_attr(uid, 'day', int(i), Context.json_dumps(day_list[int(i)]))
            Context.Data.set_task_attr(uid, 'day', 'day_time', Time.current_ts())
        else:
            task_all_list = Context.Data.get_task_all(uid, 'day')
            for k, v in task_all_list.items():
                if k in ['day_time', 'activity_value', 'activity_receive']:
                    continue
                day_list[int(k)] = Context.json_loads(v)

        return day_list

    def get_day_task_list(self):
        day_time = self.get_day_time(100)
        day_task = Context.Data.get_task_attr(100, 'day', 'task_list', None)
        if not day_time or not day_task or int(day_time) < Time.today_start_ts():
            day_task = self.task_day_config.keys()
            day_task = random.sample(day_task, 10)
            Context.Data.set_task_attr(100, 'day', 'task_list', Context.json_dumps(day_task))
            Context.Data.set_task_attr(100, 'day', 'day_time', Time.current_ts())
        else:
            day_task = Context.json_loads(day_task)
        return day_task

    def in_room_task(self, uid, types, item_id, value, room):
        if int(room) == 201:
            task_config = self.task_201_config
        elif int(room) == 202:
            task_config = self.task_202_config
        elif int(room) == 203:
            task_config = self.task_203_config
        else:
            return
        room_task = self.get_user_table_task(uid, room)
        for k, v in room_task.items():
            if v[1] == types and (v[2] == 0 or v[2] == item_id):
                if v[4] >= v[3]:
                    continue
                v[4] = v[4] + value
                if v[4] > v[3]:
                    v[4] = v[3]
                Context.Data.set_task_attr(uid, 'room_%d'%int(room), int(k), Context.json_dumps(v))
                mo = MsgPack(Message.MSG_SYS_TABLE_TASK_SINGLE | Message.ID_ACK)
                d = self.get_task_send_dict(k, v, task_config)
                info = {}
                info['t'] = room-198
                info['l'] = d
                mo.set_param('complete', info)
                Context.GData.send_to_connect(uid, mo)
        return

    def in_task(self, uid, types, item_id, value):
        day_task = self.get_user_day_task_list(uid)
        for k, v in day_task.items():
            if v[1] == types and (v[2] == item_id or v[2] == 0):
                if v[4] >= v[3]:
                    continue
                v[4] = v[4] + value
                if v[4] > v[3]:
                    v[4] = v[3]
                Context.Data.set_task_attr(uid, 'day', int(k), Context.json_dumps(v))
                if v[4] >= v[3]:
                    mo = MsgPack(Message.MSG_SYS_TABLE_TASK_SINGLE | Message.ID_ACK)
                    d = self.get_task_send_dict(k, v, self.task_day_config)
                    info = {}
                    info['t'] = 1
                    info['l'] = d
                    mo.set_param('complete', info)
                    Context.GData.send_to_connect(uid, mo)
        week_task = self.get_user_week_task_list(uid)
        for k, v in week_task.items():
            if v[1] == types and (v[2] == item_id or v[2] == 0):
                if v[4] >= v[3]:
                    continue
                v[4] = v[4] + value
                if v[4] > v[3]:
                    v[4] = v[3]
                Context.Data.set_task_attr(uid, 'week', int(k), Context.json_dumps(v))
                if v[4] >= v[3]:
                    mo = MsgPack(Message.MSG_SYS_TABLE_TASK_SINGLE | Message.ID_ACK)
                    d = self.get_task_send_dict(k, v, self.task_week_config)
                    info = {}
                    info['t'] = 2
                    info['l'] = d
                    mo.set_param('complete', info)
                    Context.GData.send_to_connect(uid, mo)
        if newactivity.TaskActivity.judge_task_activity_open():
            cnf = newactivity.TaskActivity.activity_task_config()
            task_times = Context.Activity.get_activity_data(uid, 'task', 'task_time')
            if not task_times or task_times < cnf['start'] or task_times > cnf['end']:
                newactivity.TaskActivity.get_activity_task_list(uid, cnf['task'], cnf['start'], cnf['end'])
                Context.Activity.get_activity_data(uid, 'task', 'task_time', Time.current_ts())
            task_day = int((Time.current_ts() - Time.str_to_timestamp(cnf['start']))/(3600*24)) + 1
            item_list = sorted(cnf['task'].keys(), key=lambda x: int(x), reverse=False)
            if task_day > len(item_list):
                task_day = len(item_list)
            task_id = item_list[task_day - 1]
            task_list = Context.Activity.get_activity_data_json(uid, 'task', task_id)
            if not task_list:
                newactivity.TaskActivity.get_activity_task_list(uid, cnf['task'], cnf['start'], cnf['end'])
                Context.Activity.get_activity_data(uid, 'task', 'task_time', Time.current_ts())
                task_list = Context.Activity.get_activity_data_json(uid, 'task', task_id)
            if task_list[1] == types and (task_list[2] == 0 or task_list[2] == item_id):
                if task_list[4] >= task_list[3]:
                    return
                task_list[4] = task_list[4] + value
                if task_list[4] >= task_list[3]:
                    task_list[4] = task_list[3]
                Context.Activity.set_activity_data(uid, 'task', int(task_id), Context.json_dumps(task_list))
                if task_list[4] >= task_list[3]:
                    mou = MsgPack(Message.MSG_SYS_UPDATE_ACTIVITY_CONF | Message.ID_ACK)
                    mou.set_param('model', 2)
                    Context.GData.broadcast_to_system(mou)
        return

    def get_chip_task(self, uid, value, event, room = None):
        if room and event in ['hit.world.boss', 'hit.table.boss', 'catch.bird', 'exp.upgrade',
                              'unlock.barrel', 'super.weapon.fix']:
            self.in_room_task(uid, 2, 0, value, room)
        self.in_task(uid, 2, 0, value)
        return

    def get_diamond_task(self, uid, value, event, room = None):
        if room and event in ['hit.world.boss', 'hit.table.boss', 'catch.bird', 'exp.upgrade', 'unlock.barrel']:
            self.in_room_task(uid, 3, 0, value, room)
        self.in_task(uid, 3, 0, value)
        return

    def get_freeze_task(self, uid, room):
        self.in_room_task(uid, 4, 202, 1, room)
        self.in_task(uid, 4, 202, 1)

    def get_call_task(self, uid, room):
        self.in_room_task(uid, 5, 205, 1, room)
        self.in_task(uid, 5, 205, 1)

    def get_violent_task(self, uid, room):
        self.in_room_task(uid, 6, 203, 1, room)
        self.in_task(uid, 6, 203, 1)

    def get_super_weapon_task(self, uid, room):
        self.in_room_task(uid, 7, 204, 1, room)
        self.in_task(uid, 7, 204, 1)

    def get_sign_in_task(self, uid):
        self.in_task(uid, 8, 0, 1)

    def get_share_task(self, uid):
        self.in_task(uid, 9, 0, 1)

    def get_diamond_consume_task(self, uid, value, room = None):
        if room:
            self.in_room_task(uid, 10, 0, value, room)
        self.in_task(uid, 10, 0, value)

NewTask = NewTask()
