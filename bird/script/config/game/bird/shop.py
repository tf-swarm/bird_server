#!/usr/bin/env python
# -*- coding=utf-8 -*-

import copy
from framework.helper import add_game_config

product_101807 = {
    'price': 10,
    'name': u'10元捕鸟鸟蛋礼包',
    'desc': {
#        'display': u'加赠70%',
#        'addition': 70,
        'amount': 10000,
    },
#    'first': {
#        'diamond': 70,
#    },
    'content': {
        'chip': 10000,
    }
}

product_111807 = {
    'price': 10,
    'name': u'10元捕鸟鸟蛋礼包',
    'desc': {
#        'display': u'加赠70%',
#        'addition': 70,
        'amount': 50000,
    },
#    'first': {
#        'diamond': 70,
#    },
    'content': {
        'chip': 50000,
    }
}

product_100807 = {
    'price': 10,
    'name': u'10元捕鸟鸟蛋礼包',
    'desc': {
#        'display': u'加赠5%',
#        'addition': 5,
        'amount': 10000,
    },
#    'first': {
#        'diamond': 5,
#    },
    'content': {
        'chip': 10000,
    }
}



product_100806 = {
    'price': 30,
    'name': u'30元捕鸟鸟蛋礼包',
    'desc': {
#        'display': u'加赠5%',
#        'addition': 15,
        'amount': 30000,
    },
#    'first': {
#        'diamond': 15,
#    },
    'content': {
        'chip': 30000,
    }
}

product_110806 = {
    'price': 30,
    'name': u'30元捕鸟鸟蛋礼包',
    'desc': {
#        'display': u'加赠5%',
#        'addition': 15,
        'amount': 150000,
    },
#    'first': {
#        'diamond': 15,
#    },
    'content': {
        'chip': 150000,
    }
}

product_100805 = {
    'price': 50,
    'name': u'50元捕鸟鸟蛋礼包',
    'desc': {
#        'display': u'加赠3%',
#        'addition': 15,
        'amount': 50000,
    },
#    'first': {
#        'diamond': 15,
#    },
    'content': {
        'chip': 50000,
    }
}

product_110805 = {
    'price': 50,
    'name': u'50元捕鸟鸟蛋礼包',
    'desc': {
#        'display': u'加赠3%',
#        'addition': 15,
        'amount': 250000,
    },
#    'first': {
#        'diamond': 15,
#    },
    'content': {
        'chip': 250000,
    }
}

product_100804 = {
    'price': 100,
    'name': u'100元捕鸟鸟蛋礼包',
    'desc': {
#        'display': u'加赠1%',
#        'addition': 20,
        'amount': 100000,
    },
#    'first': {
#        'diamond': 20,
#    },
    'content': {
        'chip': 100000,
    }
}

product_110804 = {
    'price': 100,
    'name': u'100元捕鸟鸟蛋礼包',
    'desc': {
#        'display': u'加赠1%',
#        'addition': 20,
        'amount': 500000,
    },
#    'first': {
#        'diamond': 20,
#    },
    'content': {
        'chip': 500000,
    }
}

product_100803 = {
    'price': 500,
    'name': u'500元捕鸟鸟蛋礼包',
    'desc': {
#        'display': u'加赠1%',
#        'addition': 50,
        'amount': 500000,
    },
#    'first': {
#        'diamond': 50,
#    },
    'content': {
        'chip': 500000,
    }
}

product_110803 = {
    'price': 500,
    'name': u'500元捕鸟鸟蛋礼包',
    'desc': {
#        'display': u'加赠1%',
#        'addition': 50,
        'amount': 2500000,
    },
#    'first': {
#        'diamond': 50,
#    },
    'content': {
        'chip': 2500000,
    }
}

product_100802 = {
    'price': 1000,
    'name': u'1000元捕鸟鸟蛋礼包',
    'desc': {
    #    'display': u'加赠1%',
    #    'addition': 100,
        'amount': 1000000,
    },
    #'first': {
    #    'diamond': 100,
    #},
    'content': {
        'chip': 1000000,
    }
}

product_110802 = {
    'price': 1000,
    'name': u'1000元捕鸟鸟蛋礼包',
    'desc': {
    #    'display': u'加赠1%',
    #    'addition': 100,
        'amount': 5000000,
    },
    #'first': {
    #    'diamond': 100,
    #},
    'content': {
        'chip': 5000000,
    }
}

product_100801 = {
    'price': 10,
    'name': u'10元捕鸟钻石礼包',
    'desc': {
#	    'display': u'加赠5%',
#        'addition': 5,
        'amount': 20
    },
#    'first': {
#        'diamond': 5
#    },
    'content': {
        'diamond': 20
    }
}

product_110801 = {
    'price': 10,
    'name': u'10元捕鸟钻石礼包',
    'desc': {
#	    'display': u'加赠5%',
#        'addition': 5,
        'amount': 100
    },
#    'first': {
#        'diamond': 5
#    },
    'content': {
        'diamond': 100
    }
}

product_100800 = {
    'price': 30,
    'name': u'30元捕鸟钻石礼包',
    'desc': {
#        'display': u'加赠5%',
#        'addition': 15,
        'amount': 60,
    },
#    'first': {
#        'diamond': 15,
#    },
    'content': {
        'diamond': 60,
    }
}

product_110800 = {
    'price': 30,
    'name': u'30元捕鸟钻石礼包',
    'desc': {
#        'display': u'加赠5%',
#        'addition': 15,
        'amount': 300,
    },
#    'first': {
#        'diamond': 15,
#    },
    'content': {
        'diamond': 300,
    }
}

product_100799 = {
    'price': 50,
    'name': u'50元捕鸟钻石礼包',
    'desc': {
#        'display': u'加赠3%',
#        'addition': 15,
        'amount': 100,
    },
#    'first': {
#        'diamond': 15,
#    },
    'content': {
        'diamond': 100,
    }
}

product_110799 = {
    'price': 50,
    'name': u'50元捕鸟钻石礼包',
    'desc': {
#        'display': u'加赠3%',
#        'addition': 15,
        'amount': 500,
    },
#    'first': {
#        'diamond': 15,
#    },
    'content': {
        'diamond': 500,
    }
}

product_100798 = {
    'price': 100,
    'name': u'100元捕鸟钻石礼包',
    'desc': {
#        'display': u'加赠1%',
#        'addition': 20,
        'amount': 200,
    },
#    'first': {
#        'diamond': 20,
#    },
    'content': {
        'diamond': 200,
    }
}

product_110798 = {
    'price': 100,
    'name': u'100元捕鸟钻石礼包',
    'desc': {
#        'display': u'加赠1%',
#        'addition': 20,
        'amount': 1000,
    },
#    'first': {
#        'diamond': 20,
#    },
    'content': {
        'diamond': 1000,
    }
}

product_100797 = {
    'price': 300,
    'name': u'300元捕鸟钻石礼包',
    'desc': {
#        'display': u'加赠1%',
#        'addition': 30,
        'amount': 600,
    },
#    'first': {
#        'diamond': 30,
#    },
    'content': {
        'diamond': 600,
    }
}

product_110797 = {
    'price': 300,
    'name': u'300元捕鸟钻石礼包',
    'desc': {
#        'display': u'加赠1%',
#        'addition': 30,
        'amount': 3000,
    },
#    'first': {
#        'diamond': 30,
#    },
    'content': {
        'diamond': 3000,
    }
}

product_101808 = {
    'price': 500,
    'name': u'500元捕鸟钻石礼包',
    'desc': {
#        'display': u'加赠1%',
#        'addition': 50,
        'amount': 1000,
    },
#    'first': {
#        'diamond': 50,
#    },
    'content': {
        'diamond': 1000,
    }
}

product_111808 = {
    'price': 500,
    'name': u'500元捕鸟钻石礼包',
    'desc': {
#        'display': u'加赠1%',
#        'addition': 50,
        'amount': 5000,
    },
#    'first': {
#        'diamond': 50,
#    },
    'content': {
        'diamond': 5000,
    }
}


month_card_reward = {
    'chip': 8888,
    'diamond': 10,
    'props': [{'id': 202, 'count': 2}],
}

add_game_config(2, 'month.card.reward', month_card_reward)

product_100808 = {
    'price': 50,
    'name': u'贵族礼包',
    'content': month_card_reward
}

product_100783 = {
    'price': 50,
    'name': u'狂怒炎龙',
    'weaponid': 20004,
}

product_100782 = {
    'price': 88,
    'name': u'雷鸣宙斯',
    'weaponid': 20006,
}

product_100781 = {
    'price': 128,
    'name': u'暗夜魅影',
    'weaponid': 20007,
}

product_100780 = {
    'price': 998,
    'name': u'无毁月光',
    'weaponid': 20009,
}

product_100784 = {
    'price': 188,
    'name': u'恭贺新春',
    'weaponid': 20010,
}

product_100900 = {
    'price': 160,
    'name': u'恭贺新春(8.5折)',
    'weaponid': 20010,
}

product_100904 = {
    'price': 150,
    'name': u'恭贺新春(8折)',
    'weaponid': 20010,
}

product_100903 = {
    'price': 132,
    'name': u'恭贺新春(7折)',
    'weaponid': 20010,
}

product_100901 = {
    'price': 75,
    'name': u'雷鸣宙斯(8.5折)',
    'weaponid': 20006,
}

product_100906 = {
    'price': 70,
    'name': u'雷鸣宙斯(8折)',
    'weaponid': 20006,
}

product_100905 = {
    'price': 62,
    'name': u'雷鸣宙斯(7折)',
    'weaponid': 20006,
}

product_100902 = {
    'price': 109,
    'name': u'暗夜魅影(8.5折)',
    'weaponid': 20007,
}

product_100908 = {
    'price': 102,
    'name': u'暗夜魅影(8折)',
    'weaponid': 20007,
}

product_100907 = {
    'price': 90,
    'name': u'暗夜魅影(7折)',
    'weaponid': 20007,
}

product_100911 = {
    'price': 43,
    'name': u'狂怒炎龙(8.5折)',
    'weaponid': 20004,
}

product_100910 = {
    'price': 40,
    'name': u'狂怒炎龙(8折)',
    'weaponid': 20004,
}

product_100909 = {
    'price': 35,
    'name': u'狂怒炎龙(7折)',
    'weaponid': 20004,
}

product_100785 = {
    'price': 328,
    'name': u'超值礼包',
    'worth': 448,
    'content': {
        'chip': 1600000,
        'diamond': 188,
        'props': [{'id': 202, 'count': 20}, {'id': 203, 'count': 20}],
    }
}

__love_product_template = {
    'price': 15,
    'name': u'公益礼包',
    'content': {
        'props': [{'id': 215, 'count': 10}, {'id': 216, 'count': 10}, {'id': 217, 'count': 10}, {'id': 218, 'count': 10}],
        # 'chip': 60000,
        # 'props': [{'id': 201, 'count': 20}, {'id': 202, 'count': 10}],
    }
}

product_100604 = {
    'price': 30,
    'name': u'紫晶石*15',
    'exp': 200,
    'content': {
        'props': [{'id': 217, 'count': 15}],
    }
}

product_100603 = {
    'price': 30,
    'name': u'蓝魔石*15',
    'exp': 200,
    'content': {
        'props': [{'id': 216, 'count': 15}],
    }
}

product_100602 = {
    'price': 30,
    'name': u'血精石*15',
    'exp': 200,
    'content': {
        'props': [{'id': 218, 'count': 15}],
    }
}

product_100601 = {
    'price': 30,
    'name': u'绿灵石*15',
    'exp': 200,
    'content': {
        'props': [{'id': 215, 'count': 15}],
    }
}

#product_101001= {
#    'price': 50,
#    'name': u'狂暴无双*10',
#    'content': {
#        'props': [{'id': 203, 'count': 10}],
#    }
#}

product_101111 = {
    'price': 6,
    'name': u'活动礼包1',
}

product_101112 = {
    'price': 88,
    'name': u'活动礼包2',
}

product_101113 = {
    'price': 6,
    'name': u'活动礼包3',
}

product_101114 = {
    'price': 88,
    'name': u'活动礼包4',
}


product_102001 = {
    'price': 68,
    'name': u'黄金月卡',
    'diamond_price': 680,
    'content': {'chip':8000},
    'first_content': {'chip':128000},
}


product_102002 = {
    'price': 216,
    'name': u'至尊月卡',
    'diamond_price': 2160,
    'content': {'chip':18000},
    'first_content': {'chip':618000},
}

product_102003 = {
    'price': 6,
    'name': u'六元新手礼包',
    'content': {
        'chip':50000,
        'props': [{'id': 203, 'count': 2}, {'id': 202, 'count': 5}, {'id': 205, 'count': 5}],
    },
}


__product_config = {
    '101807': product_101807, #10元捕鸟鸟蛋礼包（oppo新春）
    '111807': product_111807, #10元捕鸟鸟蛋礼包（oppo新春） v2
    '100807': product_100807, #10元捕鸟鸟蛋礼包
    '100806': product_100806, #30元捕鸟鸟蛋礼包
    '110806': product_110806, #30元捕鸟鸟蛋礼包  v2
    '100805': product_100805, #50元捕鸟鸟蛋礼包
    '110805': product_110805, #50元捕鸟鸟蛋礼包   v2
    '100804': product_100804, #100元捕鸟鸟蛋礼包
    '110804': product_110804, #100元捕鸟鸟蛋礼包  v2
    '100803': product_100803, #500元捕鸟鸟蛋礼包
    '110803': product_110803, #500元捕鸟鸟蛋礼包  v2
    '100802': product_100802, #1000元捕鸟鸟蛋礼包
    '110802': product_110802, #1000元捕鸟鸟蛋礼包 v2
    '100801': product_100801, #10元捕鸟钻石礼包
    '110801': product_110801, #10元捕鸟钻石礼包   v2
    '100800': product_100800, #30元捕鸟钻石礼包
    '110800': product_110800, #30元捕鸟钻石礼包   v2
    '100799': product_100799, #50元捕鸟钻石礼包
    '110799': product_110799, #50元捕鸟钻石礼包  v2
    '100798': product_100798, #100元捕鸟钻石礼包
    '110798': product_110798, #100元捕鸟钻石礼包   v2
    '100797': product_100797, #300元捕鸟钻石礼包
    '110797': product_110797, #300元捕鸟钻石礼包  v2
	'101808': product_101808, #500元捕鸟钻石礼包
    '111808': product_111808, #500元捕鸟钻石礼包   v2
    '100808': product_100808, #贵族礼包
    '100783': product_100783, #炮台: 狂怒炎龙
    '100782': product_100782, #炮台: 雷鸣宙斯
    '100781': product_100781, #炮台: 暗夜魅影
    '100780': product_100780, #炮台: 无毁月光
	'100784': product_100784, #炮台: 恭贺新春
	'100900': product_100900, #炮台: 恭贺新春（活动打折8.5）
	'100904': product_100904, #炮台: 恭贺新春（活动打折8）
    '100903': product_100903, #炮台: 恭贺新春（活动打折7）
	'100901': product_100901, #炮台: 雷鸣宙斯（活动打折8.5）
	'100906': product_100906, #炮台: 雷鸣宙斯（活动打折8）
	'100905': product_100905, #炮台: 雷鸣宙斯（活动打折7）
	'100902': product_100902, #炮台: 暗夜魅影（活动打折8.5）
	'100908': product_100908, #炮台: 暗夜魅影（活动打折8）
	'100907': product_100907, #炮台: 暗夜魅影（活动打折7）
	'100911': product_100911, #炮台: 狂怒炎龙（活动打折8.5）
	'100910': product_100910, #炮台: 狂怒炎龙（活动打折8）
	'100909': product_100909, #炮台: 狂怒炎龙（活动打折7）
    '100785': product_100785, #超值礼包

    '100601': product_100601, #强化石,
    '100602': product_100602, #强化石
    '100603': product_100603, #强化石
    '100604': product_100604, #强化石
#	'101001': product_101001, #狂暴无双*10（活动打折8）
    '101111': product_101111, #活动礼包1
    '101112': product_101112, #活动礼包2
    '101113': product_101113,  # 活动礼包3
    '101114': product_101114,  # 活动礼包4

    '102001': product_102001,  # 黄金月卡
    '102002': product_102002,  # 至尊月卡
    '102003': product_102003,  # 六元新手礼包
}

# 商城活动配置
_activity_shop_config = {
    'weapon':[
#         活动-打折时商品id    正常商品id
        {'a_pid':'100903', 'pid': '100784'},
    ]
}

__shop_config = {
    'chip': ['101807', '100805', '100804', '100803', '100802', '111807', '110805', '110804', '110803', '110802'],
    'diamond': ['100801', '100799', '100798', '100797', '101808', '110801', '110799', '110798', '110797', '111808'],
    'card': ['100808', '102001', '102002'],
    'first': ['100785', '102003',],
    'weapon': ['100780', '100781', '100782', '100783', '100784', '100900', '100904', '100903', '100901', '100906', '100905', '100902', '100908', '100907', '100911', '100910', '100909'],
    'props': ['100601', '100602', '100603', '100604'],
    'activity': ['101111', '101112', '101113', '101114'],
}



# 新增道具商城
# 商品id:
    #0:道具名称
    #1:道具id
    #2:货币类型（1、鸟蛋，2、钻石，3、RMB，（非币种解锁，需VIP等级解锁））
    #3:价格
    #4:购买限制（vip），0代表免费玩家，1及以上代表VIP等级玩家
    #5:限购类型，1日个人限购，2日全服限购， 3周个人限购， 4周全服限购， 5月个人限购， 6月全服限购（没有限购填1）
    #6:限购数量
    #7:道具说明
__prop_shop_config = {
    30000: [u'冰冻*40', {'props': [{'id': 202, 'count': 40}]}, 2, 200, 0, [{'type':1,'num':0}], u'什么！鸟要逃走了？赶快使用全屏冰冻，瞬间为你冰冻。', '0'],
    30001: [u'狂暴无双*10', {'props': [{'id': 203, 'count': 10}]}, 2, 500, 2, [{'type':1,'num':0}], u'使用狂暴技能，立即获得双倍击杀概率。', '0'],
    30002: [u'超级武器*1', {'props': [{'id': 204, 'count': 1}]}, 2, 200, 2, [{'type':1,'num':0}], u'发射一颗威力强大的超级武器，记得对准鸟多的地方扔哦！(对BOSS无效)', '0'],
    30003: [u'赏金传送*100', {'props': [{'id': 205	, 'count': 100}]}, 2, 500, 0, [{'type':1,'num':0}], u'快快使用传送门，传送出一只神秘奖金鸟吧。', '0'],
    # 30004: [u'绿灵石*15', {'props': [{'id': 215, 'count': 15}]}, 3, 30, 0, [{'type':1,'num':0}], u'绿灵石是用于强化1000倍以上炮台的必备材料。', '100601'],
    # 30005: [u'血精石*15', {'props': [{'id': 218, 'count': 15}]}, 3, 30, 0, [{'type':1,'num':0}], u'血精石是用于强化1000倍以上炮台的必备材料。', '100602'],
    # 30006: [u'蓝魔石*15', {'props': [{'id': 216, 'count': 15}]}, 3, 30, 0, [{'type':1,'num':0}], u'蓝魔石是用于强化1000倍以上炮台的必备材料。', '100603'],#强化武器时必要的材料之一
    # 30007: [u'紫晶石*15', {'props': [{'id': 217, 'count': 15}]}, 3, 30, 0, [{'type':1,'num':0}], u'紫晶石是用于强化1000倍以上炮台的必备材料。', '100604'],
}

# 新增武器商城
# 炮台id:
    #炮台名称
    #购买类型（1、鸟蛋，2、钻石，3、RMB，4、VIP等级（非币种解锁，需VIP等级解锁））
    #购买价格
    #炮台说明
    #产品对应id
    #限时炮台一台1天能换多少金币    
	#限时炮=ID+000（代表天数）PS：20009030=30天激光炮

__weaponshop_config = {
    20000:[u'零式火炮', 0, 0, u'简介：初出茅庐，永战征途。', '0', 0],
    20001:[u'流沙之鳞', 1, 100000, u'简介：沉睡在沙漠中的远古守护者，只为有一天能被唤醒。', '0', 1],
    20002:[u'冰翼猎手', 2, 300, u'简介：在凛冬的极点观看着人世的丑态。', '0', 1],
    20003:[u'翡翠荆棘', 4, 4, u'简介：绚丽的外表下，总是隐藏着深邃的诅咒。', '0', 1],
    20004:[u'狂怒炎龙', 3, 50, u'简介：桀骜不羁的人生，总是憧憬能实现惊天伟业。', '100783', 1],
    20005:[u'死亡之翼', 4, 6, u'简介：如果你在凝望深渊，那么深渊也在凝视着你。', '0', 1],
	20006:[u'雷鸣宙斯', 3, 88, u'简介：化身宙斯，降愤怒于苍穹。', '100782', 1],
    20007:[u'暗夜魅影', 3, 128, u'简介：看穿一切，洞穿无限。', '100781', 1],
    20008:[u'九五至尊', 4, 8, u'简介：无上荣耀，九五至尊。', '0', 1],
    #20009:[u'无毁月光', 3, 998, u'简介：心之所向，无坚不摧，无所不得。', '100780', 6666],
	20010:[u'恭贺新春', 3, 188, u'简介：吉祥如意，恭喜发财。', '100784', 1],
}

# 实物兑换商城
__exchange_config = {
    # 40101: [u'50元话费直充', 2, {'props': [{'id': 408, 'count': 1}]}, 5, 65, 1, [{'type':1,'num':999}, {'type':2,'num':99999}], u'暂无描述',0],
	# 40102: [u'100元话费卡密', 4, {'props': [{'id': 405, 'count': 1}]}, 5, 130, 1, [{'type':1,'num':999}, {'type':2,'num':99999}], u'暂无描述',0],
    # 40103: [u'100元话费直充', 2, {'props': [{'id': 409, 'count': 1}]}, 5, 130, 1, [{'type':1,'num':999}, {'type':2,'num':99999}], u'暂无描述',0],
    # 40104: [u'200元加油卡', 1, {'props': [{'id': 410, 'count': 1}]}, 5, 260, 1, [{'type':1,'num':999}, {'type':2,'num':99999}], u'暂无描述',0],
    # 40105: [u'500元京东卡', 1, {'props': [{'id': 411, 'count': 1}]}, 5, 650, 2, [{'type':1,'num':999}, {'type':2,'num':99999}], u'暂无描述',0],
    
}
__point_shop_config = {
    40000: [u'美的多功能电烤箱', 1, {'props': [{'id': 401, 'count': 1}]}, 6, 288, 1, [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],
    40001: [u'罗马仕充电宝', 1, {'props': [{'id': 402, 'count': 1}]}, 6, 130, 1, [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],
    40002: [u'美的电饭煲', 1, {'props': [{'id': 403, 'count': 1}]}, 6, 388, 1, [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],
    40003: [u'小米手环', 1, {'props': [{'id': 404, 'count': 1}]}, 6, 182, 1, [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],
    40051: [u'美的热水壶', 1, {'props': [{'id': 451, 'count': 1}]}, 6, 168, 1, [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1]
}



# 新增限时商城
# 商品id:
    #0:道具名称
    #1:道具或实物，1是数码设备、2是充值卡、3是虚拟道具、4卡密、5卡类实物
    #2:道具
    #3:货币类型（1、鸟蛋，2、钻石，3、RMB、4非币种解锁，需VIP等级解锁，5、鸟卷, 6、积分）
    #4:价格
    #5:购买限制（vip）
    #6:限购类型，1日个人限购，2日全服限购
    #7:限购数量
    #8:道具说明
	#9:商品上下架 0=下架  1=上架
__limit_shop_config = {
    '1001_0':
        {
            40000: [u'美的多功能电烤箱', 1, {'props': [{'id': 401, 'count': 1}]}, 5, 1152, 1,
                    [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],
            40001: [u'罗马仕充电宝', 1, {'props': [{'id': 402, 'count': 1}]}, 5, 520, 1,
                    [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],
            40002: [u'美的电饭煲', 1, {'props': [{'id': 403, 'count': 1}]}, 5, 1552, 1,
                    [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],
            40003: [u'小米手环', 1, {'props': [{'id': 404, 'count': 1}]}, 5, 728, 1,
                    [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],
            40051: [u'美的热水壶', 1, {'props': [{'id': 451, 'count': 1}]}, 5, 672, 1,
                    [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],
            40052: [u'美的加湿器', 1, {'props': [{'id': 452, 'count': 1}]}, 5, 872, 1,
                    [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],
            40053: [u'美的豆浆机', 1, {'props': [{'id': 453, 'count': 1}]}, 5, 1272, 1,
                    [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],
            40054: [u'美的挂烫机', 1, {'props': [{'id': 454, 'count': 1}]}, 5, 952, 1,
                    [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],
            40055: [u'美的吸尘器', 1, {'props': [{'id': 455, 'count': 1}]}, 5, 1552, 1,
                    [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],
            40056: [u'美的空调扇', 1, {'props': [{'id': 456, 'count': 1}]}, 5, 2432, 1,
                    [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 0],
            40057: [u'飞利浦电吹风', 1, {'props': [{'id': 457, 'count': 1}]}, 5, 472, 1,
                    [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],
            40058: [u'飞利浦蓝牙音响', 1, {'props': [{'id': 458, 'count': 1}]}, 5, 672, 1,
                    [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],
            40059: [u'飞利浦蓝牙耳机', 1, {'props': [{'id': 459, 'count': 1}]}, 5, 1192, 1,
                    [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],
            40060: [u'飞利浦剃须刀', 1, {'props': [{'id': 460, 'count': 1}]}, 5, 1552, 1,
                    [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],
            40061: [u'飞利浦电动牙刷', 1, {'props': [{'id': 461, 'count': 1}]}, 5, 1272, 1,
                    [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],
            40062: [u'Olay烟酰胺沐浴露', 1, {'props': [{'id': 462, 'count': 1}]}, 5, 272, 1,
                    [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],
            40063: [u'沙宣洗发水', 1, {'props': [{'id': 463, 'count': 1}]}, 5, 272, 1,
                    [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],
            40064: [u'膜法世家面膜', 1, {'props': [{'id': 464, 'count': 1}]}, 5, 352, 1,
                    [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],
            40065: [u'云南白药牙膏', 1, {'props': [{'id': 465, 'count': 1}]}, 5, 352, 1,
                    [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],

            40004: [u'100元话费卡密', 4, {'props': [{'id': 405, 'count': 1}]}, 5, 520, 1,
                    [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],
            40005: [u'500元加油卡', 5, {'props': [{'id': 406, 'count': 1}]}, 5, 2600, 2,
                    [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],
            40101: [u'50元话费直充', 2, {'props': [{'id': 408, 'count': 1}]}, 5, 260, 1,
                    [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],
            40102: [u'100元话费直充', 2, {'props': [{'id': 409, 'count': 1}]}, 5, 520, 1,
                    [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],
            40103: [u'200元加油卡', 5, {'props': [{'id': 410, 'count': 1}]}, 5, 1040, 1,
                    [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],
            40104: [u'500元京东卡', 5, {'props': [{'id': 411, 'count': 1}]}, 5, 2600, 2,
                    [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 1],

            40007: [u'250000鸟蛋', 3, {'chip': 250000}, 5, 260, 1, [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}],
                    u'暂无描述', 1],
            40008: [u'200钻石', 3, {'diamond': 200}, 5, 104, 1, [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}],
                    u'暂无描述', 1],
            #40009: [u'绿灵石（10）', 3, {'props': [{'id': 215, 'count': 10}]}, 5, 26, 1,
            #        [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 0],
            #40010: [u'血精石（10）', 3, {'props': [{'id': 218, 'count': 10}]}, 5, 26, 1,
            #        [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 0],
            #40011: [u'蓝魔石（10）', 3, {'props': [{'id': 216, 'count': 10}]}, 5, 26, 1,
            #        [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 0],
            #40012: [u'紫晶石（10）', 3, {'props': [{'id': 217, 'count': 10}]}, 5, 26, 1,
            #        [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 0],
            #40013: [u'强化精华（10）', 3, {'props': [{'id': 219, 'count': 10}]}, 5, 65, 1,
            #        [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}], u'暂无描述', 0],
            #40014: [u'靶场卷（5）', 3, {'target': 5}, 5, 20, 2, [{'type': 1, 'num': 999}, {'type': 2, 'num': 99999}],
            #        u'暂无描述', 0],
        },

    # 如果这里增加了 兑换鸟蛋、钻石、靶场券等处理，需要再下面的_limit_coupon_cost_pay  增加id，作为特殊充值处理

}

# 特殊鸟券消耗，需要增加玩家的支付额度
_limit_coupon_cost_pay = {
    # 特殊支付产品id
    'as_pay':[40007, 40008, 40014]
}

# 开启时间，结束时间，需要vip等级上
__limit_time_config = [0,24,0]


# 钻石商城，金币商城
for i in xrange(1, 11):
    # key = str(100785 + i)
    # key = ['100786', '100788', '100789', '100790', '100791', '100792', '100793', '100794', '100795', '100796']
    product = copy.deepcopy(__love_product_template)
    product['price'] *= i
    product['name'] = u'%s元%s' % (product['price'], product['name'])
    if 'chip' in product['content']:
        product['content']['chip'] *= i
    for p in product['content']['props']:
        p['count'] *= i
    # __product_config[key[i-1]] = product
    # __shop_config['love'].append(key[i-1])


# 鸟蛋的商品（用于充值翻倍的属于，只要买过此如下商品就不能再充值翻倍，****添加了鸟蛋商品****）
add_game_config(2, 'chip.product.config', ['100807', '101807', '100806', '100805', '100804', '100803', '100802'] )

add_game_config(2, 'product.config', __product_config)

add_game_config(2, 'shop.config', __shop_config)

add_game_config(2, 'limit_coupon_cost_pay.config', _limit_coupon_cost_pay)

add_game_config(2, 'activity_shop.config', _activity_shop_config)

add_game_config(2, 'exchange.config', __exchange_config)

add_game_config(2, 'weaponshop.config', __weaponshop_config)

add_game_config(2, 'props.shop.config', __prop_shop_config)

add_game_config(2, 'limit.shop.config', __limit_shop_config, False)
add_game_config(2, 'limit.time.config', __limit_time_config)

add_game_config(2, 'point.shop.config', __point_shop_config, False)

add_game_config(2, 'qifan.app.info', {
    'appId': '10149',
    'appKey': '14311117e9cad2f6b379754fb587ec47',
})
