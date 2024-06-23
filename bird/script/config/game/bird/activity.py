#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-02-17

from framework.helper import add_game_config


def __expand_props(*props_list):
    props = []
    for _id, _count in props_list:
        props.append({'id': _id, 'count': _count})
    return props


add_game_config(2, 'activity.config', {
    'version': 1,
    'tip': u'有新活动啦! 快来参加吧',
    'list': [
        {
            'id': 380,
            'type': 380,
            'key': 'act_380_161001_161007',
            'var': {
                '0': {'props': __expand_props([201, 1], [202, 1])},
                '1': {'diamond': 5, 'props': __expand_props([201, 2], [202, 2])},
                '2': {'diamond': 5, 'props': __expand_props([201, 2], [202, 2], [204, 1])},
                '3': {'diamond': 10, 'props': __expand_props([201, 2], [202, 2], [203, 1])},
                '4': {'diamond': 10, 'props': __expand_props([201, 5], [202, 5], [205, 5], [203, 1])},
                '5': {'diamond': 15, 'props': __expand_props([201, 5], [202, 5], [203, 3])},
                '6': {'diamond': 15, 'props': __expand_props([201, 10], [202, 10], [205, 10], [203, 3])},
                '7': {'props': __expand_props([211, 1])},
                '8': {'props': __expand_props([212, 1])},
                '9': {'props': __expand_props([213, 1])},
            },
            'desc': u'国庆专享福利，登陆免费领道具',
            'start': '2016-10-01 00:00:00',
            'end': '2016-10-07 23:59:59',
        },
        {
            'id': 381,
            'type': 381,
            'var': [
                [200000, {'props': __expand_props([201, 1], [202, 1])}],
                [500000, {'props': __expand_props([201, 2], [202, 2])}],
                [1000000, {'props': __expand_props([201, 2], [202, 2], [205, 2])}],
                [3000000, {'diamond': 2, 'props': __expand_props([201, 3], [202, 2], [205, 2])}],
                [5000000, {'diamond': 3, 'props': __expand_props([201, 3], [202, 2], [205, 3])}],
                [10000000, {'diamond': 5, 'props': __expand_props([201, 3], [202, 3], [205, 3])}],
                [15000000, {'diamond': 5, 'props': __expand_props([201, 5], [202, 3], [205, 5])}],
                [20000000, {'diamond': 8, 'props': __expand_props([201, 8], [202, 3], [205, 5])}],
                [20000000, {'diamond': 10, 'props': __expand_props([201, 10], [202, 3], [205, 8])}],
            ],
            'desc': u'欢乐国庆，你捕鸟我送礼',
            'start': '2016-10-01 00:00:00',
            'end': '2016-10-07 23:59:59',
        },
        {
            'id': 382,
            'type': 382,
            'var': [
                [0.15, {'props': __expand_props([202, 2])}],
                [0.05, {'diamond': 2}],
                [0.15, {'chip': 20000}],
                [0.05, {'props': __expand_props([203, 1])}],
                [0.15, {'diamond': 5}],
                [0.1, {'chip': 50000}],
                [0.3, {'props': __expand_props([201, 2])}],
                [0.05, {'props': __expand_props([205, 2])}],
            ],
            'desc': u'鸟蛋抽奖',
            'start': '2016-10-01 00:00:00',
            'end': '2016-10-07 23:59:59',
        },
        {
            'id': 383,
            'type': 383,
            'key': 'act_380_170127_170202',
            'var': {
                '0': {'props': __expand_props([201, 15], [202, 5])},
                '1': {'props': __expand_props([201, 20], [202, 5])},
                '2': {'props': __expand_props([201, 20], [202, 5], [205, 5])},
                '3': {'props': __expand_props([201, 20], [202, 5], [205, 5], [203, 5])},
                '4': {'props': __expand_props([201, 20], [202, 5], [205, 5], [203, 10])},
                '5': {'props': __expand_props([201, 30], [202, 5], [205, 5], [203, 10])},
                '6': {'props': __expand_props([201, 40], [202, 5], [205, 5], [203, 10])},
                '7': {'props': __expand_props([201, 40], [202, 5], [205, 5], [203, 10], [204, 5])},
                '8': {'props': __expand_props([201, 40], [202, 5], [205, 5], [203, 10], [204, 10])},
                '9': {'props': __expand_props([201, 40], [202, 5], [205, 5], [203, 10], [204, 15])},
            },
            'desc': u'春节活动',
            'start': '2017-01-27 00:00:00',
            'end': '2017-02-02 23:59:59',
        },
    ]
})

add_game_config(2, 'red_packet.config', {
    'min_cost': 500000,     # 最少100rmb才发送红包
    'percentage': 1,      #红包比例%
    'average_chip_count': 1000,   # 平均获得鸟蛋数
})

add_game_config(2, 'special_packet.config', {
    'start_today': '2018-10-18 00:00:00',
    'end_today': '2018-10-18 23:59:59',
    'start_hours': '18:00:00',
    'end_hours': '20:00:00',
    'total_price': 50, #红包数量(万)
    'number': 1000,     #红包个数
    'interval_time': 600,  #每次发放间隔分钟
    'get_time': 10,     #领取次数
})


# 活动的hot字段: 0-没有，1-最新，2-推荐，3-热门

# 奖励配置是参考的动享捕鱼，概率是凭感觉瞎填的
# 概率‘万分比’，8合1=1W
add_game_config(2, 'activity.pay.config',
    {
        'id': '101_2019-04-17',
        'model': 1,
        'hot':2,
		'show': 0,
        'tips':1,
        'order':10,
        'name': u'幸运轮盘',
        'start': '2019-04-17 00:00:00',
        'end': '2019-04-18 23:59:59',
        'need_pay': 100,
        'desc': u'充值转盘抽奖',
        'rw_list': {
            '0': {'rate': 2250, 'reward': {'chip': 5000}},
            '1': {'rate': 600, 'reward': {'diamond': 30}},
            '2': {'rate': 600, 'reward': {'props': [{'id': 203, 'count': 2}]}},
            '3': {'rate': 2250, 'reward': {'diamond': 10}},
            '4': {'rate': 1200, 'reward': {'chip': 10000}},
            '5': {'rate': 600, 'reward': {'props': [{'id': 202, 'count': 20}]}},
            '6': {'rate': 100, 'reward': {'props': [{'id': 204, 'count': 1}]}},
            '7': {'rate': 1200, 'reward': {'diamond': 20}},
            '8': {'rate': 600, 'reward': {'chip': 15000}},
            '9': {'rate': 600, 'reward': {'props': [{'id': 205, 'count': 20}]}},
        }
    }
, False)

# 七日类活动【爆蛋7天乐  登录有礼】
# 任务id:
# 0日常类型（3：表示初级场场次任务，4：表示中级场场次任务，5：表示高级场场次任务，1：表示每日任务，2：表示每周任务，6:活动任务）
# 1任务类型（0：击杀任意怪，1：击杀指定怪，2：获取金币，3：获取钻石，4：使用冰冻，5：使用召唤，6：使用狂暴，7：使用超级武器，8：签到，9：分享，10：消耗钻石）
# 2任务类型指定的id，没有为0
# 3任务需要的次数
# 4完成任务给予的活跃度
# 5奖励
# 6任务名称
add_game_config(2, 'activity.task.config',
    {
        'id': '201_2019-04-16',
        'model': 2,
        'hot':3,
        'show': 0,
        'tips':1,
        'order':8,
        'name': u'爆蛋7天乐',
        'start': '2019-04-16 00:00:00',
        'end': '2019-04-22 23:59:59',
        'reward':{'chip': 50000},
        'desc': u'在指定时间内，捕捉指定数量鸟类，可以获得奖励',
        'task':{
        105001:[6, 0, 0, 600, 0, {'diamond': 5}, '累计捕鸟600只' ],
        105002:[6, 1, 181, 10, 0, {'diamond': 10}, '捕捉10只奖金仙鹤' ],
        105003:[6, 0, 0, 1200, 0, {'diamond': 15}, '累计捕鸟1200只' ],
        105004:[6, 1, 182, 15, 0, {'diamond': 20}, '捕捉15只奖金极乐鸟' ],
        105005:[6, 0, 0, 1800, 0, {'diamond': 25}, '累计捕鸟1800只' ],
        105006:[6, 1, 183, 36, 0, {'diamond': 30}, '捕捉36只奖金凤凰' ],
        105007:[6, 0, 0, 2888, 0, {'props': [{'id': 203, 'count': 1}]}, '累计捕鸟2888只' ],
        }
    }
, False)

#type
#    1: 表示打怪消耗金币数的排行榜
add_game_config(2, 'activity.rank.config',
    {
        'id': '301_2019-04-20',
        'model': 3,
        'type':1,
        'hot':3,
        'show': 0,
        'tips':1,
        'order':6,
        'name': u'炮王之王',
        'start': '2019-04-10 00:00:00',
        'end': '2019-04-12 23:59:59',
        'desc': u'在指定时间内，获取排名可以获得奖励',
        'count':20,
        'level':[[1], [2], [3], range(4, 10+1), range(11, 20+1)],
        'reward':[
                {'chip': 1000000},
                {'chip': 500000},
                {'chip': 300000},
                {'props': [{'id': 20008007, 'count': 1}]},
                {'props': [{'id': 20007007, 'count': 1}]},
                ]
    }
, False)

add_game_config(2, 'activity.login.config',
    {
        'id': '401_2018-12-12',
        'model': 4,
        'hot':2,
        'show': 0,
        'tips':1,
        'order':4,
        'name': u'登录有礼',
        'start': '2019-01-17 00:00:00',
        'end': '2019-01-17 23:59:59',
        'desc': u'签到领奖',
        'reward':[
                {'props': [{'id': 20010001, 'count': 1}, {'id': 202, 'count': 1}, {'id': 205, 'count': 1}]},
                {'props': [{'id': 20003001, 'count': 1}, {'id': 202, 'count': 1}, {'id': 205, 'count': 1}]},
                {'props': [{'id': 20004001, 'count': 1}, {'id': 202, 'count': 1}, {'id': 205, 'count': 1}]},
                {'props': [{'id': 20005001, 'count': 1}, {'id': 202, 'count': 1}, {'id': 205, 'count': 1}, {'id': 203, 'count': 1}]},
                {'props': [{'id': 20006001, 'count': 1}, {'id': 202, 'count': 2}, {'id': 205, 'count': 2}]},
                {'props': [{'id': 20007001, 'count': 1}, {'id': 202, 'count': 2}, {'id': 205, 'count': 2}]},
                {'props': [{'id': 20008001, 'count': 1}, {'id': 202, 'count': 2}, {'id': 205, 'count': 2}, {'id': 203, 'count': 2}]}
                ]
    }
, False)

add_game_config(2, 'activity.share.config',
    {
        'id': '501_2018-09-01',
        'model': 5,
        'hot':1,
        'show': 0,
        'tips':1,
        'order':1,
        'name': u'关注有礼',
        'start': '2018-09-01 00:00:00',
        'end': '2018-09-01 23:59:59',
        'desc': u'关注福利',
    }
, False)


# type 1:武器，2:鸟蛋，3:钻石
add_game_config(2, 'activity.discount.config',
    {
        'id': '601_2019-04-17',
        'model': 6,
        'hot':3,
        'show': 0,
        'tips':1,
        'order':2,
        'name': u'直购特卖场',
        'start': '2019-04-17 00:00:00',
        'end': '2019-04-18 23:59:59',
        'desc': u'商品打折',
        'product':[
            {'type':1, 'id':20006, 'product_id':'100901', 'price': 79, 'discount': '9'}
        ]
    }
, False)

add_game_config(2, 'activity.give.config',
    {
        'id': '701_2019-04-20',
        'model': 7,
        'hot':2,
		'show': 0,
        'tips':1,
        'order':12,
        'name': u'神兵天降',
        'start': '2019-04-10 00:00:00',
        'end': '2019-04-12 23:59:59',
        'desc': u'累积充值对应的奖励金额，即可享受限时免费的超级炫酷炮台<color=#FFFF00FF>一天</color>！',
        'rw_list':
            {1280: {'props': [{'id': 20007007, 'count': 1}]},
            500: {'props': [{'id': 20004007, 'count': 1}]},
            880: {'props': [{'id': 20006007, 'count': 1}]},
            200: {'props': [{'id': 20001007, 'count': 1}]},
            300: {'props': [{'id': 20002007, 'count': 1}]}},

    }
, False)
