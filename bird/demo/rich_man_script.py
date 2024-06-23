# -*- coding=utf-8 -*-

#!/usr/bin/env python
# -*- coding=utf-8 -*-

import random
import json
import os, csv, copy

class Const(object):
    MESSAGE_START_GAME =1
    MESSAGE_ROLL_THE_DICE = 2
    MESSAGE_END_GAME = 3

    EVENT_EMPTY = 0         # 空事件
    EVENT_DICE_TWO = 1      #筛子*2
    EVENT_DICE_THREE = 2    #筛子*3
    EVENT_REWARD_TWO = 3    #奖励*2
    EVENT_NO_TICKET = 4     #免票


class RichMan(object):
    PRICE_DICT = {
        202: 2500,
        203: 25000,
        204: 100000,
        205: 2500,
        211: 150000,
        212: 300000,
        213: 500000,
        214: 1000000,
        215: 10000,
        216: 10000,
        217: 10000,
        218: 10000,
        219: 25000,
        220: 5000,
        'diamond': 500,
        'coupon': 5000,
        'target': 20000,
    }

    def __init__(self):
        self.game_name = 'rich_man'
        self.level = 3
        pool_dict = {
            1:5000000,
            2:15000000,
            3:25000000,
        }
        self.pool_num = pool_dict.get(self.level)
        self.player_data = {}

    def get_config(self):
        cnf = {
                1:{                    # 初级场
                    'vip_limit':2,
                    'ticket':10,       # 钻石
                    'map':{
                        2:[5,10],
                        3:[10,20],
                        4:[1,3],
                        5:[2,5],
                        6:[1,2],
                        7:[2,5],
                        8:[8,12],
                        9:[3,6],
                        10:[3,6],
                        11:[3,6],
                    },
                    'floor_num':98,
                    'average_line':5000000,
                    'range_line':100000,
                    'average_rate':0.2,
                    'range_rate':0.01,
                    'win':[1.0, 3.0],
                    'lose':[0.05, 1.0],

                    'end_win': [3.0, 5.0],
                    'end_lose': [2.0, 3.0],

                    'spacial_reward':{
                        '3':{'rw1':{'props':[{'id':202, 'count':1}]}, 'rw2':{'props':[{'id':203, 'count':1}]}},
                        '9':{'chip': 20000},
                        '10':{'coupon': 4},
                        '11':{'props':[{'id':203, 'count':1}]},
                    }
                },
                2: {                    # 中级场
                    'vip_limit': 2,
                    'ticket': 30,  # 钻石
                    'map': {
                        2: [15, 20],
                        3: [5, 15],
                        4: [1, 3],
                        5: [1, 3],
                        6: [1, 2],
                        7: [2, 5],
                        8: [8, 12],
                        9: [2, 5],
                        10: [4, 7],
                        11: [3, 6],
                    },
                    'floor_num': 98,
                    'average_line': 15000000,
                    'range_line': 300000,
                    'average_rate': 0.2,
                    'range_rate': 0.01,
                    'win': [1.0, 3.0],
                    'lose': [0.05, 1.0],

                    'end_win': [3.0, 5.0],
                    'end_lose': [2.0, 3.0],

                    'spacial_reward': {
                        '3':{'rw1':{'props':[{'id':220, 'count':1}]}, 'rw2':{'props':[{'id':203, 'count':2}]}},
                        '9': {'chip': 60000},
                        '10': {'coupon': 12},
                        '11': {'props': [{'id': 203, 'count': 2}]},
                    }
                },
                3: {                # 高级场
                    'vip_limit': 2,
                    'ticket': 60,  # 钻石
                    'map': {
                        2: [15, 20],
                        3: [5, 10],
                        4: [1, 3],
                        5: [1, 3],
                        6: [1, 2],
                        7: [1, 3],
                        8: [8, 12],
                        9: [2, 5],
                        10: [5, 8],
                        11: [2, 5],
                    },
                    'floor_num': 98,
                    'average_line': 25000000,
                    'range_line': 500000,
                    'average_rate': 0.2,
                    'range_rate': 0.01,
                    'win': [1.0, 3.0],
                    'lose': [0.05, 1.0],

                    'end_win': [3.0, 5.0],
                    'end_lose': [2.0, 3.0],

                    'spacial_reward': {
                        '3':{'rw1':{'props':[{'id':203, 'count':1}]}, 'rw2':{'props': [{'id':204, 'count':1}]}},
                        '9': {'chip': 120000},
                        '10': {'coupon': 24},
                        '11': {'props': [{'id': 204, 'count': 1}]},
                    }
                },
            }
        config = cnf.get(self.level)
        return config

    def json_dumps(self, o, **kwargs):
        if 'separators' not in kwargs:
            kwargs['separators'] = (',', ':')
        return json.dumps(o, **kwargs)

    def json_loads(self, s, ex=False):
        """
        @param ex: 兼容老数据, 慎用, 禁止将dict, list, set, tuple等类型的数据直接str成字符串
        """
        try:
            return json.loads(s)
        except Exception, e:
            if ex:
                return eval(s)
            else:
                raise e

    def to_int(self, v, default=None):
        if v is None:
            return default
        return int(v)

    def copy_json_obj(self, j):
        t = json.dumps(j)
        return json.loads(t)

    # 获取商品的鸟蛋价值
    def get_props_price(self, rewards_info):
        result = 0
        if 'chip' in rewards_info:
            result += self.to_int(rewards_info['chip'], 0)
        if 'diamond' in rewards_info:
            diamond = self.to_int(rewards_info['diamond'], 0) * self.PRICE_DICT['diamond']
            result += diamond
        if 'coupon' in rewards_info:
            coupon = self.to_int(rewards_info['coupon'], 0) * self.PRICE_DICT['coupon']
            result += coupon
        if 'target' in rewards_info:
            target = self.to_int(rewards_info['target'], 0) * self.PRICE_DICT['target']
            result += target
        if 'props' in rewards_info:
            for one in rewards_info['props']:
                props = self.to_int(one['count'], 0) * self.PRICE_DICT[one['id']]
                result += props
        return result

    def merge_reward(self, *args):
        if not args:
            return {}
        if len(args) == 1:
            return args[0]
        rewards = {}
        for arg in args:
            rewards = self.__merge_reward(rewards, arg)
        return rewards

    def __merge_reward(self, prev, later):
        if not prev:
            return self.copy_json_obj(later)
        if not later:
            return self.copy_json_obj(prev)

        rewards = {}
        # merge鸟蛋
        if 'chip' in prev or 'chip' in later:
            rewards['chip'] = prev.get('chip', 0) + later.get('chip', 0)
        # merge钻石
        if 'diamond' in prev or 'diamond' in later:
            rewards['diamond'] = prev.get('diamond', 0) + later.get('diamond', 0)
        # merge兑换券
        if 'coupon' in prev or 'coupon' in later:
            rewards['coupon'] = prev.get('coupon', 0) + later.get('coupon', 0)
        if 'target' in prev or 'target' in later:
            rewards['target'] = prev.get('target', 0) + later.get('target', 0)
        # merge道具
        props = {}
        for tmp in [prev, later]:
            if 'props' in tmp:
                for prop in tmp['props']:
                    if prop['id'] not in props:
                        props[prop['id']] = prop
                    else:
                        props[prop['id']]['count'] += prop['count']

        if props:
            rewards['props'] = props.values()

        return rewards

    def deal_none_reward(self, reward):
        result = {}
        if 'chip' in reward and reward['chip'] > 0:
            result['chip'] = reward['chip']
        if 'coupon' in reward and reward['coupon'] > 0:
            result['coupon'] = reward['coupon']
        if 'diamond' in reward and reward['diamond'] > 0:
            result['diamond'] = reward['diamond']
        if 'props' in reward:
            props = []
            for one in reward['props']:
                if one['count'] > 0:
                    props.append(one)
            if len(props) > 0:
                result['props'] = props
        return result

    def start_game(self, cnf):
        self.init_player_data(cnf)

    def end_game(self, cnf):
        pool = self.get_pool()

        ticket = cnf.get('ticket')
        end_reward = {}

        win_rate = self.get_win_rate(pool, cnf)
        P = random.random()
        if P < win_rate:
            interval = cnf.get('end_win')
        else:
            interval = cnf.get('end_lose')

        multiple = random.uniform(interval[0], interval[1])
        coupon = int(multiple * ticket / 10)
        end_reward['coupon'] = coupon
        rw_price = self.get_props_price(end_reward)
        self.incr_pool(-rw_price)

        m_reward = self.get_reward()
        if end_reward:
            m_reward = self.merge_reward(False, m_reward, end_reward)
            self.set_reward(m_reward)
        return

    def roll_dice(self, cnf):
        event = self.pop_event()
        ticket = cnf.get('ticket')
        if event != Const.EVENT_NO_TICKET:
            diamond_price = self.get_props_price({'diamond': ticket})
            pool = self.incr_pool(diamond_price)
            self.incr_consume(ticket)
        else:
            pool = self.get_pool()

        self.incr_floor_count(1)
        shake_num = random.randint(1, 6)
        if event == Const.EVENT_DICE_TWO:
            shake_num = shake_num*2
        if event == Const.EVENT_DICE_THREE:
            shake_num = shake_num*3
        flag = self.deal_reward( event, cnf, shake_num, ticket, pool)
        return flag

    def set_reward(self, reward):
        self.player_data['reward'] = reward

    def get_reward(self):
        return self.player_data['reward']

    def incr_consume(self, num):
        self.player_data['consume'] = self.player_data['consume'] + num
        return self.player_data['consume']

    def incr_floor(self, num):
        self.player_data['floor'] = self.player_data['floor'] + num
        return self.player_data['floor']

    def incr_floor_count(self, num):
        self.player_data['floor_count'] = self.player_data['floor_count'] + num
        return self.player_data['floor_count']

    def deal_reward(self, use_event, cnf, shake_num, ticket, pool):
        floor = self.incr_floor(shake_num)
        map_list = self.player_data['map']
        reward = self.player_data['reward']
        if not map_list:
            return False

        if floor >= len(map_list)-1:
            self.end_game(cnf)
            return False

        floor_num = self.to_int(map_list[floor], 0)
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
            self.set_event(get_event)
        elif floor_num == 5: # 色子3倍
            get_event = Const.EVENT_DICE_THREE
            self.set_event(get_event)
        elif floor_num == 6: # 奖励两倍
            get_event = Const.EVENT_REWARD_TWO
            self.set_event(get_event)
        elif floor_num == 7: # 门票免费
            get_event = Const.EVENT_NO_TICKET
            self.set_event(get_event)
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
            props = copy.deepcopy(cnf.get('spacial_reward').get(str(floor_num)))
            if use_event == Const.EVENT_REWARD_TWO:
                count = props.get('props')[0].get('count')
                count *= 3
                props['props'][0]['count'] = count
            add_reward = props

        if add_reward:
            reward_price = self.get_props_price(add_reward)
            self.incr_pool(-reward_price)
            rw = self.merge_reward(reward, add_reward)
            self.player_data['reward'] = rw

        return True

    def get_pool(self):
        pool = self.pool_num
        return pool

    def incr_pool(self, price):
        self.pool_num += price
        return self.get_pool()

    def pop_event(self):
        event = self.player_data['eve']
        if event != Const.EVENT_EMPTY:
            self.player_data['eve'] = Const.EVENT_EMPTY
        return event

    def set_event(self, event):
        self.player_data['eve'] = event
        return

    ## 新建地图
    def make_map(self, cnf):
        map_data = cnf.get('map')
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

        event_index_dict = []
        index_list = range(0, 92)

        for i in event_list:
            index = random.choice(index_list)
            index_list.remove(index)
            if index + 1 in index_list:
                index_list.remove(index + 1)
            event_index_dict.append([i, index])

        d_list = sorted(event_index_dict, key=lambda x: int(x[1]), reverse=False)
        for i in d_list:
            map_list.insert(int(i[1]), int(i[0]))
        map_list.insert(0, 0)
        map_list.insert(len(map_list), 0)
        return map_list

    def init_player_data(self, cnf):
        sp_rw = cnf.get('spacial_reward').get(str(3))
        props_rw1 = sp_rw.get('rw1').get('props')[0].get('id')
        props_rw2 = sp_rw.get('rw2').get('props')[0].get('id')
        reward = {
            'chip': 0,
            'coupon': 0,
            'props':[{'id':props_rw1, 'count': 0}, {'id':props_rw1, 'count': 0}]
        }

        map_list = self.make_map(cnf)
        eve_list = []
        self.player_data = {
            'map':map_list,
            'floor': 0,
            'eve': Const.EVENT_EMPTY,
            'reward': reward,
            'consume': 0,
            'floor_count': 0,
            'eve_list': eve_list,
            'level':1,
        }
        return

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

    def play_game(self, cnf):
        flag = self.roll_dice(cnf)
        if flag:
            self.play_game(cnf)
        return

    def save_cache(cls, dir, name, l):
        cd = os.path.dirname(os.getcwd())
        if not os.path.exists(cd + "/history/%s"%(dir)):
            os.makedirs(cd + "/history/%s"%(dir))
        with open(cd + "/history/%s/%s.csv"%(dir, name), "w+") as csvfile:
            writer = csv.writer(csvfile)
            # 先写入columns_name
            writer.writerow(["reward", "pool", 'count', 'consume', 'add_value'])
            # 写入多行用writerows
            for i in l:
                writer.writerows([i])

    def run_task(self, n = 100):
        cnf = self.get_config()
        t_list = []
        m_reward = {}
        dimond_total = 0
        for i in range(n):
            self.start_game(cnf)
            self.play_game(cnf)
            and_value = 0
            # if self.pool_num < 18000000:
            #     and_value = int((25000000 - self.pool_num) * random.randint(50, 100)/100.0)
            #     self.pool_num += and_value
            a = [self.player_data['reward'], self.pool_num, self.player_data['floor_count'], self.player_data['consume']]
            m_reward = self.merge_reward(False, m_reward, self.player_data['reward'])
            dimond_total += self.player_data['consume']
            print i, a
            t_list.append(a)
        print m_reward, dimond_total, self.get_props_price(m_reward), 25000000-self.pool_num
        self.save_cache('rich_man', 'test_1', t_list)


Const = Const()
RichMan = RichMan()

RichMan.run_task(10)