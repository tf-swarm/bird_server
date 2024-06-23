#!/usr/bin/env python
# -*- coding=utf-8 -*-


from framework.helper import add_game_config, add_room_map, Global


add_game_config(2, 'room.config', [
    {
        'room_type': 200, # 新手房配置
        'room_name': u'新手海岛',
        'room_fee': 0,
        'base_point': 1,
        'chip_min': 0,
        'chip_max': -1,
        'barrel_min': 1,            # 能进入最小炮倍数
        'barrel_max': 30,           # 能进入最大炮倍数
        'level_min': 1,
        'level_max': 4,
        'barrel_min1': 1,           # 能开炮最小开炮倍数
        'barrel_max1': 30,          # 能开炮最大炮倍数
        'level_min1': 1,
        'level_max1': 4,
        'max_point': 250,           # 最大鸟分数倍率
    },
    {
        'room_type': 201,
        'room_name': u'新手海岛',
        'room_fee': 0,
        'base_point': 1,
        'chip_min': 0,
        'chip_max': -1,
        'barrel_min': 1,            # 能进入最小炮倍数
        'barrel_max': 10000,           # 能进入最大炮倍数，默认为90（修改）
        'level_min': 1,
        'level_max': 32,
        'barrel_min1': 5,           # 能开炮最小开炮倍数
        'barrel_max1': 250,          # 能开炮最大炮倍数
        'level_min1': 1,
        'level_max1': 14,
        'max_point': 250,           # 最大鸟分数倍率
    },
    {
        'room_type': 202,
        'room_name': u'林海雪原',
        'room_fee': 0,
        'base_point': 1,
        'chip_min': 50000,
        'chip_max': -1,
        'barrel_min': 300,          
        'barrel_max': 10000,        
        'level_min': 15,
        'level_max': 32,
        'barrel_min1': 300,
        'barrel_max1': 1500,
        'level_min1': 15,
        'level_max1': 25,
        'max_point': 500,           # 最大鸟分数倍率
    },
    {
        'room_type': 203,
        'room_name': u'猎龙峡谷',
        'room_fee': 0,
        'base_point': 1,
        'chip_min': 100000,
        'chip_max': -1,
        'barrel_min': 2000,
        'barrel_max': 10000,
        'level_min': 26,
        'level_max': 32,
        'barrel_min1': 2000,
        'barrel_max1': 10000,
        'level_min1': 26,
        'level_max1': 32,
        'red_dragon': 1,
        'vip_limit': 2,
        'max_point': 500,           # 最大鸟分数倍率
    },

    {
        'room_type': 209,
        'room_name': u'vip房',
        'room_fee': 0,
        'base_point': 1,
        'chip_min': 0,
        'chip_max': -1,
        'barrel_min': 1,
        'barrel_max': 10000,
        'level_min': 1,
        'level_max': 32,
        'barrel_min1': 1,
        'barrel_max1': 10000,
        'level_min1': 1,
        'level_max1': 37,
        'red_dragon': 1,
        'vip_limit': 2,
        'max_point': 500,
    },
])

if Global.run_mode == 1:
    add_room_map(2, 200, [20001])
    add_room_map(2, 201, [20000, 20002, 20004])
    add_room_map(2, 202, [20006, 20008, 20010])
    add_room_map(2, 203, [20012, 20014])
    add_room_map(2, 209, [20009])
    add_room_map(2, 211, [20016])
    add_room_map(2, 231, [20018])
elif Global.run_mode == 2:
    add_room_map(2, 200, 20001)
    add_room_map(2, 201, 20000)
    add_room_map(2, 202, 20002)
    add_room_map(2, 203, 20004)
    add_room_map(2, 209, 20009)
    add_room_map(2, 211, 20100)
    add_room_map(2, 231, 20300)
else:
    add_room_map(2, 200, 20001)
    add_room_map(2, 201, 20000)
    add_room_map(2, 202, 20002)
    add_room_map(2, 203, 20004)
    add_room_map(2, 209, 20009)
    add_room_map(2, 211, 20100)
    add_room_map(2, 231, 20300)

add_game_config(2, 'timeline.200.config', {
    'total': 17 * 600,
    'boss': [],
    'tide': [15 * 600, 15 * 600],
    'bounty': [],
    'year_monster':[],
    'diamond':[],
})

add_game_config(2, 'timeline.201.config', {
    'total': 17 * 600,
    'boss': [6 * 600, 8 * 600], # 单位：600=1min
    'tide': [15 * 600, 15 * 600],
    'bounty': [],
    'year_monster':[20 * 600, 20 * 600],
    'diamond':[1 * 600, 10 * 600, [2,8]],
})

add_game_config(2, 'timeline.202.config', {
    'total': 21 * 600,
    'boss': [6 * 600, 5 * 600],
    'tide': [15 * 600, 15 * 600],
    'bounty': [16 * 600],
    'year_monster':[20 * 600, 20 * 600],
    'diamond':[1 * 600, 10 * 600, [16, 60]],
})

add_game_config(2, 'timeline.203.config', {
    'total': 21 * 600,
    'boss': [6 * 600, 5 * 600],
    'tide': [15 * 600, 15 * 600],
    'bounty': [16 * 600],
    'year_monster':[20 * 600, 20 * 600],
    'diamond':[1 * 600, 10 * 600, [60,240]],
})

add_game_config(2, 'timeline.209.config', {
    'total': 21 * 600,
    'boss': [6 * 600, 8 * 600],
    'tide': [15 * 600, 15 * 600],
    'bounty': [16 * 600],
    'year_monster':[20 * 600, 20 * 600],
    'diamond':[1 * 600, 10 * 600, [16, 60]],
})

add_game_config(2, 'timeline.211.config', {
    'total': 17 * 600,
    'boss': [],
    'tide': [],
    'bounty': [],
    'year_monster':[],
    'diamond':[],
})

add_game_config(2, 'timeline.231.config', {
    'total': 17 * 600,
    'boss': [],
    'tide': [],
    'bounty': [],
    'year_monster':[],
    'diamond':[],
})

add_game_config(2, 'dragon.boat.reward', {
    'rate':
        {
            'B':20,
            'C':20,
            'D':0,
        },
    'add_rate':0.625,
    'random_rate':[5,10],
})

'''
超级武器配置
multi  击杀倍率
baseReward  基础奖励参考值
minR 最小获得奖励倍率
maxR 最大获得奖励倍率
c_reward = baseReward * random(minR, maxR)
r_realreward = multi * birdlist  r_realreward ≈ c_reward && r_realreward < maxReward
'''

add_game_config(2, 'super.weapon.200.config', {'multi': 1000, 'baseReward': 100000, 'minR': 0.1, 'maxR': 3})
add_game_config(2, 'super.weapon.201.config', {'multi': 1000, 'baseReward': 100000, 'minR': 0.1, 'maxR': 3})
add_game_config(2, 'super.weapon.202.config', {'multi': 1000, 'baseReward': 100000, 'minR': 0.1, 'maxR': 3})
add_game_config(2, 'super.weapon.203.config', {'multi': 1000, 'baseReward': 100000, 'minR': 0.1, 'maxR': 3})
add_game_config(2, 'super.weapon.209.config', {'multi': 1000, 'baseReward': 100000, 'minR': 0.1, 'maxR': 3})
add_game_config(2, 'super.weapon.211.config', {'multi': 1000, 'baseReward': 100000, 'minR': 0.1, 'maxR': 3})
add_game_config(2, 'super.weapon.231.config', {'multi': 1000, 'baseReward': 100000, 'minR': 0.1, 'maxR': 3})

add_game_config(2, 'bonus.pool.ratio', 0)

__barrel_unlock_config = [
    {'level': 1, 'multiple': 5}, 
    {'level': 2, 'multiple': 10, 'diamond': 3, 'reward': {'chip': 500}}, 
    {'level': 3, 'multiple': 20, 'diamond': 3, 'reward': {'chip': 500}}, 
    {'level': 4, 'multiple': 30, 'diamond': 5, 'reward': {'chip': 750}}, 
    {'level': 5, 'multiple': 40, 'diamond': 5, 'reward': {'chip': 750}}, 
    {'level': 6, 'multiple': 50, 'diamond': 7, 'reward': {'chip': 1000}}, 
    {'level': 7, 'multiple': 60, 'diamond': 7, 'reward': {'chip': 1000}}, 
    {'level': 8, 'multiple': 70, 'diamond': 10, 'reward': {'chip': 1250}}, 
    {'level': 9, 'multiple': 80, 'diamond': 10, 'reward': {'chip': 1250}}, 
    {'level': 10, 'multiple': 90, 'diamond': 15, 'reward': {'chip': 1500}}, 
    {'level': 11, 'multiple': 100, 'diamond': 15, 'reward': {'chip': 1500}}, 
    {'level': 12, 'multiple': 150, 'diamond': 20, 'reward': {'chip': 1750}}, 
    {'level': 13, 'multiple': 200, 'diamond': 20, 'reward': {'chip': 1750}}, 
    {'level': 14, 'multiple': 250, 'diamond': 25, 'reward': {'chip': 2000}}, 
    {'level': 15, 'multiple': 300, 'diamond': 25, 'reward': {'chip': 2000}}, 
    {'level': 16, 'multiple': 350, 'diamond': 30, 'reward': {'chip': 2250}}, 
    {'level': 17, 'multiple': 400, 'diamond': 30, 'reward': {'chip': 2250}}, 
    {'level': 18, 'multiple': 450, 'diamond': 35, 'reward': {'chip': 2500}}, 
    {'level': 19, 'multiple': 500, 'diamond': 40, 'reward': {'chip': 2500}}, 
    {'level': 20, 'multiple': 600, 'diamond': 45, 'reward': {'chip': 3000}}, 
    {'level': 21, 'multiple': 700, 'diamond': 50, 'reward': {'chip': 3000}}, 
    {'level': 22, 'multiple': 800, 'diamond': 60, 'reward': {'chip': 3500}}, 
    {'level': 23, 'multiple': 900, 'diamond': 70, 'reward': {'chip': 3500}}, 
    {'level': 24, 'multiple': 1000, 'diamond': 80, 'reward': {'chip': 4000}}, 
    {'level': 25, 'multiple': 1500, 'diamond': 90, 'reward': {'chip': 4500}}, 
    {'level': 26, 'multiple': 2000, 'diamond': 100, 'reward': {'chip': 5000}}, 
    {'level': 27, 'multiple': 2500, 'diamond': 200, 'reward': {'chip': 6000}}, 
    {'level': 28, 'multiple': 3000, 'diamond': 300, 'reward': {'chip': 7000}}, 
    {'level': 29, 'multiple': 3500, 'diamond': 400, 'reward': {'chip': 8000}}, 
    {'level': 30, 'multiple': 4000, 'diamond': 500, 'reward': {'chip': 9000}}, 
    {'level': 31, 'multiple': 4500, 'diamond': 550, 'reward': {'chip': 10000}}, 
    {'level': 32, 'multiple': 5000, 'diamond': 600, 'reward': {'chip': 12500}}, 
]

add_game_config(2, 'barrel.unlock.config', __barrel_unlock_config)
add_game_config(2, 'barrel.unlock.led', 28) #炮升级到多少开始发公告
add_game_config(2, 'barrel.unlock.use', 3)  #炮升级到多少使用道具
add_game_config(2, 'barrel.new.player', 4)  #炮升级到多少就不算新手需要蓄水抽水
add_game_config(2, 'barrel.new.room', 4)    #炮升级到多少就从新手场进入到初级
add_game_config(2, 'barrel.max.level', 32)  #炮的最大等级
add_game_config(2, 'barrel.unlock.strong', [37, 37]) #炮在哪个阶段开始强化

add_game_config(2, 'table.limit.times', 20) #退出一个房间多少秒内不再进入此房间

__barrel_level_config = [t['multiple'] for t in __barrel_unlock_config]
add_game_config(2, 'barrel.level.config', __barrel_level_config)


#前面的vip翻倍，后面的不翻倍
add_game_config(2, 'login.reward', {
    'new': [
        [{'chip':1000}, {}],
        [{'chip':800}, {}],
        [{'chip':1000}, {'props':[{'id': 202, 'count':2}]}],
        [{'chip':1500}, {'props':[{'id': 205, 'count':2}]}],
        [{'chip':1500}, {'props':[{'id': 203, 'count':2}]}],
        [{'chip':2000}, {}],
        [{'chip':8000}, {}],
    ],
    'common': [
        [{'chip': 500}, {}],
        [{'chip': 800}, {}],
        [{'chip': 1000}, {'props': [{'id': 202, 'count': 2}]}],
        [{'chip': 1500}, {'props': [{'id': 205, 'count': 2}]}],
        [{'chip': 1500}, {'props': [{'id': 203, 'count': 2}]}],
        [{'chip': 2000}, {}],
        [{'chip': 8000}, {}],
    ],
})

# 游戏启动配置  [0]=初始拥有鸟蛋，[1]=新手池中鸟蛋数,[2]=private池中鸟卷数量
add_game_config(2, 'game.startup', [500, 50000, 5])

add_game_config(2, 'benefit.config', {
    'wait': [15, 30, 180, 300, 300],
    'reward': [
    {'max': 0, 'times': 0},
    {'max': 500, 'times': 1},
    {'max': 800, 'times': 1},
    {'max': 1000, 'times': 1},
    {'max': 2000, 'times': 1},
    {'max': 3000, 'times': 1},
    {'max': 5000, 'times': 1},
    {'max': 8000, 'times': 1},
    {'max': 10000, 'times': 1},
    {'max': 15000, 'times': 1},
    {'max': 20000, 'times': 1},
    {'max': 30000, 'times': 1},
    {'max': 50000, 'times': 1},
    ],
    'base': 200,
    # 'limit': 0,
})

add_game_config(2, 'system.announcement', [
    {'content': '过故人庄:', 'font': 2},
    {'content': '   故人具鸡黍，邀我至田家。', 'font': 1},
    {'content': '   绿树村边合，青山郭外斜。', 'font': 1},
    {'content': '   开轩面场圃，把酒话桑麻。', 'font': 1},
    {'content': '   待到重阳日，还来就菊花。', 'font': 1},
])

add_game_config(2, 'expression.config', [
    {'id': 1, 'cost': 100, 'limit': 2000, 'desc': u'好感'},
    {'id': 2, 'cost': 100, 'limit': 2000, 'desc': u'鸡蛋'},
    {'id': 3, 'cost': 100, 'limit': 2000, 'desc': u'小鞋'},
    {'id': 4, 'cost': 100, 'limit': 2000, 'desc': u'酒'},
    {'id': 5, 'cost': 100, 'limit': 2000, 'desc': u'炸弹'},
])

add_game_config(2, 'led.config', {
    'enable': 1,
    'cost': 50,
})

add_game_config(2, 'exp.level',
                [0, 20, 70, 220, 520, 1020, 1770, 2770, 4270, 6270, 
                8770, 11770, 15770, 20770, 26770, 33770, 41770, 50770, 60770, 72770, 
                90770, 111770, 134770, 159770, 187270, 217270, 249770, 284770, 322770, 362770
])

add_game_config(2, 'exp.level.reward', [
    # coupon 话费券 201锁定 202冰冻 203嗜血 204超级武器 205传送门
    {'coupon': 1, 'props': [{'id': 202, 'count': 1}]}, 
    {'diamond': 3, 'props': [{'id': 205, 'count': 1}]},
    {'diamond': 6, 'props': [{'id': 202, 'count': 1}]},
    {'diamond': 10, 'props': [{'id': 205, 'count': 1}]},
    {'diamond': 10, 'props': [{'id': 202, 'count': 1}]},
    {'diamond': 10, 'props': [{'id': 205, 'count': 1}]},
    {'diamond': 10, 'props': [{'id': 202, 'count': 1}]},
    {'diamond': 10, 'props': [{'id': 205, 'count': 1}]},
    {'diamond': 10, 'props': [{'id': 202, 'count': 1}]},
    {'diamond': 10, 'props': [{'id': 203, 'count': 1}]},
    {'diamond': 20, 'props': [{'id': 202, 'count': 1}]},
    {'diamond': 0, 'props': [{'id': 205, 'count': 1}]},
    {'diamond': 0, 'props': [{'id': 202, 'count': 1}]},
    {'diamond': 0, 'props': [{'id': 205, 'count': 1}]},
    {'diamond': 0, 'props': [{'id': 202, 'count': 1}]},
    {'diamond': 0, 'props': [{'id': 205, 'count': 1}]},
    {'diamond': 0, 'props': [{'id': 202, 'count': 1}]},
    {'diamond': 0, 'props': [{'id': 205, 'count': 1}]},
    {'diamond': 0, 'props': [{'id': 202, 'count': 1}]},
    {'diamond': 0, 'props': [{'id': 203, 'count': 1}]},
    {'diamond': 20, 'props': [{'id': 202, 'count': 1}]},
    {'diamond': 20, 'props': [{'id': 205, 'count': 1}]},
    {'diamond': 20, 'props': [{'id': 202, 'count': 1}]},
    {'diamond': 25, 'props': [{'id': 205, 'count': 1}]},
    {'diamond': 25, 'props': [{'id': 202, 'count': 1}]},
    {'diamond': 30, 'props': [{'id': 205, 'count': 1}]},
    {'diamond': 30, 'props': [{'id': 202, 'count': 1}]},
    {'diamond': 35, 'props': [{'id': 205, 'count': 1}]},
    {'diamond': 40, 'props': [{'id': 202, 'count': 1}]},
    {'diamond': 45, 'props': [{'id': 203, 'count': 1}]},
])

add_game_config(2, 'vip.level', [50, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000,100000,150000,200000])

add_game_config(2, 'vip.config', [
    # 单次领取救济金    领取救济金次数  挪到vip
    # 累计充值
    
    # 特权总类——
    # "gift1"赠送礼包1-215
    # "gift2"赠送礼包2-216
    # "skill_wild"开启狂暴
    # "skill_s_weapon"开启超级武器
    # "s_shop"开启限时商城 
    # "day_gift"每日登陆赠送                                                                                                            
    # "day_fill_chip"每日登陆补足
    # "rebate"充值额外返利
    # "weaponId"专属炮台
    # "day_sign_times"7日登录签到奖励翻倍数
    # "kill_box_p"击杀青铜|白银|黄金宝箱概率提升
    # "kill_b_coupon"鸟券怪击杀概率提升
    # "send_t"物品赠送数量
    # "target_range"打靶次数限制
	# "critM"轮盘鸟的翻倍数
	# "red_packets_general"普通红包的VIP领取次数限制
	# "target_exchange" 靶卷兑换数量限制
    {	
        #vip1
        'pay': 50,
        'gift1': {'name': 'v1冲天礼包', 'props': [{'id':202, 'count': 5}]},
        'gift2': {'name': 'v1无双礼包', 'chip': 500},
        'skill_wild': 0, 
        'skill_s_weapon': 0, 
        's_shop': 0, 
        # 'day_gift': {'props': [{'id':215, 'count': 1}, {'id':216, 'count': 1}, {'id':217, 'count': 1}, {'id':218, 'count': 1}]}, 
        'day_sign_times': [500, 750, 750, 1000, 1250, 1250, 1500], 
        # 'kill_box_p': [.015, .01, .005], 
        # 'kill_b_coupon': .01,
        'target_range': [{ 'room_type':201, 'count': 3}],
        'target_exchange': 0,
        'red_packets_general': 2,
        'desc': u'new每日可领取救济金<color=#FFB90F>500</color>鸟蛋\n'
		        #u'new救济金领取次数高达<color=#FFB90F>1</color>次\n'
				# u'new每日登陆额外赠送<color=#FFB90F>4种武器强化材料*1</color>\n'
				#u'new每日签到奖励额外获得高达<color=#FFB90F>125%左右的</color>奖励\n'
				#u'new每日红包领取次数高达<color=#FFB90F>5</color>次\n'
				# u'new击杀<color=#FFB90F>青铜宝箱</color>概率<color=#FFB90F>小幅度</color>提升\n'
				# u'new击杀<color=#FFB90F>鸟券怪</color>概率<color=#FFB90F>小幅度</color>提升\n'
				# u'new命中<color=#FFB90F>世界BOSS</color>鸟蛋奖励<color=#FFB90F>小幅度</color>提升\n'
				u'new每日可进入“初级靶场”<color=#FFB90F>3</color>次\n'
    },	
    {	
        #vip2
        'pay': 200,
        'gift1': {'name': 'v2冲天礼包', 'props': [{'id':202, 'count': 10}]},
        'gift2': {'name': 'v2无双礼包', 'chip': 1000},
        'skill_wild': 1, 
        'skill_s_weapon': 1, 
        's_shop': 1, 
        # 'day_gift': {'props': [{'id':215, 'count': 2}, {'id':216, 'count': 2}, {'id':217, 'count': 2}, {'id':218, 'count': 2}]}, 
        'day_sign_times': [750, 750, 1000, 1250, 1500, 1500, 1750], 
        # 'kill_box_p': [.01875, .0125, .00625], 
        # 'kill_b_coupon': .0125,
        'target_range': [{'room_type':201, 'count': 5},{'room_type':202, 'count': 3}],
        'target_exchange': 2,
        'red_packets_general': 3,
        'desc': u'new每日可领取救济金<color=#FFB90F>800</color>鸟蛋\n'
		        #u'救济金领取次数高达<color=#FFB90F>1</color>次\n'
				u'new永久解锁<color=#FFB90F>狂暴无双</color>限制\n'
				u'new永久解锁<color=#FFB90F>超级武器</color>限制\n'
				u'new永久开启<color=#FFB90F>限时商城</color>功能\n'
				# u'new每日登陆额外赠送<color=#FFB90F>4种武器强化材料*2</color>\n'
				#u'new每日签到奖励额外获得高达<color=#FFB90F>150%左右的</color>奖励\n'
				#u'new每日红包领取次数高达<color=#FFB90F>6</color>次\n'
				# u'击杀<color=#FFB90F>青铜宝箱</color>概率<color=#FFB90F>小幅度</color>提升\n'
				# u'new击杀<color=#FFB90F>白银宝箱</color>概率<color=#FFB90F>小幅度</color>提升\n'
				# u'击杀<color=#FFB90F>鸟券怪</color>概率<color=#FFB90F>小幅度</color>提升\n'
				# u'命中<color=#FFB90F>世界BOSS</color>鸟蛋奖励<color=#FFB90F>小幅度</color>提升\n'
				u'new每日可进入“初级靶场”<color=#FFB90F>5</color>次\n'
				u'new每日可进入“中级靶场”<color=#FFB90F>3</color>次\n'
    },	
    {	
        #vip3
        'pay': 500,
        'gift1': {'name': 'v3冲天礼包', 'props': [{'id':203, 'count': 15}]},
        'gift2': {'name': 'v3无双礼包', 'chip': 2500},
        'skill_wild': 1, 
        'skill_s_weapon': 1, 
        's_shop': 1, 
        # 'day_gift': {'props': [{'id':215, 'count': 3}, {'id':216, 'count': 3}, {'id':217, 'count': 3}, {'id':218, 'count': 3}]}, 
        'day_sign_times': [750, 1000, 1250, 1500, 1750, 1750, 2000], 
        # 'kill_box_p': [.0225, .015, .0075], 
        # 'kill_b_coupon': .015,
        'target_range': [{'room_type':201, 'count': 10},{'room_type':202, 'count': 8},{'room_type':203, 'count': 5}],
        'target_exchange': 4,
        'red_packets_general': 4,
        'desc': u'new每日可领取救济金<color=#FFB90F>1000</color>鸟蛋\n'
		        #u'救济金领取次数高达<color=#FFB90F>1</color>次\n'
				# u'new每日登陆额外赠送<color=#FFB90F>4种武器强化材料*3</color>\n'
				#u'new每日签到奖励额外获得高达<color=#FFB90F>175%左右的</color>奖励\n'
				#u'new每日红包领取次数高达<color=#FFB90F>7</color>次\n'
				# u'击杀<color=#FFB90F>青铜宝箱</color>概率<color=#FFB90F>小幅度</color>提升\n'
				# u'击杀<color=#FFB90F>白银宝箱</color>概率<color=#FFB90F>小幅度</color>提升\n'
				# u'击杀<color=#FFB90F>鸟券怪</color>概率<color=#FFB90F>小幅度</color>提升\n'
				# u'命中<color=#FFB90F>世界BOSS</color>鸟蛋奖励<color=#FFB90F>小幅度</color>提升\n'
				u'new每日可进入“初级靶场”<color=#FFB90F>10</color>次\n'
				u'new每日可进入“中级靶场”<color=#FFB90F>8</color>次\n'
				u'new每日可进入“高级靶场”<color=#FFB90F>5</color>次\n'
    },	
    {	
        #vip4
        'pay': 1000,
        'gift1': {'name': 'v4冲天礼包', 'diamond': 30},
        'gift2': {'name': 'v4无双礼包', 'chip': 5000},
        'skill_wild': 1, 
        'skill_s_weapon': 1, 
        's_shop': 1, 
        # 'day_gift': {'props': [{'id':215, 'count': 5}, {'id':216, 'count': 5}, {'id':217, 'count': 5}, {'id':218, 'count': 5}]}, 
        'day_sign_times': [1000, 1250, 1500, 1750, 2000, 2250, 2500], 
        # 'kill_box_p': [.0375, .025, .0125], 
        # 'kill_b_coupon': .025,
        'weaponId': 20003,
        # 'send_t': 20,
        # 'rebate': 0,
		'target_range': [{'room_type':201, 'count': 20},{'room_type':202, 'count': 15}, {'room_type':203, 'count': 10}],
        'target_exchange': 6,
        'red_packets_general': 5,
        'desc': u'new每日可领取救济金<color=#FFB90F>2000</color>鸟蛋\n'
		        #u'救济金领取次数高达<color=#FFB90F>1</color>次\n'
				# u'new每日登陆额外赠送<color=#FFB90F>4种武器强化材料*5</color>\n'
				#u'new每日签到奖励额外获得高达<color=#FFB90F>200%左右的</color>奖励\n'
				u'new获得贵族专属<color=#FFB90F>翡翠荆棘</color>永久武器\n'
				#u'new每日红包领取次数高达<color=#FFB90F>8</color>次\n'
				# u'new击杀<color=#FFB90F>青铜宝箱</color>概率<color=#FFB90F>中幅度</color>提升\n'
				# u'击杀<color=#FFB90F>白银宝箱</color>概率<color=#FFB90F>小幅度</color>提升\n'
				# u'new击杀<color=#FFB90F>黄金宝箱</color>概率<color=#FFB90F>小幅度</color>提升\n'
				# u'new击杀<color=#FFB90F>鸟券怪</color>概率<color=#FFB90F>中幅度</color>提升\n'
				# u'new命中<color=#FFB90F>世界BOSS</color>鸟蛋奖励<color=#FFB90F>中幅度</color>提升\n'
				# u'new永久开启<color=#FFB90F>道具赠送</color>功能\n'
				# u'new每日赠送他人道具上限<color=#FFB90F>20</color>个\n'
				u'new每日可进入“初级靶场”<color=#FFB90F>20</color>次\n'
				u'new每日可进入“中级靶场”<color=#FFB90F>15</color>次\n'
				u'new每日可进入“高级靶场”<color=#FFB90F>10</color>次\n'
    },	
    {	
        #vip5
        'pay': 2000,
        'gift1': {'name': 'v5冲天礼包', 'diamond': 88},
        'gift2': {'name': 'v5无双礼包', 'chip': 10000},
        'skill_wild': 1, 
        'skill_s_weapon': 1, 
        's_shop': 1, 
        # 'day_gift': {'props': [{'id':215, 'count': 8}, {'id':216, 'count': 8}, {'id':217, 'count': 8}, {'id':218, 'count': 8}]}, 
        'day_sign_times': [1250, 1500, 1750, 2000, 2500, 2750, 3000], 
        # 'kill_box_p': [.045, .03, .015], 
        # 'kill_b_coupon': .03,
        # 'send_t': 50,
        # 'rebate': 0,
		'target_range':[{'room_type':201, 'count': -1 },{'room_type':202, 'count': -1}, {'room_type':203, 'count': -1}],
        'target_exchange': 8,
        'red_packets_general': 5,
        'desc': u'new每日可领取救济金<color=#FFB90F>3000</color>鸟蛋\n'
		        #u'救济金领取次数高达<color=#FFB90F>1</color>次\n'
				# u'new每日登陆额外赠送<color=#FFB90F>4种武器强化材料*8</color>\n'
				#u'new每日签到奖励额外获得高达<color=#FFB90F>250%左右的</color>奖励\n'
				#u'new每日红包领取次数高达<color=#FFB90F>9</color>次\n'
				# u'击杀<color=#FFB90F>青铜宝箱</color>概率<color=#FFB90F>中幅度</color>提升\n'
				# u'new击杀<color=#FFB90F>白银宝箱</color>概率<color=#FFB90F>中幅度</color>提升\n'
				# u'击杀<color=#FFB90F>黄金宝箱</color>概率<color=#FFB90F>小幅度</color>提升\n'
				# u'击杀<color=#FFB90F>鸟券怪</color>概率<color=#FFB90F>中幅度</color>提升\n'
				# u'命中<color=#FFB90F>世界BOSS</color>鸟蛋奖励<color=#FFB90F>中幅度</color>提升\n'
				# u'new每日赠送他人道具上限<color=#FFB90F>50</color>个\n'
				u'new每日进入“靶场”<color=#FFB90F>无限</color>次\n'
    },	
    {	
        #vip6
        'pay': 5000,
        'gift1': {'name': 'v6冲天礼包', 'diamond': 188},
        'gift2': {'name': 'v6无双礼包', 'chip': 30000},
        'skill_wild': 1, 
        'skill_s_weapon': 1, 
        's_shop': 1, 
        # 'day_gift': {'props': [{'id':215, 'count': 10}, {'id':216, 'count': 10}, {'id':217, 'count': 10}, {'id':218, 'count': 10}]}, 
        'day_sign_times': [1250, 1500, 2000, 2250, 2750, 3000, 3250], 
        # 'kill_box_p': [.0525, .035, .0175], 
        # 'kill_b_coupon': .035,
        'weaponId': 20005,
        # 'send_t': 100,
        # 'rebate': 0,
        # 'critM': 1.25,
		'target_range': [{'room_type':201, 'count': -1},{'room_type':202, 'count': -1}, {'room_type':203, 'count': -1}],
        'target_exchange': 10,
        'red_packets_general': 5,
        'desc': u'new每日可领取救济金<color=#FFB90F>5000</color>鸟蛋\n'
		        #u'救济金领取次数高达<color=#FFB90F>1</color>次\n'
				# u'new每日登陆额外赠送<color=#FFB90F>4种武器强化材料*10</color>\n'
				#u'new每日签到奖励额外获得高达<color=#FFB90F>275%左右的</color>奖励\n'
				u'new获得贵族专属<color=#FFB90F>死亡之翼</color>永久武器\n'
				#u'new每日红包领取次数高达<color=#FFB90F>10</color>次\n'
				# u'击杀<color=#FFB90F>青铜宝箱</color>概率<color=#FFB90F>中幅度</color>提升\n'
				# u'击杀<color=#FFB90F>白银宝箱</color>概率<color=#FFB90F>中幅度</color>提升\n'
				# u'new击杀<color=#FFB90F>黄金宝箱</color>概率<color=#FFB90F>中幅度</color>提升\n'
				# u'击杀<color=#FFB90F>鸟券怪</color>概率<color=#FFB90F>中幅度</color>提升\n'
				# u'命中<color=#FFB90F>世界BOSS</color>鸟蛋奖励<color=#FFB90F>中幅度</color>提升\n'
				# u'new每日赠送他人道具上限<color=#FFB90F>100</color>个\n'
				u'每日进入“靶场”<color=#FFB90F>无限</color>次\n'
				# u'new击杀<color=#FFB90F>金鸟</color>有概率获得<color=#FFB90F>1.25</color>倍鸟蛋奖励\n'
    },	
    {	
        #vip7
        'pay': 10000,
        'gift1': {'name': 'v7冲天礼包', 'diamond': 388},
        'gift2': {'name': 'v7无双礼包', 'chip': 60000},
        'skill_wild': 1, 
        'skill_s_weapon': 1, 
        's_shop': 1, 
        # 'day_gift': {'props': [{'id':215, 'count': 12}, {'id':216, 'count': 12}, {'id':217, 'count': 12}, {'id':218, 'count': 12}]}, 
        'day_sign_times': [1500, 1750, 2250, 2500, 3000, 3250, 3750], 
        # 'kill_box_p': [.0675, .045, .0225], 
        # 'kill_b_coupon': .045,
        # 'send_t': 200,
        # 'rebate': 0,
        # 'day_fill_chip': 500000,
        # 'critM': 1.25,
		'target_range': [{'room_type':201, 'count': -1},{'room_type':202, 'count': -1}, {'room_type':203, 'count': -1}],
        'target_exchange': 12,
        'red_packets_general': 5,
        'desc': u'new每日可领取救济金<color=#FFB90F>8000</color>鸟蛋\n'
		        #u'救济金领取次数高达<color=#FFB90F>1</color>次\n'
				# u'new每日登陆额外赠送<color=#FFB90F>4种武器强化材料*12</color>\n'
				#u'new每日签到奖励额外获得高达<color=#FFB90F>300%左右的</color>奖励\n'
				#u'new每日红包领取次数高达<color=#FFB90F>11</color>次\n'
				# u'击杀<color=#FFB90F>青铜宝箱</color>概率<color=#FFB90F>中幅度</color>提升\n'
				# u'击杀<color=#FFB90F>白银宝箱</color>概率<color=#FFB90F>中幅度</color>提升\n'
				# u'击杀<color=#FFB90F>黄金宝箱</color>概率<color=#FFB90F>中幅度</color>提升\n'
				# u'击杀<color=#FFB90F>鸟券怪</color>概率<color=#FFB90F>中幅度</color>提升\n'
				# u'命中<color=#FFB90F>世界BOSS</color>鸟蛋奖励<color=#FFB90F>中幅度</color>提升\n'
				# u'new每日赠送他人道具上限<color=#FFB90F>200</color>个\n'
				u'每日进入“靶场”<color=#FFB90F>无限</color>次\n'
				# u'击杀<color=#FFB90F>金鸟</color>有概率获得<color=#FFB90F>1.25</color>倍鸟蛋奖励\n'
    },	
    {	
        #vip8
        'pay': 20000,
        'gift1': {'name': 'v8冲天礼包', 'diamond': 888},
        'gift2': {'name': 'v8无双礼包', 'chip': 120000},
        'skill_wild': 1, 
        'skill_s_weapon': 1, 
        's_shop': 1, 
        # 'day_gift': {'props': [{'id':215, 'count': 15}, {'id':216, 'count': 15}, {'id':217, 'count': 15}, {'id':218, 'count': 15}]}, 
        'day_sign_times': [1750, 2000, 2500, 3000, 3500, 3750, 4250], 
        # 'kill_box_p': [.09, .06, .03], 
        # 'kill_b_coupon': .06,
        'weaponId': 20008,
        # 'send_t': 300,
        # 'rebate': 0,
        # 'day_fill_chip': 1000000,
        # 'critM': 1.5,
		'target_range': [{'room_type':201, 'count': -1},{'room_type':202, 'count': -1}, {'room_type':203, 'count': -1}],
        'target_exchange': 14,
        'red_packets_general': 8,
        'desc': u'new每日可领取救济金<color=#FFB90F>10000</color>鸟蛋\n'
		        #u'救济金领取次数高达<color=#FFB90F>1</color>次\n'
				# u'new每日登陆额外赠送<color=#FFB90F>4种武器强化材料*15</color>\n'
				#u'new每日签到奖励额外获得高达<color=#FFB90F>350%左右的</color>奖励\n'
				u'new获得贵族专属<color=#FFB90F>九五至尊</color>永久武器\n'
				#u'new每日红包领取次数高达<color=#FFB90F>12</color>次\n'
				# u'new击杀<color=#FFB90F>青铜宝箱</color>概率<color=#FFB90F>大幅度</color>提升\n'
				# u'new击杀<color=#FFB90F>白银宝箱</color>概率<color=#FFB90F>大幅度</color>提升\n'
				# u'new击杀<color=#FFB90F>黄金宝箱</color>概率<color=#FFB90F>大幅度</color>提升\n'
				# u'new击杀<color=#FFB90F>鸟券怪</color>概率<color=#FFB90F>大幅度</color>提升\n'
				# u'new命中<color=#FFB90F>世界BOSS</color>鸟蛋奖励<color=#FFB90F>大幅度</color>提升\n'
				# u'new每日赠送他人道具上限<color=#FFB90F>300</color>个\n'
				u'每日进入“靶场”<color=#FFB90F>无限</color>次\n'
				# u'new击杀<color=#FFB90F>金鸟</color>有概率获得<color=#FFB90F>1.5</color>倍鸟蛋奖励\n'
    },	
    {	
        #vip9
        'pay': 50000,
        'gift1': {'name': 'v9冲天礼包', 'diamond': 1888},
        'gift2': {'name': 'v9无双礼包', 'chip': 300000},
        'skill_wild': 1, 
        'skill_s_weapon': 1, 
        's_shop': 1, 
        # 'day_gift': {'props': [{'id':215, 'count': 20}, {'id':216, 'count': 20}, {'id':217, 'count': 20}, {'id':218, 'count': 20}]}, 
        'day_sign_times': [2000, 2500, 3000, 3500, 4000, 4500, 5000], 
        # 'kill_box_p': [.1125, .075, .0375], 
        # 'kill_b_coupon': .075,
        # 'send_t': 400,
        # 'rebate': 0,
        # 'day_fill_chip': 2000000,
        # 'critM': 1.5,
		'target_range':[{'room_type':201, 'count': -1},{'room_type':202, 'count': -1}, {'room_type':203, 'count': -1}],
        'target_exchange': 16,
        'red_packets_general': 8,
        'desc': u'new每日可领取救济金<color=#FFB90F>15000</color>鸟蛋\n'
		        #u'救济金领取次数高达<color=#FFB90F>1</color>次\n'
				# u'new每日登陆额外赠送<color=#FFB90F>4种武器强化材料*20</color>\n'
				#u'new每日签到奖励额外获得高达<color=#FFB90F>400%左右的</color>奖励\n'
				#u'new每日红包领取次数高达<color=#FFB90F>13</color>次\n'
				# u'击杀<color=#FFB90F>青铜宝箱</color>概率<color=#FFB90F>大幅度</color>提升\n'
				# u'击杀<color=#FFB90F>白银宝箱</color>概率<color=#FFB90F>大幅度</color>提升\n'
				# u'击杀<color=#FFB90F>黄金宝箱</color>概率<color=#FFB90F>大幅度</color>提升\n'
				# u'击杀<color=#FFB90F>鸟券怪</color>概率<color=#FFB90F>大幅度</color>提升\n'
				# u'命中<color=#FFB90F>世界BOSS</color>鸟蛋奖励<color=#FFB90F>大幅度</color>提升\n'
				# u'new每日赠送他人道具上限<color=#FFB90F>400</color>个\n'
				u'每日进入“靶场”<color=#FFB90F>无限</color>次\n'
				# u'击杀<color=#FFB90F>金鸟</color>有概率获得<color=#FFB90F>1.5</color>倍鸟蛋奖励\n'
    },
    {	
        #vip10
        'pay': 100000,
        'gift1': {'name': 'v10冲天礼包', 'diamond': 3888},
        'gift2': {'name': 'v10无双礼包', 'chip': 600000},
        'skill_wild': 1,
        'skill_s_weapon': 1, 
        's_shop': 1, 
        # 'day_gift': {'props': [{'id':215, 'count': 25}, {'id':216, 'count': 25}, {'id':217, 'count': 25}, {'id':218, 'count': 25}]}, 
        'day_sign_times': [2500, 3000, 3750, 4250, 5000, 5500, 6250], 
        # 'kill_box_p': [.15, .1, .05], 
        # 'kill_b_coupon': .1,
        # 'send_t': 500,
        # 'rebate': 0,
        # 'day_fill_chip': 2500000,
        # 'critM': 2,
        'target_range':[{'room_type':201, 'count': -1},{'room_type':202, 'count': -1}, {'room_type':203, 'count': -1}],
        'target_exchange': 18,
        'red_packets_general': 10,
        'desc': u'new每日可领取救济金<color=#FFB90F>20000</color>鸟蛋\n'
		        #u'救济金领取次数高达<color=#FFB90F>1</color>次\n'
				# u'new每日登陆额外赠送<color=#FFB90F>4种武器强化材料*25</color>\n'
				#u'new每日签到奖励额外获得高达<color=#FFB90F>500%左右的</color>奖励\n'
				#u'new每日红包领取次数高达<color=#FFB90F>14</color>次\n'
				# u'击杀<color=#FFB90F>青铜宝箱</color>概率<color=#FFB90F>大幅度</color>提升\n'
				# u'击杀<color=#FFB90F>白银宝箱</color>概率<color=#FFB90F>大幅度</color>提升\n'
				# u'击杀<color=#FFB90F>黄金宝箱</color>概率<color=#FFB90F>大幅度</color>提升\n'
				# u'击杀<color=#FFB90F>鸟券怪</color>概率<color=#FFB90F>大幅度</color>提升\n'
				# u'命中<color=#FFB90F>世界BOSS</color>鸟蛋奖励<color=#FFB90F>大幅度</color>提升\n'
				# u'new每日赠送他人道具上限<color=#FFB90F>500</color>个\n'
				u'每日进入“靶场”<color=#FFB90F>无限</color>次\n'
				# u'new击杀<color=#FFB90F>金鸟</color>有概率获得<color=#FFB90F>2</color>倍鸟蛋奖励\n'
    },	
    {	
        #vip11
        'pay': 150000,
        'gift1': {'name': 'v11冲天礼包', 'diamond': 5888},
        'gift2': {'name': 'v11无双礼包', 'chip': 1000000},
        'skill_wild': 1, 
        'skill_s_weapon': 1, 
        's_shop': 1, 
        # 'day_gift': {'props': [{'id':215, 'count': 30}, {'id':216, 'count': 30}, {'id':217, 'count': 30}, {'id':218, 'count': 30}]}, 
        'day_sign_times': [3000, 3750, 4500, 5250, 6000, 6750, 7500], 
        # 'kill_box_p': [.1875, .125, .0625], 
        # 'kill_b_coupon': .125,
        # 'send_t': 750,
        # 'rebate': 0,
        # 'day_fill_chip': 3000000,
        # 'critM': 2.5,
        'target_range':[{'room_type':201, 'count': -1},{'room_type':202, 'count': -1}, {'room_type':203, 'count': -1}],
        'target_exchange': 20,
        'red_packets_general': 12,
        'desc': u'new每日可领取救济金<color=#FFB90F>30000</color>鸟蛋\n'
		        #u'救济金领取次数高达<color=#FFB90F>1</color>次\n'
				# u'new每日登陆额外赠送<color=#FFB90F>4种武器强化材料*30</color>\n'
				#u'new每日签到奖励额外获得高达<color=#FFB90F>600%左右的</color>奖励\n'
				#u'new每日红包领取次数高达<color=#FFB90F>15</color>次\n'
				# u'new击杀<color=#FFB90F>青铜宝箱</color>概率<color=#FFB90F>极大幅度</color>提升\n'
				# u'new击杀<color=#FFB90F>白银宝箱</color>概率<color=#FFB90F>极大幅度</color>提升\n'
				# u'new击杀<color=#FFB90F>黄金宝箱</color>概率<color=#FFB90F>极大幅度</color>提升\n'
				# u'new击杀<color=#FFB90F>鸟券怪</color>概率<color=#FFB90F>极大幅度</color>提升\n'
				# u'new命中<color=#FFB90F>世界BOSS</color>鸟蛋奖励<color=#FFB90F>极大幅度</color>提升\n'
				# u'new每日赠送他人道具上限<color=#FFB90F>750</color>个\n'
				u'每日进入“靶场”<color=#FFB90F>无限</color>次\n'
				# u'new击杀<color=#FFB90F>金鸟</color>有概率获得<color=#FFB90F>2.5</color>倍鸟蛋奖励\n'
    },	
    {	
        #vip12
        'pay': 200000,
        'gift1': {'name': 'v12冲天礼包', 'diamond': 8888},
        'gift2': {'name': 'v12无双礼包', 'chip': 2000000},
        'skill_wild': 1, 
        'skill_s_weapon': 1, 
        's_shop': 1, 
        # 'day_gift': {'props': [{'id':215, 'count': 35}, {'id':216, 'count': 35}, {'id':217, 'count': 35}, {'id':218, 'count': 35}]}, 
        'day_sign_times': [3500, 4250, 5250, 6000, 7000, 7750, 8750], 
        # 'kill_box_p': [.225, .15, .075], 
        # 'kill_b_coupon': .15,
        # 'send_t': 1000,
        # 'rebate': 0,
        # 'day_fill_chip': 4000000,
        # 'critM': 3,
        'target_range':[{'room_type':201, 'count': -1},{'room_type':202, 'count': -1}, {'room_type':203, 'count': -1}],
        'target_exchange': 22,
        'red_packets_general': 15,
        'desc': u'new每日可领取救济金<color=#FFB90F>50000</color>鸟蛋\n'
		        #u'救济金领取次数高达<color=#FFB90F>1</color>次\n'
				# u'new每日登陆额外赠送<color=#FFB90F>4种武器强化材料*35</color>\n'
				#u'new每日签到奖励额外获得高达<color=#FFB90F>700%左右的</color>奖励\n'
				#u'new每日红包领取次数高达<color=#FFB90F>16</color>次\n'
				# u'击杀<color=#FFB90F>青铜宝箱</color>概率<color=#FFB90F>极大幅度</color>提升\n'
				# u'击杀<color=#FFB90F>白银宝箱</color>概率<color=#FFB90F>极大幅度</color>提升\n'
				# u'击杀<color=#FFB90F>黄金宝箱</color>概率<color=#FFB90F>极大幅度</color>提升\n'
				# u'击杀<color=#FFB90F>鸟券怪</color>概率<color=#FFB90F>极大幅度</color>提升\n'
				# u'命中<color=#FFB90F>世界BOSS</color>鸟蛋奖励<color=#FFB90F>极大幅度</color>提升\n'
				# u'new每日赠送他人道具上限<color=#FFB90F>1000</color>个\n'
				u'每日进入“靶场”<color=#FFB90F>无限</color>次\n'
				# u'new击杀<color=#FFB90F>金鸟</color>有概率获得<color=#FFB90F>3</color>倍鸟蛋奖励\n'
    },	
])

add_game_config(2, 'raffle.config', {
    'config': [
        # [概率， 上限， 奖励]
        # 上限 -1：走其他规则 0
        {
            'id': 1,
            'name': u'普通抽奖',
            'limit': 0,
            'coupon_reward': {'rate': 0.1, 'reward': {'coupon': 2}},
            'other_reward': [
                {'weight_f': 1, 'reward':{'diamond': 10}},
                {'weight_f': 1, 'reward':{'diamond': 5}},
                {'weight_f': 1, 'reward':{'chip': 1000}},
                {'weight_f': 1, 'reward':{'chip': 500}},
                {'weight_f': 1, 'reward':{'chip': 200}}
            ],
            'formula': {
                201: [10000, 10000],
                202: [10000, 10000],
                203: [10000, 10000]
            },

        },

        {
            'id': 2,
            'name': u'青铜抽奖',
            'limit': 10000,
            'coupon_reward': {'rate': 0.1, 'reward': {'coupon': 5}},
            'other_reward': [
                {'weight_f': 1, 'reward':{'diamond': 25}},
                {'weight_f': 1, 'reward':{'diamond': 10}},
                {'weight_f': 1, 'reward':{'chip': 100000}},
                {'weight_f': 1, 'reward':{'chip': 50000}},
                {'weight_f': 1, 'reward':{'chip': 10000}}
            ],
            'formula': {
                201: [100000, 100000],
                202: [100000, 100000],
                203: [100000, 100000]
            },
        },

        {
            'id': 3,
            'name': u'白银抽奖',
            'limit': 100000,
            'coupon_reward': {'rate': 0.15, 'reward': {'coupon': 15}},
            'other_reward': [
                {'weight_f': 1, 'reward':{'diamond': 50}},
                {'weight_f': 0.75, 'reward':{'props': [{'id':211, 'count':1}]}},
                {'weight_f': 1, 'reward':{'chip': 300000}},
                {'weight_f': 1, 'reward':{'chip': 200000}},
                {'weight_f': 1, 'reward':{'chip': 100000}}
            ],
            'formula': {
                201: [1000000, 1000000],
                202: [1000000, 1000000],
                203: [1000000, 1000000]
            },
        },

        {
            'id': 4,
            'name': u'黄金抽奖',
            'limit': 300000,
            'coupon_reward': {'rate': 0.2, 'reward': {'coupon': 25}},
            'other_reward': [
                {'weight_f': 1, 'reward':{'diamond': 100}},
                {'weight_f': 0.75, 'reward':{'props': [{'id':212, 'count':1}]}},
                {'weight_f': 1, 'reward':{'chip': 500000}},
                {'weight_f': 1, 'reward':{'chip': 400000}},
                {'weight_f': 1, 'reward':{'chip': 300000}}
            ],
            'formula': {
                201: [3000000, 3000000],
                202: [3000000, 3000000],
                203: [3000000, 3000000]
            },
        },

        {
            'id': 5,
            'name': u'白金抽奖',
            'limit': 500000,
            'coupon_reward': {'rate': 0.2, 'reward': {'coupon': 50}},
            'other_reward': [
                {'weight_f': 1, 'reward':{'diamond': 250}},
                {'weight_f': 0.75, 'reward':{ 'props': [{'id':213, 'count':1}]}},
                {'weight_f': 1, 'reward':{'chip': 1000000}},
                {'weight_f': 1, 'reward':{'chip': 800000}},
                {'weight_f': 1, 'reward':{'chip': 500000}}
            ],
            'formula': {
                201: [5000000, 5000000],
                202: [5000000, 5000000],
                203: [5000000, 5000000]
            },
        },

        {
            'id': 6,
            'name': u'至尊抽奖',
            'limit': 1000000,
            'coupon_reward': {'rate': 0.2, 'reward': {'coupon': 100}},
            'other_reward': [
                {'weight_f': 1, 'reward':{'diamond': 500}},
                {'weight_f': 0.75, 'reward':{'props': [{'id':214, 'count':1}]}},
                {'weight_f': 1, 'reward':{'chip': 2000000}},
                {'weight_f': 1, 'reward':{'chip': 1500000}},
                {'weight_f': 1, 'reward':{'chip': 1000000}}
            ],
            'formula': {
                201: [10000000, 10000000],
                202: [10000000, 10000000],
                203: [10000000, 10000000]
            },
        },
    ],
    'loop': [5, 5, 10],
})

add_game_config(2, 'props.config', [
    {
        'id': 201,
        'diamond': 200,
        'count': 100,
        'price': 2,
        'present': {'pay': 500},
        'desc': u'看到大鸟别犹豫，立即使用锁定技能！要不就被别人抢走了'
    },
    {
        'id': 202,
        'diamond': 200,
        'count': 40,
        'price': 5,
        'present': {'pay': 500},
        'desc': u'什么！鸟要逃走了？赶快使用#全屏冰冻，瞬间为你冰冻。'
    },
    {
        'id': 203,
        'diamond': 500,
        'count': 10,
        'price': 50,
        'present': {'pay': 500},
        'use': {'vip': 2},
        'buy': {'vip': 2},
        'desc': u'使用狂暴技能，立即获得双倍#击杀概率。'
    },
    {
        'id': 204,
        'diamond': 200,
        'count': 1,
        'price': 200,
        'present': {'pay': 500},
        'use': {'vip': 2},
        'buy': {'vip': 2},
        'desc': u'发射一颗威力强大的超级武器#，记得对准鸟多的地方扔哦！#(对活动首领无效)'
    },
    {
        'id': 205,
        'diamond': 200,
        'count': 100,
        'price': 5,
        'present': {'pay': 500},
        'desc': u'快快使用传送门，传送出一只#神秘奖金鸟吧。'
    },
    {
        'id': 211,
        'count': 1,
        'content': {'chip': 150000},
        'present': {'pay': 500},
        'desc': u'使用后可获得150000鸟蛋!#获得途径：#1.抽奖获得 #2.击杀青铜宝箱怪有概率掉落'
    },
    {
        'id': 212,
        'count': 1,
        'content': {'chip': 250000},
        'present': {'pay': 500},
        'desc': u'使用后可获得250000鸟蛋!#获得途径：#1.抽奖获得 #2.击杀白银宝箱怪有概率掉落'
    },
    {
        'id': 213,
        'count': 1,
        'content': {'chip': 500000},
        'present': {'pay': 500},
        'desc': u'使用后可获得500000鸟蛋!#获得途径：#1.抽奖获得 #2.击杀黄金宝箱怪有概率掉落'
    },
    {
        'id': 214,
        'count': 1,
        'content': {'chip': 1000000},
        'present': {'pay': 500},
        'desc': u'使用后可获得1000000鸟蛋!#获得途径：#1.抽奖获得 #2.排行榜奖励获得 #3.击杀世界BOSS有概率掉落'
    },
    {
        'id': 215,
        'diamond': 200,
        'count': 10,
        'price': 2,
        'present': {'pay': 500},
        'resolve': [1, 1],
        'desc': u'绿灵石是用于强化1000倍以上#炮台的必备材料；#获得途径：#1.VIP每日登陆赠送 #2.击杀BOSS有概率掉落 #3.限时商城中兑换 '
    },
    {
        'id': 216,
        'diamond': 200,
        'count': 10,
        'price': 2,
        'present': {'pay': 500},
        'resolve': [1, 1],
        'desc': u'蓝魔石是用于强化1000倍以上#炮台的必备材料；#获得途径：#1.VIP每日登陆赠送 #2.击杀BOSS有概率掉落 #3.限时商城中兑换 '
    },
    {
        'id': 217,
        'diamond': 200,
        'count': 10,
        'price': 2,
        'present': {'pay': 500},
        'resolve': [1, 1],
        'desc': u'紫晶石是用于强化1000倍以上#炮台的必备材料；#获得途径：#1.VIP每日登陆赠送 #2.击杀BOSS有概率掉落 #3.限时商城中兑换 '
    },
    {
        'id': 218,
        'diamond': 200,
        'count': 10,
        'price': 2,
        'present': {'pay': 500},
        'resolve': [1, 1],
        'desc': u'血精石是用于强化1000倍以上#炮台的必备材料；#获得途径：#1.VIP每日登陆赠送 #2.击杀BOSS有概率掉落 #3.限时商城中兑换 '
    },
    {
        'id': 219,
        'diamond': 200,
        'count': 10,
        'price': 2,
        'present': {'pay': 500},
        'desc': u'强化精华是用于强化1000倍以#上炮台的成功率材料；#获得途径：#1.强化失败可返还一定数量的#强化精华 #2.分解绿灵石、蓝魔石、紫晶#石、血精石获得 #3.限时商城中兑换 '
    },
    {
        'id': 220,
        'count': 1000,
        'price': 10000,
        'recovery_price': 1,
        'present': {'pay': 500},
        'desc': u'vip房卡,消耗后可创建VIP房。 '
    },
    # 新增宝箱怪物奖励ID
    {
        'id': 601,
        'count': 1,
        'content': {'chip': 500000},
        'desc': u'使用后可获得500000鸟蛋!#获得途径：#1.在鸟场击杀青铜宝箱怪物'
    },
    {
        'id': 602,
        'count': 1,
        'content': {'chip': 1500000},
        'desc': u'使用后可获得500000鸟蛋!#获得途径：#1.在鸟场击杀青铜宝箱怪物'
    },
    {
        'id': 603,
        'count': 1,
        'content': {'chip': 2000000},
        'desc': u'使用后可获得500000鸟蛋!#获得途径：#1.在鸟场击杀青铜宝箱怪物'
    },
])

#id
    #属性
    #速度
    #反弹次数
    #穿透次数
    #特性
    #描述
add_game_config(2,'weapon.config',[
    {'id':20000,'speed':5,'rebound':9999,'shut':1,'pene':[],'desc':u''},
    {'id':20001,'speed':5,'rebound':9999,'shut':1,'pene':[],'desc':u''},
    {'id':20002,'speed':5,'rebound':9999,'shut':1,'pene':[],'desc':u''},
    {'id':20003,'speed':5,'rebound':9999,'shut':1,'pene':[],'desc':u''},
    {'id':20004,'speed':5,'rebound':9999,'shut':1,'pene':[],'desc':u''},
    {'id':20005,'speed':5,'rebound':9999,'shut':1,'pene':[],'desc':u''},
    {'id':20006,'speed':5,'rebound':9999,'shut':1,'pene':[],'desc':u''},
    {'id':20007,'speed':5,'rebound':9999,'shut':1,'pene':[],'desc':u''},
    {'id':20008,'speed':5,'rebound':9999,'shut':1,'pene':[],'desc':u''},
    #{'id':20009,'speed':5,'rebound':0,'shut':999,'pene':[8],'desc':u'特性：无视射击路径上的一切障碍，都可进行击杀概率判定，但概率随命中数量增多而逐步衰减。'},
	{'id':20010,'speed':5,'rebound':5,'shut':1,'pene':[],'desc':u''},
])

#特性id
#prob：概率（特效概率）
#coeff：击杀概率衰减参数（穿透是依次递减，闪电是所有都是此参数递减）
#addi：效果时间/条数（闪电是条数，其它都是时间，0不管）
add_game_config(2,'weaponeff.config',[
    {'id':1,'prob':0.25,'coeff':0,'addi':1,'desc':u''},
    {'id':2,'prob':0.1,'coeff':0,'addi':2,'desc':u''},
    {'id':3,'prob':0.005,'coeff':0,'addi':0,'desc':u''},
    {'id':4,'prob':0.03,'coeff':0,'addi':4,'desc':u''},
    {'id':5,'prob':0.1,'coeff':2,'addi':3,'desc':u''},
    {'id':6,'prob':1,'coeff':2,'addi':0,'desc':u''},
    {'id':7,'prob':1,'coeff':0,'addi':0,'desc':u''},
	{'id':8,'prob':1,'coeff':0,'addi':0,'desc':u''},
])

add_game_config(2,'weaponeffect.config',[
    {'id':'20001','speed':1,'rebound':3,'effects':0,'addition':0},
])

# # 实物兑换商城
# add_game_config(2, 'exchange.config', [
#     {'type': 'phone', 'desc': u'30元话费', 'cost': 300, 'count': 30},
#     {'type': 'diamond', 'desc': u'500钻石', 'cost': 300, 'count': 500},
#     {'type': 'props', 'desc': u'鸟蛋', 'cost': 300, 'id': 213, 'count': 1},
#     # 新增物品
#     {'type': 'props', 'desc': u'移动话费卡', 'cost': 100, 'id': 301, 'count': 1},
#     {'type': 'props', 'desc': u'电信话费卡', 'cost': 101, 'id': 302, 'count': 1},
#     {'type': 'props', 'desc': u'联通话费卡', 'cost': 102, 'id': 303, 'count': 1},
#     {'type': 'props', 'desc': u'京东E卡', 'cost': 103, 'id': 304, 'count': 1},
#     {'type': 'props', 'desc': u'数码设备抵扣卷', 'cost': 104, 'id': 305, 'count': 1},
#     {'type': 'props', 'desc': u'食品类抵扣卷', 'cost': 105, 'id': 306, 'count': 1},
#     {'type': 'props', 'desc': u'家用电器抵扣卷', 'cost': 106, 'id': 307, 'count': 1},
# ])

if Global.run_mode in (1, 2):
    add_game_config(2, 'cdkey.server.url', 'http://127.0.0.1:7070/v1/cdkey/checkCode')
else:
    add_game_config(2, 'cdkey.server.url', 'http://127.0.0.1:7070/v1/cdkey/checkCode')

if Global.run_mode == 1:
    add_game_config(2, 'stat.server.url', 'http://127.0.0.1')
elif Global.run_mode == 2:
    add_game_config(2, 'stat.server.url', 'http://127.0.0.1')
else:
    add_game_config(2, 'stat.server.url', 'http://127.0.0.1/lybn')

# html
__url_base_old = Global.http_game + '/static/bird/%(platform)s/%(channel)s'
html_config_old = {
    'http_game': Global.http_game,
    'activity': __url_base_old + '/activity/index.html',
    'rank': __url_base_old + '/rank/index.html',
    'history': __url_base_old + '/history/index.html'
}
add_game_config(2, 'html.config.old', html_config_old)

if Global.run_mode == 1:
    __url_base_new = 'http://xxx47.92.72.109/lybn' #'http://lybn.dapai1.com'
elif Global.run_mode == 2:
    __url_base_new = 'http://xxx92.72.109/lybn' #'http://lybntest.dapai1.com'
else:
    __url_base_new = 'http://xxx47.92.72.109/lybn' #'http://192.168.1.21/lybn'

html_config_new = {
    'http_game': Global.http_game,
    'activity': __url_base_new + '/bnactivity0612/index/userId/%d/session/%s/flag/300',
    'rank': __url_base_new + '/bnranking/index/userId/%d/session/%s',
    'history': Global.http_game + '/static/bird/android/qifan/history/index.html',
    'exchange': __url_base_new + '/goods/index/userId/%d/session/%s'
}
add_game_config(2, 'html.config.new', html_config_new)

add_game_config(2, 'share.config', {
    # 好友达成目标自己可得奖励
    'friend_reward': [
        {"id": 1, 'barrel': 1000, 'reward': {'diamond': 50}},
        {"id": 2, 'barrel': 3000, 'reward': {'diamond': 80}},
        {"id": 3, 'barrel': 5000, 'reward': {'diamond': 100}},
    ],
    # 分享成功后获得的奖励 钻石
    'welfare': [
        {'reward': {'chip': 5000}},
        {'reward': {'diamond': 60}},
        {'reward': {'props': [{'id': 202, 'count': 1}]}},
    ],
})

add_game_config(2, 'sms.config', {
    'appId': '8aaf070862cc8e560162d68bf34605cd',
    'accountSid': '8aaf070862cc8e560162d68bf2e005c6',
    'accountToken': 'd31c764d79d34c77959c2415bd038c89',
    'serverIP': 'app.cloopen.com',
    'serverPort': '8883',
    'tempId_arr': ['408562', '417474', '417475', '417476', '417477', '417478', '417480', '417483', '417484', '417485'],
    'softVersion': '2013-12-26'
})

add_game_config(2, 'poke_mole.config', {
    # hammer 锤子信息
    'hammer': [
        {"id": 1,
         'price': 500,
         'drop': [[500, 0.34], [1000, 0.02], [5000, 0.02], [1000, 0.003],
                  [5000, 0.001]]},
        {"id": 2,
         'price': 1000,
         'drop': [[1000, 0.34], [5000, 0.022], [10000, 0.09], [50000, 0.002],
                  [100000, 0.001]]},
        {"id": 3,
         'price': 2000,
         'drop': [[2000, 0.32], [10000, 0.019], [50000, 0.005],
                  [100000, 0.002], [200000, 0.001]]},
        {"id": 4,
         'price': 5000,
         'drop': [[5000, 0.3], [20000, 0.01], [100000, 0.005], [500000, 0.001],
                  [1000000, 0.001]]},
        {"id": 5,
         'price': 10000,
         'drop': [[10000, 0.33], [100000, 0.005], [200000, 0.003],
                  [1000000, 0.001], [2000000, 0.001]]},
        {"id": 6,
         "long": 3,
         'price': 20000,
         'drop': [[20000, 0.33], [100000, 0.012], [500000, 0.002],
                  [2000000, 0.001], [4000000, 0.001]]},
        {"id": 7,
         "drop": 500,
         "max_num": 75,
         "lo": 30},
        {"id": 8,
         "lo": 60,
         'drop': [[200000, 0.665], [300000, 0.24], [500000, 0.05],
                  [1000000, 0.03], [3000000, 0.01],
                  [6000000, 0.005]]},
    ],
    # 消耗多少钱攒满能量条
    'mp_chip': 2000000,
    # 消耗多少钱攒满雷神锤能量
    'mp_hammer': 2000000,
    # 切换场景时间
    'scene': 120,
    # 间隔时间 【普通场景，鸟蛋潮】
    'long': [1, 1],
    # 放大显示【前三锤，后三锤】
    'show': [50000, 100000],
    # 进入打地鼠最少鸟蛋
    'min_chip': 50000,
    # 在线人数
    'online_num': [50, 200, 30],
    # vip额外奖励
    'vip': {5: 0.1, 6: 0.15, 7: 0.2, 8: 0.25, 9: 0.3},
    'coupon': [5, 0.01, 200]
})

# 概率加成
add_game_config(2, 'odds.addition.violent', 0.5)

add_game_config(2, 'odds.addition.pay', {
    'damping': 0.1,
    'total': 10,
    'addition': 2.5,
    'multi': 10000
})

add_game_config(2, 'odds.addition.egg', {
    'addition': 1,
    'max': 15000000,
    '213': 300000,
    '214': 600000
})

# 是否是审核阶段0 否 1 是  默认1
# pay_type 0只包括微信和支付宝 1只使用官方支付 2显示所有支付
# 如果是appstore paytype 默认值为1， 其他的默认值为0
# 如果是3 不开充值 如果是4，提示去公众号充值
# more_game  找刺激 开关 1 有 默认1
add_game_config(2, 'switch.config', [
    {'version': '1.0.1', 'channel': 'appstore', 'is_review': 0, 'pay_type': 1},
    {'version': '1.0.2', 'channel': 'appstore', 'is_review': 0, 'pay_type': 1},
    {'version': '1.0.3', 'channel': 'appstore', 'is_review': 0, 'pay_type': 1},
    {'version': '1.0.4', 'channel': 'appstore', 'is_review': 0, 'pay_type': 1},
    {'version': '1.0.5', 'channel': 'appstore', 'is_review': 1, 'pay_type': 1},
])

add_game_config(2, 'pet.config', {
    # level 1 A 2 B 3 C 4 S
    'pet_info': [
        {
            'id': 110,
            'level': 1,
            'jjcAdd': 0.03,
            'ptAdd': 0.03,
            'name': u'真情宝宝',
        },
        {
            'id': 111,
            'level': 1,
            'jjcAdd': 0.03,
            'ptAdd': 0.03,
            'name': u'平安宝宝',
        },
        {
            'id': 120,
            'level': 2,
            'jjcAdd': 0.02,
            'ptAdd': 0.02,
            'name': u'火龙精灵',
        },
        {
            'id': 121,
            'level': 2,
            'jjcAdd': 0.02,
            'ptAdd': 0.02,
            'name': u'海洋精灵',
        },
        {
            'id': 130,
            'level': 3,
            'jjcAdd': 0.01,
            'ptAdd': 0.01,
            'name': u'紫翼幼龙',
        },
        {
            'id': 131,
            'level': 3,
            'jjcAdd': 0.01,
            'ptAdd': 0.01,
            'name': u'赤炎幼龙',
        },
        {
            'id': 140,
            'level': 4,
            'jjcAdd': 0.035,
            'jjcLvAdd': 0.005,
            'ptAdd': 0.035,
            'name': u'白玉灵猫',
        },
        {
            'id': 141,
            'level': 4,
            'jjcAdd': 0.035,
            'jjcLvAdd': 0.005,
            'ptAdd': 0.035,
            'name': u'黄玉灵猫',
        },
    ],
    'exp': [20, 30, 40, 50, 60, 70, 80, 90, 100, 220,
            240, 260, 280, 300, 320, 340, 360, 380, 400, 630,
            660, 690, 720, 750, 780, 810, 840, 870, 900],
    'compose': [
        [2, 200000, 0.15, [110, 111]],
        [3, 100000, 0.3, [120, 121]],
    ],
    'up': [[211, 1, 1], [212, 1, 2], [213, 1, 5], [214, 1, 10],
           [215, 10, 1], [216, 10, 1], [217, 10, 1], [218, 10, 1]],
})

add_game_config(2, 'protect.config', {
    'common': [10000, 50000, 2],          # 普通用户 低值 到达高值 概率变化系数
    'vip': [10000, 20000, 2, 10000000],  # 付费用户 低值 充值金额系数高值 概率变化系数 高值上限
})

__online_reward_pool = {
    0: [[5, 20], [0, 0], [5, 200], [0, 0], [5, 500], [0, 0], [5, 1000], [0, 0], [5, 2000], [0, 0]], # 废弃配置
    1: [[3, 1], [3, 5], [3, 20], [2, 5], [2, 10], [202, 1], [202, 2], [1, 1000], [1, 2000], [1, 5000]],
    2: [[3, 1], [3, 5], [3, 20], [2, 5], [2, 10], [202, 1], [202, 2], [1, 1000], [1, 2000], [1, 5000]],
    3: [[3, 1], [3, 5], [3, 20], [2, 5], [2, 10], [202, 1], [202, 2], [1, 1000], [1, 2000], [1, 5000]],
    4: [[3, 1], [3, 5], [3, 20], [2, 5], [2, 10], [202, 1], [202, 2], [1, 1000], [1, 2000], [1, 5000]],
    5: [[3, 1], [3, 5], [3, 20], [2, 5], [2, 10], [202, 1], [202, 2], [1, 1000], [1, 2000], [1, 5000]],
    6: [[202, 1], [203, 1], [204, 1], [202, 2], [205, 2], [2, 3], [2, 5], [1, 1000], [1, 2000], [1, 5000]],
    }

__online_reward_pool_a = {}
for k, v in __online_reward_pool.items():
    __online_reward_pool_a[k] = []
    for online_reward in v:
        if online_reward[0] == 0:
            __online_reward_pool_a[k].append({})
        elif online_reward[0] == 1:
            __online_reward_pool_a[k].append({'chip': online_reward[1]})
        elif online_reward[0] == 2:
            __online_reward_pool_a[k].append({'diamond': online_reward[1]})
        elif online_reward[0] == 3:
            __online_reward_pool_a[k].append({'coupon': online_reward[1]})
        elif online_reward[0] == 5:
            __online_reward_pool_a[k].append({'vip_exp': online_reward[1]})
        else:
            __online_reward_pool_a[k].append({'props': [{'id': online_reward[0], "count": online_reward[1]}]})

add_game_config(2, 'online_reward.config', {
    'cd': {
        1: [[90, 1], [180, 4], [360, 2], [600, 3], [600, 5], [900, 3]],
        2: [[90, 6], [180, 6], [360, 6], [600, 6], [600, 6], [900, 6]],
        3: [[90, 6], [180, 6], [360, 6], [600, 6], [600, 6], [900, 6]],
        4: [[90, 6], [180, 6], [360, 6], [600, 6], [600, 6], [900, 6]],
        5: [[90, 6], [180, 6], [360, 6], [600, 6], [600, 6], [900, 6]],
        6: [[90, 6], [180, 6], [360, 6], [600, 6], [600, 6], [900, 6]],
        7: [[90, 6], [180, 6], [360, 6], [600, 6], [600, 6], [900, 6]],
     },
    'pool_info': __online_reward_pool,
    'pool_reward': __online_reward_pool_a,
    'odds': {
        0: [0.91, 0.01, 0.003, 0, 0.001, 0.02, 0.0005, 0.025, 0.0001, 0.03], # 废弃配置
        1: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        2: [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        3: [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        4: [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        5: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        6: [0.1, 0.01, 0, 0.1, 0.2, 0.1, 0.1, 0.2, 0.1, 0.1],
     },
})

#修改昵称需消耗的钻石数（按次数来）
__nickname_diamoncost = [0,100,100,100,100,100,100,100,100,100]
add_game_config(2, 'nickname.diamoncost.config', __nickname_diamoncost)

# 新增绑定手机奖励
add_game_config(2, 'bindPhone.reward', [{'chip': 5000, 'diamond': 5, 'props': [{'id': 202, 'count': 1}, {'id': 205, 'count': 1}]}])

# 新增世界boss奖励
add_game_config(2, 'world_boss.reward',{
                'count':20,
                'level':[[1],[2],[3],range(4,10+1),range(11,20+1)],
                'reward':[
                            {'chip': 100000, 'diamond': 50},
                            {'chip': 80000, 'diamond': 30},
                            {'chip': 50000, 'diamond': 20},
                            {'chip': 30000, 'diamond': 10},
                            {'chip': 20000, 'diamond': 5},
                          ]
                 }
    )

# 充值日榜奖励
add_game_config(2, 'pay.rank.reward',{
                'limit':50,
                'count':20,
                'level':[[1], [2], [3], range(4, 10+1), range(11, 20+1)],
                'reward':[
                            {'props': [{'id': 202, 'count': 1}]},
                            {'props': [{'id': 202, 'count': 1}]},
                            {'props': [{'id': 202, 'count': 1}]},
                            {'props': [{'id': 202, 'count': 1}]},
                            {'props': [{'id': 202, 'count': 1}]},
                        ]
                 }
    )

# 初级场榜奖励
add_game_config(2, 'primary.rank.reward',{
                'count':50,
                'level':[[1], [2], [3], range(4, 10+1), range(11, 20+1)],
                'reward':[
                            {'props': [{'id': 202, 'count': 1}]},
                            {'props': [{'id': 202, 'count': 1}]},
                            {'props': [{'id': 202, 'count': 1}]},
                            {'props': [{'id': 202, 'count': 1}]},
                            {'props': [{'id': 202, 'count': 1}]},
                        ]
                 }
    )

# 中级场周榜奖励
add_game_config(2, 'middle.rank.reward',{
                'count':50,
                'level':[[1], [2], [3], range(4, 10+1), range(11, 20+1)],
                'reward':[
                            {'props': [{'id': 202, 'count': 1}]},
                            {'props': [{'id': 202, 'count': 1}]},
                            {'props': [{'id': 202, 'count': 1}]},
                            {'props': [{'id': 202, 'count': 1}]},
                            {'props': [{'id': 202, 'count': 1}]},
                        ]
                 }
    )

# 高级场周榜奖励
add_game_config(2, 'high.rank.reward',{
                'count':50,
                'level':[[1], [2], [3], range(4, 10+1), range(11, 20+1)],
                'reward':[
                            {'props': [{'id': 202, 'count': 1}]},
                            {'props': [{'id': 202, 'count': 1}]},
                            {'props': [{'id': 202, 'count': 1}]},
                            {'props': [{'id': 202, 'count': 1}]},
                            {'props': [{'id': 202, 'count': 1}]},
                        ]
                 }
    )

add_game_config(2, 'village.config', {
    'exp': [1000, 1500, 2000, 2500],
    'num': [50, 100, 150, 200, 250],
    'interval_ts': 7*24*60*60
})

add_game_config(2, 'tips.config', [
    u'鸟券可以兑换礼品，努力积攒鸟券吧亲。',
    u'炮倍越高，鸟券的获得速度越快。',
    u'开启锁定模式后，您将追杀它至天涯海角。',
    u'鸟券可通过抽奖、打鸟、活动、排行、靶场等方式获得。',
	u'关注官方微信公众号，并参与活动，每天可领取大量奖励。',
    u'七日豪礼，神秘大奖等你来拿。',
    u'新手礼包，7天月卡，每天领鸟蛋，助你赢得更多鸟券。',
])

add_game_config(2, 'robot.config', {
    # {u'join': {u'1': 0.2, u'2': 0.2, u'3': 0.1}, u'leave': {u'2': 0.6, u'3': 0.1}, u'rand': 0.07, u'info': {u'chip': {u'201': [10000, 99999], u'202': [10000, 99999]},
    # u'diamond': [10, 999], u'barrel_multiple': {u'201': [20, 25, 30], u'202': [30, 35, 40, 45]}, u'exp_level': {u'201': [1, 10], u'202': [10, 20]}}}
    'join': {1: 0.8, 2: 0.6, 3: 0.8},
    'leave': {2: 0.5, 3: 0.3},
    'rand': 0.03,

    'info': {'chip': {201: [30000, 150000], 202: [50000, 440000]},
             'diamond': [0, 2],
             'barrel_multiple': {201: [25, 30], 202: [100, 150]},
             'barrel_level': {201: [13, 14], 202: [23, 24]},
             'exp_level': {201: [2, 3], 202: [3, 4]},
            },

})

add_game_config(2, 'fanfanle.config',{
    '0':{                                                          #鸟蛋场
        'entrance_cost': [1000, 30000, 50000],  # 门票费用
        'switchCard_cost': [500, 15000, 25000],  # 换牌费用
        'vip_level':1,
        'little_reward':0.035,
        'lowRate': 0.3,
        'highRate': 0.6,
        'diamond_chip': 500,  # 钻石跟金币的比例关系
        'rate_calc': {  # 基准线，用于判断翻翻乐成功几率及换牌成功几率
            '1': {
                'baseLine': 250000,
                'addLine': 2500,
                'addRate': 0.01
            },
            '2': {
                'baseLine': 6000000,
                'addLine': 60000,
                'addRate': 0.01
            },
            '3': {
                'baseLine': 10000000,
                'addLine': 100000,
                'addRate': 0.01
            }
        },
        'reward_scale': {  # 奖励比例，分别为金币、金币、鸟券3类奖励
            'reward_A': [3, 1, 0.3],  # chip_reward_group_A
            'reward_B': [8, 2, 0.5],  # chip_reward_group_B
            'reward_C': [15, 3, 1],  # coupn_reward_group
            'reward_C_chip_ex_coupon': 5000,  # 鸟卷兑换关系
        },
        'reward_model':
              [['chip', 'chip', 'chip'],
               ['chip', 'chip', 'chip'],
               ['chip', 'chip', 'chip']]
    },
    '1':{                                                   #钻石场
        'entrance_cost': [20, 100, 200],  # 门票费用
        'switchCard_cost': [10, 50, 100],  # 换牌费用
        'vip_level': 1,
        'little_reward':0.035,
        'lowRate': 0.3,
        'highRate': 0.6,
        'diamond_chip': 500,  # 钻石跟金币的比例关系
        'rate_calc': {  # 基准线，用于判断翻翻乐成功几率及换牌成功几率
            '1': {
                'baseLine': 2500000,
                'addLine': 25000,
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
        'reward_model':
            [['diamond', 'diamond', 'diamond'],
            ['diamond', 'diamond', 'coupon'],
            ['diamond', 'diamond', 'coupon']]
        }
})

add_game_config(2, 'chip_ex_coupon.config',{
        'chip_ex_coupon': 5000,
})

add_game_config(2, 'vip_room.config',{
    'vip_room_price': 5000,
    'vip_card_price': 1,
    'vip_room_level': 2,
})

# 1：鸟蛋奖励
# 2：鸟券奖励
# 3：道具狂暴
# 4：事件筛子*2
# 5：事件筛子*3
# 6：事件奖励*2
# 7：事件筛子免费
# 8：空格
# 9：固定5倍门票的鸟蛋数
# 10：固定5倍门票的鸟券数
# 11：固定稀有道具奖励


add_game_config(2, 'RichMan.config', {
                1:{                    # 初级场
                    'vip_limit':1,
                    'ticket':10,       # 钻石
                    'map':{
                        2:[5,10],
                        3:[10,20],
                        4:[1,3],
                        5:[2,5],
                        6:[1,2],
                        7:[2,5],
                        8:[8,12],
                        9:[3,5],
                        10:[3,5],
                        11:[3,5],
                    },
                    'floor_num':98,
                    'average_line':5000000,
                    'range_line':100000,
                    'average_rate':0.2,
                    'range_rate':0.01,
                    'win': [0.8, 1.5],
                    'lose': [0.05, 0.5],

                    'end_win': [3.0, 5.0],
                    'end_lose': [1.5, 2.5],

                    'spacial_reward':{
                        '3':{'rw1':{'props':[{'id':202, 'count':1}]}, 'rw2':{'props':[{'id':203, 'count':1}]}},
                        '9':{'chip': 20000},
                        '10':{'coupon': 4},
                        '11':{'props':[{'id':203, 'count':1}]},
                    }
                },
                2: {                    # 中级场
                    'vip_limit': 1,
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
                        10: [3, 5],
                        11: [4, 6],
                    },
                    'floor_num': 98,
                    'average_line': 15000000,
                    'range_line': 300000,
                    'average_rate': 0.2,
                    'range_rate': 0.01,
                    'win': [0.8, 1.5],
                    'lose': [0.05, 0.5],

                    'end_win': [3.0, 5.0],
                    'end_lose': [1.5, 2.5],

                    'spacial_reward': {
                        '3':{'rw1':{'props':[{'id':220, 'count':1}]}, 'rw2':{'props':[{'id':203, 'count':2}]}},
                        '9': {'chip': 60000},
                        '10': {'coupon': 12},
                        '11': {'props': [{'id': 203, 'count': 2}]},
                    }
                },
                3: {                # 高级场
                    'vip_limit': 1,
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
                        10: [3, 5],
                        11: [4, 6],
                    },
                    'floor_num': 98,
                    'average_line': 25000000,
                    'range_line': 500000,
                    'average_rate': 0.2,
                    'range_rate': 0.01,
                    'win': [0.8, 1.5],
                    'lose': [0.05, 0.5],

                    'end_win': [3.0, 5.0],
                    'end_lose': [1.5, 2.5],

                    'spacial_reward': {
                        '3':{'rw1':{'props':[{'id':203, 'count':1}]}, 'rw2':{'props': [{'id':204, 'count':1}]}},
                        '9': {'chip': 120000},
                        '10': {'coupon': 24},
                        '11': {'props': [{'id': 204, 'count': 1}]},
                    }
                },
            }
)

add_game_config(2, 'hit_bird.addition.config', {
    'vip':{
            0: 0,
            1: 0,
            2: 0.001,
            3: 0.001,
            4: 0.001,
            5: 0.002,
            6: 0.002,
            7: 0.003,
            8: 0.003,
            9: 0.004,
            10: 0.004,
            11: 0.004,
            12: 0.004,
    },
})

add_game_config(2, 'smart_game_ddz.config', 'http://a158.aiqipai.top/xmdrddz/index.html')
