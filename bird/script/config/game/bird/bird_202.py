#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-03-14


from framework.helper import add_game_config


add_game_config(2, 'builder.202.config', {
    'ratio': [
        [101, 5],
        [102, 5],
        [103, 5],
        [104, 5],
        [105, 6],
        [106, 6],
        [107, 6],
        [108, 6],
        [109, 6],
        [110, 4],
        [111, 4],
        [112, 4],
        [113, 4],
        [114, 4],
        [115, 2],
        [116, 2],
        [117, 2],
        # [178, 2],
        # [179, 2],
        # [180, 2],
        # [181, 2],
    ],
    
    'cd': 5,
    'count': 29,
    'Zmin': 21,
    'Zmax': 50,
    'Bg': 50, # 36
    'G': -0.35,
    'Xg': -0.35,
})

add_game_config(2, 'bonus.202.config',[180, 181, 178, 179])

# 鸟id: {
# t: 刷新初始时间,刷新间隔时间（因为是同一时间四选1，一网打尽，551，552，553需要一样）
# l：存活时间
# b：鸟的组id（用于同类型炸弹）
# a：鸟的区域范围（用于区域炸弹）}

add_game_config(2, 'boom.202.config',
    {
        551:{
            't':[5 * 600, 5 * 600],
            'l':60,
            'b':[107,108,109,110,111]
        },
        552:{
            't': [5 * 600, 5 * 600],
            'l': 90,
            'a': 500,
        },
        553:{
            't': [5 * 600, 5 * 600],
            'l': 90,
        },
        # 一网打尽并没有id，用554这个不存在的id来填写配置
        554: {
            't': [5 * 600, 5 * 600],
            'l': 60,
        },
        555: {
            't': [5 * 600, 5 * 600],
            'l': 90,
        },
    }
)

add_game_config(2, 'bird_spacial.202.config',{
    'lst':{
			# 1: ['i', 'b', 'i', 'b', 'i', 'a', 'i', 'a', 'i', 'h', 'i', 'a', 'i', 'a', 'i', 'b', 'i']
            1: ['a', 'b', 'e', 'a', 'b', 'e', 'i', 'a', 'f', 'e', 'a', 'h', 'e', 'a', 'f', 'b', 'e', 'a', 'i', 'e', 'b', 'f']
        },
    'group':{
            'a': [554, 552],    # 552区域炸弹怪  554 惊弓之鸟
            'b': [551, 553],    # 551同类炸弹怪 553 全屏炸弹怪
            'c': [501],         # 501鸟券怪
            'd': [511],         # 靶卷怪
            'e': [201, 202, 203, 204, 205, 206],
            'f': [1, 2, 3, 4, 5],  # 随机不重复
            'g': [521],
            'h': [701],
            'i': [555],
            'j': [702],
        },
    'interval':[15,16]
})

add_game_config(2, 'bird_type_list.202.config',{
        'update':{
            1: ['f', 'c', 'e', 'd', 'b', 'b', 'a', 'd', 'd', 'c', 'c', 'b', 'd', 'c', 'a', 'f', 'd', 'a', 'd', 'c', 'b', 'e', 'h', 'd', 'a', 'b', 'b', 'a', 'd', 'c', 'f', 'b', 'e', 'd', 'a', 'b', 'b', 'c', 'd', 'a', 'c', 'a', 'd', 'd', 'a', 'f', 'c', 'b', 'd', 'a', 'a', 'e', 'a', 'c', 'h', 'b', 'd', 'a', 'b', 'd'],
            2: ['f', 'c', 'd', 'b', 'a', 'b', 'd', 'a', 'e', 'a', 'c', 'b', 'd', 'c', 'a', 'f', 'b', 'd', 'd', 'c', 'a', 'd', 'h', 'd', 'a', 'b', 'b', 'a', 'e', 'c', 'f', 'a', 'd', 'c', 'a', 'b', 'a', 'b', 'd', 'a', 'c', 'c', 'd', 'a', 'd', 'f', 'c', 'a', 'e', 'b', 'c', 'd', 'd', 'a', 'h', 'b', 'b', 'd', 'a', 'd'],
        },
        'flush':[
            'a', 'f', 'b', 'd', 'e', 'a', 'd', 'b', 'a', 'd', 'b', 'd', 'd', 'f', 'b', 'd', 'c', 'b', 'e', 'c', 'd', 'a', 'b', 'f', 'a', 'b', 'd', 'c', 'a', 'e', 'd',
            'a', 'f', 'b', 'd', 'e', 'a', 'd', 'b', 'a', 'd', 'b', 'd', 'd', 'f', 'b', 'd', 'c', 'b', 'e', 'c', 'd', 'a', 'b', 'f', 'a', 'b', 'd', 'c', 'a', 'e', 'h',
            'a', 'f', 'b', 'd', 'e', 'a', 'd', 'b', 'a', 'd', 'b', 'd', 'd', 'f', 'b', 'd', 'c', 'b', 'e', 'c', 'd', 'a', 'b', 'f', 'a', 'b', 'd', 'c', 'a', 'e', 'h',
        ],
    }
)

add_game_config(2, 'not_flush.202.config',['c', 'd', 'e', 'f'])
add_game_config(2, 'type_bird.202.config',{
        'a':[101,102,103],              # 2 3 4 分鸟
        'b':[104,105],                  # 5 6 分
        'c':[106,107,108],              # 7 8 9分
        'd':[109,110,111],              # 10 12 15分
        'e':[112,113,114],              # 18 20 25分
        'f':[115,116,117,176,177,178],              # 30 35 40 50 60 70
        #'g':[],              # 50 60 70
        'h':[179,180,181,182,183],              # 80 90 100  125 150
        #'i':[182,183],                  # 125 150
    }
)


#机器人配置
add_game_config(2, 'aiInfo.202.config',
    {
        1:{
            'barrel_level':[3,6],
            'betMul':[200,250],
            'chip':[86400,135000],
            'diamond': [0, 2],
            'strategy':1,
            'priority':[],
            'vip_level':[0,1],
            'equipBattery':[20000],
            'lastTime':[8,10],
            'leaveCoin':[0,10],
            'departure_time':[30,90],
            'new_hand_ai': 80,
            'total_people': 3000,
            'no_hand_ai': 60,
            'addAI_time': 1,
            'addAI_prob': 80,
            'delay_time': 3,
            'restart': [1, 3],
        },
        2: {
            'barrel_level': [3, 7],
            'betMul': [300,350],
            'chip': [162000, 226800],
            'diamond': [0, 2],
            'strategy': 2,
            'priority': ['bonus', 'common'],
            'vip_level': [2, 3, 4, 5],
            'equipBattery': [20003, 20004, 20005],
            'lastTime': [10, 12],
            'leaveCoin': [0, 10],
            'departure_time': [30, 90],
            'new_hand_ai': 80,
            'total_people': 3000,
            'no_hand_ai': 60,
            'addAI_time': 1,
            'addAI_prob': 80,
            'delay_time': 3,
            'restart': [1, 3],
        },
        3: {
            'barrel_level': [4, 8],
            'betMul': [400,450],
            'chip': [259200, 364500],
            'diamond': [0, 2],
            'strategy': 2,
            'priority': ['boss','special', 'bonus'],
            'vip_level': [6, 7, 8, 9],
            'equipBattery': [20003, 20004, 20005],
            'lastTime': [12, 15],
            'leaveCoin': [0, 10],
            'departure_time': [30, 90],
            'new_hand_ai': 80,
            'total_people': 3000,
            'no_hand_ai': 60,
            'addAI_time': 1,
            'addAI_prob': 80,
            'delay_time': 3,
            'restart': [1, 3],
        },
        'join': {1: 0.8, 2: 0.6, 3: 0.8},
        'rand': 0.03,
    }
)


add_game_config(2, 'box.202.config',
    {
        # 'box_id': [601, 602],
        # 'refresh_time': [1 * 600, 1 * 600],
        # 'life_time':120,
        # 'vip_level':{601:0, 602:2},
        # 'factor_k': 0.75,
    }
)

#鸟券怪
add_game_config(2, 'coupon.202.config',
    {
        'box_id': [501],
        'refresh_time': [12.5 * 600, 10 * 600],
        'life_time':120,
        'vip_level':{501:2},
        'factor_k': 0.75,
        'count': [5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
        'rand_range': [[800, 1000], [1000, 1500], [1250, 1750]], # 鸟券怪难度随机区间
    }
)

#靶场券怪
add_game_config(2, 'target.202.config',
    {
        'box_id': [511],
        'refresh_time': [15 * 600, 10 * 600],
        'life_time': 120,
        'vip_level': {511: 0},
        'factor_k': 0.75,
        'count': [1, 2, 3, 4, 5],
        'rand_range': [[0.3, [800, 1000]], [0.3, [1000, 1500]], [0.3, [1500, 2000]], [0.09, [2000, 3000]], [0.01, [3000, 4000]]], # 靶券怪难度随机区间
    }
)

add_game_config(2,  'flush.202.config',  [

        {
        'type': 4,
        'var': 1,
        'b': [[104, 1, 1]],
        },

])

add_game_config(2, 'fall.202.config', [
    {
        'id': 101, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .05, 1]], 
        }, 
        {
        'id': 102, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .05, 1]], 
        }, 
        {
        'id': 103, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .05, 1]], 
        }, 
        {
        'id': 104, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .05, 1]], 
        }, 
        {
        'id': 105, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .05, 1]], 
        }, 
        {
        'id': 106, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .05, 1]], 
        }, 
        {
        'id': 107, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .05, 1]], 
        }, 
        {
        'id': 108, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .05, 1]], 
        }, 
        {
        'id': 109, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .05, 1]], 
        }, 
        {
        'id': 110, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .05, 1]], 
        }, 
        {
        'id': 111, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .05, 1]], 
        }, 
        {
        'id': 112, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .05, 1]], 
        }, 
        {
        'id': 113, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .05, 1]], 
        }, 
        {
        'id': 114, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .05, 1]], 
        }, 
        {
        'id': 115, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .05, 1]], 
        }, 
        {
        'id': 116, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .05, 1]], 
        }, 
        {
        'id': 117, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .05, 1]], 
        }, 

        {
        'id': 176, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .05, 1]], 
        }, 
        {
        'id': 177, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .05, 1]], 
        }, 
        {
        'id': 178, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .05, 1]], 
        }, 
        {
        'id': 179, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .05, 1]], 
        }, 
        {
        'id': 180, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .05, 1]], 
        }, 
        {
        'id': 181, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .05, 1]], 
        }, 
        {
        'id': 182, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .05, 1]], 
        }, 
        {
        'id': 183, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .05, 1]], 
        }, 

        {
        'id': 201, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .5, 1], [205, 1, .5, 1]], 
        'c': [[2, 10, .5, 1]], 
        }, 
        {
        'id': 202, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .5, 1], [205, 1, .5, 1]], 
        'c': [[2, 10, .5, 1]], 
        }, 
        {
        'id': 203, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .5, 1], [205, 1, .5, 1]], 
        'c': [[2, 10, .5, 1]], 
        }, 
        {
        'id': 204, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .5, 1], [205, 1, .5, 1]], 
        'c': [[2, 10, .5, 1]], 
        }, 
        {
        'id': 205, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .5, 1], [205, 1, .5, 1]], 
        'c': [[2, 10, .5, 1]], 
        }, 
        {
        'id': 206, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .5, 1], [205, 1, .5, 1]], 
        'c': [[2, 10, .5, 1]], 
        }, 

        {
        'id': 302, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .1, 1]], 
        }, 
        {
        'id': 303, 
        'a': [[1, 0, 0, 1]], 
        'b': [[202, 1, .2, 1], [205, 1, .1, 1]], 
        'c': [[2, 1, .1, 1]], 
        }, 

    # 新增601、602、603，宝箱奖励
    {
             'id': 601,
             'p': {'props':[{'id':211, 'count':1}]},
             'needCoin': 150000,
             },
    {
             'id': 602,
             'p': {'props':[{'id':212, 'count':1}]},
             'needCoin': 250000,
             },
    {
             'id': 603,
             'p': {'props':[{'id':213, 'count':1}]},
             'needCoin': 500000,
             },
    # 新增451，boss最后一击击杀奖励
    {
             'id': 451,
             'c': [[203, 2, 0.1, 1], [204, 1, 0.1, 1], [205, 5, 0.1, 1], [211, 1, 0.5, 1], [212, 1, 0.5, 1], [213, 1, 0.1, 1], [2, 20, 1, 1], [3, 5, 0.25, 1]],
             },
])

add_game_config(2, 'table.boss.202.config', {
    # 'leave': [4320000, (30, 45, 60)], # 总血量， 奖励触发所需子弹数
    # 'life_minute': range(0, 5),  # 生存时长，配置5分钟
    # 'coupon_n': 1000,  # 记录boss鸟卷普通掉落，暂时无效
    # 'reward_list': {  # boss创建时间及奖励类型
    #     0: ['stone', 'coupon', 'prop', 'chip'], # 'stone', 'coupon', 'prop', 'egg', 'chip'，取消掉'egg'配置
    #     1: ['stone', 'coupon', 'prop', 'chip'],
    #     2: ['stone', 'coupon', 'prop', 'chip'],
    #     3: ['stone', 'coupon', 'prop', 'chip'],
    #     4: ['stone', 'coupon', 'prop', 'chip'],
    #     5: ['stone', 'coupon', 'prop', 'chip'],
    #     6: ['stone', 'coupon', 'prop', 'chip'],
    #     7: ['stone', 'coupon', 'prop', 'chip'],
    #     8: ['stone', 'coupon', 'prop', 'chip'],
    #     9: ['stone', 'coupon', 'prop', 'chip'],
    #     10: ['stone', 'coupon', 'prop', 'chip'],
    #     11: ['stone', 'coupon', 'prop', 'chip'],
    #     12: ['stone', 'coupon', 'prop', 'chip'],
    #     13: ['stone', 'coupon', 'prop', 'chip'],
    #     14: ['stone', 'coupon', 'prop', 'chip'],
    #     15: ['stone', 'coupon', 'prop', 'chip'],
    #     16: ['stone', 'coupon', 'prop', 'chip'],
    #     17: ['stone', 'coupon', 'prop', 'chip'],
    #     18: ['stone', 'coupon', 'prop', 'chip'],
    #     19: ['stone', 'coupon', 'prop', 'chip'],
    #     20: ['stone', 'coupon', 'prop', 'chip'],
    #     21: ['stone', 'coupon', 'prop', 'chip'],
    #     22: ['stone', 'coupon', 'prop', 'chip'],
    #     23: ['stone', 'coupon', 'prop', 'chip'],
    # },
    # 'reward': {
    #     'stone': [[1, 215], [1, 216], [1, 217], [1, 218]], # 概率2代表2%，物品ID，数量默认1
    #     'prop': [],
    #     'coupon': [], # [[如鸟卷池有鸟卷50%概率，掉落1个]， [房间内boss此字段无效]]
    #     'chip': [
    #         [100, 0, 0, [[0.5, 1, 0.55], [0.75, 1, 0.3], [1, 2, 0.1], [1, 2.5, 0.05]]], 
    #         [100, 0, 0, [[0.5, 1, 0.55], [0.75, 1.25, 0.3], [1, 2, 0.1], [1, 2.5, 0.05]]], 
    #         [100, 0, 0, [[0.5, 1, 0.55], [0.75, 1.25, 0.3], [1, 2, 0.1], [1, 2.5, 0.05]]], 
    #         [100, 0, 0, [[0.5, 1, 0.55], [0.75, 1.25, 0.3], [1, 2, 0.1], [1, 2.5, 0.05]]], 
    #         [100, 0, 0, [[0.5, 1, 0.55], [0.75, 1.25, 0.3], [1, 2.5, 0.1], [1, 2.5, 0.05]]], 
    #         [100, 0, 0, [[0.5, 1, 0.55], [0.75, 1.25, 0.3], [1, 2.5, 0.1], [1, 2.5, 0.05]]], 
    #         [100, 0, 0, [[0.5, 1, 0.55], [0.75, 1.25, 0.3], [1, 2.5, 0.1], [1, 2.5, 0.05]]], 
    #         [100, 0, 0, [[0.5, 1, 0.55], [0.75, 1.25, 0.3], [1, 2.5, 0.1], [1, 2.5, 0.05]]], 
    #         [100, 0, 0, [[0.5, 1, 0.55], [0.75, 1.25, 0.3], [1, 2.5, 0.1], [1.5, 3, 0.05]]], 
    #         [100, 0, 0, [[0.5, 1, 0.55], [0.75, 1.25, 0.3], [1, 2.5, 0.1], [1.5, 3, 0.05]]], 
    #         [100, 0, 0, [[0.5, 1, 0.55], [0.75, 1.25, 0.3], [1, 2.5, 0.1], [1.5, 3, 0.05]]], 
    #         [100, 0, 0, [[0.5, 1, 0.55], [0.75, 1.25, 0.3], [1, 2.5, 0.1], [2, 3.5, 0.05]]], 
    #         [100, 0, 0, [[0.5, 1, 0.55], [0.75, 1.25, 0.3], [1, 2.5, 0.1], [2, 3.5, 0.05]]], 
    #     ],
    # },
    # 'exp': 100,  # 打死BOSS的经验
    # 'shot_times': 9,  # 打几炮才触发掉落判断
})

add_game_config(2, 'world.boss.202.config', {
    # 'leave': [20000000, (30, 45, 60), 10000000], # 全服总血量， 奖励触发所需子弹数， 胜利失败增减血量
    # 'life_minute': range(0, 10),  # 生存时长，配置10分钟
    # 'kill_rate': [0, 10],  # 击杀概率（已废弃）
    # 'coupon_n': 1000,  # 记录boss鸟卷普通掉落，暂时无效
    # 'reward_list': {  # boss创建时间及奖励类型
    #     20: ['stone', 'coupon', 'prop', 'chip'],
    #     21: ['stone', 'coupon', 'prop', 'chip'],
    # },
    # 'reward': {
    #     'stone': [[1, 215], [1, 216], [1, 217], [1, 218]], # 概率2代表2%，物品ID，数量默认1
    #     'prop': [],
    #     'coupon': [], # [[如鸟卷池有鸟卷50%概率，掉落1个]， [房间内boss此字段无效]]
    #     'chip': [
    #         [100, 0, 0, [[0.5, 1, 0.55], [0.75, 1, 0.3], [1, 2, 0.1], [1, 2.5, 0.05]]], 
    #         [100, 0, 0, [[0.5, 1, 0.55], [0.75, 1.25, 0.3], [1, 2, 0.1], [1, 2.5, 0.05]]], 
    #         [100, 0, 0, [[0.5, 1, 0.55], [0.75, 1.25, 0.3], [1, 2, 0.1], [1, 2.5, 0.05]]], 
    #         [100, 0, 0, [[0.5, 1, 0.55], [0.75, 1.25, 0.3], [1, 2, 0.1], [1, 2.5, 0.05]]], 
    #         [100, 0, 0, [[0.5, 1, 0.55], [0.75, 1.25, 0.3], [1, 2.5, 0.1], [1, 2.5, 0.05]]], 
    #         [100, 0, 0, [[0.5, 1, 0.55], [0.75, 1.25, 0.3], [1, 2.5, 0.1], [1, 2.5, 0.05]]], 
    #         [100, 0, 0, [[0.5, 1, 0.55], [0.75, 1.25, 0.3], [1, 2.5, 0.1], [1, 2.5, 0.05]]], 
    #         [100, 0, 0, [[0.5, 1, 0.55], [0.75, 1.25, 0.3], [1, 2.5, 0.1], [1, 2.5, 0.05]]], 
    #         [100, 0, 0, [[0.5, 1, 0.55], [0.75, 1.25, 0.3], [1, 2.5, 0.1], [1.5, 3, 0.05]]], 
    #         [100, 0, 0, [[0.5, 1, 0.55], [0.75, 1.25, 0.3], [1, 2.5, 0.1], [1.5, 3, 0.05]]], 
    #         [100, 0, 0, [[0.5, 1, 0.55], [0.75, 1.25, 0.3], [1, 2.5, 0.1], [1.5, 3, 0.05]]], 
    #         [100, 0, 0, [[0.5, 1, 0.55], [0.75, 1.25, 0.3], [1, 2.5, 0.1], [2, 3.5, 0.05]]], 
    #         [100, 0, 0, [[0.5, 1, 0.55], [0.75, 1.25, 0.3], [1, 2.5, 0.1], [2, 3.5, 0.05]]], 
    #     ],
    # },
    # 'exp': 100,  # 打死BOSS的经验
    # 'shot_times': 9,  # 打几炮才触发掉落判断(已废弃)
    # 'type':452, # 怪物ID
    # 'Ln':0, # 无效字段
    # 'Lj':50000, # 无效字段
})

# 任务id:
# 日常类型（3：表示初级场场次任务，4：表示中级场场次任务，5：表示高级场场次任务，1：表示每日任务，2：表示每周任务）
# 任务类型（0：击杀任意怪，1：击杀指定怪，2：获取金币，3：获取钻石，4：使用冰冻，5：使用召唤，6：使用狂暴，7：使用超级武器）
# 任务类型指定的id，没有为0
# 任务需要的次数
# 完成任务给予的活跃度
# 奖励
add_game_config(2, 'task.202.config', {
    100021: [4, 0, 0, 75, 0, {'props':[{'id': 202, 'count': 1}]}, '捕捉<任意鸟类>75个'], 
    100022: [4, 2, 0, 450000, 0, {'props':[{'id': 205, 'count': 1}]}, '捕获鸟蛋45万'], 
    100023: [4, 0, 0, 75, 0, {'props':[{'id': 202, 'count': 1}]}, '捕捉<任意鸟类>75个'], 
    100024: [4, 2, 0, 750000, 0, {'props':[{'id': 205, 'count': 1}]}, '捕获鸟蛋75万'], 
    100025: [4, 1, 104, 22, 0, {'props':[{'id': 202, 'count': 1}]}, '捕捉翠鸟22个'], 
    100026: [4, 1, 105, 22, 0, {'props':[{'id': 205, 'count': 1}]}, '捕捉八哥22个'], 
    100027: [4, 1, 106, 22, 0, {'props':[{'id': 202, 'count': 1}]}, '捕捉黄鹂22个'], 
    100028: [4, 1, 107, 22, 0, {'props':[{'id': 205, 'count': 1}]}, '捕捉画眉22个'], 
    100029: [4, 1, 108, 18, 0, {'props':[{'id': 202, 'count': 1}]}, '捕捉杜鹃18个'], 
    100030: [4, 1, 109, 18, 0, {'props':[{'id': 205, 'count': 1}]}, '捕捉鹦鹉18个'], 
    100031: [4, 1, 112, 45, 0, {'props':[{'id': 202, 'count': 1}]}, '捕捉飞龙45个'], 
    100032: [4, 1, 113, 45, 0, {'props':[{'id': 205, 'count': 1}]}, '捕捉秃鹫45个'], 
    100035: [4, 1, 114, 45, 0, {'props':[{'id': 202, 'count': 1}]}, '捕捉蝙蝠45个'], 
    100036: [4, 1, 115, 45, 0, {'props':[{'id': 205, 'count': 1}]}, '捕捉仙鹤45个'], 
    100033: [4, 1, 116, 36, 0, {'props':[{'id': 202, 'count': 1}]}, '捕捉极乐鸟36个'], 
    100034: [4, 1, 117, 36, 0, {'props':[{'id': 205, 'count': 1}]}, '捕捉凤凰36个'], 
    100037: [4, 4, 202, 1, 0, {'props':[{'id': 202, 'count': 1}]}, '使用<全屏冰冻>'], 
    100038: [4, 5, 205, 2, 0, {'props':[{'id': 205, 'count': 1}]}, '使用<赏金传送>'], 
    100039: [4, 4, 202, 2, 0, {'props':[{'id': 203, 'count': 1}]}, '使用<全屏冰冻>'], 
    100040: [4, 5, 205, 4, 0, {'props':[{'id': 203, 'count': 1}]}, '使用<赏金传送>'], 
})
