#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-03-14

from lemon.entity.props import Props
from framework.context import Context
from framework.util.tool import Time, Tool

class BirdProps(Props):
    PROP_LOCK_BIRD = 201        # 锁定
    PROP_FREEZE = 202           # 冰冻
    PROP_VIOLENT = 203          # 狂暴
    PROP_SUPER_WEAPON = 204     # 超级武器
    PROP_PORTAL = 205           # 传送门
    PROP_EGG_BRONZE = 211       # 青铜宝箱
    PROP_EGG_SILVER = 212       # 白银宝箱
    PROP_EGG_GOLD = 213         # 黄金宝箱
    PROP_EGG_COLOR = 214        # 至尊宝箱
    GREEN_STONE = 215           # 绿灵石
    YELLOW_STONE = 216          # 血精石
    VIOLET_STONE = 217          # 蓝魔石
    RED_STONE = 218             # 紫晶石
    GEM = 219                   # 强化精华
    CREATE_TABLE_CARD = 220     # 创房卡
    B_PET_EGG = 221             # B宠物蛋
    A_PET_EGG = 222             # A宠物蛋
    S_PET_EGG = 223             # S宠物蛋
    PROP_SUMMON_MONSTER = 224   # 召唤红龙
    ROOM_CARD = 225             # 房卡
    # 新增物品
    PROP_CARD_10086 = 301       # 移动话费卡
    PROP_CARD_189 = 302         # 电信话费卡
    PROP_CARD_10010 = 303       # 联通话费卡
    PROP_CARD_JD = 304          # 京东E卡
    PROP_CARD_Digital = 305     # 数码设备抵扣卷
    PROP_CARD_FOOD = 306        # 食品类抵扣卷
    PROP_CARD_HOUSEHOLD = 307   # 家用电器抵扣卷
    # 二期新增物品
    PROP_MIDEA_ELECTRIC_OVEN = 401 # 美的多功能电烤箱
    PROP_ROMOSS_CHARGE_PAL = 402   # 罗马仕充电宝
    PROP_MIDEA_RICE_COOKER = 403   # 美的电饭煲
    PROP_MIUI_BRACELET = 404       # 小米手环
    PROP_SECRET_CARD_100R = 405     # 100元话费卡密
    PROP_FUEL_CARD_500R = 406       # 500元加油卡
    
    PROP_PHONE_CARD_50R = 408         # 50元话费直充
    PROP_PHONE_CARD_100R = 409      # 100元话费直充
    PROP_FUEL_CARD_200R = 410        # 200元加油卡
    PROP_CARD_JD_500R = 411        # 500元京东卡


    PROP_BOX_BRONZE = 601
    PROP_BOX_SILVER = 602
    PROP_BOX_GOLD= 603

    # 新增掉落测试
    PROP_COUPON = 3             # 鸟卷掉落


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

    def check_props(self, pid):
        if pid > 10000*1000:
            return True
        return pid in (201, 202, 203, 204, 205, 211, 212, 213, 214, 215, 216,
                       217, 218, 219, 220, 221, 222, 223, 224, 225,
                       301, 302, 303, 304, 305, 306, 307,
                       3,
                       601,602,603)

    def stat_props(self, uid, gid, pid, count, event):
        if count > 0 and pid in [211, 212, 213, 214] and event in ['bird.fall', 'bonus.raffle']:
            # 个人 宝盒 统计
            Context.Data.hincr_game(uid, gid, 'in_props_'+str(pid), count)

    def pet_egg_ids(self):
        return [220, 221, 222, 223]

    def get_props_config(self, gid):
        return Context.Configure.get_game_item_json(gid, 'props.config')

    def get_config_by_id(self, gid, pid):
        conf = Context.Configure.get_game_item_json(gid, 'props.config')
        for item in conf:
            if item['id'] == pid:
                return item

    def get_props_list(self, uid, gid, pids=None):
        if pids is None:
            pids = [201, 202, 203, 204, 205, 211, 212, 213, 214, 215, 216,
                    217, 218, 219, 220, 221, 222, 223, 224, 225,
                    301, 302, 303, 304, 305, 306, 307,
                    3,
                    601,602,603]
        key = 'props:%d:%d' % (gid, uid)
        kvs = Context.RedisCluster.hash_getall(uid, key)
        props_list = []
        for k, v in kvs.iteritems():
            if (int(k) in pids or int(k) > 10000*1000) and int(v) > 0:
                props_list.append([int(k), int(v)])
        return props_list

    def filter_props_by_version(self, uid, gid, props, version=None):
        # if version is None:
        #     version = Context.Data.get_game_attr(uid, gid, 'session_ver')

        # low_then_1_2_0 = bool(Upgrade.cmp_version(version, '1.2.0') < 0)
        # if low_then_1_2_0:
        #     low_then_1_1_0 = bool(Upgrade.cmp_version(version, '1.1.0') < 0)
        #     if low_then_1_1_0:
        #         pids = (201, 202, 203, 204, 205, 211, 212, 213, 214)
        #     else:
        #         pids = (201, 202, 203, 204, 205, 211, 212, 213, 214, 215, 216, 217, 218, 219)

        #     pl = []
        #     for item in props:
        #         if isinstance(item, dict):
        #             if item['id'] in pids:
        #                 pl.append(item)
        #         else:
        #             if item[0] in pids:
        #                 pl.append(item)
        #     return pl
        # else:
        return props

    def get_egg_count(self, uid, gid):
        key = 'props:%d:%d' % (gid, uid)
        kvs = Context.RedisCluster.hash_mget_as_dict(uid, key, 211, 212, 213, 214)
        count = 0
        for k, v in kvs.iteritems():
            if int(v) > 0:
                count += int(v)
        return count

    # 获取商品的鸟蛋价值
    def get_props_price(self, rewards_info):
        result = 0
        if 'chip' in rewards_info:
            result += Tool.to_int(rewards_info['chip'], 0)
        if 'diamond' in rewards_info:
            diamond = Tool.to_int(rewards_info['diamond'], 0) * self.PRICE_DICT['diamond']
            result += diamond
        if 'coupon' in rewards_info:
            coupon = Tool.to_int(rewards_info['coupon'], 0) * self.PRICE_DICT['coupon']
            result += coupon
        if 'target' in rewards_info:
            target = Tool.to_int(rewards_info['target'], 0) * self.PRICE_DICT['target']
            result += target
        if 'props' in rewards_info:
            for one in rewards_info['props']:
                props = Tool.to_int(one['count'], 0) * self.PRICE_DICT[one['id']]
                result += props
        return result

    def get_props_desc(self, pid):
        if pid == self.PROP_LOCK_BIRD:
            return u'锁定'
        elif pid == self.PROP_FREEZE:
            return u'冰冻'
        elif pid == self.PROP_VIOLENT:
            return u'狂暴'
        elif pid == self.PROP_SUPER_WEAPON:
            return u'超级武器'
        elif pid == self.PROP_PORTAL:
            return u'传送门'
        elif pid == self.PROP_EGG_BRONZE:
            return u'青铜宝箱'
        elif pid == self.PROP_EGG_SILVER:
            return u'白银宝箱'
        elif pid == self.PROP_EGG_GOLD:
            return u'黄金宝箱'
        elif pid == self.PROP_EGG_COLOR:
            return u'至尊宝箱'
        elif pid == self.GREEN_STONE:
            return u'绿灵石'
        elif pid == self.RED_STONE:
            return u'血精石'
        elif pid == self.YELLOW_STONE:
            return u'蓝魔石'
        elif pid == self.VIOLET_STONE:
            return u'紫晶石'
        elif pid == self.GEM:
            return u'强化精华'
        elif pid == self.CREATE_TABLE_CARD:
            return u'创房卡'
        elif pid == self.B_PET_EGG:
            return u'B级宠物蛋'
        elif pid == self.A_PET_EGG:
            return u'A级宠物蛋'
        elif pid == self.S_PET_EGG:
            return u'S级宠物蛋'
        elif pid == self.PROP_SUMMON_MONSTER:
            return u'召唤技能'
        elif pid == self.ROOM_CARD:
            return u'房卡道具'
        # 以下为新增
        elif pid == self.PROP_CARD_10086:
            return u'移动话费卡'
        elif pid == self.PROP_CARD_189:
            return u'电信话费卡'
        elif pid == self.PROP_CARD_10010:
            return u'联通话费卡'
        elif pid == self.PROP_CARD_JD:
            return u'京东E卡'
        elif pid == self.PROP_CARD_Digital:
            return u'数码设备抵扣卷'
        elif pid == self.PROP_CARD_FOOD:
            return u'食品类抵扣卷'
        elif pid == self.PROP_CARD_HOUSEHOLD:
            return u'家用电器抵扣卷'
        elif pid == self.PROP_BOX_BRONZE:
            return u'青铜宝箱'
        elif pid == self.PROP_BOX_SILVER:
            return u'白银宝箱'
        elif pid == self.PROP_BOX_GOLD:
            return u'黄金宝箱'
        # 以下为二期新增
        elif pid == self.PROP_MIDEA_ELECTRIC_OVEN:
            return u'美的多功能电烤箱'
        elif pid == self.PROP_ROMOSS_CHARGE_PAL:
            return u'罗马仕充电宝'
        elif pid == self.PROP_MIDEA_RICE_COOKER:
            return u'美的电饭煲'
        elif pid == self.PROP_MIUI_BRACELET:
            return u'小米手环'
        elif pid == self.PROP_SECRET_CARD_100R:
            return u'100元话费卡密'
        elif pid == self.PROP_FUEL_CARD_500R:
            return u'500元加油卡'
        elif pid == self.PROP_PHONE_CARD_50R:
            return u'50元话费直充'
        elif pid == self.PROP_PHONE_CARD_100R:
            return u'100元话费直充'
        elif pid == self.PROP_FUEL_CARD_200R:
            return u'200元加油卡'
        elif pid == self.PROP_CARD_JD_500R:
            return u'500元京东卡'
        # 新增掉落测试
        elif pid == self.PROP_COUPON:
            return u'鸟券'
        elif pid == 220:
            return u'创房卡'

        # 限时炮道具
        elif pid >= 20000*1000 and pid <= 30000*1000:
            props_id = int(pid/1000)
            props_day = int(pid % 1000)
            name = u''
            if props_id == 20000:
                name += u'零式火炮'
            if props_id == 20001:
                name += u'流沙之鳞'
            if props_id == 20002:
                name += u'冰翼猎手'
            if props_id == 20003:
                name += u'翡翠荆棘'
            if props_id == 20004:
                name += u'狂怒炎龙'
            if props_id == 20005:
                name += u'死亡之翼'
            if props_id == 20006:
                name += u'雷鸣宙斯'
            if props_id == 20007:
                name += u'暗夜魅影'
            if props_id == 20008:
                name += u'九五至尊'
            name = name + u'%d天'%(props_day)
            return name

    def convert_reward(self, rewards_info):
        result = {}
        if 'chip' in rewards_info:
            result['c'] = rewards_info['chip']
        if 'diamond' in rewards_info:
            result['d'] = rewards_info['diamond']
        if 'fake_chip' in rewards_info:
            result['f'] = rewards_info['fake_chip']
        if 'coupon' in rewards_info:
            result['o'] = rewards_info['coupon']
        if 'target' in rewards_info:
            result['tg'] = rewards_info['target']
        if 'auto_shot' in rewards_info:
            result['auto_shot'] = rewards_info['auto_shot']
        if 'weapon' in rewards_info:
            result['weapon'] = rewards_info['weapon']
        if 'props' in rewards_info:
            props = []
            for one in rewards_info['props']:
                props.append([one['id'], one['count']])
            if props:
                result['p'] = props
        if 'reward' in rewards_info:
            rw = self.convert_reward(rewards_info['reward'])
            if rw:
                result['w'] = rw
        return result

    #奖励翻倍
    def reward_doubling(self, rewards_info, multiple):
        result = {}
        if 'chip' in rewards_info:
            result['chip'] = int(rewards_info['chip'] * multiple)
        if 'diamond' in rewards_info:
            result['diamond'] = int(rewards_info['diamond'] * multiple)
        if 'fake_chip' in rewards_info:
            result['fake_chip'] = int(rewards_info['fake_chip'] * multiple)
        if 'coupon' in rewards_info:
            result['coupon'] = int(rewards_info['coupon'] * multiple)
        if 'target' in rewards_info:
            result['target'] = int(rewards_info['target'] * multiple)
        if 'props' in rewards_info:
            props = []
            for one in rewards_info['props']:
                rw = {}
                rw['id'] = one['id']
                rw['count'] = int(one['count'] * multiple)
                props.append(rw)
            if props:
                result['props'] = props
        return result

    def convert_pid_count(self, reward):
        if 'chip' in reward:
            return BirdProps.PROP_CHIP, reward['chip']
        elif 'diamond' in reward:
            return BirdProps.PROP_DIAMOND, reward['diamond']
        elif 'coupon' in reward:
            return BirdProps.PROP_COUPON, reward['coupon']
        elif 'rmb' in reward:
            return BirdProps.PROP_RMB, reward['rmb']
        elif 'props' in reward:
            for one in reward['props']:
                return one['id'], one['count']
        return None, None


BirdProps = BirdProps()

if __name__ == '__main__':
    Context.init_with_redis_key('127.0.0.1:6379:0')
    Context.load_lua_script()
    print BirdProps.get_vip(22228, 2)
