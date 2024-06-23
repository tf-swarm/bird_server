#!/usr/bin/env python
# -*- coding=utf-8 -*-

import random, os, csv, json

class BirdFanFanLe(object):
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

    def copy_json_obj(self, j):
        t = json.dumps(j)
        return json.loads(t)

    def to_int(self, v, default=None):
        if v is None:
            return default
        return int(v)

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

    def get_config(self, index):
        conf = {
                    'entrance_cost': [20, 100, 200],  # 门票费用
                    'switchCard_cost': [10, 50, 100],  # 换牌费用
                    'little_reward':0.035,
                    'lowRate': 0.3,
                    'highRate': 0.6,
                    'diamond_chip': 500,  # 钻石跟金币的比例关系
                    'rate_calc': {  # 基准线，用于判断翻翻乐成功几率及换牌成功几率
                        '1': {
                            'baseLine': 2500000,
                            'addLine': 20000,
                            'addRate': 0.01
                        },
                        '2': {
                            'baseLine': 10000000,
                            'addLine': 100000,
                            'addRate': 0.01
                        },
                        '3': {
                            'baseLine': 20000000,
                            'addLine': 200000,
                            'addRate': 0.01
                        }
                    },
                    'reward_scale': {  # 奖励比例，分别为金币、金币、鸟券3类奖励
                        'reward_A': [3, 1, 0.3],  # chip_reward_group_A
                        'reward_B': [8, 2, 0.5],  # chip_reward_group_B
                        'reward_C': [15, 3, 1],  # coupn_reward_group
                        'reward_C_chip_ex_coupon': 5000,  # 鸟卷兑换关系
                    },
            }
        if index == 1:
            conf['reward_model'] = ['diamond', 'diamond', 'coupon']
            return conf
        else:
            _conf = self.copy_json_obj(conf)
            entrance_cost = _conf.get('entrance_cost')
            switchCard_cost = _conf.get('switchCard_cost')
            diamond_chip = _conf.get('diamond_chip')
            chip_entrance_cost = list(map(lambda x: x * diamond_chip, entrance_cost))
            chip_switchCard_cost = list(map(lambda x: x * diamond_chip, switchCard_cost))
            _conf['entrance_cost'] = chip_entrance_cost
            _conf['switchCard_cost'] = chip_switchCard_cost
            _conf['reward_model'] = ['chip', 'chip', 'chip']
            return _conf

    def open_game(self, index, price):
        conf = self.get_config(index)
        pool = conf.get('rate_calc').get(str(price)).get('baseLine')
        self.pool_value = pool

    # 开始玩翻翻乐
    def start_game(self, index, price):
        _conf = self.get_config(int(index))
        return self.get_result( _conf, index, price)

    def check_enable_play_cost(self, cost):
        self.incr_pool_value(cost)
   
    # 获取本次翻翻乐结果
    def get_result(self, conf, index, priceIdx):
        entrance_cost = conf.get('entrance_cost')
        cost = entrance_cost[priceIdx - 1]
        diamond_chip = 1
        if index == 1:
            diamond_chip = conf.get('diamond_chip')
        self.check_enable_play_cost(cost * diamond_chip)
        return self.get_game_relust(conf, index, priceIdx)

    def _get_calc_rate(self, conf, price_idx):
        pool_value = self.get_pool_value()
        rate_data = conf.get('rate_calc').get(str(price_idx))

        base_line = rate_data.get('baseLine')
        add_line = rate_data.get('addLine')
        add_rate = rate_data.get('addRate')
        lowRate = conf.get('lowRate')
        highRate = conf.get('highRate')

        add_value = int((pool_value - base_line)/(add_line))*float(add_rate)
        low_rt = lowRate+add_value
        high_rt = highRate + add_value

        return low_rt, high_rt

    def get_game_relust(self, conf, index, price_idx):
        low_rt, high_rt = self._get_calc_rate( conf, price_idx) # 根据池子获取区间
        level_rand = random.random()
        if level_rand < low_rt:
            level = 3
        elif level_rand < high_rt:
            level = 2
        else:
            level = 1
        little_rand = random.random()
        if little_rand < conf.get('little_reward') and low_rt > 0:
            result = 5
        else:
            result_rand = random.random()
            if result_rand < low_rt:
                result = 4
            elif result_rand < high_rt:
                result = 3
            else:
                level = 0
                result = 2

        if result < 3:
            level = 0
            result = 2

        # 池中扣除奖励内容
        reward = self.get_reard_data(index, level, conf, result, price_idx)
        reward_chip = self.get_props_price(reward)
        self.incr_pool_value(-reward_chip)

        return level, result, reward, self.pool_value

    # 根据玩家翻牌状态数据获取玩家的奖励
    def get_reard_data(self, index, level, conf, result, price_idx):
        if level <= 0 or result <= 2:
            return {}

        price_cost = conf.get('entrance_cost')[price_idx - 1]

        reward_model = conf.get('reward_model')[level-1]
        if level == 3:
            reward_list = conf.get('reward_scale').get('reward_C')
        elif level == 2:
            reward_list = conf.get('reward_scale').get('reward_B')
        else:
            reward_list = conf.get('reward_scale').get('reward_A')

        if reward_model == 'diamond':
            count = int(reward_list[5 - result] * price_cost)
            reward = {'diamond': count}
        elif reward_model == 'chip':
            count = int(reward_list[5 - result] * price_cost)
            reward = {'chip': count}
        else:
            if index == 1:
                diamond_chip = conf.get('diamond_chip')
            else:
                diamond_chip = 1
            chip_ex_coupon = conf.get('reward_scale').get('reward_C_chip_ex_coupon')
            count = int(reward_list[5 - result] * price_cost * diamond_chip / chip_ex_coupon)
            reward = {'coupon': count}
        return reward

    #获取池子数据
    def get_pool_value(self):
        return self.pool_value

    # 增减池
    def incr_pool_value(self, delta):
        assert isinstance(delta, int)
        self.pool_value += delta
        return self.pool_value


    def save_cache(cls, dir, name, l):
        cd = os.path.dirname(os.getcwd())
        if not os.path.exists(cd + "/history/%s"%(dir)):
            os.makedirs(cd + "/history/%s"%(dir))
        with open(cd + "/history/%s/%s.csv"%(dir, name), "w+") as csvfile:
            writer = csv.writer(csvfile)
            # 先写入columns_name
            writer.writerow(["level", "result", 'reward', 'pool'])
            # 写入多行用writerows
            for i in l:
                writer.writerows([i])

    def run_task(self, index, price, n):
        self.open_game(index, price)
        record_list = []
        a0_2 = 0

        a1_3 = 0
        a1_4 = 0
        a1_5 = 0

        a2_3 = 0
        a2_4 = 0
        a2_5 = 0

        a3_3 = 0
        a3_4 = 0
        a3_5 = 0
        for i in range(n):
            level, result, reward, pool_value = self.start_game(index, price)
            print level, result, reward, pool_value
            record_list.append([level, result, reward, pool_value])
            if level == 0 and result == 2:
                a0_2 += 1

            if level == 1 and result == 3:
                a1_3 += 1
            if level == 1 and result == 4:
                a1_4 += 1
            if level == 1 and result == 5:
                a1_5 += 1


            if level == 2 and result == 3:
                a2_3 += 1
            if level == 2 and result == 4:
                a2_4 += 1
            if level == 2 and result == 5:
                a2_5 += 1

            if level == 3 and result == 3:
                a3_3 += 1
            if level == 3 and result == 4:
                a3_4 += 1
            if level == 3 and result == 5:
                a3_5 += 1

        print a0_2,  a1_3, a1_4, a1_5 , a2_3, a2_4, a2_5, a3_3, a3_4, a3_5,
        self.save_cache('fanfanle', 'test_1', record_list)

BirdFanFanLe = BirdFanFanLe()

index = 0
price = 1
n = 20000
BirdFanFanLe.run_task(index, price, n)
