#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-12-04

import random
import copy
from framework.context import Context
from framework.util.tool import Algorithm, Time
from newactivity import DragonBoatActivity


class PathMaker(object):
    area_range = (
        ((100, 780), (0, 0)), ((980, 1700), (0, 0)),
        ((1920, 1920), (300, 540)), ((1920, 1920), (540, 780)),
        ((980, 1700), (1350, 1350)), ((100, 780), (1350, 1350)),
        ((0, 0), (540, 780)), ((0, 0), (300, 540))
    )
    pt_type_undefine = 0    #没有轨迹
    pt_type_line = 1        #直线
    pt_type_spline = 2      #样条路径
    pt_type_bezier = 3      #贝塞尔曲线
    pt_type_inprinting = 10 #组合曲线

    def generate_in_out_pt(self):
        area_len = len(self.area_range)
        index = random.randrange(0, area_len)
        p1_range = self.area_range[index]
        index = random.randrange(index + 2, index + 7) % area_len
        p2_range = self.area_range[index]
        x1 = random.randint(*p1_range[0])
        y1 = random.randint(*p1_range[1])
        x2 = random.randint(*p2_range[0])
        y2 = random.randint(*p2_range[1])
        return x1, y1, x2, y2

    def generate_in_out_pt_2(self):
        area_len = len(self.area_range)
        index = random.randrange(0, area_len)
        p1_range = self.area_range[index]
        index = random.randrange(index + 3, index + 6) % area_len
        p2_range = self.area_range[index]
        x1 = random.randint(*p1_range[0])
        y1 = random.randint(*p1_range[1])
        x2 = random.randint(*p2_range[0])
        y2 = random.randint(*p2_range[1])
        return x1, y1, x2, y2

    def generate_spacial_pt(self):#起点在左边或者下边
        p = random.choice([1,2])
        if p == 1:
            x1 = random.randint(0, 0)
            y1 = random.randint(100, 780)
            x2 = random.randint(1920, 1920)
            y2 = random.randint(100, 780)
        else:
            x1 = random.randint(300, 1600)
            y1 = random.randint(0, 0)
            x2 = random.randint(300, 1600)
            y2 = random.randint(1080, 1080)
        return [self.pt_type_line, x1, y1, x2, y2]

    def generate_inner_pt(self):
        x = random.randint(600, 1200)
        y = random.randint(350, 650)
        return x, y

    def build_line(self):
        x1, y1, x2, y2 = self.generate_in_out_pt_2()
        return [self.pt_type_line, x1, y1, x2, y2]

    def build_line_2(self):
        y1 = y2 = random.randint(380, 780)
        if random.randint(0, 1) == 0:
            x1, x2 = 0, 1920
        else:
            x1, x2 = 1920, 0
        return [self.pt_type_line, x1, y1, x2, y2]

    # def build_circle_line(self):
    #     tp = random.choice(range(4))
    #     if tp == 0:
    #         x1, x2 = 0, 0
    #         y1 = random.randint(250, 850)
    #         y2 = random.randint(250, 850)
    #     elif tp == 1:
    #         y1, y2 = 0, 0
    #         x1 = random.randint(200, 1600)
    #         x2 = random.randint(200, 1600)
    #     elif tp == 2:
    #         x1, x2 = 1920, 1920
    #         y1 = random.randint(250, 850)
    #         y2 = random.randint(250, 850)
    #     else:
    #         y1, y2 = 1080, 1080
    #         x1 = random.randint(200, 1600)
    #         x2 = random.randint(200, 1600)
    #     x, y = self.generate_inner_pt()
    #     return [self.pt_type_bezier, x1, y1, x, y, x2, y2]


    def build_spline(self):
        x1, y1, x2, y2 = self.generate_in_out_pt_2()
        spline = [self.pt_type_spline, x1, y1]
        while len(spline) < 13:
            x, y = self.generate_inner_pt()
            spline.append(x)
            spline.append(y)
        spline.append(x2)
        spline.append(y2)
        return spline

    def build_bezier(self):
        x1, y1, x2, y2 = self.generate_in_out_pt_2()
        x, y = self.generate_inner_pt()
        return [self.pt_type_bezier, x1, y1, x, y, x2, y2]



    def generate_inprinting(self):
        count = random.randrange(5, 10)
        inprinting = [self.pt_type_inprinting, count, 1500]
        t = random.choice([self.build_line, self.build_bezier])()
        inprinting.extend(t)
        return inprinting

    def generate_basic_path(self):
        funcs = [self.build_line, self.build_bezier]
        func = random.choice(funcs)
        return func()


class MapBuilder(PathMaker):

    map_event_common = 0
    map_event_boss = 1
    map_event_tide = 2
    map_event_special = 3
    map_event_bonus = 4
    map_event_red_dragon = 5
    map_event_bounty = 6

    bird_info_map = {}
    timeline_map = {}
    builder_map = {}
    boom_config = {}
    box_config = {}
    coupon_config = {}
    target_config = {}
    bsize_config = {}
    bonus_config = {}
    bird_path_config = {}
    bird_type_config = {}
    bird_time_config = {}
    bird_group_config = {}
    type_bird_config = {}
    bird_type_list_config = {}
    tide_config = {}
    spacial_bird_config = {}

    bk_imgs = ('1', '2', '3', '4')

    def __init__(self, roomtype):
        self.roomtype = roomtype
        self.listener = None
        self.bird_id = 0
        self.uptime = 0
        self.start_ms = 0
        self.events = []
        self.birds = []
        self.tide = {}
        self.bounty = {}
        self.img = None
        self.next_img = None
        self.tide_img = None
        self.bird_map = {}
        self.bird_info = {}
        self.total_ts = 0
        self.wipe_birds = []
        self.boom_birds_type = -1
        self.bird_path = {}
        self.bird_queue_id = None       #普通鸟生态链的id
        self.bird_queue_list = None     #普通鸟生态链的list
        self.bird_flush_list = None     #补充鸟生态链的list

        self.spacial_queue_id = None    #特殊鸟生态链的id
        self.spacial_queue_list = None  #特殊鸟生态链的list

        self.spacial_bird_refresh_time = None          # 特殊怪的刷新时间

        self.tide_refresh_start = -1

    @classmethod
    def load_config(cls, gid):
        #200 新手场 # 201 初级场 202 中级场 203 高级场 211 竞技 231 公会
        for roomtype in (200, 201, 202, 203, 209, 211, 231):
            conf = Context.Configure.get_game_item_json(gid, 'timeline.%d.config' % roomtype)
            conf = Context.copy_json_obj(conf)
            for k in ['bounty',]:
                conf[k] = [int(t * 10) for t in conf[k]]
            cls.timeline_map[roomtype] = conf

            conf = Context.Configure.get_game_item_json(gid, 'bird.config')
            point_map = dict([(bird['type'], bird['point']) for bird in conf['all']])
            cls.bird_info_map[roomtype] = {
                'common': conf['common'],
                'special': conf['special'],
                'little': conf['common'][:9],
                'middle': conf['common'][9:],
                'bonus': conf['bonus'][:-1],    # 红龙任务中红龙奖金鸟去掉
                'boss': conf['boss'][:-1],      # 红龙任务中红龙去掉
            }

            conf = Context.Configure.get_game_item_json(gid, 'builder.%d.config' % roomtype)
            conf = Context.copy_json_obj(conf)
            order_type, info_map = [], {}
            for k, v in conf['ratio']:
                order_type.append(k)
                info_map[k] = {'value': point_map[k] / float(conf['count']), 'ratio': v}
            del conf['ratio']
            conf['birds'] = order_type
            conf['map'] = info_map
            cls.builder_map[roomtype] = conf
            cls.boom_config[roomtype] = Context.Configure.get_game_item_json(gid, 'boom.%d.config' % roomtype)
            cls.box_config[roomtype] = Context.Configure.get_game_item_json(gid, 'box.%d.config' % roomtype)
            cls.coupon_config[roomtype] = Context.Configure.get_game_item_json(gid, 'coupon.%d.config' % roomtype)
            cls.target_config[roomtype] = Context.Configure.get_game_item_json(gid, 'target.%d.config' % roomtype) #靶卷
            cls.bonus_config[roomtype] = Context.Configure.get_game_item_json(gid, 'bonus.%d.config' % roomtype)
            cls.bsize_config = Context.Configure.get_game_item_json(gid, 'bsize.config')    #靶卷
            cls.bird_path_config = Context.Configure.get_game_item_json(gid, 'bird.path.config')
            cls.bird_type_config = Context.Configure.get_game_item_json(gid, 'bird.type.config')    #
            cls.bird_time_config = Context.Configure.get_game_item_json(gid, 'bird.time.config')    #鸟的生存周期
            cls.bird_group_config = Context.Configure.get_game_item_json(gid, 'bird.group.config')  #鸟的组群
            cls.tide_config = Context.Configure.get_game_item_json(gid, 'bird.tide.config')

            cls.type_bird_config[roomtype] = Context.Configure.get_game_item_json(gid, 'type_bird.%d.config' % roomtype)
            cls.bird_type_list_config[roomtype] = Context.Configure.get_game_item_json(gid, 'bird_type_list.%d.config' % roomtype)
            cls.spacial_bird_config[roomtype] = Context.Configure.get_game_item_json(gid, 'bird_spacial.%d.config' % roomtype)

    @classmethod
    def get_default_builder_info(cls, roomtype):
        return Context.copy_obj(cls.builder_map[roomtype])

    @classmethod
    def get_total_time(cls, roomtype):
        return cls.timeline_map[roomtype]['total']

    @classmethod
    def get_boom_config(cls, roomtype, bird_type):
        if not cls.boom_config[roomtype]:
            return None
        return cls.boom_config[roomtype][str(bird_type)]

    @classmethod
    def get_bsize_config(cls):
        if not cls.bsize_config:
            return None
        return cls.bsize_config

    @classmethod
    def get_tide_config(cls):
        if not cls.tide_config:
            return None
        return cls.tide_config

    @classmethod
    def get_box_config(cls, roomtype):
        if not cls.box_config[roomtype]:
            return None
        return cls.box_config[roomtype]

    @classmethod
    def get_coupon_config(cls, roomtype):
        if not cls.coupon_config[roomtype]:
            return None
        return cls.coupon_config[roomtype]

    @classmethod
    def get_bonus_config(cls, roomtype):
        if not cls.bonus_config[roomtype]:
            return None
        return cls.bonus_config[roomtype]

    @classmethod
    def get_target_roll_config(cls, roomtype):
        if not cls.target_config[roomtype]:
            return None
        return cls.target_config[roomtype]

    @classmethod
    def get_type_bird_config(cls, roomtype):
        if not cls.type_bird_config[roomtype]:
            return None
        return cls.type_bird_config[roomtype]

    @classmethod
    def get_bird_type_list_config(cls, roomtype):
        if not cls.bird_type_list_config[roomtype]:
            return None
        return cls.bird_type_list_config[roomtype]

    @classmethod
    def get_spacial_bird_config(cls, roomtype):
        if not cls.spacial_bird_config[roomtype]:
            return None
        return cls.spacial_bird_config[roomtype]

    @property
    def little(self):
        return self.bird_info_map[self.roomtype]['little']

    @property
    def middle(self):
        return self.bird_info_map[self.roomtype]['middle']

    @property
    def common(self):
        return self.bird_info_map[self.roomtype]['common']

    @property
    def boss(self):
        return self.bird_info_map[self.roomtype]['boss']

    @property
    def bonus(self):
        return self.bird_info_map[self.roomtype]['bonus']

    @classmethod
    def get_bird_path_type(cls, bird_type):
        for k,v in cls.bird_type_config.items():
            if bird_type in v:
                return k
        return '1'

    @classmethod
    def get_bird_group(cls, bird_type):
        if not cls.bird_group_config:
            return False, None, None
        group_dict = cls.bird_group_config.get('gid')
        group_num = cls.bird_group_config.get('num')
        group = group_dict.get(str(bird_type))
        if not group:
            return False, None, None
        gid = random.choice(group)
        num = random.choice(group_num.get(gid))
        return True, int(gid), num

    @classmethod
    def get_bird_times(cls, bird_type, bird_path):
        if bird_type != None:
            if cls.bird_time_config.has_key(str(bird_type)):
                d = cls.bird_time_config.get(str(bird_type))
                if d.has_key(str(bird_path)):
                    return random.choice(d.get(str(bird_path)))
        return 30

    @classmethod
    def get_bird_path_config(cls):
        return cls.bird_path_config

    # 获取鸟的路径 （算法：路径择1，然后删除选择的这条路径，直到路径选完，则重新设值再选一轮）
    def get_bird_path(self, bird_path):
        if len(self.bird_path) <= 0 or not self.bird_path.has_key(str(bird_path)):
            self.bird_path = copy.deepcopy(self.get_bird_path_config())

        path_list = self.bird_path.get(str(bird_path))
        if len(path_list) <= 0:
            pl = self.get_bird_path_config().get(str(bird_path))
            path_list = copy.deepcopy(pl)
            self.bird_path[str(bird_path)] = path_list
        path = random.choice(path_list)
        path_list.remove(path)
        self.bird_path[str(bird_path)] = path_list
        return path

    def bird_type(self, bird):
        b = self.bird_map.get(bird)
        if b:
            return b['t']

    def bird_hunter(self, bird):
        b = self.bird_info.get(bird)
        if b:
            return b['h']

    def bird_hit(self, bird, uid):
        b = self.bird_info.get(bird)
        if b:
            t = b.get('t')
            if t:
                return t.get(uid, 0)
        return 0

    def bird_cost(self, bird, uid=None):
        b = self.bird_info.get(bird)
        if not b:
            return 0
        aj = 0
        if 'c' in b:
            if uid:
                return b['c'].get(uid, 0)
            else:
                for _, _aj in b['c'].items():
                    aj += _aj
                return aj
        return 0

    def bird_W(self, uid, bird):
        b = self.bird_info.get(bird)
        if b:
            if 'w' in b:
                return b['w'].get(uid, 0)
        return 0

    def update_bird_stat(self, uid, bird, cost=None, unit_W=None):
        b = self.bird_info.get(bird)
        if b:
            if 't' not in b:
                b['t'] = {}
            if uid not in b['t']:
                b['t'][uid] = 1
            else:
                b['t'][uid] += 1

            if cost:
                if 'c' not in b:
                    b['c'] = {}
                if uid not in b['c']:
                    b['c'][uid] = cost
                else:
                    b['c'][uid] += cost
            if unit_W:
                if 'w' not in b:
                    b['w'] = {}
                if uid not in b['w']:
                    b['w'][uid] = unit_W
                else:
                    b['w'][uid] += unit_W

    def remove_bird(self, bird):
        del self.bird_map[bird]
        del self.bird_info[bird]

    def new_map(self, builder_info, hunter, next_img=None):
        duration, ev_list, birds = self.__new_map(builder_info, hunter, next_img)
        self.events.extend(ev_list)
        self.birds.extend(birds)
        return duration, ev_list, birds

    def __new_map(self, builder_info, hunter, next_img):
        if next_img:
            self.img = next_img
        else:
            self.img = random.choice(self.bk_imgs)
        imgs = [k for k in self.bk_imgs if k != self.img]
        self.next_img, self.tide_img = random.sample(imgs, 2)
        self.total_ts = self.get_total_time(self.roomtype)
        self.start_ms = Context.Time.current_ms()
        self.uptime = 300
        start, birds = 0, []

        spacial_bird_config = self.get_spacial_bird_config(self.roomtype)
        if spacial_bird_config != None:
            interval = spacial_bird_config.get('interval')
            self.spacial_bird_refresh_time = random.randint(*interval) * 10

        if not builder_info['count']:
            return 30, [], []
        step = 300 / builder_info['count']

        #入场时添加一些加速进场的鸟
        start_num = random.randint(5, 8)
        for i in range(start_num):
            bird = self.make_a_bird(-step, builder_info, hunter)
            if isinstance(bird, list):
                birds.extend(bird)
            else:
                birds.append(bird)

        # bonus_flag = False
        #正常流程
        for i in range(builder_info['count']):
            t = random.randrange(start, start + step)
            start += step
            bird = self.make_a_bird(t, builder_info, hunter)

            if isinstance(bird, list):
                birds.extend(bird)
            else:
                birds.append(bird)

        return 30, [], birds

    def has_more_map(self):
        return self.uptime + 100 < self.total_ts * 10

    def clear_map(self):
        self.bird_map.clear()
        self.bird_info.clear()
        self.tide.clear()
        self.birds = []
        self.events = []

    def get_tide_state(self):
        if not self.tide or not self.tide.has_key('show'):
            return False
        real_time = (Context.Time.current_ms() - self.start_ms - self.listener.total_freeze)/100

        if self.tide.has_key('show') and self.tide_refresh_start > 0 and \
                self.tide_refresh_start + (self.tide['show'])*10 >= real_time\
                and self.tide_refresh_start < real_time:
            return True
        else:
            return False

    # def clear_bounty_event(self):
    #     self.events = [ev for ev in self.events if ev['type'] != self.map_event_bounty]

    def get_tide_map(self, uptime, hunter, which):
        start = uptime
        info = self.new_bird_tide(start, hunter, which)
        if info:
            show, tide = info
            self.tide_refresh_start = start
            # self.uptime = start + show * 10
            event = {'in': start, 'type': self.map_event_tide, 'show': show}
            self.events.append(event)
            return show, [event], tide
        return None


    def delta_map(self, builder_info, hunter, count = -1):
        start = self.uptime
        info = self.__delta_map(start, builder_info, hunter)
        if not info:
            return
        duration, ev_list, birds = info
        self.events.extend(ev_list)
        self.birds.extend(birds)
        return start, duration, ev_list, birds

    def __delta_map(self, start, builder_info, hunter):
        self.uptime = start + 300
        birds, event_list = [], []
        step = 300 / builder_info['count']

        for i in range(builder_info['count']):
            bird = None
            if start > self.spacial_bird_refresh_time:
                time, bird, event = self.make_spacial_bird(start, hunter)
                if event != None:
                    event_list.append(event)
                spacial_bird_config = self.get_spacial_bird_config(self.roomtype)
                if spacial_bird_config != None:
                    interval = spacial_bird_config.get('interval')
                    if time != None:
                        time = time*10
                    else:
                        time = 0
                    self.spacial_bird_refresh_time += (time + random.randint(*interval) * 10)

            if bird and not isinstance(bird, int):
                if isinstance(bird, list):
                    birds.extend(bird)
                else:
                    birds.append(bird)

            t = random.randrange(start, start + step)
            start += step
            if self.tide_refresh_start > 0 and self.tide.has_key('show') and\
                    self.tide_refresh_start + (self.tide['show']) * 10 >= start \
                    and self.tide_refresh_start < start:
                continue

            bird = self.make_a_bird(t, builder_info, hunter)
            if isinstance(bird, list):
                birds.extend(bird)
            else:
                birds.append(bird)
        return 30, event_list, birds

    def get_map_info(self):
        map_info = {
            'img': self.img,
            'next_img': self.next_img,
        }
        if self.tide:
            map_info['tide'] = self.tide
        if self.birds:
            birds = []
            for k, v in self.bird_map.items():
                birds.append(v)
            map_info['birds'] =birds
        if self.events:
            map_info['events'] = self.events
        if self.bounty:
            map_info['bounty'] = self.bounty
        return map_info

    def adjust_map_info(self, uptime):
        index = 0
        for i, bird in enumerate(self.birds, 1):
            if 'p' in bird and bird['p'][0] == self.pt_type_inprinting:
                end_ts = bird['n'] * 100 + bird['s'] * 1000 + bird['p'][1] * bird['p'][2]
            else:
                end_ts = bird['n'] * 100 + bird['s'] * 1000
            if uptime <= end_ts:
                break
            index = i
        if index > 0:
            del self.birds[0:index]

        if self.tide:
            end_ts = self.tide['in'] * 100 + self.tide['show'] * 1000
            if uptime >= end_ts:
                self.tide.clear()

        if self.events:
            ev_list = []
            for ev in self.events:
                end_ts = ev['in'] * 100 + ev['show'] * 1000
                if uptime < end_ts:
                    ev_list.append(ev)
            self.events = ev_list

    def get_all_wipe_bird(self):
        return self.wipe_birds

    def clear_wipe_bird(self):
        self.wipe_birds = []

    def get_boom_birds_type(self):
        return self.boom_birds_type

    def clear_boom_birds_type(self):
        self.boom_birds_type = -1

    def make_spacial_bird(self, start, hunter):
        spacial_bird = self.get_spacial_bird()
        if spacial_bird is None:
            return None, None, None
        if spacial_bird < 20:
            return self.listener.map_as_tide(start, hunter, spacial_bird)
        if spacial_bird == 551:
            return self.__make_boom_type(start, hunter)
        if spacial_bird == 552:
            return self.__make_boom_area(start, hunter)
        if spacial_bird == 553:
            return self.__make_boom_all(start, hunter)
        if spacial_bird == 554:
            return self.__make_boom_wipe(start, hunter)
        if spacial_bird == 555:
            return self.__make_boom_drill(start, hunter)
        if spacial_bird in [601, 602, 603]:
            return self.__make_box(start, hunter, spacial_bird)
        if spacial_bird == 501:
            return self.make_coupon(start, hunter)
        if spacial_bird == 511:
            return self.make_target(start, hunter)
        if spacial_bird == 521:
            return self.__make_diamond(start, hunter)
        if spacial_bird == 701:
            return self.__make_year_monster(start, hunter)
        if spacial_bird == 702:
            return self.__make_dragon_boat(start, hunter)
        if spacial_bird in [201, 202, 203, 204, 205, 206]:
            return self.__make_boss(start, hunter, spacial_bird)


    # 从鸟的生态链中取特殊鸟出来（炸弹, 鸟群, 宝箱, boss等 ）
    def get_spacial_bird(self):
        spacial_bird_config = copy.deepcopy(self.get_spacial_bird_config(self.roomtype))
        if not spacial_bird_config:
            return None
        spacial_list = spacial_bird_config.get('lst')
        if spacial_list == None:
            return None
        spacial_queue_keys = spacial_list.keys()
        type_spacial_config = spacial_bird_config.get('group')
        if self.spacial_queue_id == None:
            self.spacial_queue_id = random.choice(spacial_queue_keys)
        if self.spacial_queue_list == None:
            self.spacial_queue_list = spacial_list.get(self.spacial_queue_id)
        if len(self.spacial_queue_list) <= 0:
            if len(spacial_queue_keys) > 1:
                spacial_queue_keys.remove(self.spacial_queue_id)
            self.spacial_queue_id = random.choice(spacial_queue_keys)
            self.spacial_queue_list = spacial_list.get(self.spacial_queue_id)

        spacial_keys = self.spacial_queue_list.pop(0)
        if not type_spacial_config.has_key(spacial_keys):
            return None
        type_spacial_lst = type_spacial_config[spacial_keys]
        bird_type = random.choice(type_spacial_lst)
        return bird_type

    # 从鸟的生态链中取普通的鸟出来
    def get_common_bird_type(self, flush = False):
        bird_type_list = copy.deepcopy(self.get_bird_type_list_config(self.roomtype))
        type_bird_config = self.get_type_bird_config(self.roomtype)
        if flush:
            bird_type_list = bird_type_list.get('flush')
            if not isinstance(bird_type_list, list):
                return self.rand_common_bird_type()
            if self.bird_flush_list == None or len(self.bird_flush_list) <= 0:
                self.bird_flush_list = copy.deepcopy(bird_type_list)
            bird_keys = self.bird_flush_list.pop(0)
            if not type_bird_config.has_key(bird_keys):
                return self.rand_common_bird_type()
            type_bird_lst = type_bird_config[bird_keys]
            bird_type = random.choice(type_bird_lst)
        else:
            bird_type_list = bird_type_list.get('update')
            if not isinstance(bird_type_list, dict):
                return self.rand_common_bird_type()
            bird_queue_keys = bird_type_list.keys()
            if self.bird_queue_id == None:
                self.bird_queue_id = random.choice(bird_queue_keys)
            if self.bird_queue_list == None:
                self.bird_queue_list = bird_type_list.get(self.bird_queue_id)
            if len(self.bird_queue_list) <= 0:
                bird_queue_keys.remove(self.bird_queue_id)
                self.bird_queue_id = random.choice(bird_queue_keys)
                self.bird_queue_list = bird_type_list.get(self.bird_queue_id)
            bird_keys = self.bird_queue_list.pop(0)
            if not type_bird_config.has_key(bird_keys):
                return self.rand_common_bird_type()
            type_bird_lst = type_bird_config[bird_keys]
            bird_type = random.choice(type_bird_lst)
        return bird_type

    def rand_common_bird_type(self):
        if random.randint(0, 90) > 30:
            bird_type = random.choice(self.little)
        else:
            bird_type = random.choice(self.middle)
        return bird_type

    def __make_common(self, start, hunter, bird_type=None, group = False):
        self.bird_id += 1
        if bird_type is None:
            bird_type = self.get_common_bird_type()

        path_type = self.get_bird_path_type(bird_type)
        path = self.get_bird_path(path_type)
        times = self.get_bird_times(bird_type, path)
        pt = {'ps':path_type, 'pl':path}
        bird_list = []
        is_group, gid, num = False, 0, 0
        if group:
            is_group, gid, num = self.get_bird_group(bird_type)
        bird = {
            't': bird_type,
            'i': self.bird_id,
            'n': start,
            's': times,
            'pn': pt,
        }

        self.bird_map[self.bird_id] = bird
        self.bird_info[self.bird_id] = {'h': hunter}
        if not is_group:
            return bird
        # 群鸟
        else:
            bird_head = copy.deepcopy(bird)
            bl = range(self.bird_id, self.bird_id + num)
            bird_head['g'] = {'gid': gid, 'gl': bl}
            self.bird_map[self.bird_id] = bird_head
            bird_list.append(bird_head)
            bid_start, bid_end = self.bird_id+1, self.bird_id+num
            for i in range(bid_start, bid_end):
                self.bird_id = i
                bird_body = {
                    't': bird_type,
                    'i': self.bird_id,
                    'n': start,
                    's': times,
                    'pn': pt,
                }
                self.bird_map[self.bird_id] = bird_body
                self.bird_info[self.bird_id] = {'h': hunter}
                bird_list.append(bird_body)
        return bird_list

    def __make_boss(self, start, hunter, bird_type=None):
        if len(self.timeline_map[self.roomtype]['boss']) <= 0:
            return None, None
        self.bird_id += 1
        if bird_type:
            t = bird_type
        else:
            if self.roomtype == 201:
                t = random.choice([201, 202])
            elif self.roomtype == 202:
                t = random.choice([201, 202, 203, 204, 205, 206])
            elif self.roomtype == 203:
                t = random.choice([201, 202, 203, 204, 205, 206])
            elif self.roomtype == 209:
                t = random.choice([201, 202, 203, 204, 205, 206])
            else:
                t = random.choice(self.boss)
        bird = {
            't': t,
            'i': self.bird_id,
            'n': start,
            's': 90,
            'p': self.build_line_2(),
        }
        self.bird_map[self.bird_id] = bird
        self.bird_info[self.bird_id] = {'h': hunter}

        event = {'in': start, 'type': self.map_event_boss, 'show': 90}
        Context.Log.error('make boss')
        return 90, bird, event

    def __make_year_monster(self, start, hunter):
        primary_key = 'game.2.year_monster'
        year_monster_pool_chip = Context.RedisMix.hash_get_int(primary_key, 'year_monster_pool', 0)
        if year_monster_pool_chip <= 20000:
            return None, None, None
        self.bird_id += 1
        t = 701

        bird = {
            't': t,
            'i': self.bird_id,
            'n': start,
            's': 90,
            'p': self.build_line_2(),
        }

        self.bird_map[self.bird_id] = bird
        self.bird_info[self.bird_id] = {'h': hunter}
        Context.Log.debug('make year monster')
        return 90, bird, None

    def __make_dragon_boat(self, start, hunter):
        if not DragonBoatActivity.judge_dragon_boat_activity_open():
            return None, None, None

        primary_key = 'game.2.year_monster'
        dragon_boat_pool_chip = Context.RedisMix.hash_get_int(primary_key, 'dragon_boat_pool', 0)
        if dragon_boat_pool_chip <= 20000:
            return None, None, None
        self.bird_id += 1
        t = 702

        bird = {
            't': t,
            'i': self.bird_id,
            'n': start,
            's': 100,
            'p': self.build_line_2(),
        }

        self.bird_map[self.bird_id] = bird
        self.bird_info[self.bird_id] = {'h': hunter}
        Context.Log.debug('make dragon boat')
        return 100, bird, None

    def __make_diamond(self, start, hunter, bird_type=None):
        diamond_data = self.timeline_map[self.roomtype]['diamond']
        if len(diamond_data) <= 0:
            return None, None, None
        if bird_type == None:
            bird_type = 521
        self.bird_id += 1
        count = random.randint(diamond_data[2][0], diamond_data[2][1])
        bird = {
            't': bird_type,
            'i': self.bird_id,
            'n': start,
            's': 120,
            'p': self.build_line_2(),
            'number': count,
        }
        self.bird_map[self.bird_id] = bird
        self.bird_info[self.bird_id] = {'h': hunter}
        Context.Log.debug('make diamond')
        return 120, bird, None

    def __make_box(self, start, hunter, bird_type=None):
        self.bird_id += 1
        box_info = self.get_box_config(self.roomtype)
        if bird_type is None:
            bird_type = random.choice(box_info['box_id'])
        bird = {
            't': bird_type,
            'i': self.bird_id,
            'n': start,
            's': box_info['life_time'],
            'p': self.build_line_2(),
        }
        self.bird_map[self.bird_id] = bird
        self.bird_info[self.bird_id] = {'h': hunter}
        Context.Log.error('__make_box')
        return box_info['life_time'], bird, None

    def make_coupon(self, start, hunter, bird_type=None):
        self.bird_id += 1
        if bird_type is None:
            bird_type = 501

        coupon_info = self.get_coupon_config(self.roomtype)
        count = random.choice(coupon_info['count'])
        rand_range = random.choice(coupon_info['rand_range'])
        bird = {
            't': bird_type,
            'i': self.bird_id,
            'n': start,
            's': coupon_info['life_time'],
            'p': self.build_line_2(),
            'number': count,
            'rand_range': rand_range,
        }
        self.bird_map[self.bird_id] = bird
        self.bird_info[self.bird_id] = {'h': hunter}
        return coupon_info['life_time'], bird, None

    def make_target(self, start, hunter, bird_type=None):
        self.bird_id += 1
        if bird_type is None:
            bird_type = 511
        target_info = self.get_target_roll_config(self.roomtype)
        count = random.choice(target_info['count'])
        __rand_range = target_info['rand_range']
        __r = random.random()
        for __item in __rand_range:
            if __r < __item[0]:
                rand_range = __item[1]
                break
            else:
                __r -= __item[0]
        bird = {
            't': bird_type,
            'i': self.bird_id,
            'n': start,
            's': target_info['life_time'],
            'p': self.build_line_2(),
            'number': count,
            'rand_range': rand_range,
        }
        self.bird_map[self.bird_id] = bird
        self.bird_info[self.bird_id] = {'h': hunter}
        return target_info['life_time'], bird, None

    #t同类型炸弹
    def __make_boom_type(self, start, hunter, bird_type=None):
        birds = []
        self.bird_id += 1
        if bird_type is None:
            bird_type = 551
        boom_info = self.get_boom_config(self.roomtype, bird_type)
        sk = random.choice(boom_info['b'])
        bird = {
            't': bird_type,
            'i': self.bird_id,
            'n': start,
            's': boom_info['l'],
            'p': self.build_line_2(),
            'sk': sk,
        }
        self.bird_map[self.bird_id] = bird
        birds.append(bird)
        self.bird_info[self.bird_id] = {'h': hunter}
        self.clear_boom_birds_type()
        self.boom_birds_type = sk
        for i in xrange(6):
            self.bird_id += 1
            bird = self.__make_common(start+30*(i+1), hunter, self.boom_birds_type)
            self.bird_map[self.bird_id] = bird
            birds.append(bird)
        Context.Log.error('make_boom_type')
        return boom_info['l'], birds, None

    #全屏炸弹
    def __make_boom_all(self, start, hunter, bird_type=None):
        self.bird_id += 1
        if bird_type is None:
            bird_type = 553
        boom_info = self.get_boom_config(self.roomtype, bird_type)
        bird = {
            't': bird_type,
            'i': self.bird_id,
            'n': start,
            's': boom_info['l'],
            'p': self.build_line_2(),
        }
        self.bird_map[self.bird_id] = bird
        self.bird_info[self.bird_id] = {'h': hunter}
        Context.Log.error('make_boom_all')
        return boom_info['l'], bird, None

    #一网打尽
    def __make_boom_wipe(self, start, hunter):
        birds = []
        self.clear_wipe_bird()
        boom_info = self.get_boom_config(self.roomtype, 554)
        ids = random.sample((161, 162, 163, 164, 165, 166, 167, 168), 6)
        for i in (0, 1, 2, 3, 4, 5):
            self.bird_id += 1
            line = self.generate_spacial_pt()
            bird_type = ids[i]
            bird = {
                't': bird_type,
                'i': self.bird_id,
                'n': start,
                's': boom_info['l'],
                'p': line,
            }
            self.bird_map[self.bird_id] = bird
            self.bird_info[self.bird_id] = {'h': hunter}
            self.wipe_birds.append(self.bird_id)
            birds.append(bird)
        Context.Log.error('make_boom_wipe')
        return boom_info['l'], birds, None

    #区域炸弹
    def __make_boom_area(self, start, hunter, bird_type=None):
        self.bird_id += 1
        if bird_type is None:
            bird_type = 552
        boom_info = self.get_boom_config(self.roomtype, bird_type)
        bird = {
            't': bird_type,
            'i': self.bird_id,
            'n': start,
            's': boom_info['l'],
            'p': self.build_line_2(),
        }
        self.bird_map[self.bird_id] = bird
        self.bird_info[self.bird_id] = {'h': hunter}
        Context.Log.error('make_boom_area')
        return boom_info['l'], bird, None

    #区域炸弹
    def __make_boom_drill(self, start, hunter, bird_type=None):
        self.bird_id += 1
        if bird_type is None:
            bird_type = 555
        boom_info = self.get_boom_config(self.roomtype, bird_type)
        bird = {
            't': bird_type,
            'i': self.bird_id,
            'n': start,
            's': boom_info['l'],
            'p': self.build_line_2(),
        }
        self.bird_map[self.bird_id] = bird
        self.bird_info[self.bird_id] = {'h': hunter}
        Context.Log.error('make_boom_drill')
        return boom_info['l'], bird, None

    def make_bonus(self, start, hunter):
        bird = self.__make_bonus(start, hunter)
        for i, b in enumerate(self.birds):
            if b['n'] > start:
                self.birds.insert(i, bird)
                break
        else:
            self.birds.append(bird)
        return bird

    def __make_bonus(self, start, hunter, inner=True, bird_type=None):
        self.bird_id += 1

        if bird_type is None:
            bird_type = random.choice(self.bonus)
        if inner:
            pt = self.generate_basic_path()
            _t = self.generate_inner_pt()
            pt[1] = _t[0]
            pt[2] = _t[1]
            bird = {
                't': bird_type,
                'i': self.bird_id,
                'n': start,
                's': 50,
                'p': pt,
                'cs':1,
            }
        else:
            path_type = self.get_bird_path_type(bird_type)
            path = self.get_bird_path(path_type)
            times = self.get_bird_times(bird_type, path)
            pt = {'ps': path_type, 'pl': path}
            bird = {
                't': bird_type,
                'i': self.bird_id,
                'n': start,
                's': times,
                'pn': pt,
            }

        self.bird_map[self.bird_id] = bird
        self.bird_info[self.bird_id] = {'h': hunter}
        return bird

    def make_table_boss(self, hunter):
        self.bird_id += 1
        bird = {
            't': 451,
            'i': self.bird_id,
            'n': 0,
            's': 300,  # 存活时间,
        }
        self.bird_map[self.bird_id] = bird
        self.bird_info[self.bird_id] = {'h': hunter}
        # self.table_boss_refresh_in_time = self.uptime
        # Context.Log.error('make world boss')
        Context.Log.debug('=====world=make=001', bird)
        return bird

    def make_world_boss(self, hunter):
        self.bird_id += 1
        bird = {
            't': 452,
            'i': self.bird_id,
            'n': 0,
            's': 600,  # 存活时间,
        }
        self.bird_map[self.bird_id] = bird
        self.bird_info[self.bird_id] = {'h': hunter}
        Context.Log.debug('=====world=make=001', bird)
        return bird

    def new_bird_tide(self, start, hunter, which):
        tide_conf = self.get_tide_config()
        if not tide_conf.has_key(str(which)):
            return None
        func = getattr(self, '_make_tide')
        return func(start, hunter, which)

    def _make_tide(self, start, hunter, which):
        tide_conf = self.get_tide_config().get(str(which))
        tide_info = tide_conf.get('lst')
        tide_time = tide_conf.get('time')
        return self.__make_tide(start, int(which), tide_info, hunter, tide_time)

    def __make_tide(self, start, which, tide_info, hunter, showtime=53):
        info = []
        tide = {
            'type': which,
            'info': info,
            'in': start,
            'show': showtime,
            'img': self.tide_img,
        }
        self.tide = tide
        for bird_ifo in tide_info:
            _t = bird_ifo[0]
            _c = bird_ifo[1]
            _d = {'id': self.bird_id + 1, 'type': _t}
            info.append(_d)
            while _c > 0:
                _c -= 1
                self.bird_id += 1
                bird = {
                    't': _t,
                    'i': self.bird_id,
                    'n': start,
                    's': showtime,
                }
                if _t == 551:
                    bird['sk'] = bird_ifo[2]

                self.bird_map[self.bird_id] = bird
                self.bird_info[self.bird_id] = {'h': hunter}

        return showtime, tide

    def make_a_bird(self, start, builder_info, hunter):
        index, _ = Algorithm.choice_by_ratio(builder_info['odds'], 100000)
        bird_type = builder_info['birds'][index]
        if bird_type in self.bonus:
            bird = self.__make_bonus(start, hunter, False, bird_type)
        else:
            bird = self.__make_common(start, hunter, group = True)
        return bird

    def flush_new_bird(self, start, bird_type, hunter):
        big_bird_type = bird_type % 1000
        if big_bird_type in self.common or big_bird_type in self.bonus:
            #bird_type = self.get_common_bird_type(True)
            bird = self.__make_common(start, hunter, bird_type=bird_type)
        else:
            return
        for i, b in enumerate(self.birds):
            if b['n'] > start:
                self.birds.insert(i, bird)
                break
        else:
            if isinstance(bird, list):
                self.birds.extend(bird)
            else:
                self.birds.append(bird)
        return bird
