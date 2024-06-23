#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-01-12

from framework.helper import add_game_config

add_game_config(2, 'task.config', {
    'task': [
        {'type': 1, 'desc': u'捕获', 'range': [10, 50], 'degree': [[30, 10], [10, 5]]},
        {'type': 2, 'desc': u'捕获BOSS', 'range': [1, 3], 'degree': 10},
        {'type': 3, 'desc': u'捕获奖金鸟', 'range': [3, 5], 'degree': 10},
        {'type': 11, 'desc': u'赚取鸟蛋', 'range': [300, 500], 'degree': 10},
        {'type': 21, 'desc': u'每日登陆', 'degree': 10},
        {'type': 31, 'desc': u'充值任意金额', 'degree': 20}
    ],
    'daily': [
        [2, 3, 11, 21],
        [2, 3, 11, 21],
        [2, 3, 11, 21],
        [2, 3, 11, 21],
        [2, 3, 11, 21],
        [2, 3, 11, 21],
        [2, 3, 11, 21, 31],
    ],
    'total_degree': 100,
    'reward': [
        {'degree': 50, 'reward': {'chip': 2000}},
        {'degree': 80, 'reward': {'chip': 5000}},
        {'degree': 100, 'reward': {'chip': 10000}},
    ]
})

# 任务id:
# 0日常类型（3：表示初级场场次任务，4：表示中级场场次任务，5：表示高级场场次任务，1：表示每日任务，2：表示每周任务）
# 1任务类型（0：击杀任意怪，1：击杀指定怪，2：获取金币，3：获取钻石，4：使用冰冻，5：使用召唤，6：使用狂暴，7：使用超级武器，8：签到，9：分享，10：消耗钻石）
# 2任务类型指定的id，没有为0
# 3任务需要的次数
# 4完成任务给予的活跃度
# 5奖励
# 6任务名称
add_game_config(2, 'task.daily.config', {
    103001: [1, 8, 0, 1, 10, {}, '签到1次'], 
    103002: [1, 0, 0, 1000, 15, {}, '捕捉<任意鸟类>1000个'], 
    103003: [1, 2, 0, 100000, 15, {}, '捕鸟获得100000鸟蛋'], 
    103004: [1, 3, 0, 10, 15, {}, '获得10钻石'], 
    103005: [1, 4, 202, 3, 10, {}, '使用道具<全屏冰冻>3次'], 
    103006: [1, 5, 205, 2, 10, {}, '使用道具<赏金传送>2次'], 
    103007: [1, 6, 203, 1, 20, {}, '使用道具<狂暴无双>1次'], 
    103008: [1, 7, 204, 1, 20, {}, '使用道具<超级武器>1次'], 
    103009: [1, 10, 0, 20, 20, {}, '消费20钻石'], 
    103010: [1, 1, 553, 1, 15, {}, '捕捉<全屏炸弹怪>1个'], 
})

add_game_config(2, 'task.week.config', {
    104001: [2, 8, 0, 5, 15, {}, '签到5次'], 
    104002: [2, 4, 202, 30, 15, {}, '使用道具<全屏冰冻>30次'], 
    104003: [2, 5, 205, 30, 15, {}, '使用道具<赏金传送>30次'], 
    104004: [2, 1, 501, 5, 10, {}, '捕捉<鸟卷怪>5个'], 
    104005: [2, 1, 511, 5, 10, {}, '捕捉<靶卷怪>5个'], 
    104006: [2, 0, 0, 15000, 15, {}, '捕捉<任意鸟类>15000个'], 
    104007: [2, 2, 0, 5000000, 15, {}, '捕鸟获得5000000鸟蛋'], 
    104008: [2, 3, 0, 30, 20, {}, '获得30钻石'],
    104009: [2, 10, 0, 500, 20, {}, '消费500钻石'], 
    104010: [2, 9, 0, 3, 15, {}, '完成<分享>3次'], 
})

add_game_config(2, 'day.activity.config', {
    30: {'diamond': 1}, 
    60: {'diamond': 2}, 
    90: {'diamond': 5}, 
    120: {'diamond': 8}, 
    150: {'diamond': 12}, 
})

add_game_config(2, 'week.activity.config', {
    30: {'diamond': 2}, 
    60: {'diamond': 5}, 
    90: {'diamond': 10}, 
    120: {'diamond': 15}, 
    150: {'diamond': 30}, 
})
