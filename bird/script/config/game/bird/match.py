#!/usr/bin/env python
# -*- coding=utf-8 -*-

from framework.helper import add_game_config


add_game_config(2, 'match.config', {
    'room_type': 211,
    'room_name': u'快速场',
    'room_fee': 0,
    'base_point': 1,
    'chip_min': 0,
    'chip_max': -1,
    'barrel_min': 5,
    'barrel_max': 5000,
    'level_min': 1,
    'level_max': 32,
    'barrel_min1': 5,
    'barrel_max1': 5000,
    'level_min1': 1,
    'level_max1': 32,
    'max_point': 500,
    'show': '00:00:00',
    'start': '00:00:00',
    'end_apply': '23:59:59',
    'end': '23:00:00',
})


add_game_config(2, 'match.normal.config',
    {
        'bullet':[600, 400, 200],
        'barrel':[10, 15, 20],
        'left_time': 60*3.5,
        'start_1': 12,
        'end_1': 14,
        'start_2': 20,
        'end_2': 22,
}, False)

add_game_config(2, 'match.rank.reward',
            {
                1:{
                    'cost': 2000,
                    'count':3,
                    'level':[[1], [2], [3]],
                    'reward':[
                                {'chip': 8000},
                                {'chip': 4000},
                                {'chip': 2400},
                            ]
                },
                2:{
                    'cost': 12500,
                    'count':3,
                    'level':[[1], [2], [3]],
                    'reward':[
                                {'chip': 50000},
                                {'chip': 25000},
                                {'chip': 15000},
                            ]
                },
                3:{
                    'cost': 125000,
                    'count':3,
                    'level':[[1], [2], [3]],
                    'reward':[
                                {'chip': 500000},
                                {'chip': 250000},
                                {'chip': 150000},
                            ]
                }
            }
    )

add_game_config(2, 'match.event.config', [
    {'action': 'day_rank', 'loop': 'daily', 'hms': '00:00:10'},  # 每天00:00发放前一天奖励
    {'action': 'week_rank', 'loop': 'weekly', 'hms': '12:00:00', 'weekday': 1},  # 每周一中午12:00发放上周冠军奖励 (1-7)
    # {'action': 'month_rank', 'loop': 'monthly', 'hms': '12:00:30', 'day': 1},  # 每月一号中午12:00发放上月冠军奖励 (1-31)
    {'action': 'end_match', 'loop': 'daily', 'hms': '23:00:00'}  # 比赛结束
])


def __expand_props(*props_list):
    props = []
    for _id, _count in props_list:
        props.append({'id': _id, 'count': _count})
    return props


add_game_config(2, 'day.match.reward', [
    {'rank': [0, 0], 'reward': {'props': __expand_props([214, 40])}},
    {'rank': [1, 1], 'reward': {'props': __expand_props([214, 20])}},
    {'rank': [2, 2], 'reward': {'props': __expand_props([214, 10])}},
    {'rank': [3, 9], 'reward': {'props': __expand_props([214, 5])}},
    {'rank': [10, 49], 'reward': {'props': __expand_props([213, 5])}},
    {'rank': [50, 99], 'reward': {'props': __expand_props([213, 3])}},
    {'rank': [100, 199], 'reward': {'props': __expand_props([212, 3])}},
    {'rank': [200, 299], 'reward': {'props': __expand_props([211, 3])}},
    {'rank': [300, 499], 'reward': {'props': __expand_props([211, 2])}},
    {'rank': [500, 999], 'reward': {'props': __expand_props([211, 1])}}
])

__fake_rank = [
    [10, 15, 5],
    [20, 40, 20],
    [50, 90, 40],
    [100, 190, 90],
    [200, 290, 90],
    [300, 480, 180],
    [500, 900, 400]
]

__fake_rank_total = 0
for _left, _right, _count in __fake_rank:
    __fake_rank_total += _count

add_game_config(2, 'day.fake.rank', {
    'fake': __fake_rank,
    'fake_total': __fake_rank_total,
    'total': 1000
})

# add_game_config(2, 'week.match.reward', {'rmb': 20000})
add_game_config(2, 'week.match.reward', {'props': __expand_props([214, 200])})

add_game_config(2, 'month.match.reward', {'rmb': 80000})

add_game_config(2, 'match.task.config', {'id': 101, 'score': 2400, 'reward': {'diamond': 100}})

add_game_config(2, 'match.vip.addition', [
    [9, 15, u'加成15%'],
    [8, 10, u'加成10%'],
    [7, 7, u'加成7%']
])

add_game_config(2, 'match.barrel.addition', [
    [10000, 15, u'加成15%'],
    [9000, 10, u'加成10%'],
    [8000, 8, u'加成8%'],
    [7000, 6, u'加成6%'],
    [6000, 4, u'加成4%'],
    [5000, 2, u'加成2%']
])

add_game_config(2, 'match.cook.task', [
    {'left': 1500, 'score': 100},
    {'left': 1000, 'score': 200},
    {'left': 500, 'score': 300}
])
