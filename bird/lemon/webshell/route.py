#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-02-26
import datetime
from framework.context import Context
from lemon.entity.upgrade import Upgrade
from framework.entity.msgpack import MsgPack
from framework.util.exceptions import NotFoundException
from framework.util.exceptions import ForbiddenException
from framework.util.tool import Time, Tool
from framework.util.tool import Algorithm
from sdk.modules.order import Order
from lemon.games.bird.newtask import NewTask
from lemon.games.bird.entity import BirdEntity
from lemon.games.bird.shop import Shop
from lemon.games.bird.props import BirdProps

from lemon.games.bird.account import BirdAccount


class HttpShell(object):
    token = None
    def __init__(self):
        self.token = Context.Configure.get_global_item('shell.access_key')
        self.token_special = Context.Configure.get_global_item('shell.special_access_key')
        self.cdkey_access_key = Context.Configure.get_global_item('cdkey.access_key')
        self.special_json_path = {
            #'/v1/game/str_order':self.str_order,
        }
        self.json_path = {
            #'/v1/shell/gm/reward/chip': self.gm_reward_chip,
            #'/v1/shell/gm/reward/coupon': self.gm_reward_coupon,
            #'/v1/shell/gm/reward/diamond': self.gm_reward_diamond,
            #'/v1/shell/gm/reward/egg_buff': self.gm_reward_egg_pool,
            #'/v1/shell/gm/query/egg_buff': self.gm_query_egg_pool,
            #'/v1/shell/gm/reward/coupon_buff': self.gm_reward_coupon_pool,
            #'/v1/shell/gm/query/coupon_buff': self.gm_query_coupon_pool,
            #'/v1/shell/gm/version/upgrade': self.gm_version_upgrade,
            #'/v1/shell/query/online': self.query_online,        # 查询在线用户
            #'/v1/shell/weixin/pay/creat_order': self.weixin_pay_creat_order,
            #'/v1/shell/alipay/pay/creat_order': self.alipay_pay_creat_order,
            #'/v1/shell/fix/order': self.fix_order,
            #'/v1/game/product/test': self.test,
            #'/v1/game/str_order':self.str_order,
            #'/v1/shell/gm/push/led': self.gm_push_led,  # 广播

            '/v1/shell/gm/account/disable': self.disable_user,  # 封号
            #'/v1/shell/gm/reward/pay': self.gm_pay,  # 待定  用于赠送礼包  模拟充值
            '/v1/shell/query/summary': self.query_summary,  # 查询玩家信息
            '/v1/shell/query/online_detail': self.query_online_detail,  # 在线详情
            '/v1/shell/query/money/count': self.query_money_count,  # 货币统计
            '/v1/shell/query/coupon_output': self.coupon_output,  # 鸟卷产出
            '/v1/shell/query/super_weapon_count': self.super_weapon_count,  # 超级武器统计
            '/v1/shell/query/query_box_fall': self.query_box_fall,  # 宝箱掉落
            '/v1/shell/query/query_carry_chip': self.query_carry_chip,  # 查询金币携带
            '/v1/shell/query/shop_info': self.query_shop_info,  # 商城信息
            '/v1/shell/shop/shipping_info': self.shipping_info,  # 发货信息
            '/v1/shell/shop/shipping_state': self.shipping_state,  # 发货状态
            '/v1/shell/order/order_query': self.order_query,  # 支付订单查询
            '/v1/shell/game/game_data': self.game_data,         # 游戏数据查询

            '/v1/shell/addcdkey': self.add_cdkey,               # 增加cdkey
            '/v1/shell/alter_cdkey':self.alter_cdkey,           #修改兑换码失效
            '/v1/shell/query_overview': self.query_overview,          # 查询兑换码总览
            '/v1/shell/export_cdkey': self.export_cdkey,        # 导出cdkey
            '/v1/shell/cdkey_exchange_query': self.cdkey_exchange_query,  # 兑换查询
            '/v1/shell/get_version_cdk': self.get_version_cdk,
            '/v1/shell/modify_cdkey': self.modify_cdkey,

            '/v2/shell/query_user_daily_info': self.query_user_daily_info,  # 获取用户的每日信息
            '/v1/shell/get_smart_game_data': self.get_smart_game_data,      # 获取小游戏数据

            '/v2/shell/query_user_data': self.query_user_data,  # 获取玩家数据 db2 user:uid

            '/v2/shell/query_match_data': self.query_match_single_data,  # 获取竞技场单场数据
            '/v2/shell/query_match_all_data': self.query_match_all_data,        # 获取竞技场数据

            '/v2/shell/get_1004_1/transferred': self.change_1004_1_packet, #转1004_1包
            '/v2/shell/getVerifyCode': self.getphoneVerifyCode,  # 获取手机验证码
            '/v2/shell/gm_reset_password': self.reset_player_password,  # 修改玩家密码
            '/v2/shell/gm/player/query_data': self.query_player_data,   #玩家兑换查询
            '/v2/shell/gm/player/unlock': self.unlock_player_info,       #玩家兑换解锁
            '/v2/shell/gm/query/player_days_period': self.player_days_period_data,  # 玩家每日的期间数据
            '/v2/shell/gm/calc/out_coupon_rate': self.calc_coupon_rate,        #计算出券率
            #'/v2/shell/gm/fix_daily_data': self.fix_daily_data_his_total_pay,  #修复旧的每日数据
            '/v2/shell/query_statistic_data': self.query_statistic_data,    # 查询统计数据（每小时的在线人数和付费人数）
            '/v2/shell/burying_point_data': self.burying_point_data,  # 查询埋点数据
            '/v2/shell/gm/redis/get_server_data': self.get_server_redis_data,  # 获取Redis数据

            '/v2/shell/gm/checkcoin': self.checkcoin,       # 金币查询
        }

    def checkcoin(self, gid, mi, request):
        # 总充值额度
        total_pay_total = 0
        # 总打鸟掉落话费券
        total_coupon_fall_hit = 0
        # 总打鸟掉落靶场券
        total_target_fall_hit = 0
        # 总拥有话费券
        total_own_coupon = 0
        # 总拥有靶场券
        total_own_target = 0
        # 总兑换消耗
        total_coupon_exchange_out = 0
        # 总虚拟兑换消耗

        # 总拥有鸟蛋
        total_own_chip = 0
        # 总充值鸟蛋
        total_pay_chip = 0
        # 总产出鸟蛋
        total_in_chip = 0
        # 总拥有钻石
        total_own_diamond = 0
        # 总池子额度
        total_coin_pool = 0
        # 总池子盈利
        total_coin_profit = 0
        # 总池子初始额度
        total_coin_pool_init = 0


        ret = Context.RedisCluster.hget_keys('game:2:*')
        for game in ret:
            uid = int(game.split(':')[2])
            if uid <= 1000000:
                continue

            # 总充值额度
            pay_total = Context.Data.get_game_attr_int(uid, gid, 'pay_total', 0)
            total_pay_total += pay_total
            # 总打鸟掉落话费券
            total_coupon_fall_hit += Tool.to_int(
                Context.RedisStat.hash_get('user:2:%d' % uid, 'in.coupon.coupon_pool.hit.bird', 0))
            # 总打鸟掉落靶券
            total_target_fall_hit += Tool.to_int(
                Context.RedisStat.hash_get('user:2:%d' % uid, 'in.target_coupon.coupon_pool.coupon.bird.fall', 0))
            # 总拥有话费券
            total_own_coupon += Context.Data.get_game_attr_int(uid, gid, 'coupon', 0)
            # 总拥有靶场券
            total_own_target += Context.Data.get_game_attr_int(uid, gid, 'target_coupon', 0)
            # 总兑出消耗话费券
            total_coupon_exchange_out += Tool.to_int(
                Context.RedisStat.hash_get('user:2:%d' % uid, 'out.coupon.limit.shop.buy', 0))
            # 总拥有鸟蛋
            total_own_chip += Context.Data.get_game_attr_int(uid, gid, 'chip', 0)
            # 总充值金币
            total_pay_chip += Tool.to_int(Context.RedisStat.hash_get('user:2:%d' % uid, 'in.chip.buy.product', 0))
            total_pay_chip += Tool.to_int(
                Context.RedisStat.hash_get('user:2:%d' % uid, 'in.chip.month.card.reward', 0))
            total_pay_chip += Tool.to_int(
                Context.RedisStat.hash_get('user:2:%d' % uid, 'in.chip.new.month.card102003', 0))
            total_pay_chip += Tool.to_int(
                Context.RedisStat.hash_get('user:2:%d' % uid, 'in.chip.new.month.card102001', 0))
            # 总产出鸟蛋
            kvs = Context.RedisStat.hash_getall('user:2:%d' % uid)
            for k, v in kvs.iteritems():
                if k.startswith('in.chip.') and '.catch.bird.' not in k:
                    total_in_chip += Tool.to_int(v, 0)
            # 总拥有钻石
            total_own_diamond += Context.Data.get_game_attr_int(uid, gid, 'diamond', 0)


        relax_list = Context.RedisCache.hget_keys('relax_table:2:*')
        for room in relax_list:
            room_id = room.split(':')[2]
            room_type = Context.RedisCache.hash_get('relax_table:2:{}'.format(room_id), 'room_type', 0)
            room_type = Tool.to_int(room_type)
            if room_type in [200, 201, 202, 203, 209]:
                table_pool = Context.RedisCache.hash_get('relax_table:2:{}'.format(room_id), 'table_pool', 0)
                # Context.Log.debug('table', room_id, table_pool)
                total_coin_pool += Tool.to_int(table_pool)
                table_profit = Context.RedisCache.hash_get('relax_table:2:{}'.format(room_id), 'table_profit', 0)
                total_coin_profit += Tool.to_int(table_profit)
                if room_type == 200:
                    total_coin_pool_init += 30*1250
                    Context.Log.debug('200', table_pool,  30*1250)
                elif room_type == 201:
                    total_coin_pool_init += 250*1250
                    Context.Log.debug('201', table_pool, 250*1250)
                elif room_type == 202:
                    total_coin_pool_init += 1500*1250
                    Context.Log.debug('202', table_pool, 1500*1250)
                elif room_type == 203:
                    total_coin_pool_init += 10000*1250
                    Context.Log.debug('203', table_pool, 10000*1250)
                elif room_type == 209:
                    total_coin_pool_init += 10000*1250
                    Context.Log.debug('209', table_pool, 10000*1250)


        Context.Log.debug('总充值额度', total_pay_total)
        Context.Log.debug('总打鸟掉落话费券', total_coupon_fall_hit)
        Context.Log.debug('总打鸟掉落靶场券', total_target_fall_hit)
        Context.Log.debug('总拥有话费券', total_own_coupon)
        Context.Log.debug('总拥有靶场券', total_own_target)
        Context.Log.debug('总兑换消耗', total_coupon_exchange_out)
        Context.Log.debug('总虚拟兑换消耗', 0)
        Context.Log.debug('总拥有鸟蛋', total_own_chip)
        Context.Log.debug('总充值鸟蛋', total_pay_chip)
        Context.Log.debug('总产出鸟蛋', total_in_chip)
        Context.Log.debug('总拥有钻石', total_own_diamond)
        Context.Log.debug('总池子额度', total_coin_pool)
        Context.Log.debug('总池子盈利', total_coin_profit)
        Context.Log.debug('总池子初始额度', total_coin_pool_init)

    def burying_point_data(self, gid, mi, request):
        pid = mi.get_param('pid')
        if pid == 1:
            mo = self.query_burying_point_data()
        elif pid == 2:
            mo = self.delete_burying_point_data(gid, mi)
        else:
            return MsgPack.Error(0, 1, 'not exist pid')
        return mo

    def query_burying_point_data(self):
        k = 'burying_point:*'
        keys = Context.RedisStat.hget_keys(k)
        info = {}
        for i in keys:
            spl = i.split(':')
            uid = spl[1]
            key = spl[2]
            dat = Context.RedisStat.list_range(i)
            if not info.has_key(uid):
                info[uid] = {}
                createTime = str(Context.Data.get_attr(int(uid), "createTime"))[:19]
                info[uid]['createTime'] = createTime
            info[uid][key] = dat
        mo = MsgPack(0)
        mo.set_param('ret', info)
        return mo

    def delete_burying_point_data(self, gid, mi):
        user_list = mi.get_param('ul')
        for i in user_list:
            uid = int(i)
            barrel_level = Context.Data.get_game_attr_int(uid, gid, 'barrel_level', 1)
            if barrel_level >= 14:
                return
            k = 'burying_point:%d:*'%i
            keys = Context.RedisStat.hget_keys(k)
            for j in keys:
                Context.RedisStat.delete(j)
        mo = MsgPack(0)
        return mo

    def query_statistic_data(self, gid, mi, request):
        start = str(mi.get_param('start'))
        end = str(mi.get_param('end'))
        start_day = Time.str_to_datetime(start,'%Y-%m-%d')
        end_day = Time.str_to_datetime(end,'%Y-%m-%d')

        channel_id = mi.get_param('c')
        if channel_id == None:
            channel_dict = Context.Configure.get_game_item_json(gid, 'channel.path.config')
            channel_list = []
            for k,v in channel_dict.items():
                if len(k) == 6:
                    channel_list.append(k)
        else:
            channel_list = [channel_id]
        info = {}
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            day_data = {}
            for i in channel_list:
                k = 'statistics:%s:%s:'%(i, fmt)
                keys = Context.RedisStat.hget_keys('%s*'%k)
                if not keys or len(keys) <= 0:
                    continue
                channel_data = {}
                for j in keys:
                    ks = j.split(k)[1]
                    ret = Context.RedisStat.hash_getall(j)
                    channel_data[ks] = ret
                day_data[i] = channel_data
            info[fmt] = day_data
            start_day = Time.next_days(start_day)
        mo = MsgPack(0)
        mo.set_param('ret', info)
        return mo

    # 获取今日剩余鸟蛋， 时间设置为明天
    def get_now_own_chip(self, uid, cur_day_dt):
        channel_id = Context.Data.get_attr(int(uid), 'channelid', '1001_0')

        today_day = Time.datetime()
        next_day = Time.next_days(cur_day_dt)
        while next_day <= today_day:
            next_day_ftm = Time.datetime_to_str(next_day, '%Y-%m-%d')
            key = 'user_daily:%s:%s:%s' % (channel_id, next_day_ftm, str(uid))
            daily_data = Context.RedisStat.hash_getall(key)

            #if 'fix_last_own_chip' in daily_data:
            #    return daily_data['fix_last_own_chip']

            if 'fix_own_chip' in daily_data:
                all_in_chip = 0
                all_out_chip = 0
                for k,v in daily_data.items():
                    if k.startswith('in.chip.'):
                        all_in_chip += int(v)
                    elif k.startswith('out.chip'):
                        all_out_chip += int(v)

                return Tool.to_int(daily_data['fix_own_chip'], 0) + all_out_chip - all_in_chip

            next_day = Time.next_days(next_day)

        return Tool.to_int(Context.RedisCluster.hash_get(uid, 'game:2:%s' %uid, 'chip'), 0)

    def fix_daily_own_chip(self, gid, mi, request):

        start_day = Time.str_to_datetime('2019-05-11', '%Y-%m-%d')
        end_day = Time.str_to_datetime('2018-12-01', '%Y-%m-%d')

        while start_day >= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            key = 'user_daily:*:%s:*' % fmt
            daily_keys = Context.RedisStat.hget_keys(key)

            for key in daily_keys:
                daily_data = Context.RedisStat.hash_getall(key)
                Context.Log.debug('key', key)
                if True: #'fix_own_chip' not in daily_data:
                    now_own_chip = self.get_now_own_chip(key.split(':')[3], start_day)

                    Context.RedisStat.hash_set(key, 'fix_own_chip', now_own_chip)
                    Context.Log.debug('now_own_chip', now_own_chip)
                if True: #'fix_last_own_chip' not in daily_data:
                    last_day = Time.next_days(start_day, -1)
                    last_own_chip = self.get_now_own_chip(key.split(':')[3], last_day)
                    Context.RedisStat.hash_set(key, 'fix_last_own_chip', last_own_chip)
                    Context.Log.debug('fix_last_own_chip', last_own_chip)

            start_day = Time.next_days(start_day, -1)
        Context.Log.debug('fix_daily_own_chip suc')

    # 获取当天的历史充值总额度
    def get_his_pay_total(self, uid, day_time):
        data = Context.RedisStat.list_range('order:2:%s:user' % uid, 0, -1)
        his_pay_total = 0
        for orderid in data:
            order_info = Context.RedisPay.hash_getall('order:' + orderid)
            Context.Log.debug('order_info', order_info)
            if order_info['createTime'][:10] <= day_time:  # 创建时间等于当前查询时间
                if str(order_info['state']) == '6':
                    his_pay_total += int(float(order_info['cost']))
            else:
                break
        return his_pay_total

    # 修复旧的每日数据
    def fix_daily_data_his_total_pay(self, gid, mi, request):
        all_keys = Context.RedisStat.hget_keys('user_daily:*')
        for daily_key in all_keys:
        # daily_key = 'user_daily:1004_0:2019-05-07:1050774'
            daily_data = Context.RedisStat.hash_getall(daily_key)
            if len(daily_data) > 0:
                data_arr = daily_key.split(':')
                uid = data_arr[3]
                day_time = data_arr[2]
                his_pay_total = self.get_his_pay_total(uid, day_time)
                Context.RedisStat.hash_set(daily_key, 'his_pay_total', his_pay_total)


    def unlock_player_info(self, gid, mi, request):
        # tf add record
        Context.Log.debug("gm_unlock_player_info:", mi)
        Context.Record.add_record_unlock_player_info(mi)
        uid = int(mi.get_param('userId'))
        if not Context.UserAttr.check_exist(uid, gid):
            return MsgPack.Error(0, 1, 'uid not exist')
        mo = MsgPack()
        Context.Data.set_attr(uid, 'pay_channel_flag', "normal")
        mo.set_param('ret', 1)
        return mo

    def query_player_data(self, gid, mi, request):
        # tf add record
        Context.Log.debug("gm_query_player_data:", mi)
        Context.Record.add_record_query_player_data(mi)
        uid = int(mi.get_param('userId'))
        if not Context.UserAttr.check_exist(uid, gid):
            return MsgPack.Error(0, 1, 'uid not exist')

        mo = MsgPack()
        # 虚拟兑换消耗
        virtual_coupon = 0  # 兑换虚拟道具
        data = Context.Data.get_shop_all(uid, 'shop:order')
        for k, v in data.items():
            record_json = Context.json_loads(v)
            if int(record_json["good_type"]) == 3:
                virtual_coupon += int(record_json["price"])

        user_list = ['channelid','nick','idType','userName','pay_channel_flag']
        user_info = Context.Data.get_attrs_dict(uid, user_list)
        game_list = ['pay_total', 'coupon', 'in_coupon']
        user_data = Context.Data.get_game_attrs_dict(uid, gid, game_list)

        user_data.update(user_info)
        user_data['in_kind_coupon'] = int(user_data.get('in_coupon', 0)) - virtual_coupon - int(user_data.get('coupon', 0))

        phone = Context.Data.get_shop_attr(uid, 'shop:user', 'phone')
        if not phone:
            user_data['shop_phone'] = 0
        else:
            user_data['shop_phone'] = phone

        pay_channel = str(user_data.get('pay_channel_flag', 0))
        if pay_channel == "forbit":
            user_data['pay_channel'] = 1
        else:
            user_data['pay_channel'] = 0

        idType = int(user_data.get('idType', 0))
        if idType == 13:
            user_data['mobile'] = user_data['userName']
        else:
            user_data['mobile'] = 0

        mo.set_param('ret', user_data)
        return mo


    def reset_player_password(self, gid, mi, request):
        # tf add record
        Context.Log.debug("gm_reset_player_password:", mi)
        Context.Record.add_record_reset_player_password(mi)
        uid = mi.get_param('userId')
        if not Context.UserAttr.check_exist(int(uid), gid):
            return MsgPack.Error(0, 1, 'uid not exist')

        user_list = ['idType', 'userName', 'channelid']
        user_info = Context.Data.get_attrs_dict(int(uid), user_list)

        idType = int(user_info.get('idType', 0))
        if idType == 13:
            mobile = user_info['userName']
            mi.set_param('mobile', mobile)
        else:
            return MsgPack.Error(0, 2, 'mobile not exist')
        channelid = user_info["channelid"],
        mi.set_param('channelid', channelid)
        ts = mi.get_param('ts', 0)
        s = 'gameId=%d&token=%s&ts=%d' % (gid, self.cdkey_access_key, ts)
        sign = Algorithm.md5_encode(s)
        mi.set_param('sign', sign)

        url = Context.Global.http_sdk() + "/v2/gm/player/ResetPassword"
        return Context.WebPage.wait_for_page(url, postdata=mi.pack())

    def query_match_single_data(self, gid, mi, request):
        start = str(mi.get_param('start'))
        end = str(mi.get_param('end'))
        t = mi.get_param('type')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        keys = 'match_table_data'
        if t != 1:
            return MsgPack.Error(0, 3, 'not type')
        mo = MsgPack()
        group = [1,2,3]
        info = []
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            for i in group:
                ks = '%s:%d:%s' % (keys, i, fmt)
                ret = Context.RedisStat.hash_getall(ks)
                for k, v in ret.items():
                    times = int(k) / 1000
                    d = {}
                    d['md'] = v
                    d['ts'] = times
                    d['type'] = t
                    d['g'] = i
                    info.append(d)
            start_day = Time.next_days(start_day)
        mo.set_param('info', info)
        return mo


    def get_smart_game_data(self, gid, mi, request):
        start = str(mi.get_param('start'))
        end = str(mi.get_param('end'))
        t = mi.get_param('type')
        uid = mi.get_param('uid')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        mo = MsgPack(0)
        if t == 1:
            keys = 'fanfanle'
            info = self.get_game_info(start_day, end_day, uid, keys)
        elif t == 2:
            keys = 'target'
            info = self.get_game_info(start_day, end_day, uid, keys)
        elif t == 3:
            keys = 'rich_man'
            info = self.get_game_info(start_day, end_day, uid, keys)
        else:
            info = self.get_third_game(start_day, end_day, uid)

        mo.set_param('info', info)
        return mo

    def get_game_info(self,start_day, end_day, uid, keys):
        info = []
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            if uid == None:
                keys_list = Context.RedisStat.hget_keys("{}:{}:*".format(keys,fmt))
                for day_user in keys_list:
                    ret = Context.RedisStat.hash_getall(day_user)
                    user_id = day_user.split(':')[2]
                    channel_id = Context.Data.get_attr(int(user_id), 'channelid')
                    nick = Context.Data.get_attr(int(user_id), 'nick')
                    for key, value in ret.items():
                        mini_info = {}
                        times = int(key) / 1000
                        mini_info.update(Context.json_loads(value))
                        mini_info.update({"uid":user_id,"nick":nick,"cid":channel_id,"unique_id":key,"time":times})
                        info.append(mini_info)
            else:
                keys = "{}:{}:{}".format(keys, fmt, uid)
                ret = Context.RedisStat.hash_getall(keys)
                channel_id = Context.Data.get_attr(int(uid), 'channelid')
                nick = Context.Data.get_attr(int(uid), 'nick')
                for key, value in ret.items():
                    mini_info = {}
                    times = int(key) / 1000
                    mini_info.update(Context.json_loads(value))
                    mini_info.update({"uid": uid, "nick": nick, "cid": channel_id, "unique_id": key, "time": times})
                    info.append(mini_info)
            start_day = Time.next_days(start_day)
        return info

    def get_third_game(self, start_day, end_day, uid):
        Tichu_info = []
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            if uid == None:
                user_info = Context.RedisCache.hget_keys("third_game:ddz:{}:*".format(fmt))
                for info in user_info:
                    user_list = Context.RedisCache.hash_getall(info)
                    user_id = info.split("third_game:ddz:{}:".format(fmt))[1]
                    channel_id = Context.Data.get_attr(int(user_id), 'channelid')
                    nick = Context.Data.get_attr(int(user_id), 'nick')
                    for k, v in user_list.items():
                        data = Context.json_loads(v)
                        data['unique_id'] = k
                        data['uid'] = user_id
                        data['cid'] = channel_id
                        data['nick'] = nick
                        Tichu_info.append(data)
            else:
                keys = "third_game:ddz:{}:{}".format(fmt,uid)
                user_list = Context.RedisCache.hash_getall(keys)
                channel_id = Context.Data.get_attr(int(uid), 'channelid')
                nick = Context.Data.get_attr(int(uid), 'nick')
                for k, v in user_list.items():
                    data = Context.json_loads(v)
                    data['unique_id'] = k
                    data['uid'] = uid
                    data['cid'] = channel_id
                    data['nick'] = nick
                    Tichu_info.append(data)
            start_day = Time.next_days(start_day)
        return Tichu_info

    def alter_cdkey(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_alter_cdkey:", mi)
        Context.Record.add_record_gm_alter_cdkey(mi)

        ts = mi.get_param('ts', 0)
        s = 'gameId=%d&token=%s&ts=%d' % (gid, self.cdkey_access_key, ts)
        sign = Algorithm.md5_encode(s)
        mi.set_param('sign', sign)

        url = Context.Global.http_cdkey() + "/v1/cdkey/alter_cdkey"
        return Context.WebPage.wait_for_page(url, postdata=mi.pack())


    def add_cdkey(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_add_cdkey:", mi)
        Context.Record.add_record_gm_add_cdkey(mi)

        ts = mi.get_param('ts', 0)
        s = 'gameId=%d&token=%s&ts=%d' % (gid, self.cdkey_access_key, ts)
        sign = Algorithm.md5_encode(s)
        mi.set_param('sign', sign)

        url = Context.Global.http_cdkey() + "/v1/cdkey/addsdkey"
        return Context.WebPage.wait_for_page(url, postdata=mi.pack())

    def query_overview(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_cdkey_query_overview:", mi)
        Context.Record.add_record_gm_add_cdkey(mi)

        ts = mi.get_param('ts', 0)
        s = 'gameId=%d&token=%s&ts=%d' % (gid, self.cdkey_access_key, ts)
        sign = Algorithm.md5_encode(s)
        mi.set_param('sign', sign)

        url = Context.Global.http_cdkey() + "/v1/cdkey/queryoverview"
        return Context.WebPage.wait_for_page(url, postdata=mi.pack())

    def export_cdkey(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_export_cdkey:", mi)
        Context.Record.add_record_gm_export_cdkey(mi)

        # 需要用到时需要处理
        ts = mi.get_param('ts', 0)
        s = 'gameId=%d&token=%s&ts=%d' % (gid, self.cdkey_access_key, ts)
        sign = Algorithm.md5_encode(s)
        mi.set_param('sign', sign)

        url = Context.Global.http_cdkey() + "/v1/cdkey/export"
        return Context.WebPage.wait_for_page(url, postdata=mi.pack())

    def cdkey_exchange_query(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_cdkey_exchange_query:", mi)
        Context.Record.add_record_gm_cdkey_exchange_query(mi)

        ts = mi.get_param('ts', 0)
        s = 'gameId=%d&token=%s&ts=%d' % (gid, self.cdkey_access_key, ts)
        sign = Algorithm.md5_encode(s)
        mi.set_param('sign', sign)

        url = Context.Global.http_cdkey() + "/v1/cdkey/exchange_query"
        return Context.WebPage.wait_for_page(url, postdata=mi.pack())

    def get_version_cdk(self, gid, mi, request):
        # dz add record
        # Context.Log.debug("gm_cdkey_exchange_query:", mi)
        # Context.Record.add_record_gm_cdkey_exchange_query(mi)

        ts = mi.get_param('ts', 0)
        s = 'gameId=%d&token=%s&ts=%d' % (gid, self.cdkey_access_key, ts)
        sign = Algorithm.md5_encode(s)
        mi.set_param('sign', sign)

        url = Context.Global.http_cdkey() + "/v1/cdkey/get_version_cdk"
        return Context.WebPage.wait_for_page(url, postdata=mi.pack())

    def modify_cdkey(self, gid, mi, request):
        # dz add record
        # Context.Log.debug("gm_cdkey_exchange_query:", mi)
        # Context.Record.add_record_gm_cdkey_exchange_query(mi)

        ts = mi.get_param('ts', 0)
        s = 'gameId=%d&token=%s&ts=%d' % (gid, self.cdkey_access_key, ts)
        sign = Algorithm.md5_encode(s)
        mi.set_param('sign', sign)

        url = Context.Global.http_cdkey() + "/v1/cdkey/modify_cdkey"
        return Context.WebPage.wait_for_page(url, postdata=mi.pack())

    def getphoneVerifyCode(self, gid, mi, request):
        # tf add record
        ts = mi.get_param('ts', 0)
        s = 'gameId=%d&token=%s&ts=%d' % (gid, self.cdkey_access_key, ts)
        sign = Algorithm.md5_encode(s)
        mi.set_param('sign', sign)

        url = Context.Global.http_sdk() + "/v2/transferred/getVerifyCode"
        return Context.WebPage.wait_for_page(url, postdata=mi.pack())

    def change_1004_1_packet(self, gid, mi, request):
        # tf add record
        ts = mi.get_param('ts', 0)
        s = 'gameId=%d&token=%s&ts=%d' % (gid, self.cdkey_access_key, ts)
        sign = Algorithm.md5_encode(s)
        mi.set_param('sign', sign)

        url = Context.Global.http_sdk() + "/v2/user/transferred"
        return Context.WebPage.wait_for_page(url, postdata=mi.pack())

    def str_order(self, gid, mi, request):
        param_id = mi.get_param('order')
        ret = eval(param_id)
        mo = MsgPack(0)
        if type(ret) in [dict, list, tuple]:
            ret = Context.json_dumps(ret)
        mo.set_param('ret', ret)
        return mo

    def get_player_pay_info(self, day_time, uid):
        data = Context.RedisStat.list_range('order:2:%s:user' % uid, 0, -1)
        pay_third = 0
        pay_gm = 0
        for orderid in data:
            order_info = Context.RedisPay.hash_getall('order:' + orderid)
            Context.Log.debug('order_info', order_info)
            if order_info['createTime'][:10] == day_time:  # 创建时间等于当前查询时间
                if str(order_info['state']) == '6':
                    if str(order_info.get('paytype', 0)) == '3':
                        pay_third += int(order_info['cost'])
                    elif str(order_info.get('paytype', '0')) == '0' and order_info['platform'] == 'gm':
                        pay_gm += int(order_info['cost'])

        return pay_third, pay_gm

    def fix_pay_data(self):
        ret = Context.RedisStat.hget_keys('user_daily:*')
        if not ret:
            Context.Log.debug('error fix_pay_data')
            return 0

        for item in ret:
            user_data_daily = Context.RedisStat.hash_getall(item)
            cur_time = item.split(':')[2]
            uid = item.split(':')[3]
            if '1004_0.pay.user.pay_total' in user_data_daily :
                pay_third, pay_gm = self.get_player_pay_info(cur_time, uid)

                old_gm_pay = Context.RedisStat.hash_get(item, '1004_0.gm_pay.user.pay_total', 0)
                gm_pay_space = pay_gm - int(old_gm_pay)
                if gm_pay_space != 0:
                    Context.RedisStat.hash_incrby(item, '1004_0.gm_pay.user.pay_total', gm_pay_space)  # 玩家当天数据
                    Context.RedisStat.hash_incrby('user:2:%s' % uid, '1004_0.gm_pay.user.pay_total', gm_pay_space)   # 玩家总数据
                    Context.RedisStat.hash_incrby('stat:1004_0:%s' % cur_time, '1004_0.gm_pay.user.pay_total', gm_pay_space)   # 渠道数据

                old_pay_third = Context.RedisStat.hash_get(item, '1004_0.sdk_pay.user.pay_total', 0)
                third_pay_space = pay_third - int(old_pay_third)
                if third_pay_space != 0:
                    Context.RedisStat.hash_incrby(item, '1004_0.sdk_pay.user.pay_total', third_pay_space)   # 玩家当天数据
                    Context.RedisStat.hash_incrby(item, '1004_0.sdk_pay.user.pay_total', third_pay_space)   # 玩家当天数据
                    Context.RedisStat.hash_incrby('user:2:%s' % uid, '1004_0.sdk_pay.user.pay_total', third_pay_space)  # 玩家总数据
                    Context.RedisStat.hash_incrby('stat:1004_0:%s' % cur_time, '1004_0.sdk_pay.user.pay_total', third_pay_space)  # 渠道数据
            elif '1005_0.pay.user.pay_total' in user_data_daily:
                pay_third, pay_gm = self.get_player_pay_info(cur_time, uid)

                old_gm_pay = Context.RedisStat.hash_get(item, '1005_0.gm_pay.user.pay_total', 0)
                gm_pay_space = pay_gm - int(old_gm_pay)
                if gm_pay_space != 0:
                    Context.RedisStat.hash_incrby(item, '1005_0.gm_pay.user.pay_total', gm_pay_space)  # 玩家当天数据
                    Context.RedisStat.hash_incrby('user:2:%s' % uid, '1005_0.gm_pay.user.pay_total', gm_pay_space)  # 玩家总数据
                    Context.RedisStat.hash_incrby('stat:1005_0:%s' % cur_time, '1005_0.gm_pay.user.pay_total', gm_pay_space)  # 渠道数据

                old_pay_third = Context.RedisStat.hash_get(item, '1005_0.sdk_pay.user.pay_total', 0)
                third_pay_space = pay_third - int(old_pay_third)
                if third_pay_space != 0:
                    Context.RedisStat.hash_incrby(item, '1005_0.sdk_pay.user.pay_total', third_pay_space)  # 玩家当天数据
                    Context.RedisStat.hash_incrby('user:2:%s' % uid, '1005_0.sdk_pay.user.pay_total', third_pay_space)  # 玩家总数据
                    Context.RedisStat.hash_incrby('stat:1005_0:%s' % cur_time, '1005_0.sdk_pay.user.pay_total', third_pay_space)  # 渠道数据

        Context.Log.debug('修复完成')



    def order_query(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_order_query:", mi)
        Context.Record.add_record_order_query(mi)

        start = mi.get_param('start_time')
        end = mi.get_param('end_time')
        order_list = []
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        while start_day <= end_day:
            user_info = {}
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            order_info = self.get_daily_order_info(fmt)
            for i in order_info:
                user_pay_total = 0
                data = Context.RedisPay.hash_getall('order:' + i)
                if data["createTime"][:10] == fmt:
                    uid = int(data["userId"])
                    channel_id = Context.Data.get_attr(uid, 'channelid')
                    nick = Context.Data.get_attr(uid, 'nick')
                    user_day = Context.RedisStat.hash_getall('user_daily:%s:%s:%s' % (channel_id, fmt, str(uid)))
                    for k, v in user_day.items():
                        # 获取当天充值额度
                        if k.startswith(str(channel_id) + '.pay.user.pay_total'):
                            user_pay_total = int(v)
                    pay_total, exp = Context.Data.get_game_attrs(uid, gid, ['pay_total', 'exp'])
                    if pay_total:
                        pay_total = pay_total
                    else:
                        pay_total = 0
                    user_info.update({"nick": nick,"channelid": channel_id,"pay_total": pay_total, "exp": exp,"day_pay_total":user_pay_total})
                    data.update(user_info)
                    order_list.append({"{}".format(i):data})
                else:
                    continue
            start_day = Time.next_days(start_day)
        mo = MsgPack(0)
        mo.set_param('order', order_list)
        return mo

    def get_daily_order_info(self, fmt):
        data = Context.RedisStat.list_range('order:2:%s:daily' % fmt, 0, -1)
        return data

    def test(self, gid, mi, request):#红包测试接口
        uid = mi.get_param('uid')
        kvs = BirdEntity.on_product_deliver(uid, 2, mi)
        return kvs

    def query_shop_info(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_query_shop_info:", mi)
        Context.Record.add_record_query_shop_info(mi)

        mo = MsgPack(0)
        info =[]
        ntype = mi.get_param('ntype')
        channel_id = mi.get_param('cid')
        if int(ntype) == 1:
            limit_config = Context.Configure.get_game_item_json(gid, 'limit.shop.config')
            if not limit_config.has_key(channel_id):
                channel_id = '1001_0'
            shop_config = limit_config.get(channel_id, None)
        else:
            shop_config = Context.Configure.get_game_item_json(gid, 'exchange.config')
        if not shop_config:
            return MsgPack.Error(0, 2, 'not config')
        sort = 1
        update = Context.RedisConfig.hash_get_int('configitem', 'update.time')
        if not update:
            return MsgPack.Error(0, 3, 'not update time')
        update_time = Time.timestamp_to_str(update)
        limit_shop_status = Context.RedisMix.get('limit.shop.open')
        if limit_shop_status == None:
            limit_shop_status = 0
        for k,v in shop_config.items():
            limit =[]
            for i in v[6]:
                if int(i['type']) == 1:
                    continue
                limit.append({'buy_limit':int(i['type']), 'limit_num': int(i['num'])})
            prop = {
                'id': int(k), #商品id
                'sort': sort, #排序
                'name': str(v[0]), #商品名称
                'goods_type': Tool.to_int(v[1], 1), #1数码设备、2充值卡、3虚拟道具
                'goods': BirdProps.convert_reward(v[2]), #道具
                'buy_type': int(v[3]), #货币类型（1、鸟蛋，2、钻石，3、RMB、4非币种解锁，需VIP等级解锁，5、鸟卷）
                'price': int(v[4]), #价格
                'vip_limit': int(v[5]), #购买限制（vip）
                'limit': limit, #限购类型，1日个人限购，2日全服限购
                'desc': str(v[7]), #道具说明
                'update_time': update_time,
                'line':int(v[8]),  #0上线 1下线
            }
            info.append(prop)
            sort = sort + 1
        mo.set_param('shop_config', info)
        channel_list = Context.Configure.get_game_item_json(gid, 'channel.path.config', {})
        mo.set_param('clist', channel_list)
        mo.set_param('shop_status', limit_shop_status)
        return mo


    def shipping_info(self, gid, mi, request): #发货信息
        # dz add record
        Context.Log.debug("gm_shipping_info:", mi)
        Context.Record.add_record_shipping_info(mi)

        order_id = mi.get_param('order_id')
        uid = int(mi.get_param('uid'))
        if order_id!=None:
            order = Context.Data.get_shop_attr(uid, 'shop:order', order_id)
            order_status = Context.json_loads(order)
            info = Context.Data.get_shop_all(uid, 'shop:user')
            info.update(order_status)
        else:
            info = Context.Data.get_shop_all(uid, 'shop:user')
        mo = MsgPack(0)
        mo.set_param('info', info)
        return mo

    def shipping_state(self, gid, mi, request): #发货状态
        # dz add record
        Context.Log.debug("gm_shipping_state:", mi)
        Context.Record.add_record_shipping_state(mi)

        order_id = str(mi.get_param('order_id'))
        order_info = mi.get_param('order_info')
        uid = int(mi.get_param('uid'))

        order = Context.Data.get_shop_attr(uid, 'shop:order', order_id)
        order_state = Context.json_loads(order)
        order_state['stat'] = 2
        order_state['end_time'] = Time.current_ts()
        # order_state['order_number'] = order_info
        order_state.update({'order_number':order_info })
        Context.Data.set_shop_attr(uid, 'shop:order', order_id, Context.json_dumps(order_state))
        return MsgPack(0)

    def gm_pay(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_pay:", mi)
        Context.Record.add_record_pay(mi)

        # 模拟充值
        userId = mi.get_param('userId')
        if not Context.UserAttr.check_exist(userId, gid):
            return MsgPack.Error(0, 1, 'not exist')
        productId = mi.get_param('productId')
        if not Context.UserAttr.check_exist(userId, gid):
            return MsgPack.Error(0, 7, 'id error')
        res = Order.otherCreateOrder(gid, userId, str(productId), 'gm', 'gm')
        if res.is_error():
            return MsgPack.Error(0, 8, 'order create fail')
        orderId = res.get_param('orderId')
        return self.drop_order(orderId)

    def fix_order(self, gid, mi, request):
        orderId = mi.get_param('order_id')
        return self.drop_order(orderId)

    def drop_order(self, orderId):
        Context.Log.debug('fix_order=========', orderId)
        if not orderId:
            return MsgPack.Error(0, 1, 'id error')
        parseInfo = Order.parse_order(orderId)
        if not parseInfo:
            return MsgPack.Error(0, 2, 'id error')
        orderInfo = Order.getOrderInfo(orderId)
        Context.Log.debug('orderInfo-----', orderInfo)
        if not orderInfo:
            return MsgPack.Error(0, 3, 'id error')

        state = int(orderInfo['state'])
        if state >= Order.state_pre_deliver:  # 可能并没有成功, 需要检查对单
            return MsgPack.Error(0, 4, 'id error')

        userId = int(orderInfo['userId'])
        gameId = int(orderInfo['gameId'])
        productId = orderInfo['productId']

        all_product = Context.Configure.get_game_item_json(gameId, 'product.config')
        gift_config = Context.RedisActivity.get('gift_shop:product_config')
        if gift_config:
            gift_config = Context.json_loads(gift_config)
        else:
            gift_config = {}
        if productId not in all_product and productId not in gift_config:
            return MsgPack.Error(0, 5, 'id error')

        Order.updateOrder(orderId, state=Order.state_pre_deliver)
        kvs = {
            'payTime': Time.current_time(),
            'deliverTime': Time.current_time(),
        }
        if Order.deliver_product(userId, gameId, orderId, orderInfo, productId, 'NaN'):
            kvs['state'] = Order.state_deliver_success
        else:
            kvs['state'] = Order.state_deliver_failed

        Order.updateOrder(orderId, **kvs)
        Context.Log.debug('fix_order======== success', orderId)
        return MsgPack(0)

    def alipay_pay_creat_order(self, gid, mi, request):
        # 阿里支付下单
        userId = mi.get_param('userId')
        productId = mi.get_param('productId')
        if not Context.UserAttr.check_exist(userId, gid):
            return MsgPack.Error(0, 7, 'id error')
        return Order.otherCreateOrder(gid, userId, productId, 'alipay', 'weixin')

    def weixin_pay_creat_order(self, gid, mi, request):
        # 微信支付下单
        userId = mi.get_param('userId')
        productId = mi.get_param('productId')
        if not Context.UserAttr.check_exist(userId, gid):
            return MsgPack.Error(0, 7, 'id error')
        return Order.otherCreateOrder(gid, userId, productId, 'weixin', 'weixin')

    def check_token(self, gid, mi):
        sign = mi.get_param('sign')
        ts = mi.get_param('ts')
        gid = mi.get_param('gameId')
        line = 'gameId=%d&token=%s&ts=%d' % (gid, self.token, ts)
        _sign = Algorithm.md5_encode(line)
        if sign != _sign:
            Context.Log.error('verify token key failed', _sign, sign)
            return False
        return True

    def check_special_token(self, gid, mi):
        sign = mi.get_param('sign')
        ts = mi.get_param('ts')
        gid = mi.get_param('gameId')
        line = 'gameId=%d&token=%s&ts=%d' % (gid, self.token_special, ts)
        _sign = Algorithm.md5_encode(line)
        if sign != _sign:
            Context.Log.error('verify token key failed', _sign, sign)
            return False
        return True

    def onMessage(self, request):
        if request.method.lower() == 'post':
            #Context.Log.debug(request)
            data = request.raw_data()
            #Context.Log.debug(data)
            mi = MsgPack.unpack(0, data)
            #Context.Log.debug(mi)
            gid = mi.get_param('gameId')
            if not self.check_token(gid, mi):
                if not self.check_special_token(gid, mi):
                    raise ForbiddenException('no permission access')
                else:
                    channel_id = mi.get_param('channel_id')
                    channel_dict = Context.Configure.get_game_item_json(gid, 'channel.path.config')
                    channel_info = channel_dict.keys()
                    if request.path in self.special_json_path:
                        if channel_id in channel_info:
                            return self.special_json_path[request.path](gid, mi, request)
                    from lemon import classMap
                    if gid in classMap:
                        http = classMap[gid].get('shell')
                        if http and request.path in http.special_json_path and channel_id in channel_info:
                            return http.special_json_path[request.path](gid, mi, request)
            else:
                if request.path in self.json_path:
                    return self.json_path[request.path](gid, mi, request)
                from lemon import classMap
                if gid in classMap:
                    http = classMap[gid].get('shell')
                    if http and request.path in http.json_path:
                        return http.json_path[request.path](gid, mi, request)

        raise NotFoundException('Not Found')

    def disable_user(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_disable_user:", mi)
        Context.Record.add_record_disable(mi)

        uid = mi.get_param('userId')
        if not Context.UserAttr.check_exist(uid, gid):
            return MsgPack.Error(0, 1, 'not exist')
        disable = mi.get_param('disable')
        if disable:
            Context.RedisMix.set_add('game.%d.disable.user' % gid, uid)
        else:
            Context.RedisMix.set_rem('game.%d.disable.user' % gid, uid)
        return MsgPack(0)

    #def gm_reward_chip(self, gid, mi, request):
    #    uid = mi.get_param('userId')
    #    if not Context.UserAttr.check_exist(uid, gid):
    #        return MsgPack.Error(0, 1, 'not exist')
    #    chip = mi.get_param('chip')
    #    real, final = Context.UserAttr.incr_chip(uid, gid, chip, 'gm.reward')
    #    if chip > 0:
    #        NewTask.get_chip_task(uid, chip, 'gm.reward')
    #    if real != chip:
    #        MsgPack.Error(0, 1, 'not enough')
    #    return MsgPack(0, {'chip': final, 'delta': real})

    # def gm_reward_shit(self, gid, mi, request):
    #     uid = mi.get_param('userId')
    #     if not Context.UserAttr.check_exist(uid, gid):
    #         return MsgPack.Error(0, 1, 'not exist')
    #     shit = mi.get_param('shit')
    #     real, final = Context.UserAttr.incr_shit(uid, gid, shit, 'gm.reward')
    #     if real != shit:
    #         MsgPack.Error(0, 1, 'not enough')
    #     return MsgPack(0, {'shit': final, 'delta': real})

    # def gm_reward_chip_pool(self, gid, mi, request):
    #     uid = mi.get_param('userId')
    #     if not Context.UserAttr.check_exist(uid, gid):
    #         return MsgPack.Error(0, 1, 'not exist')
    #     chip_pool = mi.get_param('chip_pool')
    #     real, final = Context.UserAttr.incr_chip_pool(uid, gid, chip_pool, 'gm.reward')
    #     if real != chip_pool:
    #         MsgPack.Error(0, 1, 'not enough')
    #     return MsgPack(0, {'chip_pool': final, 'delta': real})

    def gm_reward_egg_pool(self, gid, mi, request):
        uid = mi.get_param('userId')
        if not Context.UserAttr.check_exist(uid, gid):
            return MsgPack.Error(0, 1, 'not exist')

        buff_info = Context.Data.get_game_attr_json(uid, gid, 'recharge_buff', {})
        info = mi.get_param('info')
        info = Context.json_loads(info)
        for ii, xx in info.items():
            if ii not in ['211', '212', '213', '214']:
                continue
            if ii in buff_info:
                if xx + buff_info[ii] >= 0:
                    buff_info[ii] += xx
            else:
                if xx > 0:
                    buff_info[ii] = xx
        Context.Data.set_game_attr(uid, gid, 'recharge_buff', Context.json_dumps(buff_info))

        return MsgPack(0)

    def gm_query_egg_pool(self, gid, mi, request):
        uid = mi.get_param('userId')
        if not Context.UserAttr.check_exist(uid, gid):
            return MsgPack.Error(0, 1, 'not exist')

        buff_info = Context.Data.get_game_attr_json(uid, gid, 'recharge_buff', {})
        res_info = {}
        for ii, xx in buff_info.items():
            if str(ii) not in res_info:
                res_info[str(ii)] = xx
            else:
                res_info[str(ii)] += xx
        for _id in ['211', '212', '213', '214']:
            if _id not in res_info:
                res_info[_id] = 0
        return MsgPack(0, res_info)

    def gm_reward_diamond(self, gid, mi, request):
        Context.Log.debug('gm_reward_diamond-----')

        uid = mi.get_param('userId')
        if not Context.UserAttr.check_exist(uid, gid):
            return MsgPack.Error(0, 1, 'not exist')
        diamond = mi.get_param('diamond')
        real, final = Context.UserAttr.incr_diamond(uid, gid, diamond, 'gm.reward')
        if diamond > 0:
            NewTask.get_diamond_task(uid, diamond, 'gm.reward')
        if real != diamond:
            MsgPack.Error(0, 1, 'not enough')
        return MsgPack(0, {'diamond': final, 'delta': real})

    def gm_reward_coupon(self, gid, mi, request): #"error":404,"desc":"Not Found"
        uid = mi.get_param('userId')
        if not Context.UserAttr.check_exist(uid, gid):
            return MsgPack.Error(0, 1, 'not exist')

        coupon = mi.get_param('coupon')
        Context.Log.info("tf", mi,coupon)
        real, final = Context.UserAttr.incr_coupon(uid, gid, coupon, 'gm.reward')
        if real != coupon:
            MsgPack.Error(0, 1, 'not enough')
        return MsgPack(0, {'coupon': final, 'delta': real})

    def gm_version_upgrade(self, gid, mi, request):
        Context.Log .report('gm_version_upgrade`')

        # test
        version = '1.2.5.1'
        changelog = 'update to v1.2.5.1'
        size = '60M'
        _bytes = 76688495
        _md5 = '0fddd251ad3f9603c3c5196f6117d80b'
        url = 'https://pro-app-qn.fir.im/24a680a4e7f6675dfaf1af04d08e31de4519688c.apk?attname=BirdMaster_Ximao_1.2.5.1-release-signed.apk_1.2.5.1.apk'
        channel = 'XiMao'
        platform = 'android'
        prompt = '1.2.5.1'
        force = 2

        #end

#
#     version = mi.get_param('version')
#     if not Upgrade.check_version(version):
#         return MsgPack.Error(0, 1, 'version error')
#     changelog = mi.get_param('changelog')
#     if not isinstance(changelog, (str, unicode)) or changelog == '':
#         return MsgPack.Error(0, 2, 'changelog error')
#     size = mi.get_param('size')
#     if not isinstance(size, (str, unicode)) or size == '':
#         return MsgPack.Error(0, 3, 'size error')
#     _bytes = mi.get_param('bytes')
#     if not isinstance(_bytes, int) or _bytes < 0:
#         return MsgPack.Error(0, 4, '_bytes error')
#     _md5 = mi.get_param('md5')
#     if not isinstance(_md5, (str, unicode)) or len(_md5) != 32:
#         return MsgPack.Error(0, 5, 'md5 error')
#     url = mi.get_param('url')
#     if not isinstance(url, (str, unicode)) or url.find('http') == -1:
#         return MsgPack.Error(0, 6, 'url error')
#     channel = mi.get_param('channel')
#     if channel and not isinstance(channel, (str, unicode)):
#         return MsgPack.Error(0, 7, 'channel error')
#     platform = mi.get_param('platform')
#     if platform not in ('android', 'ios'):
#         return MsgPack.Error(0, 8, 'platform error')
#     prompt = mi.get_param('prompt')
#     if prompt and Upgrade.cmp_version(prompt, version) > 0:
#         return MsgPack.Error(0, 9, 'prompt error')
#     force = mi.get_param('force')


        if force and Upgrade.cmp_version(force, version) > 0:
            return MsgPack.Error(0, 10, 'force error')
        if not prompt and not force:
            return MsgPack.Error(0, 11, 'force or prompt must one')

        if not channel:
            channel = 'all'

        info = {
            'version': version,
            'changelog': changelog,
            'size': size,
            'bytes': _bytes,
            'md5': _md5,
            'url': url,
        }
        if prompt:
            info['prompt'] = prompt
        if force:
            info['force'] = force
        key = 'game.%d.version.upgrade' % gid
        field = platform + ':' + channel
        Context.RedisMix.hash_set(key, field, Context.json_dumps(info))
        Context.Log.report('gm_version_upgrade2')
        return MsgPack(0)

    def gm_push_led(self, gid, mi, request):
        msg = mi.get_param('msg')
        if not msg:     # 清除led
            Context.RedisCache.delete('game.%d.led.list' % gid)
        else:
            led = Context.json_dumps({'led': msg, 'ts': Time.current_ts()})
            Context.RedisCache.list_lpush('game.%d.led.list' % gid, led)
        return MsgPack(0)

    def query_summary(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_query_summary:", mi)
        Context.Record.add_record_query_summary(mi)

        # 新增设备, 新增用户, 活跃用户, (新)付费玩家, (新)用户付费, 充值次数
        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        mo = MsgPack(0)
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            kvs = Context.Stat.get_day_data(gid, fmt)
            channel_info = {}
            for k, v in kvs.iteritems():
                if (k.endswith('.new.device.count') or k.endswith('.new.user.count') or
                        k.endswith('.login.user.count') or k.endswith('.new.pay.user.count') or
                        k.endswith('.new.pay.user.pay_total') or k.endswith('.pay.user.count') or
                        k.endswith('.pay.user.pay_total') or k.endswith('.user.pay.times')):
                    channel, key = k.split('.', 1)
                    if channel not in channel_info:
                        channel_info[channel] = {}
                    channel_info[channel][key] = int(v)

            mo.set_param(fmt, channel_info)
            start_day = Time.next_days(start_day)
        return mo

    def query_online(self, gid, mi, request):
        times = mi.get_param('times')
        times_day = Time.str_to_datetime(times, '%Y-%m-%d')
        game_room = Context.GData.map_room_type.get(gid)
        room_types = sorted(game_room.keys())
        mo = MsgPack(0)
        for i in room_types:
            fmt = Time.datetime_to_str(times_day, '%Y-%m-%d')
            kvs = Context.Stat.get_online_data(gid, fmt, i)
            mo.set_param(i, kvs)
        return mo

    def checkDicDic(self, dict, key):
        if not dict.has_key(key):
            dict[key] = {}

    def get_daily_player_info(self, uid, fmt):
        channel_id = Context.Data.get_attr(int(uid), 'channelid', '1001_0')
        result = Context.Stat.get_daily_user_data(channel_id, uid, fmt)
        if len(result) <= 0:
            Context.Log.debug('uid', uid)
            return False, {}

        return True, result

    def get_user_all_pay(self,gid,uid):
        pay_info = {}
        channel_id = Context.Data.get_attr(int(uid), 'channelid', '1001_0')
        user_day = Context.RedisStat.hash_getall('user:%s:%s' % (gid, str(uid)))
        weixin_pay,sdk_pay,ali_pay,cdkey_pay =0,0,0,0
        for key, value in user_day.items():
            # 获取微信充值额度
            if key.startswith('{}.weixin_pay.user.pay_total'.format(channel_id)):
                weixin_pay = int(value)
            # 获取sdk支付
            elif key.startswith('{}.sdk_pay.user.pay_total'.format(channel_id)):
                sdk_pay = int(value)
            # 获取兑换码充值额度
            elif key.startswith('{}.cdkey_pay.user.pay_total'.format(channel_id)):
                cdkey_pay = int(value)
            # 获取支付宝充值额度
            elif key.startswith('{}.ali_pay.user.pay_total'.format(channel_id)):
                ali_pay = int(value)
        pay_info['user_weixin_pay'],pay_info['user_sdk_pay'],pay_info['user_ali_pay'],pay_info['user_cdkey_pay'] = weixin_pay,sdk_pay,ali_pay,cdkey_pay
        return pay_info

    def query_user_data(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_query_user_data:", mi)
        Context.Record.add_record_gm_query_user_daily_info(mi)

        uid = mi.get_param('uid', 0)   # 获取从此uid开始的到结束的所有数据
        mo = MsgPack(0)

        all_user_info = []

        ret = Context.RedisCluster.hget_keys('user:*')
        if not ret:
            return MsgPack.Error(0, 2, 'not exist')
        for item in ret:
            user_id = item.split(':')[1]
            if int(user_id) >= int(uid):

                kvs = Context.Data.get_all(int(user_id))
                if len(kvs) == 0:  # 没有记录
                    return mo

                user_info = {}
                user_info.update({'uid': user_id})
                user_info.update({'data': kvs})
                all_user_info.append(user_info)

        mo.set_param("ret", all_user_info)
        return mo

    def player_days_period_data(self, gid, mi, request):
        Context.Log.debug("gm_query_user_days_period_data:", mi)
        Context.Record.add_record_gm_query_user_period_data(mi)
        period_data = {}
        uid = mi.get_param('uid')
        start_day = Time.str_to_datetime(str(mi.get_param('start')), '%Y-%m-%d')
        end_day = Time.str_to_datetime(str(mi.get_param('end')), '%Y-%m-%d')
        if uid != None:
            # creat_day = Time.str_to_datetime(str(Context.Data.get_attr(int(uid), 'createTime'))[:10],'%Y-%m-%d')
            creat_day = start_day
            while creat_day <= end_day:
                everyday = {}
                days = Time.datetime_to_str(creat_day, '%Y-%m-%d')
                coupon = Context.Data.get_game_attr_int(int(uid), gid, 'coupon', 0)
                channel_id = Context.Data.get_attr(int(uid), 'channelid')
                pay_total = Context.Data.get_game_attr_int(int(uid), gid, 'pay_total', 0)
                all_pay_info = self.get_user_all_pay(gid, uid)
                user_day = Context.RedisStat.hash_getall('user_daily:{}:{}:{}'.format(channel_id, days, uid))
                if len(user_day) > 0:
                    if days == Time.current_time("%Y-%m-%d"):
                        surplus_coupon = coupon
                    else:
                        surplus_coupon = self.calc_coupon(uid, coupon, days)
                    super_weapon = self.get_super_weapon(channelids=channel_id, fmt=days, uid=uid)
                    user_day.update(all_pay_info)
                    user_day.update({'in.chip.super.weapon.fix.new': super_weapon,"surplus_coupon": surplus_coupon, "pay_total": pay_total,"channel":channel_id})
                    everyday[uid] = user_day
                    period_data[days] = everyday
                creat_day = Time.next_days(creat_day)
        else:
            while start_day <= end_day:
                everyday = {}
                days = Time.datetime_to_str(start_day, '%Y-%m-%d')
                user_list = Context.RedisStat.hget_keys('user_daily:*:{}:*'.format(days))
                for user_str in user_list:
                    user_id = user_str.split(':')[3]
                    coupon = Context.Data.get_game_attr_int(int(user_id), gid, 'coupon', 0)
                    channel_id = Context.Data.get_attr(int(user_id), 'channelid')
                    pay_total = Context.Data.get_game_attr_int(int(user_id), gid, 'pay_total', 0)
                    all_pay_info = self.get_user_all_pay(gid, user_id)
                    user_day = Context.RedisStat.hash_getall('user_daily:{}:{}:{}'.format(channel_id, days, user_id))
                    if len(user_day) > 0:
                        if days == Time.current_time("%Y-%m-%d"):
                            surplus_coupon = coupon
                        else:
                            surplus_coupon = self.calc_coupon(user_id, coupon, days)
                        super_weapon = self.get_super_weapon(channelids=channel_id, fmt=days, uid=user_id)
                        user_day.update(all_pay_info)
                        user_day.update({'in.chip.super.weapon.fix.new': super_weapon,"surplus_coupon": surplus_coupon, "pay_total": pay_total,"channel":channel_id})
                        everyday[user_id] = user_day

                period_data[days] = everyday
                start_day = Time.next_days(start_day)

        mo = MsgPack(0)
        mo.set_param('info', period_data)
        return mo

    def calc_coupon(self, uid, coupon_surplus, day_time):  # 昨日鸟券剩余 = 今日的剩余 + 今日商城兑换 - 今日产出
        channel_id = Context.Data.get_attr(int(uid), 'channelid')
        i = 0
        while True:
            day_date = Time.str_to_datetime(Time.current_time("%Y-%m-%d"), "%Y-%m-%d")
            fmt = (day_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            ex_coupon = Context.RedisStat.hash_get('user_daily:{}:{}:{}'.format(channel_id, fmt, uid),"out.coupon.limit.shop.buy")
            user_day = Context.RedisStat.hash_getall('user_daily:{}:{}:{}'.format(channel_id, fmt, uid))
            in_coupon = 0
            if len(user_day) > 0:
                for key, value in user_day.items():
                    if key.startswith('in.coupon.'):
                        in_coupon += int(value)
            else:
                in_coupon = 0

            last_time = Time.yesterday_time(Time.str_to_timestamp(fmt, "%Y-%m-%d"))
            if ex_coupon:
                coupon_surplus = (coupon_surplus + int(ex_coupon)) - in_coupon
            else:
                coupon_surplus = (coupon_surplus + 0) - in_coupon
            if last_time == day_time or last_time == "2018-12-27":
                break
            else:
                i = i - 1
        return coupon_surplus

    def calc_coupon_rate(self, gid, mi, request):
        # tf add record
        Context.Log.debug("gm_calc_coupon_rate:", mi)
        Context.Record.add_record_gm_calc_coupon_rate(mi)

        day_time = str(mi.get_param('day_time'))

        daily_list = []
        user_daily = Context.RedisStat.hget_keys('user_daily:*:{}:*'.format(day_time))
        for user in user_daily:
            user_info = {}
            uid = user.split(':')[3]
            channelid = user.split(':')[1]
            result, player_info = self.get_daily_player_info(uid, day_time)
            if result:
                super_weapon_value = self.get_super_weapon(channelids=channelid, fmt=day_time, uid=uid)
                player_info['in.chip.super.weapon.fix.new'] = super_weapon_value
                user_info.update({uid: player_info})
                daily_list.append({channelid:{day_time:user_info}})
        mo = MsgPack(0)
        mo.set_param("ret",daily_list)
        return mo

    def get_server_redis_data(self, gid, mi, request):
        Context.Log.debug("gm_server_redis_data:", mi)
        Context.Record.add_record_gm_server_redis_data(mi)

        start = mi.get_param('start')
        end = mi.get_param('end')
        user_id = mi.get_param('uid')

        stat_list = []
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        while start_day <= end_day:
            day_time = Time.datetime_to_str(start_day, '%Y-%m-%d')
            stat_info = Context.RedisStat.hget_keys('stat:*:{}'.format(day_time))
            for stat in stat_info:
                stat_dict = {}
                channelid = stat.split(':')[1]
                day_stat = Context.Stat.get_day_data(channelid, day_time)
                day_stat["day_time"] = day_time
                stat_dict.update({channelid: day_stat})
                stat_list.append(stat_dict)
            start_day = Time.next_days(start_day)

        game_list,user_list = [],[]
        if user_id:
            ret = Context.RedisCluster.hget_keys('game:2:*')
            add_list = sorted(ret)
            uid_str = "game:2:{}".format(user_id)
            id_list = [i for i, x in enumerate(add_list) if x == uid_str]
            if len(id_list) >0:
                index = id_list[0]
                for game in add_list[index:]:
                    uid = int(game.split(':')[2])
                    game_info = Context.Data.get_game_all(int(uid), 2)
                    user_info = Context.Data.get_all(int(uid))
                    if len(game_info) != 0 and len(user_info) != 0:
                        game_dict,user_dict = {},{}
                        game_dict.update({uid: game_info})
                        game_list.append(game_dict)
                        user_dict.update({uid: user_info})
                        user_list.append(user_dict)
                    else:
                        continue
        else:
            ret = Context.RedisCluster.hget_keys('game:2:*')
            for game in ret:
                uid = int(game.split(':')[2])
                if uid <= 1000000:
                    continue
                else:
                    game_info = Context.Data.get_game_all(uid, 2)
                    user_info = Context.Data.get_all(uid)
                    if len(game_info) != 0 and len(user_info) != 0:
                        game_dict, user_dict = {}, {}
                        game_dict.update({uid: game_info})
                        game_list.append(game_dict)
                        user_dict.update({uid: user_info})
                        user_list.append(user_dict)

        max_uid = Context.RedisMix.hash_get_int('global.info.hash', 'max.user.id', 0)
        mo = MsgPack(0)
        mo.set_param("stat", stat_list)
        mo.set_param("game", game_list)
        mo.set_param("user", user_list)
        mo.set_param("max_user", max_uid)
        return mo


    # 这里暂时不再提供查询所有玩家数据
    def query_user_daily_info(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_query_user_daily_info:", mi)
        Context.Record.add_record_gm_query_user_daily_info(mi)

        uid = mi.get_param('uid', 0)  # 玩家id不存在时 查询获取此时间段内所有玩家信息
        start = str(mi.get_param('start'))  # 查询时间段-开始
        end = str(mi.get_param('end'))  # 查询时间段-结束
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')

        today = Time.datetime_now('%Y-%m-%d')  # 今日时间
        #if start_day <= end_day and today == end:
        #    Context.Log.debug('BirdEntity.set_daily_date')
        #    BirdEntity.set_daily_date(2, end, False)  # 刷新数据

        #all_uid = []
        #if uid == 0:
        #    ret = Context.RedisCluster.hget_keys('user:*')
        #    if not ret:
        #        return MsgPack.Error(0, 2, 'not exist')
        #    all_uid = []
        #    for item in ret:
        #        all_uid.append(item.split(':')[1])
        #    all_uid.sort()

        days_info = {}
        while start_day <= end_day:
            day_player_info = {}
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            if uid != 0:   # 选定玩家数据获取
                result, player_info = self.get_daily_player_info(uid, fmt)
                if result:
                    channelid = Context.Data.get_attr(int(uid), 'channelid')
                    super_weapon_value = self.get_super_weapon(channelids=channelid, fmt=fmt, uid=uid)
                    player_info['in.chip.super.weapon.fix.new'] = super_weapon_value
                day_player_info.update({str(uid): player_info})
            #else:    # 所有玩家数据
            #    for uid_l in all_uid:
            #        result, player_info = self.get_daily_player_info(int(uid_l), fmt)
            #        if result:
            #            channelid = Context.Data.get_attr(int(uid_l), 'channelid')
            #            super_weapon_value = self.get_super_weapon(channelids=channelid, fmt=fmt, uid=uid_l)
            #            player_info['in.chip.super.weapon.fix.new'] = super_weapon_value
            #        day_player_info.update({str(uid_l): player_info})
            days_info.update({fmt: day_player_info})

            start_day = Time.next_days(start_day)

        mo = MsgPack(0)
        mo.set_param("ret", days_info)
        return mo

    def query_money_count(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_query_money_count:", mi)
        Context.Record.add_record_query_money_count(mi)
        return

        # 货币统计
        mo = MsgPack(0)
        start = str(mi.get_param('start'))
        end = str(mi.get_param('end'))
        # channel = mi.get_param('channel')
        start_day = Time.str_to_datetime(start,'%Y-%m-%d')
        end_day = Time.str_to_datetime(end,'%Y-%m-%d')

        today =Time.datetime_now('%Y-%m-%d')
        #if start_day <= end_day and today == end:
        #    Context.Log.debug('BirdEntity.set_daily_date')
        #    BirdEntity.set_daily_date(2, end, False)

        # 处理统计数据
        count_info = []
        ret = Context.RedisStat.hget_keys('stat:*')
        if not ret:
            return MsgPack.Error(0, 2, 'not exist')
        ls = []
        for item in ret:
            id = item.split(':')[1]
            if id != '2' and id not in ls:
                ls.append(id)
        ls.sort()

        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')

            day_info = {}  # 本日时间记录
            channel_info = {}
            for channelid in ls:
                kvs = Context.Stat.get_day_data(channelid, fmt)  # 获取当天数据记录
                if len(kvs) == 0:  # 没有记录
                    continue

                channeldict = {}
                in_chip_total = 0   # 鸟蛋产出
                new_in_chip_free,new_in_diamond_free = 0,0  # 新免费鸟蛋和新免费钻石
                in_chip_buy = 0     # 购买的鸟蛋
                #out_chip_total = 0   # 鸟蛋消耗
                in_diamond_total = 0    # 钻石产出
                in_diamond_buy = 0      # 购买的钻石
                out_diamond_total = 0   # 钻石消耗
                in_box601 = in_box602 = in_box603 = in_box604 = 0           # 宝箱产出
                out_box601 = out_box602 = out_box603 = out_box604 = 0       # 宝箱消耗
                event_coupon_cost = 0 # 鸟蛋消耗
                # 遍历本日数据
                in_channel_coupon,out_channel_coupon = 0,0
                out_channel_target,in_channel_target = 0,0
                gift_chip = 0  #千N赠分
                props_info = {}
                prop = []
                rewards_info = {}
                for k, v in kvs.iteritems():

                    if k.startswith('in.play_shot_gift_chip.'):
                        gift_chip += int(v)

                    # 获取本日充值总金额
                    if k.startswith('{}.pay.user.pay_total'.format(channelid)):
                        channeldict['pay_total'] = str(v)
                        # 获取sdk支付
                    if k.startswith('{}.sdk_pay.user.pay_total'.format(channelid)):
                        channeldict['sdk_pay_total'] = str(v)
                    # 获取兑换码充值额度
                    elif k.endswith('.cdkey_pay.user.pay_total'):
                        channeldict['cdkey_pay_total'] = str(v)
                    # 获取微信充值额度
                    elif k.endswith('.weixin_pay.user.pay_total'):
                        channeldict['weixin_pay_total'] = str(v)
                    # 获取支付宝充值额度
                    elif k.endswith('.ali_pay.user.pay_total'):
                        channeldict['ali_pay_total'] = str(v)

                    # # 获取gm充值额度
                    # elif k.endswith('.gm_pay.user.pay_total'):
                    #     channeldict['gm_pay_total'] = str(v)

                    # 鸟券产出
                    elif k.startswith('in.coupon.'):
                        in_channel_coupon += int(v)
                        channeldict[k] = v     #dz
                    # 鸟券消耗
                    elif k.startswith('out.coupon.'):
                        out_channel_coupon += int(v)
                        channeldict[k] = v     # dz

                    # 靶场券产出
                    elif k.startswith('in.target_coupon.'):
                        in_channel_target += int(v)
                        channeldict[k] = v     # dz
                    # 靶场券消耗
                    elif k.startswith('out.target_coupon.'):
                        out_channel_target += int(v)
                        channeldict[k] = v     # dz

                    # 新手离场后富裕的鸟蛋数
                    elif k.endswith('new_player_get_chip'):
                        channeldict['new_player_get_chip'] = str(v)

                    # 鸟蛋剩余
                    elif k.endswith('server_chip'):
                        channeldict['server_chip'] = str(v)

                    # 105赠分
                    elif k.endswith('server_gift_chip'):
                        channeldict['server_gift_chip'] = str(v)

                    # 充值赠分
                    elif k.endswith('server_recharge_gift_chip'):
                        channeldict['server_recharge_gift_chip'] = str(v)

                    # 105赠分产出
                    elif k.startswith('out.gift_chip.hit.bird'):
                        channeldict[k] = str(v)
                    # 充值-赠分
                    elif k.startswith('out.recharge_gift_chip.triggle_recharge_gift'):
                        channeldict[k] = str(v)


                    # 新手期赠送
                    elif k.endswith('server_if_new_player'):
                        channeldict['server_if_new_player'] = str(v)


                    # 钻石剩余
                    elif k.endswith('server_diamond'):
                        channeldict['server_diamond'] = str(v)

                    # 鸟券剩余
                    elif k.endswith('server_coupon'):
                        channeldict['server_coupon'] = str(v)

                    # 靶场券剩余
                    elif k.endswith('server_target'):
                        channeldict['server_target'] = str(v)

                    elif k.endswith('server_pool_left'):
                        channeldict['server_pool_left'] = str(v)

                    elif k == 'server_props_202':       # 冰冻道具
                        channeldict['server_props_202'] = str(v)
                    elif k == 'server_props_203':       # 狂暴道具
                        channeldict['server_props_203'] = str(v)
                    elif k == 'server_props_204':       # 超级武器道具
                        channeldict['server_props_204'] = str(v)
                    elif k == 'server_props_205':       # 赏金传送道具
                        channeldict['server_props_205'] = str(v)
                    elif k == 'server_props_211':       # 青铜宝箱-当日剩余总数
                        channeldict['server_props_211'] = str(v)
                    elif k == 'server_props_212':       # 白银宝箱-当日剩余总数
                        channeldict['server_props_212'] = str(v)
                    elif k == 'server_props_213':       # 黄金宝箱-当日剩余总数
                        channeldict['server_props_213'] = str(v)
                    elif k == 'server_props_214':       # 至尊宝箱-当日剩余总数
                        channeldict['server_props_214'] = str(v)
                    elif k == 'server_props_215':       # 强化碎片-绿灵石
                        channeldict['server_props_215'] = str(v)
                    elif k == 'server_props_216':       # 强化碎片-蓝魔石
                        channeldict['server_props_216'] = str(v)
                    elif k == 'server_props_217':       # 强化碎片-紫晶石
                        channeldict['server_props_217'] = str(v)
                    elif k == 'server_props_218':       # 强化碎片-血晶石
                        channeldict['server_props_218'] = str(v)
                    elif k == 'server_props_219':       # 强化精华
                        channeldict['server_props_219'] = str(v)
                    elif k == 'server_bonus_pool':      # 免费抽奖池
                        channeldict['server_bonus_pool'] = str(v)

                    # TF免费抽奖
                    elif k.startswith('in.chip.') and k.endswith('.bonus.raffle'):
                        rewards_info.update({"chip":int(v)})

                    elif k.startswith('in.diamond.') and k.endswith('.bonus.raffle'):
                        rewards_info.update({"diamond":int(v)})

                    elif k.startswith('in.coupon.') and k.endswith('.bonus.raffle'):
                        rewards_info.update({"coupon":int(v)})

                    elif k.startswith('in.props.') and k.endswith('.bonus.raffle'):
                        props_id = str(filter(str.isdigit, k))
                        props_info.update({"id": int(props_id), "count": int(v)})
                        prop.append(props_info)
                        rewards_info.update({"props": prop})
                        props_info = {}

                    # 新免费鸟蛋
                    elif k.endswith('in.chip.day.activity.value.receive') \
                             or k.endswith('in.chip.exp.upgrade') or k.endswith('in.chip.bind.rewards') or k.endswith('in.chip.activity.task.reward.total')\
                             or k.endswith('in.chip.online.reward') or k.endswith('in.chip.signin.reward') \
                             or k.endswith('in.chip.task.get') or k.endswith('in.chip.unlock.barrel') \
                             or k.endswith('in.chip.vip_receive') or k.endswith('in.chip.week.activity.value.receive') \
                             or k.endswith('in.chip.activity.login.reward') or k.endswith('in.chip.boss.rank.get') \
                             or k.endswith('in.chip.primary.rank.get') or k.endswith('in.chip.middle.rank.get') \
                             or k.endswith('in.chip.high.rank.get') or k.endswith('in.chip.activity.pay.raffle') \
                             or k.endswith('in.chip.activity.login.reward') or k.endswith('in.chip.activity.task.reward.receive') \
                             or k.endswith('in.chip.activity.rank.config') or k.endswith('in.chip.game.startup') or k.endswith('in.chip.cdkey.reward.free'):
                        new_in_chip_free += int(v)

                    # 新免费钻石
                    elif k.endswith('in.diamond.day.activity.value.receive') or k.endswith('in.diamond.buy.product.extra') \
                             or k.endswith('in.diamond.exp.upgrade') or k.endswith('in.diamond.bind.rewards') \
                             or k.endswith('in.diamond.online.reward') or k.endswith('in.diamond.signin.reward') \
                             or k.endswith('in.diamond.task.get') or k.endswith('in.diamond.unlock.barrel') \
                             or k.endswith('in.diamond.vip_receive') or k.endswith('in.diamond.week.activity.value.receive') \
                             or k.endswith('in.diamond.activity.login.reward') or k.endswith('in.diamond.boss.rank.get') \
                             or k.endswith('in.diamond.primary.rank.get') or k.endswith('in.diamond.middle.rank.get') \
                             or k.endswith('in.diamond.high.rank.get') or k.endswith('in.diamond.activity.pay.raffle') \
                             or k.endswith('in.diamond.activity.login.reward') or k.endswith('in.diamond.activity.task.reward.receive') \
                             or k.endswith('in.diamond.activity.rank.config') or k.endswith('in.diamond.game.startup') or k.endswith('in.diamond.cdkey.reward.free'):
                        new_in_diamond_free += int(v)


                    # 鸟蛋产出
                    if k.startswith('in.chip.') \
                            and not k.startswith('in.chip.catch.bird') \
                            and not k.startswith('in.chip.hit.table.boss') \
                            and not k.startswith('in.chip.entity.use') \
                            and not k.startswith('in.chip.hit.world.boss')\
                            and not k.startswith('in.chip.super.weapon.fix'):
                        in_chip_total += int(v)
                        if k.startswith('in.chip.buy.') or k.endswith('in.chip.cdkey.reward'):   # 购买的鸟蛋  将cdkey购买的鸟蛋也计入
                            in_chip_buy += int(v)

                    if k.startswith('in.chip.'):
                        channeldict[k] = v  #dz

                    if k.startswith('server_chip_pool_new_gift'):   # 新手赠送额度
                        channeldict[k] = v

                    # 100:105 赠送鸟蛋
                    if k.startswith('in.gift_chip.'):
                        channeldict[k] = v  # dz

                    # 充值赠送活动赠送的鸟蛋
                    if k.startswith('in.recharge_gift_chip.'):
                        channeldict[k] = v  # dz

                    # 鸟蛋消耗
                    elif k.startswith('out.chip.'):
                        channeldict[k] = v  # dz

                    # 钻石产出
                    if k.startswith('in.diamond.'):
                        in_diamond_total += int(v)
                        channeldict[k] = v  # dz
                        if k.startswith('in.diamond.buy'):    # 购买的鸟蛋
                            in_diamond_buy += int(v)

                    # 钻石消耗
                    elif k.startswith('out.diamond.'):
                        out_diamond_total += int(v)
                        channeldict[k] = v  # dz

                    elif k.startswith('in.props.211.'):     # 产出青铜宝箱
                        in_box601 += int(v)
                    elif k.startswith('in.props.212.'):     # 产出白银宝箱
                        in_box602 += int(v)
                    elif k.startswith('in.props.213.'):     # 产出黄金宝箱
                        in_box603 += int(v)
                    elif k.startswith('in.props.214.'):     # 产出至尊宝箱
                        in_box604 += int(v)

                    elif k.startswith('out.props.211.'):    # 消耗青铜宝箱
                        out_box601 += int(v)
                    elif k.startswith('out.props.212.'):    # 消耗白银宝箱
                        out_box602 += int(v)
                    elif k.startswith('out.props.213.'):    # 消耗黄金宝箱
                        out_box603 += int(v)
                    elif k.startswith('out.props.214.'):    # 消耗至尊宝箱
                        out_box604 += int(v)


                # 获取gm充值额度
                channeldict['gm_pay_total'] = self.get_order_info(channelid=channelid,fmt=fmt)

                price=BirdProps.get_props_price(rewards_info)
                channeldict['free_prize_draw'] = str(price)
                channeldict['new_in_chip_free'] = str(new_in_chip_free)
                channeldict['new_in_diamond_free'] = str(new_in_diamond_free)
                channeldict['in_channel_coupon'] = str(in_channel_coupon)
                channeldict['out_channel_coupon'] = str(out_channel_coupon)
                channeldict['in_channel_target'] = str(in_channel_target)
                channeldict['out_channel_target'] = str(out_channel_target)

                channeldict['play_shot_gift_chip'] = str(gift_chip) # 千N赠分

                # channeldict['in_chip'] = str(in_chip_total)
                channeldict['in_chip_buy'] = str(in_chip_buy)

                channeldict['in_diamond'] = str(in_diamond_total)
                channeldict['in_diamond_buy'] = str(in_diamond_buy)
                channeldict['out_diamond'] = str(out_diamond_total)

                channeldict['in_box601'] = str(in_box601)
                channeldict['in_box602'] = str(in_box602)
                channeldict['in_box603'] = str(in_box603)
                channeldict['in_box604'] = str(in_box604)

                channeldict['out_box601'] = str(out_box601)
                channeldict['out_box602'] = str(out_box602)
                channeldict['out_box603'] = str(out_box603)
                channeldict['out_box604'] = str(out_box604)

                super_weapon_value = self.get_super_weapon(channelids=channelid, fmt=fmt)
                channeldict['in.chip.super.weapon.fix.new'] = super_weapon_value
                channeldict['in_chip'] = str(in_chip_total + super_weapon_value)

                # 计算蛋券比
                pre_day = Time.next_days(start_day, -1)
                fmt_pre = Time.datetime_to_str(pre_day, '%Y-%m-%d')
                datas = Context.Stat.get_day_data(channelid, fmt_pre)  # 获取前一天数据记录
                pre_chip = datas.get('server_chip', 0) #前一天鸟蛋
                pre_chip_pool_new_gift = datas.get('server_chip_pool_new_gift', 0)  # 前一天新手赠送鸟蛋

                pre_diamond = datas.get('server_diamond', 0)    # 前一天钻石
                pre_target = datas.get('server_target', 0)     # 前一天靶劵

                channeldict['pre_day_server_chip'] = pre_chip
                channeldict['day_server_diamond'] = pre_diamond
                channeldict['day_server_target'] = pre_target
                channeldict['pre_day_new_gift'] = pre_chip_pool_new_gift

                # 计算免费抽奖池相对前一天的值
                pre_server_bonus_pool = datas.get('server_bonus_pool', 0)
                channeldict['server_bonus_pool_space'] = str(int(channeldict.get('server_bonus_pool', 0)) - int(pre_server_bonus_pool))
                # 消耗鸟蛋计算  鸟蛋消耗=今日产出+昨日剩余-今日剩余
                channeldict['out_chip'] = str(int(pre_chip) + int(channeldict['in_chip']) - int(channeldict.get('server_chip',0)))
                # 计算得出蛋券比
                channeldict['real_cost_chip'] = str(((int(pre_chip) + in_chip_total) - int(channeldict.get('server_chip', 0))))

                channeldict['in.chip.super.weapon.fix.new'] = super_weapon_value
                channel_info[channelid] = channeldict

            kvs = Context.Stat.get_day_data(gid, fmt)  # 获取当天数据记录
            if len(kvs) > 0:
                day_info.update({'win_barrel_chip': kvs.get('win_barrel_chip', '0')})    # 炮倍池状态

            day_time = Time.str_to_datetime(fmt,'%Y-%m-%d')
            pre_day = Time.next_days(day_time, -1)
            fmt_pre = Time.datetime_to_str(pre_day, '%Y-%m-%d')
            kvs = Context.Stat.get_day_data(gid, fmt_pre)  # 获取前一天数据记录
            if len(kvs) > 0:
                last_day_chip = kvs.get('win_barrel_chip', 0)
                #if 0 == last_day_chip:
                    #strWin, strFill = BirdEntity.get_barrel_pool_win_chip(gid)
                    #last_day_chip = strFill  # 前一天炮倍池状态
                day_info.update({'pre_win_barrel_chip': last_day_chip})  # 炮倍池状态

            if len(channel_info) > 0:
                day_info.update({'time': {fmt: channel_info}})
                count_info.append(day_info)

            start_day = Time.next_days(start_day)

        mo.set_param("ret", count_info)
        return mo

    def get_super_weapon(self,channelids=None,fmt=None,uid=None):
        weapon_value = 0
        if uid:
            weapon_info = Context.RedisCluster.hash_getall(100, 'event:%s:%s' % ('super_weapon', uid))
            for stamp, data in weapon_info.iteritems():
                data = Context.json_loads(data)
                days = Time.timestamp_to_str(int(stamp[:10]), '%Y-%m-%d')
                if fmt == days:
                    weapon_value = weapon_value + data[1]
            return -(weapon_value)
        else:
            ret = Context.RedisCluster.hget_keys('event:super_weapon:*')
            if not ret:
                return weapon_value
            for item in ret:
                uids = item.split(':')[2]
                channelid = Context.Data.get_attr(int(uids), 'channelid')
                if channelids == channelid:
                    weapon_info = Context.RedisCluster.hash_getall(100, 'event:%s:%s' % ('super_weapon', uids))
                    for stamp, data in weapon_info.iteritems():
                        data = Context.json_loads(data)
                        days = Time.timestamp_to_str(int(stamp[:10]), '%Y-%m-%d')
                        if fmt == days:
                            weapon_value = weapon_value + data[1]
            return -(weapon_value)

    def get_order_info(self,channelid,fmt):
        channels = "gm"
        ret = Context.RedisPay.hget_keys('order:*')
        if not ret:
            return 0
        gm_pay_total = 0
        for item in ret:
            id = item.split(':')[1]
            data = Context.RedisPay.hash_getall('order:{}'.format(id))

            if data["createTime"][:10] == fmt:
                uid = int(data["userId"])
                channelids = Context.Data.get_attr(uid, 'channelid')
                channel = data["channel"]
                if channelids == channelid and channels ==channel:
                    gm_pay_total = gm_pay_total + int(data["cost"])


        return gm_pay_total

    def query_online_detail(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_query_online_detail:", mi)
        Context.Record.add_record_query_online_detail(mi)

        location = Context.RedisCache.hget_keys('location:2:*')
        if not location:
            return MsgPack.Error(0, 1, 'not online_user')
        online = []
        for item in location:
            online.append(item.split(':')[2])
        online.sort()
        
        '''玩家ID, 玩家名称, 绑定手机, 充值金额, 金币数量, 钻石数量, 鸟卷数量, 渠道, 
        推广员【暂无】, 创建时间, 登陆次数, 最近登陆, 最近登陆IP【暂无】, 操作【暂无】
        ——以上字段按顺序放入data中'''
        ret = []
        online_info ={}
        for uid in online:
            online_info.update({"uid":uid})
            online_info.update({"nick": Context.RedisCluster.hash_get(uid, 'user:%s' %uid, 'nick')})
            online_info.update({"mobile": Context.RedisCluster.hash_get(uid, 'user:%s' %uid, 'userName')})
            promoter = Context.RedisCluster.hash_get(uid, 'user:%s' % uid, 'inviter')
            if promoter ==None:
                promoter = "无"
            online_info.update({"promoter": promoter})
            online_info.update({"pay_total":Context.RedisCluster.hash_get(uid, 'game:2:%s' %uid, 'pay_total')})
            online_info.update({"chip": Context.RedisCluster.hash_get(uid, 'game:2:%s' % uid, 'chip')})
            online_info.update({"diamond": Context.RedisCluster.hash_get(uid, 'game:2:%s' % uid, 'diamond')})
            online_info.update({"coupon": Context.RedisCluster.hash_get(uid, 'game:2:%s' %uid, 'coupon')})
            online_info.update({"login_time": Context.RedisCluster.hash_get(uid, 'daily:2:%s' % uid, 'login.times')})
            online_info.update({"channel": Context.RedisCluster.hash_get(uid, 'user:%s' %uid, 'channelid')})
            online_info.update({"createTime": Context.RedisCluster.hash_get(uid, 'user:%s' %uid, 'createTime')})
            online_info.update({"session_login": Context.RedisCluster.hash_get(uid, 'game:2:%s' %uid, 'session_login')})
            online_info.update({"createIp": Context.RedisCluster.hash_get(uid, 'user:%s' %uid, 'createIp')})
            ret.append(online_info)
            online_info = {}
        mo = MsgPack(0)
        mo.set_param('ret', ret)
        return mo


    def coupon_output(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_query_coupon_output:", mi)
        Context.Record.add_record_query_coupon_output(mi)

        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        mo = MsgPack(0)
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            kvs = Context.Stat.get_day_data(gid, fmt)
            channel_info = {}
            channel_info['in.coupon.hit.bird'] = 0
            for k, v in kvs.iteritems():
                if k.startswith('in.coupon.') and k.endswith('.hit.bird') or k in 'in.coupon.coupon_pool_free.coupon.bird.fall':
                    channel_info['in.coupon.hit.bird'] = int(v)
                if k in ['in.coupon.award.bird', 'in.coupon.bonus.raffle','in.coupon.coupon_pool_private.coupon.bird.fall',
                         'in.coupon.online.reward', 'in.coupon.boss.rank.get',
                         'in.coupon.high.rank.get','in.coupon.exp.upgrade','in.coupon.boss.one.fall']:
                    channel_info[k] = int(v)
            mo.set_param(fmt, channel_info)
            start_day = Time.next_days(start_day)
        return mo

    def del_history_user_daily(self, gid, mi, request):
        all_keys = Context.RedisStat.hget_keys('user_daily:*')
        if not all_keys:
            Context.Log.debug('error fixed')
            return 0

        dt_last30 = Time.next_days(None, -90)
        Context.Log.debug('dt_last30', dt_last30)

        for daily_key in all_keys:
            day_fmt = daily_key.split(':')[2]
            Context.Log.debug('check', day_fmt)
            if Time.str_to_datetime(day_fmt, '%Y-%m-%d') < dt_last30:
                Context.Log.debug('del', daily_key)
                Context.RedisStat.delete(daily_key)
            elif len(Context.RedisStat.hash_getall(daily_key)) <= 5:
                Context.Log.debug('del', daily_key, Context.RedisStat.hash_getall(daily_key))
                Context.RedisStat.delete(daily_key)


    def super_weapon_count(self, gid, mi, request):
        #self.fix_daily_data_his_total_pay(gid, mi, request)
        #return

        # tf add record
        Context.Log.debug("gm_query_super_weapon_count:", mi)
        Context.Record.add_record_query_super_weapon_count(mi)
        input_data = mi.get_param('input_data')
        weapon_data = []
        mo = MsgPack(0)
        if input_data ==None:
            start = mi.get_param('start')
            end = mi.get_param('end')
            # start_day = Time.str_to_datetime(start, '%Y-%m-%d')
            # end_day = Time.str_to_datetime(end, '%Y-%m-%d')
            start_stamp = Time.str_to_timestamp(start)
            end_stamp = Time.str_to_timestamp(end)
            ret = Context.RedisCluster.hget_keys('event:super_weapon:*')
            if not ret:
                return MsgPack.Error(0, 2, 'not exist')

            for item in ret:
                uid = item.split(':')[2]
                weapon_info = Context.RedisCluster.hash_getall(100, 'event:%s:%s' % ('super_weapon', uid))
                for stamp, data in weapon_info.iteritems():
                    weapon_dict = {}
                    data = Context.json_loads(data)
                    days = int(stamp[:10])
                    if days >= start_stamp and days <= end_stamp:
                        weapon_dict.update({"uid": uid, "day_time": Time.timestamp_to_str(days), "super_weapon_bomb": -(data[1]),"pool_left_chip":int(data[3].split(':')[1])})
                        weapon_data.append(weapon_dict)
        else:
            weapon_info = Context.RedisCluster.hash_getall(100, 'event:%s:%s' % ('super_weapon', input_data))
            for stamp, data in weapon_info.iteritems():
                weapon_dict = {}
                data = Context.json_loads(data)
                days = int(stamp[:10])
                weapon_dict.update({"uid": input_data, "day_time": Time.timestamp_to_str(days), "super_weapon_bomb": -(data[1]),"pool_left_chip": int(data[3].split(':')[1])})
                weapon_data.append(weapon_dict)

        mo.set_param("info", weapon_data)
        return mo

    def query_box_fall(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_query_box_fall:", mi)
        Context.Record.add_record_query_box_fall(mi)

        # 新增设备, 新增用户, 活跃用户, (新)付费玩家, (新)用户付费, 充值次数
        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        mo = MsgPack(0)
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            kvs = Context.Stat.get_day_data(gid, fmt)
            channel_info = {}
            box601,box602,box603,box604,out601,out602,out603,out604= 0,0,0,0,0,0,0,0

            for k, v in kvs.iteritems():
                if k.startswith('out.props.211.entity'):
                    out601 -= int(v)
                elif k.startswith('out.props.212.entity'):
                    out602 -= int(v)
                elif k.startswith('out.props.213.entity'):
                    out603 -= int(v)
                elif k.startswith('out.props.214.entity'):
                    out604 -= int(v)

                elif k.startswith('in.props.211.'):
                    box601 += int(v)
                elif k.startswith('in.props.212.'):
                    box602 += int(v)
                elif k.startswith('in.props.213.'):
                    box603 += int(v)
                elif k.startswith('in.props.214.'):
                    box604 += int(v)

                elif k.startswith('out.props.211.present'):
                    box601 += -int(v)
                elif k.startswith('out.props.212.present'):
                    box602 += -int(v)
                elif k.startswith('out.props.213.present'):
                    box603 += -int(v)
                elif k.startswith('out.props.214.present'):
                    box604 += -int(v)

            channel_info['in.props.211'] = box601
            channel_info['in.props.212'] = box602
            channel_info['in.props.213'] = box603
            channel_info['in.props.214'] = box604

            channel_info['out.props.211'] = -out601
            channel_info['out.props.212'] = -out602
            channel_info['out.props.213'] = -out603
            channel_info['out.props.214'] = -out604
            mo.set_param(fmt, channel_info)
            start_day = Time.next_days(start_day)
        return mo

    def query_carry_chip(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_query_carry_chip:", mi)
        Context.Record.add_record_query_carry_chip(mi)

        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        mo = MsgPack(0)
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            kvs = Context.Stat.get_day_data(gid, fmt)
            channel_info = {}
            for k, v in kvs.iteritems():
                if k in ['carrying.volume.chip', 'login.carrying.volume.chip'] :
                    channel_info[k] = int(v)
            mo.set_param(fmt, channel_info)
            start_day = Time.next_days(start_day)
        return mo

    def gm_reward_coupon_pool(self, gid, mi, request):
        uid = mi.get_param('userId')
        if not Context.UserAttr.check_exist(uid, gid):
            return MsgPack.Error(0, 1, 'not exist')

        coupon_pool = mi.get_param('coupon_pool')
        real, final = Context.UserAttr.incr_coupon_private_pool(uid, gid, coupon_pool, 'gm.reward')
        if real != coupon_pool:
            MsgPack.Error(0, 1, 'not enough')
        return MsgPack(0, {'coupon_pool': final, 'delta': real})

    def gm_query_coupon_pool(self, gid, mi, request):
        uid = mi.get_param('userId')
        if not Context.UserAttr.check_exist(uid, gid):
            return MsgPack.Error(0, 1, 'not exist')

        coupon_pool = Context.UserAttr.get_coupon_private_pool(uid, gid, 0)
        return MsgPack(0, {'coupon_pool': coupon_pool})

    def game_data(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_query_game_data:", mi)
        Context.Record.add_record_query_game_data(mi)

        # 小游戏总览
        mo = MsgPack(0)
        start = str(mi.get_param('start'))
        end = str(mi.get_param('end'))
        game = mi.get_param('game')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')

        # 处理统计数据
        count_info = []
        channel_dict = Context.Configure.get_game_item_json(gid, 'channel.path.config')
        ls = channel_dict.keys()
        ls.sort()

        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')

            day_info = {}  # 本日时间记录
            channel_info = {}
            for channelid in ls:
                kvs = Context.Stat.get_day_data(channelid, fmt)  # 获取当天数据记录
                if len(kvs) == 0:  # 没有记录
                    start_day = Time.next_days(start_day)
                    continue
                channel_dict = {}
                if int(game) == 1:
                    server_in_211,server_in_212,server_consume,server_play_times,server_in_coupon = 0,0,0,0,0
                    for k, v in kvs.iteritems():
                        if k == 'server_target_play_times':
                            server_play_times = str(v)
                        elif k == 'out.target_coupon.target.room.consume':
                            server_consume = str(v)
                        elif k == 'in.coupon.target.room.get':
                            server_in_coupon = str(v)

                    channel_dict['server_consume'] = str(server_consume)
                    channel_dict['server_play_times'] = str(server_play_times)
                    channel_dict['server_in_coupon'] = str(server_in_coupon)

                if int(game) == 2:
                    server_fanfanle_play_times = 0
                    server_fanfanle_out_chip_pay = 0        #金币消耗
                    server_fanfanle_out_chip_change = 0     #换牌消耗
                    server_fanfanle_in_chip = 0
                    server_fanfanle_out_diamond_play = 0    #钻石消耗
                    server_fanfanle_out_diamond_change = 0  #换牌钻石消耗
                    server_fanfanle_in_diamond = 0
                    server_fanfanle_in_coupon = 0
                    server_fanfanle_exchange_times = 0
                    server_fanfanle_chip_change = 0
                    server_fanfanle_diamond_change = 0

                    for k, v in kvs.iteritems():
                        if k in ['v2_server_fanfanle_play_chip_times', 'v2_server_fanfanle_play_diamonds_times']:
                            server_fanfanle_play_times += int(v)
                        if k in ['out.chip.game.fanfanle.change']:
                            server_fanfanle_out_chip_change += int(v)
                        if k in ['out.chip.game.fanfanle.play', 'out.chip.game.fanfanle.change']:
                            server_fanfanle_out_chip_pay += int(v)
                        elif k == 'in.chip.game.fanfanle.get':
                            server_fanfanle_in_chip = int(v)
                        if k in ['out.diamond.game.fanfanle.change']:
                            server_fanfanle_out_diamond_change = +int(v)
                        if k in ['out.diamond.game.fanfanle.play', 'out.diamond.game.fanfanle.change']:
                            server_fanfanle_out_diamond_play = +int(v)
                        elif k == 'in.diamond.game.fanfanle.get':
                            server_fanfanle_in_diamond = int(v)
                        elif k == 'in.coupon.game.fanfanle.get':
                            server_fanfanle_in_coupon = int(v)
                        elif k in ['server_fanfanle_exchange_diamond_times', 'server_fanfanle_exchange_chip_times']:
                            server_fanfanle_exchange_times += int(v)
                        elif k == 'out.diamond.game.fanfanle.change':
                            server_fanfanle_chip_change = int(v)
                        elif k == 'out.chip.game.fanfanle.change':
                            server_fanfanle_diamond_change = int(v)

                    channel_dict['server_play_times'] = str(server_fanfanle_play_times)
                    channel_dict['server_out_chip_pay'] = str(server_fanfanle_out_chip_pay)
                    channel_dict['server_out_chip_change'] = str(server_fanfanle_out_chip_change)
                    channel_dict['server_in_chip'] = str(server_fanfanle_in_chip)
                    channel_dict['server_out_diamond_pay'] = str(server_fanfanle_out_diamond_play)
                    channel_dict['server_out_diamond_change'] = str(server_fanfanle_out_diamond_change)
                    channel_dict['server_in_diamond'] = str(server_fanfanle_in_diamond)
                    channel_dict['server_in_coupon'] = str(server_fanfanle_in_coupon)
                    channel_dict['server_exchange_times'] = str(server_fanfanle_exchange_times)
                    channel_dict['server_chip_change'] = str(server_fanfanle_chip_change)
                    channel_dict['server_diamond_change'] = str(server_fanfanle_diamond_change)

                if int(game) == 3:
                    server_in_203, server_in_204, server_play_times, server_in_coupon = 0, 0, 0, 0
                    server_in_chip, server_in_diamond, server_out_diamond_pay = 0, 0, 0
                    for k, v in kvs.iteritems():
                        if k == 'server_rich_man_play_times':
                            server_play_times = str(v)
                        elif k == 'in.coupon.rich.man.reward':
                            server_in_coupon = str(v)
                        elif k == 'in.props.203.rich.man.reward':
                            server_in_203 = str(v)
                        elif k == 'in.props.204.rich.man.reward':
                            server_in_204 = str(v)
                        elif k == 'in.chip.rich.man.reward':
                            server_in_chip = str(v)
                        elif k == 'out.diamond.rich.man.consume':
                            server_out_diamond_pay = str(v)
                        elif k == 'in.diamond.rich.man.reward':
                            server_in_diamond = str(v)

                    channel_dict['server_in_203'] = str(server_in_203)   # 产出道具203 狂暴
                    channel_dict['server_in_204'] = str(server_in_204)   # 产出道具204 超级武器
                    channel_dict['server_play_times'] = str(server_play_times)      # 游戏玩的次数
                    channel_dict['server_in_coupon'] = str(server_in_coupon)        # 鸟券产出

                    channel_dict['server_in_chip'] = str(server_in_chip)            # 鸟蛋产出
                    channel_dict['server_out_diamond_pay'] = str(server_out_diamond_pay)        # 玩大富翁 消耗钻石
                    channel_dict['server_in_diamond'] = str(server_in_diamond)      # 大富翁产出钻石

                channel_info[channelid] = channel_dict

            if len(channel_info) > 0:
                day_info.update({fmt: channel_info})
                count_info.append(day_info)

            start_day = Time.next_days(start_day)
        mo.set_param("game", game)
        mo.set_param("ret", count_info)
        return mo

    def query_match_all_data(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_query_match_data:", mi)
        Context.Record.add_record_query_match_data(mi)

        # 小游戏总览
        mo = MsgPack(0)
        start = str(mi.get_param('start'))
        end = str(mi.get_param('end'))
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')

        today = Time.datetime_now('%Y-%m-%d')
        #if start_day <= end_day and today == end:
        #    Context.Log.debug('BirdEntity.set_daily_date')
        #    BirdEntity.set_daily_date(2, end, False)

        # 处理统计数据
        count_info = []
        ret = Context.RedisStat.hget_keys('stat:*')
        if not ret:
            return MsgPack.Error(0, 2, 'not exist')
        ls = []
        for item in ret:
            id = item.split(':')[1]
            if id not in ls:
                ls.append(id)
        ls.sort()
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')

            day_info = {}  # 本日时间记录
            channel_info = {}

            match_player_times = 0
            match_primary_times = 0  # 金币消耗
            match_middle_times = 0  # 换牌消耗
            match_high_times = 0
            match_ticket_cost = 0  # 门票消耗
            match_reward = 0

            for channelid in ls:
                kvs = Context.Stat.get_day_data(channelid, fmt)  # 获取当天数据记录
                if len(kvs) == 0:  # 没有记录
                    continue

                for k, v in kvs.iteritems():
                    if k in ['match_quick_player']:
                        match_player_times += int(v)
                    if k in ['match_quick_1']:
                        match_primary_times += int(v)
                    if k in ['match_quick_2']:
                        match_middle_times += int(v)
                    if k in ['match_quick_3']:
                        match_high_times += int(v)

                    if k in ['match_ticket_chip']:
                        match_ticket_cost += int(v)
                    if k in ['match_reward_chip']:
                        match_reward += int(v)


            channel_info['match_player_times'] = str(match_player_times)
            channel_info['match_primary_times'] = str(match_primary_times)
            channel_info['match_middle_times'] = str(match_middle_times)
            channel_info['match_high_times'] = str(match_high_times)
            channel_info['match_ticket_cost'] = str(match_ticket_cost)
            channel_info['match_reward'] = str(match_reward)

            if len(channel_info) > 0:
                day_info.update({fmt: channel_info})
                count_info.append(day_info)

            start_day = Time.next_days(start_day)
        mo.set_param("ret", count_info)
        return mo

HttpShell = HttpShell()
