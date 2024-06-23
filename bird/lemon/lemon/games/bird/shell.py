#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-03-03

import re
import datetime
from props import BirdProps
from account import BirdAccount
from mail import Mail
from sdk.const import Const
from sdk.modules.entity import Entity
from sdk.modules.account import Account
from framework.context import Context
from framework.util.tool import Time
from framework.util.tool import Tool
from framework.entity.msgpack import MsgPack
from framework.entity.const import Message
from framework.entity.manager import TaskManager
import random, copy
from sdk.lib.yuntongxun import CCPRestSDK
from lemon.games.bird.entity import BirdEntity
from lemon.games.bird.red_packet import Red_Packet
from newactivity import *
from giftactivity import *


class BirdShell(object):
    def __init__(self):
        self.special_json_path = {
            # gm
            '/v2/shell/query/data_summary': self.data_summary,  # 数据汇总
            '/v1/shell/gm/getMVerifyCode': self.getMVerifyCode,  # 获取手机验证码
        }

        self.json_path = {
            # gm
            '/v2/shell/query/overview': self.query_overview,            #数据汇总
            # '/v1/shell/gm/reward/card': self.gm_reward_card,
            # '/v1/shell/gm/reward/prop': self.gm_reward_prop,
            #'/v1/shell/gm/exchange/phone': self.gm_exchange_phone,
            #'/v1/shell/gm/poke_mole/chip': self.gm_poke_mole_chip,
            #'/v1/shell/gm/account/block': self.gm_account_block,
            #'/v1/shell/gm/village/can_buy': self.gm_village_can_buy,
            #'/v1/shell/query/history/phone': self.query_history_phone,
            # '/v1/shell/query/shit/consume': self.query_shit_consume,
            # '/v1/shell/query/shit/produce': self.query_shit_produce,
            # '/v1/shell/query/props/egg/fall': self.query_egg_fall,
            #'/v1/shell/query/room/211': self.query_room_211,  #
            # '/v1/shell/gm/group_buy/modify_num': self.gm_modify_groupbuy_num,
            #'/v1/shell/query/coupon_event': self.coupon_event,  # 鸟卷事件
            # 微信
            #'/v1/shell/weixin/user/bind': self.wechat_bind,
            #'/v1/shell/weixin/user/unbind': self.wechat_unbind,
            #'/v1/shell/weixin/user/modify/password': self.wechat_modify_password,

            # 公告测试接口
            # '/v1/shell/gm/bulletin/info': self.gm_push_info,
            '/v1/shell/gm/special/red_packet': self.send_special_packet_info,  # 红包接口
            '/v1/shell/gm/special/remove_red_packet': self.remove_special_packet,  # 删除定时红包

            '/v1/shell/gm/reward/vip': self.gm_reward_vip,                # 赠送vip  暂时保留
            '/v1/shell/query/chip/consume': self.query_chip_consume,      # 金币消耗  待定
            '/v1/shell/query/chip/produce': self.query_chip_produce,      # 金币产出  待定
            '/v1/shell/query/diamond/consume': self.query_diamond_consume,  # 钻石消耗 待定
            '/v1/shell/query/diamond/produce': self.query_diamond_produce,  # 钻石产出 待定
            '/v1/shell/update/shop_info': self.update_shop_info,            # 商城更新
            '/v1/shell/shop/exchange_record': self.exchange_record,         # 商城兑换记录
            '/v1/shell/query/shot': self.query_shot,                        # 发炮统计
            '/v1/shell/query/raffle': self.query_raffle,                    # 抽奖统计
            '/v1/shell/query/pay/detail': self.query_pay_detail,            # 销售明细
            '/v1/shell/gm/reward/add_notice': self.gm_add_notice,           # 增加公告板
            '/v1/shell/gm/reward/add_mail': self.gm_add_mail,               # 增加邮件
            '/v1/shell/gm/getMVerifyCode': self.getMVerifyCode,             # 获取手机验证码
            '/v1/shell/gm/modifyDropCoupon': self.modifyDropCoupon,
            '/v1/shell/gm/barrel_pool_config': self.get_barrel_pool_config,       # 获取炮倍配置
            #'/v1/shell/gm/alter_barrel_pool_config': self.alter_barrel_pool_config,  #修改炮倍配
            '/v1/shell/query/all_player_data': self.all_player_data,        # 获取所有玩家信息
            '/v1/shell/gm/account/freeze': self.freeze_user,                # 冻结
            '/v1/shell/limit_shop_open': self.limit_shop_open,              # 限时商城的开启和关闭
			'/v1/shell/gm/get_red_packet_info': self.get_red_packet_info,   # 获取发红包信息
            '/v1/shell/raffle_open': self.limit_raffle_open,                # 奖金抽奖的开启和关闭
            '/v2/shell/gm/recharge/add_gift': self.recharge_add_gift,       # 充值加赠
            '/v2/shell/gm/recharge/get_add':self.get_recharge_add,          # 获取充值加赠配置
            '/v2/shell/shop/many_approve_status': self.alter_many_approve_status,  # 修改多个审核状态

            #------------------------------------活动-------------------------------------
            '/v2/shell/shop/first_recharge_query': self.first_recharge_query,
            '/v2/shell/shop/first_recharge_modify': self.first_recharge_modify,

            '/v2/shell/shop/vip_activity_query': self.vip_activity_query,
            '/v2/shell/shop/vip_activity_modify': self.vip_activity_modify,

            '/v2/shell/shop/save_money_activity_query': self.save_money_activity_query,
            '/v2/shell/shop/save_money_activity_modify': self.save_money_activity_modify,

            '/v2/shell/wx/new_player_gift':self.wx_new_player_activity_query,
            '/v2/shell/wx/new_player_modify': self.wx_new_player_activity_modify,
            # ------------------------------------活动-------------------------------------

            '/v2/shell/year_monster_pool_query': self.year_monster_pool_query,
            '/v2/shell/year_monster_pool_modify': self.year_monster_pool_modify,

            '/v2/shell/gm/broadcast_set': self.gm_broadcast_set,    # 服务器广播设置
            '/v2/shell/gm/broadcast_query': self.gm_broadcast_query,  # 服务器广播查询
            '/v2/shell/gm/account/set_kill_chip': self.set_kill_chip,  # 收分
            '/v2/shell/gm/account/set_give_chip': self.set_give_chip,  # 送分

            '/v2/shell/get_shop_tips': self.get_shop_tips,          #获取商城tips
            '/v2/shell/modify_shop_tips': self.modify_shop_tips,    #修改商城tips

            '/v2/shell/background/query_account_exist': self.query_account_exist,  #查询用户id是否存在
            '/v2/shell/receive_new_player_gift': self.receive_new_player_gift,

            '/v2/shell/background/get_channel_list':self.get_channel_list,
            '/v2/shell/get_product_list': self.get_product_list,

            '/v2/shell/activity/happy_shake':self.happy_shake,
            '/v2/shell/activity/pay_rank': self.pay_rank,
            '/v2/shell/activity/gift_box': self.gift_box,
            '/v2/shell/activity/total_pay': self.total_pay,

            '/v2/game/product/update_picture_version': self.update_picture_version,
            '/v2/game/config/update_match_config': self.match_config,
            '/v2/game/config/update_smart_game_config': self.smart_game_config,
            '/v2/shell/gm/reward/get_notice': self.gm_notice_config,  # 获取公告板

            '/v2/shell/activity/old_config':self.old_config, #老配置的修改
            '/v2/shell/activity/point_shop':self.point_shop,
            '/v2/shell/activity/gift_shop': self.gift_shop,

            '/v2/shell/activity/smash_egg':self.smash_egg,
            '/v2/shell/month_card':self.month_card,
            '/v2/shell/activity/dragon_boat': self.dragon_boat,
            '/v2/shell/gm/chip_pool_config': self.chip_pool_config,
            '/v2/shell/query_new_player_overview': self.new_player_overview, #新玩家总览
            '/v2/shell/gm/data_summarizing': self.data_summarizing,  # 新数据汇总
            '/v2/shell/gm/getMVerify_Messages': self.getMVerify_Messages,  #玩家短信通知
            '/v2/shell/gm/activity_user_rank': self.activity_user_rank,  # 炮王之王排行榜
            '/v2/shell/gm/activity_day_rank': self.activity_day_rank,  # 炮王之王当天数据
            '/v2/shell/gm/deal_coupon_info': self.deal_coupon_info,  # 当天鸟券汇总
        }

    def deal_coupon_info(self, gid, mi, request):
        period_data = {}
        start_day = Time.str_to_datetime(str(mi.get_param('start')), '%Y-%m-%d')
        end_day = Time.str_to_datetime(str(mi.get_param('end')), '%Y-%m-%d')
        deal_user = mi.get_param('user_list')
        while start_day <= end_day:
            everyday = {}
            days = Time.datetime_to_str(start_day, '%Y-%m-%d')
            user_list = Context.RedisCluster.hget_keys('user:*')
            if not user_list:
                return MsgPack.Error(0, 2, 'not exist')

            for user_str in user_list:
                user_id = int(user_str.split(':')[1])
                if user_id not in deal_user:
                    channel_id = Context.Data.get_attr(user_id, 'channelid')
                    target_coupon = Context.Data.get_game_attr_int(user_id, gid, 'target_coupon', 0)
                    chip = Context.Data.get_game_attr_int(user_id, gid, 'chip', 0)
                    coupon = Context.Data.get_game_attr_int(user_id, gid, 'coupon', 0)
                    pay_total = int(Context.Data.get_game_attr_int(user_id, gid, 'pay_total', 0))

                    if pay_total >= 50:
                        day_pay_total, weixin, alipay, cdkey_pay, sdk_pay, gm_pay = 0, 0, 0, 0, 0, 0
                        player_info, in_chip, out_chip, in_coupon, in_target_coupon = {}, 0, 0, 0, 0
                        user_day = Context.RedisStat.hash_getall('user_daily:{}:{}:{}'.format(channel_id, days, user_id))
                        if len(user_day) > 0:
                            for key, value in user_day.items():
                                # 获取今日充值
                                if key.endswith('{}.pay.user.pay_total'.format(channel_id)):
                                    day_pay_total = int(value)

                                # 微信
                                if key.startswith('{}.weixin_pay.user.pay_total'.format(channel_id)):
                                    weixin = int(value)

                                # 支付宝
                                elif key.startswith('{}.ali_pay.user.pay_total'.format(channel_id)):
                                    alipay = int(value)

                                # 兑换码
                                elif key.startswith('{}.cdkey_pay.user.pay_total'.format(channel_id)):
                                    cdkey_pay = int(value)

                                # sdk
                                elif key.startswith('{}.sdk_pay.user.pay_total'.format(channel_id)):
                                    sdk_pay = int(value)

                                # gm充值额度
                                elif key.startswith('{}.gm_pay.user.pay_total'.format(channel_id)):
                                    gm_pay = int(value)

                                if key.startswith('in.chip.') and not key.startswith('in.chip.catch.bird.'):
                                    player_info[key] = int(player_info.get(key, 0)) + int(value)
                                    in_chip += int(value)

                                if key.startswith('in.coupon.'):
                                    player_info[key] = int(player_info.get(key, 0)) + int(value)
                                    in_coupon += int(value)

                                if key.startswith('in.target_coupon.'):
                                    player_info[key] = int(player_info.get(key, 0)) + int(value)
                                    in_target_coupon += int(value)

                        if days == Time.current_time("%Y-%m-%d"):
                            surplus_coupon, surplus_chip, surplus_target = coupon, chip, target_coupon
                            last_time = Time.yesterday_time(Time.str_to_timestamp(days, "%Y-%m-%d"))
                            last_chip = self.calc_chip(last_time, channel_id, user_id, "fix_own_chip")
                            out_chip = last_chip + in_chip - surplus_chip
                        else:
                            surplus_coupon = self.calc_coupon(user_id, coupon, days)
                            surplus_chip = self.calc_chip(days, channel_id, user_id, "fix_own_chip")
                            surplus_target = self.calc_target_coupon(user_id, target_coupon, days)
                            last_time = Time.yesterday_time(Time.str_to_timestamp(days, "%Y-%m-%d"))
                            last_chip = self.calc_chip(last_time, channel_id, user_id, "fix_own_chip")
                            out_chip = last_chip + in_chip - surplus_chip

                        player_info.update({"weixin_pay_total": weixin, "ali_pay_total": alipay, "cdkey_pay_total": cdkey_pay,
                                            "sdk_pay_total": sdk_pay, "gm_pay_total": gm_pay})

                        player_info.update({"day_pay_total": day_pay_total, "channel": channel_id, "surplus_coupon": surplus_coupon,
                                            "surplus_chip": surplus_chip, "surplus_target": surplus_target})

                        player_info.update({"in_chip": in_chip, "out_chip": out_chip, "in_coupon": in_coupon,
                                            "in_target_coupon": in_target_coupon})
                        everyday[user_id] = player_info
                    else:
                        continue
                else:
                    continue
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

    def calc_chip(self, day_time, channel_id, user_id, key_name):
        result = Context.Stat.get_daily_user_data(channel_id, user_id, day_time)
        if result:
            if result.has_key("{}".format(key_name)):
                fix_own_info = int(result["{}".format(key_name)])
            else:
                fix_own_info = 0
        else:
            create_time = Context.Data.get_attr(user_id, 'createTime')[:10]
            if str(create_time) == str(day_time):
                fix_own_info = 0
            else:
                fix_own_info = 0
                start_day = Time.str_to_datetime(day_time, '%Y-%m-%d')
                end_day = Time.str_to_datetime(create_time[:10], '%Y-%m-%d')
                while start_day >= end_day:
                    fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
                    result = Context.Stat.get_daily_user_data(channel_id, user_id, fmt)
                    if result:
                        if result.has_key("{}".format(key_name)):
                            fix_own_info = int(result["{}".format(key_name)])
                            break
                        else:
                            start_day = Time.prev_days(start_day)
                            continue
                    else:
                        start_day = Time.prev_days(start_day)
                        continue
        return fix_own_info

    def calc_target_coupon(self, uid, target_surplus, day_time):
        channel_id = Context.Data.get_attr(int(uid), 'channelid')
        i = 0
        while True:
            day_date = Time.str_to_datetime(Time.current_time("%Y-%m-%d"), "%Y-%m-%d")
            fmt = (day_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            # 靶场小游戏消耗
            out_target = Context.RedisStat.hash_get('user_daily:{}:{}:{}'.format(channel_id, fmt, uid), "out.target_coupon.target.room.consume")
            user_day = Context.RedisStat.hash_getall('user_daily:{}:{}:{}'.format(channel_id, fmt, uid))
            in_target_coupon = 0
            if len(user_day) > 0:
                for key, value in user_day.items():
                    if key.startswith('in.target_coupon.'):
                        in_target_coupon += int(value)
            else:
                in_target_coupon = 0

            last_time = Time.yesterday_time(Time.str_to_timestamp(fmt, "%Y-%m-%d"))
            if out_target:
                target_surplus = (target_surplus + int(out_target)) - in_target_coupon
            else:
                target_surplus = (target_surplus + 0) - in_target_coupon
            if last_time == day_time or last_time == "2018-12-27":
                break
            else:
                i = i - 1
        return target_surplus

    def activity_day_rank(self, gid, mi, request):
        start = str(mi.get_param('start'))
        end = str(mi.get_param('end'))

        period_data, player_list = {}, []
        rank_config = Context.Configure.get_game_item_json(gid, 'activity.rank.config')
        r_len = rank_config["level"]
        level = r_len[len(r_len) - 1][len(r_len[len(r_len) - 1]) - 1]
        rank = self.get_out_chip_rank(start, end, level)
        for uid, chip in rank:
            player_list.append(uid)

        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        while start_day <= end_day:
            day_pay, day_coupon, day_weixin_pay, day_ali_pay, rank_pay, rank_coupon, rank_weixin_pay, rank_ali_pay, everyday = 0, 0, 0, 0, 0, 0, 0, 0, {}
            days = Time.datetime_to_str(start_day, '%Y-%m-%d')
            user_list = Context.RedisStat.hget_keys('user_daily:*:{}:*'.format(days))
            for user_str in user_list:
                user_id = int(user_str.split(':')[3])
                channel = Context.Data.get_attr(user_id, 'channelid')
                if user_id not in player_list:
                    user_day = Context.RedisStat.hash_getall('user_daily:{}:{}:{}'.format(channel, days, user_id))
                    for k, v in user_day.items():
                        # 今日鸟券产出
                        if k.startswith('in.coupon.'):  # in.coupon.activity.rank.get
                            day_coupon += int(v)

                        # 获取今日充值
                        if k.endswith('{}.pay.user.pay_total'.format(channel)):
                            day_pay += int(v)

                        # 微信充值额度
                        if k.startswith('{}.weixin_pay.user.pay_total'.format(channel)):
                            day_weixin_pay = int(v)

                        # 支付宝充值额度
                        if k.startswith('{}.ali_pay.user.pay_total'.format(channel)):
                            day_ali_pay = int(v)
                else:
                    user_day = Context.RedisStat.hash_getall('user_daily:{}:{}:{}'.format(channel, days, user_id))
                    for k, v in user_day.items():
                        # 今日鸟券产出
                        if k.startswith('in.coupon.'):
                            rank_coupon += int(v)

                        # 获取今日充值
                        if k.endswith('{}.pay.user.pay_total'.format(channel)):
                            rank_pay += int(v)

                        # 微信充值额度
                        if k.startswith('{}.weixin_pay.user.pay_total'.format(channel)):
                            rank_weixin_pay = int(v)

                        # 支付宝充值额度
                        if k.startswith('{}.ali_pay.user.pay_total'.format(channel)):
                            rank_ali_pay = int(v)

            everyday.update({"day_pay": day_pay, "day_coupon": day_coupon, "rank_pay": rank_pay, "rank_coupon": rank_coupon,
                             "day_weixin_pay": day_weixin_pay, "day_ali_pay": day_ali_pay, "rank_weixin_pay": rank_weixin_pay, "rank_ali_pay": rank_ali_pay,
                             })
            period_data[days] = everyday
            start_day = Time.next_days(start_day)

        mo = MsgPack(0)
        mo.set_param('day', period_data)
        return mo

    def activity_user_rank(self, gid, mi, request):
        start = str(mi.get_param('start'))
        end = str(mi.get_param('end'))

        user_list = []
        rank_config = Context.Configure.get_game_item_json(gid, 'activity.rank.config')
        r_len = rank_config["level"]
        level, reward = r_len[len(r_len) - 1][len(r_len[len(r_len) - 1]) - 1], rank_config["reward"]

        rank = self.get_out_chip_rank(start, end, level)
        player_list, rid = [], 0
        for uid, point in rank:
            if rid <= level:
                for index_list in r_len:
                    if rid + 1 in index_list:
                        player_info = {}
                        nick = Context.Data.get_attr(int(uid), 'nick')
                        channel_id = Context.Data.get_attr(int(uid), 'channelid')
                        player_info.update({"nick": nick, "uid": uid, "channel": channel_id, "point": int(point), "reward": reward[rid]})
                        player_list.append(player_info)
                rid = rid + 1
            else:
                break

        for user in player_list:
            period_pay, period_coupon = 0, 0
            uid, channel = user["uid"], user["channel"]
            start_day = Time.str_to_datetime(start, '%Y-%m-%d')
            end_day = Time.str_to_datetime(end, '%Y-%m-%d')
            while start_day <= end_day:
                fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
                user_day = Context.RedisStat.hash_getall('user_daily:{}:{}:{}'.format(channel, fmt, uid))
                for k, v in user_day.items():
                    # 今日鸟券产出
                    if k.startswith('in.coupon.'):  # in.coupon.activity.rank.get
                        period_coupon += int(v)

                    # 获取今日充值
                    if k.startswith('{}.pay.user.pay_total'.format(channel)):
                        period_pay += int(v)

                start_day = Time.next_days(start_day)
            user.update({"period_pay": period_pay, "period_coupon": period_coupon})
            user_list.append(user)

        mo = MsgPack(0)
        mo.set_param('user', user_list)
        return mo

    def get_out_chip_rank(self, start, end, num):
        user_info = {}
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            daily_str = Context.RedisStat.hget_keys('user_daily:*:{}:*'.format(fmt))
            for user_str in daily_str:
                in_chip = 0
                user_id = int(user_str.split(':')[3])
                channel = user_str.split(':')[1]
                user_day = Context.RedisStat.hash_getall('user_daily:{}:{}:{}'.format(channel, fmt, user_id))
                for k, v in user_day.items():
                    # 洗码量
                    if k.startswith('out.chip.game.shot.bullet.'):
                        in_chip += int(v)

                user_info[user_id] = user_info.get(user_id, 0) + in_chip
            start_day = Time.next_days(start_day)

        rank = sorted(user_info.iteritems(), key=lambda x: int(x[1]), reverse=True)
        return rank[:num]

    def data_summarizing(self, gid, mi, request):
        Context.Log.debug("gm_data_summarizing:", mi)
        Context.Record.add_record_gm_data_summarizing(mi)

        start = str(mi.get_param('start'))
        end = str(mi.get_param('end'))
        # channel = str(mi.get_param('channel_id'))
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')

        day_info = []
        channel_dict = Context.Configure.get_game_item_json(gid, 'channel.path.config')
        all_channel = channel_dict.keys()[1:]

        while start_day <= end_day:
            channel_data = []
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            now_time = Time.current_time("%Y-%m-%d")
            
            new_user_count = 0
            for channel in all_channel:
                if channel.encode('utf-8') == "1000":
                    
                    channel_list = channel_dict.keys()[2:]
                    all_info = {}
                    for channel_id in channel_list:
                        channel_info = self.get_each_channel_data(fmt,channel_id)
                        for channelKey, channelValue in channel_info.items():
                            if channelKey != 'day_time' and channelKey != 'channel' and channelKey != 'ltv1' and channelKey != "ltv2" and channelKey != "ltv3" and channelKey != "ltv4" and channelKey != "ltv5" \
                                    and channelKey != "ltv7" and channelKey != "ltv15" and channelKey != "ltv30" and channelKey != "ltv60" and channelKey != "ltv90" and channelKey != "ltv120":
                                all_info.update({channelKey: int(all_info.get(channelKey, 0)) + int(channelValue)})
                    # if now_time == fmt:
                    #     ltv1, ltv2, ltv3, ltv4, ltv5, ltv6, ltv7, ltv15, ltv30, ltv60, ltv90, ltv120 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                    # else:
                    #     ltv1, ltv2, ltv3,ltv4, ltv5 = self.get_ltv(fmt,1), self.get_ltv(fmt,2), self.get_ltv(fmt,3), self.get_ltv(fmt,4), self.get_ltv(fmt,5)
                    #     ltv7, ltv15, ltv30,ltv60 = self.get_ltv(fmt,7), self.get_ltv(fmt,15), self.get_ltv(fmt,30), self.get_ltv(fmt,60)
                    #     ltv90, ltv120 = self.get_ltv(fmt, 90), self.get_ltv(fmt, 120)
                    ltv1, ltv2, ltv3, ltv4, ltv5, ltv6, ltv7, ltv15, ltv30, ltv60, ltv90, ltv120 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                    all_info['ltv1'], all_info['ltv2'], all_info['ltv3'] = ltv1, ltv2, ltv3
                    all_info['ltv4'], all_info['ltv5'], all_info['ltv7'] = ltv4, ltv5, ltv7
                    all_info['ltv15'], all_info['ltv30'], all_info['ltv60'] = ltv15, ltv30, ltv60
                    all_info['ltv90'], all_info['ltv120'] = ltv90, ltv120
                    all_info['all_new_user'] = int(all_info["new_user_count"])
                else:
                    all_info = self.get_each_channel_data(fmt,channel)
                    if len(all_info) != 0:
                        new_user_count += int(all_info.get("new_user_count",0))
                        all_info["all_new_user"] = new_user_count

                if len(all_info) > 0:
                    channel_data.append({channel:all_info})
            day_info.append({fmt:channel_data})
            start_day = Time.next_days(start_day)

        mo = MsgPack(0)
        mo.set_param('info', day_info)
        return mo

    def get_each_channel_data(self,fmt,channel):
        channel_info = {}
        result = Context.Stat.get_day_data(channel, fmt)  # 获取当天数据记录
        if len(result) != 0:  # 没有数据
            channel_info["sdk_pay_total"] = result.get('{}.sdk_pay.user.pay_total'.format(channel), 0)
            channel_info["weixin_pay_total"] = result.get('{}.weixin_pay.user.pay_total'.format(channel), 0)
            channel_info["ali_pay_total"] = result.get('{}.ali_pay.user.pay_total'.format(channel), 0)
            channel_info["cdkey_pay_total"] = result.get('{}.cdkey_pay.user.pay_total'.format(channel), 0)

            channel_info["daily.pay.active.player"] = result.get('daily.pay.active.player', 0)  # 当日付费活跃
            channel_info["new_user_count"] = result.get('{}.new.user.count'.format(channel), 0)  # 新增人数
            channel_info["login_user_count"] = result.get('{}.login.user.count'.format(channel), 0)  # 活跃总数
            channel_info['pay_user_count'] = result.get('{}.pay.user.count'.format(channel), 0)  # 付费人数
            channel_info['user_pay_times'] = result.get('{}.user.pay.times'.format(channel), 0)  # 付费次数
            channel_info['pay_user_total'] = result.get('{}.pay.user.pay_total'.format(channel), 0)  # 付费额度

            new_pay_user_count, new_pay_user_times, new_pay_user_total = 0, 0, 0
            new_user_list = self.get_new_pay_data(fmt, channel)

            now_time = Time.current_time("%Y-%m-%d")

            for uid in new_user_list:
                channel_id = Context.Data.get_attr(int(uid), 'channelid')
                pay_total = Context.RedisStat.hash_get('user_daily:{}:{}:{}'.format(channel_id, fmt, uid),"{}.pay.user.pay_total".format(channel_id))
                if pay_total:
                    user_pay = int(pay_total)
                else:
                    user_pay = 0
                new_pay_user_total += user_pay

                count_number = Context.RedisStat.hash_get('user_daily:{}:{}:{}'.format(channel_id, fmt, uid),"{}.pay.user.count".format(channel_id))
                if count_number:
                    user_count = int(count_number)
                else:
                    user_count = 0
                new_pay_user_count += user_count

                times_number = Context.RedisStat.hash_get('user_daily:{}:{}:{}'.format(channel_id, fmt, uid),"{}.user.pay.times".format(channel_id))
                if times_number:
                    pay_times = int(times_number)
                else:
                    pay_times = 0
                new_pay_user_times += pay_times

            channel_info['new_pay_user_count'] = new_pay_user_count  # 新增付费人数
            channel_info['new_pay_user_times'] = new_pay_user_times  # 新增付费总次数
            channel_info['new_pay_user_total'] = new_pay_user_total  # 新增付费总额度

            # if now_time == fmt:
            #     login_level_1, login_level_2, login_level_3, login_level_4 = 0,0,0,0
            #     ltv1,ltv2,ltv3,ltv4,ltv5,ltv6,ltv7,ltv15,ltv30,ltv60,ltv90,ltv120 = 0,0,0,0,0,0,0,0,0,0,0,0
            # else:
            #     login_level_1, login_level_2, login_level_3, login_level_4 = self.get_login_level(channel, fmt)
            #     ltv1,ltv2,ltv3 = self.get_ltv(fmt,1,channel),self.get_ltv(fmt,2,channel),self.get_ltv(fmt,3,channel)
            #     ltv4, ltv5, ltv7 = self.get_ltv(fmt, 4, channel), self.get_ltv(fmt, 5, channel), self.get_ltv(fmt, 7,channel)
            #     ltv15, ltv30, ltv60 = self.get_ltv(fmt, 15, channel), self.get_ltv(fmt, 30, channel), self.get_ltv(fmt, 60,channel)
            #     ltv90, ltv120 = self.get_ltv(fmt, 90, channel), self.get_ltv(fmt, 120, channel)

            login_level_1, login_level_2, login_level_3, login_level_4 = 0, 0, 0, 0
            ltv1, ltv2, ltv3, ltv4, ltv5, ltv6, ltv7, ltv15, ltv30, ltv60, ltv90, ltv120 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            # 新增次留、新增三留
            channel_info['login_level_1'],channel_info['login_level_2'] = login_level_1,login_level_2
            # 新增七留、新增三十留
            channel_info['login_level_3'],channel_info['login_level_4'] = login_level_3,login_level_4

            channel_info['ltv1'],channel_info['ltv2'],channel_info['ltv3'] = ltv1,ltv2,ltv3
            channel_info['ltv4'],channel_info['ltv5'],channel_info['ltv7'] = ltv4, ltv5, ltv7
            channel_info['ltv15'],channel_info['ltv30'],channel_info['ltv60'] = ltv15, ltv30, ltv60
            channel_info['ltv90'],channel_info['ltv120'] = ltv90,ltv120
            
        return  channel_info


    def get_ltv(self,day_time,days,channel=None):
        if channel !=None:
            user_list = self.get_new_pay_data(day_time,channel)
        else:
            user_list = self.get_new_pay_data(day_time)
        user_count = len(user_list)
        user_total = 0
        for i in range(0, days):
            fmt = (Time.str_to_datetime(day_time, "%Y-%m-%d") + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            for uid in user_list:
                channel_id = Context.Data.get_attr(int(uid), 'channelid')
                pay_total = Context.RedisStat.hash_get('user_daily:{}:{}:{}'.format(channel_id, fmt, uid), "{}.pay.user.pay_total".format(channel_id))
                if pay_total:
                    user_pay = int(pay_total)
                else:
                    user_pay = 0
                user_total += user_pay
        if user_count == 0:
            ltv = 0.0
        else:
            ltv = round(user_total / float(user_count),2)
        return ltv

    def get_new_pay_data(self,day_time,channel=None):
        user_list = []
        start_stamp = Time.str_to_timestamp(day_time + " 00:00:00")
        end_stamp = Time.str_to_timestamp(day_time + " 23:59:59")
        if channel !=None:
            user_info = Context.RedisStat.hget_keys('user_daily:{}:{}:*'.format(channel, day_time))
        else:
            user_info = Context.RedisStat.hget_keys('user_daily:*:{}:*'.format(day_time))
        for user_str in user_info:
            user_id = int(user_str.split(':')[3])
            if user_id > 1000000:
                channel_id = Context.Data.get_attr(user_id, 'channelid')
                create_stamp = Time.str_to_timestamp(str(Context.Data.get_attr(user_id, 'createTime'))[:19])
                online = Context.RedisStat.hash_get('user_daily:{}:{}:{}'.format(channel_id, day_time, str(user_id)), "login.times")
                if online and create_stamp >= start_stamp and create_stamp <= end_stamp and str(user_id) not in user_list:
                    user_list.append(user_id)
                else:
                    continue
            else:
                continue
        return user_list

    def get_login_level(self,channel_id,day_time):
        login_level_1,login_level_2,login_level_3,login_level_4 = 0,0,0,0
        user_list = Context.RedisStat.hget_keys('user_daily:{}:{}:*'.format(channel_id, day_time))
        player_list = []
        start_stamp = Time.str_to_timestamp(day_time + " 00:00:00")
        end_stamp = Time.str_to_timestamp(day_time + " 23:59:59")
        for user_str in user_list:
            user_id = int(user_str.split(':')[3])
            if user_id > 1000000:
                create_stamp = Time.str_to_timestamp(str(Context.Data.get_attr(user_id, 'createTime'))[:19])
                if create_stamp >= start_stamp and create_stamp <= end_stamp and str(user_id) not in player_list:
                    player_list.append(user_id)
                else:
                    continue
            else:
                continue

        for uid in player_list:
            login_level = self.login_level_info()
            for index, value in login_level.items():
                if index == 1:
                    days = 1
                    result = self.get_day_login_level(day_time,channel_id,uid,days)
                    login_level_1 += result
                if index == 2:
                    days = 3
                    result = self.get_day_login_level(day_time, channel_id, uid, days)
                    login_level_2 += result
                if index == 3:
                    days = 7
                    result = self.get_day_login_level(day_time, channel_id, uid, days)
                    login_level_3 += result
                if index == 4:
                    days = 30
                    result = self.get_day_login_level(day_time, channel_id, uid, days)
                    login_level_4 += result

        return login_level_1, login_level_2, login_level_3, login_level_4

    def get_day_login_level(self,day_time,channel_id,uid,days):
        for i in range(days, days+1):
            old_day = (Time.str_to_datetime(day_time, "%Y-%m-%d") + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            user_login = Context.RedisStat.hash_get('user_daily:{}:{}:{}'.format(channel_id, old_day, uid),"login.times")
            if user_login:
                return 1
            else:
                return 0

    def login_level_info(self):
        level = {
            1: 1,
            2: 3,
            3: 7,
            4: 30,
        }
        return level


    def total_pay(self, gid, mi, request):
        pid = mi.get_param('pid')
        if pid == 1:
            ret = TotalPayActivity.get_config()
        elif pid == 2:
            ret = TotalPayActivity.set_config(mi)
        return ret

    def gift_shop(self, gid, mi, request):
        pid = mi.get_param('pid')
        product_id = mi.get_param('product_id')
        conf = Shop.get_gift_config_from_db()
        send_msg = False
        info = mi.get_param('info')
        if pid == 1:
            if conf.has_key(str(product_id)):
                del conf[str(product_id)]
                Context.RedisActivity.set('gift_shop:product_config', Context.json_dumps(conf))
                send_msg = True

        else:
            if product_id == None or not conf.has_key(str(product_id)):
                if product_id == None:
                    max_gift_product_id = Context.RedisActivity.get('gift_shop:max_gift_product_id')
                    product_id = Tool.to_int(max_gift_product_id, 1000000)
                    Context.RedisActivity.set('gift_shop:max_gift_product_id', product_id + 1)

                conf[str(product_id)] = info
                Context.RedisActivity.set('gift_shop:product_config', Context.json_dumps(conf))
                send_msg = True

            else:
                info = mi.get_param('info')
                conf[product_id] = info
                Context.RedisActivity.set('gift_shop:product_config', Context.json_dumps(conf))
                send_msg = True

        if send_msg:
            mou = MsgPack(Message.MSG_SYS_NOTICE_CLIENT_GIFT_SHOP | Message.ID_ACK)
            Context.GData.broadcast_to_system(mou)

        mo = MsgPack(0)
        mo.set_param('pid', pid)
        mo.set_param('product_id', product_id)
        return mo

    def new_player_overview(self, gid, mi, request):
        ret = Context.RedisCluster.hget_keys('user:*')
        if not ret:
            return MsgPack.Error(0, 2, 'not exist')

        user_info, online = [], []
        query_info, channel, input_data = mi.get_param('query_info'), mi.get_param('channel'), mi.get_param('input_data')
        start_time, end_time = mi.get_param('start'), mi.get_param('end')

        if query_info == "online_player" or query_info == "pay_player":
            if query_info == "online_player":
                if channel == "0":
                    location = Context.RedisCache.hget_keys('location:2:*')
                    if not location:
                        return MsgPack.Error(0, 3, 'not online_user')

                    for item in location:
                        uid = item.split(':')[2]
                        play_recharge = self.pay_total_sort(uid, gid)
                        online.append(play_recharge)
                else:
                    location = Context.RedisCache.hget_keys('location:2:*')
                    if not location:
                        return MsgPack.Error(0, 3, 'not online_user')

                    for item in location:
                        uid = item.split(':')[2]
                        play_recharge = self.pay_total_sort(uid, gid)
                        online.append(play_recharge)
            else:
                if channel == "0":
                    for item in ret:
                        uid = int(item.split(':')[1])
                        play_recharge = self.pay_total_sort(uid, gid)
                        online.append(play_recharge)
                else:
                    for item in ret:
                        uid = int(item.split(':')[1])
                        channel_id = Context.Data.get_attr(int(uid), 'channelid')
                        if channel == channel_id:
                            play_recharge = self.pay_total_sort(uid, gid)
                            online.append(play_recharge)
                        else:
                            continue

        elif query_info == "register_time" or query_info == "active_player" or query_info == "pay_active_player":
            if query_info == "register_time":
                player_list = []
                start_stamp = Time.str_to_timestamp(start_time + " 00:00:00")
                end_stamp = Time.str_to_timestamp(end_time + " 23:59:59")
                if channel == "0":
                    for item in ret:
                        user_id = int(item.split(':')[1])
                        create_stamp = Time.str_to_timestamp(str(Context.Data.get_attr(int(user_id), 'createTime'))[:19])
                        if create_stamp >= start_stamp and create_stamp <= end_stamp and user_id not in player_list:
                            player_list.append(user_id)
                            play_recharge = self.pay_total_sort(user_id, gid)
                            online.append(play_recharge)
                        else:
                            continue
                else:
                    for item in ret:
                        user_id = int(item.split(':')[1])
                        create_stamp = Time.str_to_timestamp(str(Context.Data.get_attr(user_id, 'createTime'))[:19])
                        channel_id = Context.Data.get_attr(user_id, 'channelid')
                        if channel == channel_id:
                            if create_stamp >= start_stamp and create_stamp <= end_stamp and user_id not in player_list:
                                player_list.append(user_id)
                                play_recharge = self.pay_total_sort(user_id, gid)
                                online.append(play_recharge)
                            else:
                                continue
                        else:
                            continue
            elif query_info == "active_player":
                player_list = []
                if channel == "0":
                    channel_dict = Context.Configure.get_game_item_json(gid, 'channel.path.config')
                    channel_info = channel_dict.keys()[2:]
                    start_day = Time.str_to_datetime(start_time, '%Y-%m-%d')
                    end_day = Time.str_to_datetime(end_time, '%Y-%m-%d')
                    while start_day <= end_day:
                        fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
                        for channel_id in channel_info:
                            user_list = Context.RedisStat.hget_keys('user_daily:{}:{}:*'.format(channel_id, fmt))
                            for user_str in user_list:
                                user_id = int(user_str.split(':')[3])
                                if user_id not in player_list:
                                    player_list.append(user_id)
                                    play_recharge = self.pay_total_sort(user_id, gid)
                                    online.append(play_recharge)
                                else:
                                    continue
                        start_day = Time.next_days(start_day)
                else:
                    start_day = Time.str_to_datetime(start_time, '%Y-%m-%d')
                    end_day = Time.str_to_datetime(end_time, '%Y-%m-%d')
                    while start_day <= end_day:
                        fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
                        user_list = Context.RedisStat.hget_keys('user_daily:{}:{}:*'.format(channel, fmt))
                        for user_str in user_list:
                            user_id = int(user_str.split(':')[3])
                            if user_id not in player_list:
                                player_list.append(user_id)
                                play_recharge = self.pay_total_sort(user_id, gid)
                                online.append(play_recharge)
                            else:
                                continue

                        start_day = Time.next_days(start_day)
            else:
                player_list = []
                if channel == "0":
                    channel_dict = Context.Configure.get_game_item_json(gid, 'channel.path.config')
                    channel_info = channel_dict.keys()[2:]
                    start_day = Time.str_to_datetime(start_time, '%Y-%m-%d')
                    end_day = Time.str_to_datetime(end_time, '%Y-%m-%d')
                    while start_day <= end_day:
                        fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
                        for channel_id in channel_info:
                            user_list = Context.RedisStat.hget_keys('user_daily:{}:{}:*'.format(channel_id, fmt))
                            for user_str in user_list:
                                user_id = int(user_str.split(':')[3])
                                pay_total = Tool.to_int(Context.Data.get_game_attr_int(int(user_id), gid, 'pay_total', 0))
                                if pay_total > 1 and user_id not in player_list:
                                    player_list.append(user_id)
                                    play_recharge = self.pay_total_sort(user_id, gid)
                                    online.append(play_recharge)
                                else:
                                    continue
                        start_day = Time.next_days(start_day)

                else:
                    start_day = Time.str_to_datetime(start_time, '%Y-%m-%d')
                    end_day = Time.str_to_datetime(end_time, '%Y-%m-%d')
                    while start_day <= end_day:
                        fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
                        user_list = Context.RedisStat.hget_keys('user_daily:{}:{}:*'.format(channel, fmt))
                        for user_str in user_list:
                            user_id = user_str.split(':')[3]
                            pay_total = Tool.to_int(Context.Data.get_game_attr_int(int(user_id), gid, 'pay_total', 0))
                            if pay_total > 1 and user_id not in player_list:
                                player_list.append(user_id)
                                play_recharge = self.pay_total_sort(user_id, gid)
                                online.append(play_recharge)
                            else:
                                continue
                        start_day = Time.next_days(start_day)
        else:
            if query_info == "uid" and input_data and start_time:
                if input_data.isdigit():
                    for item in ret:
                        user_id = int(item.split(':')[1])
                        if int(input_data) == user_id:
                            play_recharge = self.pay_total_sort(user_id, gid)
                            online.append(play_recharge)
                        else:
                            continue

            elif query_info == "nick" and input_data and start_time:
                for item in ret:
                    uid = int(item.split(':')[1])
                    query_date = Context.Data.get_attr(uid, str(query_info))
                    if str(input_data) == query_date:
                        play_recharge = self.pay_total_sort(uid, gid)
                        online.append(play_recharge)
                    else:
                        continue

            elif query_info == "uid" and input_data and start_time is None:
                if input_data.isdigit():
                    for item in ret:
                        user_id = int(item.split(':')[1])
                        if int(input_data) == user_id:
                            play_recharge = self.pay_total_sort(user_id, gid)
                            online.append(play_recharge)
                        else:
                            continue

            elif query_info == "nick" and input_data and start_time is None:
                for item in ret:
                    uid = int(item.split(':')[1])
                    query_date = Context.Data.get_attr(uid, str(query_info))
                    if str(input_data) == query_date:
                        play_recharge = self.pay_total_sort(uid, gid)
                        online.append(play_recharge)
                    else:
                        continue

            elif query_info == "phone" and input_data:
                for item in ret:
                    uid = int(item.split(':')[1])
                    query_date = Context.Data.get_attr(uid, "userName")
                    phone = Context.Data.get_shop_attr(uid, 'shop:user', 'phone')
                    if query_date == input_data or phone == input_data:
                        play_recharge = self.pay_total_sort(uid, gid)
                        online.append(play_recharge)
                    else:
                        continue
            # elif query_info == "promoter" and input_data:
            #     for item in ret:
            #         uid = int(item.split(':')[1])
            #         inviter = Context.Data.get_game_attr_int(uid, gid, 'inviter', 0)
            #         if inviter == inviter:
            #             play_recharge = self.pay_total_sort(uid, gid)
            #             online.append(play_recharge)
            else:
                player_list = []
                start_stamp = Time.str_to_timestamp(start_time + " 00:00:00")
                end_stamp = Time.str_to_timestamp(end_time + " 23:59:59")
                if channel == "0":
                    for item in ret:
                        user_id = int(item.split(':')[1])
                        create_stamp = Time.str_to_timestamp(
                            str(Context.Data.get_attr(int(user_id), 'createTime'))[:19])
                        if create_stamp >= start_stamp and create_stamp <= end_stamp and user_id not in player_list:
                            player_list.append(user_id)
                            play_recharge = self.pay_total_sort(user_id, gid)
                            online.append(play_recharge)
                        else:
                            continue
                else:
                    for item in ret:
                        user_id = int(item.split(':')[1])
                        create_stamp = Time.str_to_timestamp(str(Context.Data.get_attr(user_id, 'createTime'))[:19])
                        channel_id = Context.Data.get_attr(user_id, 'channelid')
                        if channel == channel_id:
                            if create_stamp >= start_stamp and create_stamp <= end_stamp and user_id not in player_list:
                                player_list.append(user_id)
                                play_recharge = self.pay_total_sort(user_id, gid)
                                online.append(play_recharge)
                            else:
                                continue
                        else:
                            continue
        for info in online:
            uid = int(info["uid"])
            result = self.new_player_info(uid, gid, start_time, end_time)
            if len(result) > 0:
                user_info.append(result)
            else:
                continue

        mo = MsgPack(0)
        mo.set_param("info", user_info)
        return mo

    def chip_pool_config(self, gid, mi, request):
        pid = mi.get_param('pid')
        if pid == 1:
            mo = self.get_chip_pool_config(gid, mi, request)#填分配置
        elif pid == 2:
            mo = self.alter_chip_fill_point(gid, mi, request) #修改填分配置
        elif pid == 3:
            mo = self.alter_chip_trigger_give(gid, mi, request) #修改赠送比
        else:
            return MsgPack.Error(0, 1, 'not exist pid')
        return mo

    def get_chip_pool_config(self, gid, mi, request):
        # tf add record
        Context.Log.debug("gm_get_chip_pool_config:", mi)
        Context.Record.add_record_get_chip_pool_config(mi)
        common_chip_pool = [] #普通鸟蛋池
        new_chip_pool = [] #新手鸟蛋池
        pool_play = Context.Configure.get_game_item_json(gid, 'barrel_pool_play_gift.config')

        # 处理统计数据
        channel_dict = Context.Configure.get_game_item_json(gid, 'channel.path.config')
        ls = channel_dict.keys()
        ls.sort()
        
        fmt = Time.datetime_to_str(Time.datetime(), '%Y-%m-%d')
        channel_info, new_channel = {}, {}
        for channel_id in ls:
            kvs = Context.Stat.get_day_data(channel_id, fmt)  #获取当天数据记录
            if len(kvs) == 0:  # 没有记录
                continue
            for k, v in kvs.iteritems():
                # 获取当前赠送状态
                if k.startswith('in.play_shot_gift_chip.'):
                    key_str = int(str(k).split('.')[2])
                    if key_str < 1000:
                        channel_info["in.play_shot_gift_chip.{}".format(key_str)] = channel_info.get("in.play_shot_gift_chip.{}".format(key_str), 0) + int(v)
                    else:
                        new_channel["in.play_shot_gift_chip.{}".format(key_str)] = new_channel.get("in.play_shot_gift_chip.{}".format(key_str), 0) + int(v)

        for pool_id, value in enumerate(pool_play["data"]): #普通玩家
            key = 'game.%d.info.play_shot_gift_pool' % gid
            key2 = 'pool.%d' % pool_id
            key3 = 'his_pool.%d' % pool_id
            key_gift = 'in.play_shot_gift_chip.%d' % pool_id
            pool_chip = Tool.to_int(Context.RedisMix.hash_get(key, key2, 0))
            his_pool_chip = Tool.to_int(Context.RedisMix.hash_get(key, key3, 0))
            value.update({"grade": pool_id,"pool_chip":pool_chip, 'his_pool_chip': his_pool_chip, 'play_shot_gift': channel_info.get(key_gift, 0)})
            common_chip_pool.append(value)

        for pool_id, value in enumerate(pool_play["new_p_data"]): #新手玩家
            new_pool_id = int(pool_id) + 1000
            key = 'game.{}.info.play_shot_gift_pool'.format(gid)
            key2 = 'pool.{}'.format(new_pool_id)
            key3 = 'his_pool.{}'.format(new_pool_id)
            key_gift = 'in.play_shot_gift_chip.{}'.format(new_pool_id)
            pool_chip = Tool.to_int(Context.RedisMix.hash_get(key, key2, 0))
            his_pool_chip = Tool.to_int(Context.RedisMix.hash_get(key, key3, 0))
            value.update({"new_grade": new_pool_id, "new_pool_chip": pool_chip, 'new_his_pool_chip': his_pool_chip, 'new_play_shot_gift': new_channel.get(key_gift, 0)})
            new_chip_pool.append(value)

        all_pool = {}
        key_kill = 'game.%d.info.kill_chip_pool' % gid
        key_give = 'game.%d.info.give_chip_pool' % gid
        kill_chip_total = 'kill_chip_total'  # 全服收分池
        give_chip_total = "give_chip_total"
        all_kill_pool = Tool.to_int(Context.RedisMix.hash_get(key_kill, kill_chip_total, 0))
        all_give_pool = Tool.to_int(Context.RedisMix.hash_get(key_give, give_chip_total, 0))
        all_pool.update({"all_kill_pool": all_kill_pool, "all_give_pool": all_give_pool})
        mo = MsgPack(0)
        mo.set_param('common_chip_pool', common_chip_pool)
        mo.set_param('new_chip_pool', new_chip_pool)
        mo.set_param('all_pool', all_pool)
        return mo

    def alter_chip_fill_point(self, gid, mi, request):
        # tf add record
        Context.Log.debug("gm_alter_chip_fillPoint:", mi)
        Context.Record.add_record_alter_chip_fill_point(mi)

        barrel_pool = mi.get_param('barrel_pool')
        fill = int(mi.get_param('fill'))
        if fill == 1:
            for pool_id, value in enumerate(barrel_pool):
                new_pool_id = int(pool_id) + 1000
                key = 'game.{}.info.play_shot_gift_pool'.format(gid)
                key2 = 'pool.{}'.format(new_pool_id)
                Context.RedisMix.hash_incrby(key, key2, value)
                key3 = 'his_pool.{}'.format(new_pool_id)  # 历史填分总额度
                Context.RedisMix.hash_incrby(key, key3, value)
        else:
            for pool_id, value in enumerate(barrel_pool):
                key = 'game.%d.info.play_shot_gift_pool' % gid
                key2 = 'pool.%d' % pool_id
                Context.RedisMix.hash_incrby(key, key2, value)
                key3 = 'his_pool.%d' % pool_id      # 历史填分总额度
                Context.RedisMix.hash_incrby(key, key3, value)
        mo = MsgPack(0)
        mo.set_param("ret", 0)
        return mo

    def alter_chip_trigger_give(self, gid, mi, request):
        # tf add record 修改赠送比
        Context.Log.debug("gm_alter_chip_trigger_give:", mi)
        Context.Record.add_record_alter_chip_trigger_give(mi)

        give = int(mi.get_param('give'))
        count_data = mi.get_param('count_data')
        barrel_pool_config = {}
        barrel_config = []
        pool_info = Context.Configure.get_game_item_json(gid, 'barrel_pool_play_gift.config')
        if give == 1:
            name = "new_p_data"
            def_name = "data"
            pool_data = pool_info["new_p_data"]
            new_pool_info = pool_info["data"]
        else:
            name = "data"
            def_name = "new_p_data"
            pool_data = pool_info["data"]
            new_pool_info = pool_info["new_p_data"]
            
        for barrel, give_data in zip(pool_data, count_data):
            barrel["triggle_count"] = int(give_data.get("triggle", 1))
            barrel["gift_count"] = int(give_data.get("gift", 1))
            barrel_config.append(barrel)

        barrel_pool_config.update({"{}".format(name): barrel_config, "{}".format(def_name): new_pool_info})

        from framework.helper import add_game_config
        add_game_config(gid, 'barrel_pool_play_gift.config', barrel_pool_config, True)
        # 数据库存储
        Context.RedisConfig.hash_set("configitem", "game:2:barrel_pool_play_gift.config", Context.json_dumps(barrel_pool_config))
        Context.RedisConfig.hash_set('configitem', 'update.time', Time.current_ts())
        Context.Configure.reload()

        cmd = Message.MSG_SYS_FILL_POINT | Message.ID_REQ
        Context.GData.send_to_entity(1000001, mi, cmd=cmd, gid=gid)


    def dragon_boat(self, gid, mi, request):
        Context.Log.info(mi)
        pid = mi.get_param('pid')
        if pid == 1:
            ret = DragonBoatActivity.query_dragon_boat(gid, mi, request)
        elif pid == 2:
            ret = DragonBoatActivity.modify_dragon_boat(gid, mi, request)
        elif pid == 3:
            ret = DragonBoatActivity.dragon_boat_pool_query(gid, mi, request)
        elif pid == 4:
            ret = DragonBoatActivity.dragon_boat_pool_modify(gid, mi, request)
        elif pid == 5:
            start_stamp = mi.get_param('start')
            end_stamp = mi.get_param('end')
            s = Time.str_to_timestamp(start_stamp)
            e = Time.str_to_timestamp(end_stamp)
            dat = DragonBoatActivity.get_activity_detail(s, e)
            ret = MsgPack(0)
            ret.set_param('ret', dat)
        else:
            return MsgPack.Error(0, 1, 'not exist pid')
        return ret

    def month_card(self, gid, mi, request):
        Context.Log.info(mi)
        pid = mi.get_param('pid')
        if pid == 1:
            ret = self.query_month_card(gid, mi, request)
        elif pid == 2:
            ret = self.modify_month_card(gid, mi, request)
        else:
            return MsgPack.Error(0, 1, 'not exist pid')
        return ret

    def query_month_card(self, gid, mi, request):
        mo = MsgPack(0)
        version = Context.RedisMix.hash_get_int('game.%d.background' % gid, 'month_card.max.version', 0)
        if version == 0:
            cnf = {}
        else:
            cnf = Context.RedisMix.hash_get_json('game:%d:month_card_version' % gid, str(version))
            if cnf == None: cnf = {}
        mo.set_param('ret', cnf)
        return mo

    def modify_month_card(self, gid, mi, request):
        modify_cnf = mi.get_param('ret')
        if not modify_cnf:
            return MsgPack.Error(0, 1, 'not modify config')
        Context.RedisMix.hash_setnx('game.%d.background' % gid, 'month_card.max.version', 1000)
        version = Context.RedisMix.hash_incrby('game.%d.background'%gid, 'month_card.max.version', 1)
        Context.RedisMix.hash_set('game:%d:month_card_version' % gid, str(version), Context.json_dumps(modify_cnf))
        return MsgPack(0)

    def smash_egg(self, gid, mi, request):
        pid = mi.get_param('pid')
        if pid == 1:
            ret = self.query_smash_egg(gid, mi, request)
        elif pid == 2:
            ret = self.modify_smash_egg(gid, mi, request)
        elif pid == 3:
            start_stamp = mi.get_param('start')
            end_stamp = mi.get_param('end')
            c = mi.get_param('channel')
            s = Time.str_to_timestamp(start_stamp)
            e = Time.str_to_timestamp(end_stamp)
            dat = SmashEggActivity.get_activity_detail(s, e, c)
            ret = MsgPack(0)
            ret.set_param('ret', dat)
        else:
            return MsgPack.Error(0, 1, 'not exist pid')
        return ret

    def query_smash_egg(self, gid, mi, request):
        mo = MsgPack(0)
        cnf = SmashEggActivity.activity_smash_egg_config()
        if cnf == None:cnf = {}
        mo.set_param('ret', cnf)
        return mo

    def modify_smash_egg(self, gid, mi, request):
        modify_cnf = mi.get_param('ret')

        if SmashEggActivity.judge_smash_egg_activity_open():
            cnf = SmashEggActivity.activity_smash_egg_config()
            if cnf.get('start') != modify_cnf.get('start'):
                return MsgPack.Error(0, 1, u'活动已开启，不可修改时间')

        Context.RedisActivity.set('smash_egg.activity.config', Context.json_dumps(modify_cnf))
        mou = MsgPack(Message.MSG_SYS_UPDATE_ACTIVITY_CONF | Message.ID_ACK)
        mou.set_param('model', 16)
        Context.GData.broadcast_to_system(mou)
        return MsgPack(0)

    def point_shop(self, gid, mi, request):
        pid = mi.get_param('pid')
        if pid == 1:
            ret = self.query_point_shop(gid, mi, request)
        elif pid == 2:
            ret = self.modify_point_shop(gid, mi, request)
        elif pid == 3:
            start_stamp = mi.get_param('start')
            end_stamp = mi.get_param('end')
            c = mi.get_param('channel')
            s = Time.str_to_timestamp(start_stamp)
            e = Time.str_to_timestamp(end_stamp)
            dat = PointShopActivity.query_background_point_shop_record(s, e, c)
            ret = MsgPack(0)
            ret.set_param('ret', dat)
        elif pid == 4:
            ret = self.query_shop_config(gid, mi, request)
        elif pid == 5:
            ret = self.modify_shop_config(gid, mi, request)
        elif pid == 6:
            ret = self.point_exchange_record(gid, mi, request)
        elif pid == 7:
            ret = self.alter_point_shop_status(gid, mi, request)
        elif pid == 8:
            ret = self.point_shopping_info(gid, mi, request)
        elif pid == 9:
            ret = self.point_shopping_state(gid, mi, request)
        else:
            return MsgPack.Error(0, 1, 'not exist pid')
        return ret

    def query_shop_config(self, gid, mi, request):
        mo = MsgPack(0)
        cnf = Shop.get_point_shop_config(gid)
        if cnf == None: cnf = {}
        mo.set_param('ret', cnf)
        return mo

    def modify_shop_config(self, gid, mi, request):
        product = mi.get_param('product_id')
        data = mi.get_param('d')
        cnf = Shop.get_point_shop_config(gid)
        if cnf == None: cnf = {}
        cnf[str(product)] = data

        Context.RedisConfig.hash_set("configitem", "game:2:point.shop.config", Context.json_dumps(cnf))
        Context.RedisConfig.hash_set('configitem', 'update.time', Time.current_ts())
        Context.Configure.reload()
        cmd = Message.MSG_SYS_UPDATE_POINT_SHOP_CONFIG | Message.ID_REQ
        mon = MsgPack(0)
        mon.set_param('cnf', cnf)
        Context.GData.send_to_entity(1000001, mon, cmd=cmd, gid=gid)

        return MsgPack(0)

    def query_point_shop(self, gid, mi, request):
        mo = MsgPack(0)
        cnf = PointShopActivity.activity_point_shop_config()
        if cnf == None:cnf = {}
        mo.set_param('ret', cnf)
        return mo

    def modify_point_shop(self, gid, mi, request):
        modify_cnf = mi.get_param('ret')

        if PointShopActivity.judge_point_shop_activity_open():
            cnf = PointShopActivity.activity_point_shop_config()
            if cnf.get('start') != modify_cnf.get('start'):
                return MsgPack.Error(0, 1, u'活动已开启，不可修改时间')

        Context.RedisActivity.set('point_shop.activity.config', Context.json_dumps(modify_cnf))
        mou = MsgPack(Message.MSG_SYS_UPDATE_ACTIVITY_CONF | Message.ID_ACK)
        mou.set_param('model', 15)
        Context.GData.broadcast_to_system(mou)
        return MsgPack(0)

    def gift_box(self, gid, mi, request):
        pid = mi.get_param('pid')
        if pid == 1:
            ret = GiftBox1Activity.query_gift_box(gid, mi)
        elif pid == 2:
            ret = GiftBox1Activity.update_gift_box_1(gid, mi)
        elif pid == 3:
            ret = GiftBox2Activity.query_gift_box(gid, mi)
        elif pid == 4:
            ret = GiftBox2Activity.update_gift_box_2(gid, mi)
        elif pid == 5:
            ret = GiftBox3Activity.query_gift_box(gid, mi)
        elif pid == 6:
            ret = GiftBox3Activity.update_gift_box_3(gid, mi)
        elif pid == 7:
            ret = GiftBox4Activity.query_gift_box(gid, mi)
        elif pid == 8:
            ret = GiftBox4Activity.update_gift_box_4(gid, mi)
        else:
            return MsgPack.Error(0, 1, 'not exist pid')
        return ret

    def smart_game_config(self,gid, mi ,request):
        Context.Log.debug('smart_game_config', mi)
        pid = mi.get_param('pid')
        if pid == 1:
            ret = self.query_fanfanle_config(gid, mi)
        elif pid == 2:
            ret = self.update_fanfanle_config(gid, mi)
        elif pid == 3:
            ret = self.query_target_config(gid, mi)
        elif pid == 4:
            ret = self.update_target_config(gid, mi)
        elif pid == 5:
            ret = self.query_rich_man_config(gid, mi)
        elif pid == 6:
            ret = self.update_rich_man_config(gid, mi)
        else:
            return MsgPack.Error(0, 1, 'not exist pid')
        return ret

    def query_rich_man_config(self, gid, mi):
        dat = BirdEntity.get_rich_man_open_config(gid)
        mo = MsgPack(0)
        mo.set_param('ret', dat)
        return mo

    def update_rich_man_config(self, gid, mi):
        open = mi.get_param('open')
        vip_limit = mi.get_param('vip_limit')
        dat = {'open': open, 'vip_limit': vip_limit}
        Context.RedisMix.hash_set('game.%d.background' % gid, 'rich_man.config', Context.json_dumps(dat))

        mo = MsgPack(Message.MSG_SYS_GET_GAME_OPEN | Message.ID_ACK)
        mo.set_param('sid', 3)
        mo.set_param('ret', dat)
        Context.GData.broadcast_to_system(mo)

        return MsgPack(0)

    def query_target_config(self, gid, mi):
        dat = BirdEntity.get_target_open_config(gid)
        mo = MsgPack(0)
        mo.set_param('ret', dat)
        return mo

    def update_target_config(self, gid, mi):
        open = mi.get_param('open')
        vlp = mi.get_param('vlp')
        vlm = mi.get_param('vlm')
        vlh = mi.get_param('vlh')
        if open is None or vlp is None or vlm is None or vlh is None:
            return MsgPack.Error(0, 1, 'param not exist')
        dat = {'open': open, 'vlp': vlp, 'vlm': vlm, 'vlh': vlh}
        Context.RedisMix.hash_set('game.%d.background' % gid, 'target.config', Context.json_dumps(dat))

        mo = MsgPack(Message.MSG_SYS_GET_GAME_OPEN | Message.ID_ACK)
        mo.set_param('sid', 1)
        mo.set_param('ret', dat)
        Context.GData.broadcast_to_system(mo)

        return MsgPack(0)

    def query_fanfanle_config(self, gid, mi):
        dat = BirdEntity.get_fanfanle_open_config(gid)
        mo = MsgPack(0)
        mo.set_param('ret', dat)
        return mo

    def update_fanfanle_config(self, gid, mi):
        open = mi.get_param('open')
        vip_limit = mi.get_param('vip_limit')
        if open is None or vip_limit is None:
            return MsgPack.Error(0, 1, 'param not exist')
        dat = {'open': open, 'vip_limit': vip_limit}
        Context.RedisMix.hash_set('game.%d.background' % gid, 'fanfanle.config', Context.json_dumps(dat))

        mo = MsgPack(Message.MSG_SYS_GET_GAME_OPEN | Message.ID_ACK)
        mo.set_param('sid', 2)
        mo.set_param('ret', dat)
        Context.GData.broadcast_to_system(mo)

        return MsgPack(0)

    def match_config(self, gid, mi, request):
        # dz add record
        # Context.Log.debug("gm_update_shop_info:", mi)
        # Context.Record.add_record_update_shop_info(mi)
        pid = mi.get_param('pid')
        if pid == 1:
            ret = self.query_normal_match_config(gid, mi)
        elif pid == 2:
            ret = self.update_normal_match_config(gid, mi)
        else:
            return MsgPack.Error(0, 1, 'not exist pid')
        return ret

    def query_normal_match_config(self, gid, mi):
        match_normal_config = Context.Configure.get_game_item_json(gid, 'match.normal.config')
        info = {}

        info['open'] = match_normal_config.get('open', 1)
        info['s1'] = match_normal_config.get('start_1', 1)
        info['e1'] = match_normal_config.get('end_1', 1)
        info['s2'] = match_normal_config.get('start_2', 1)
        info['e2'] = match_normal_config.get('end_2', 1)
        mo = MsgPack(0)
        mo.set_param('ret', info)
        return mo

    def update_normal_match_config(self, gid, mi):
        open = mi.get_param('open')
        s1 = int(mi.get_param('s1'))
        e1 = mi.get_param('e1')
        s2 = mi.get_param('s2')
        e2 = mi.get_param('e2')
        match_normal_config = Context.Configure.get_game_item_json(gid, 'match.normal.config')
        match_normal_config['open'] = open
        match_normal_config['start_1'] = s1
        match_normal_config['end_1'] = e1
        match_normal_config['start_2'] = s2
        match_normal_config['end_2'] = e2
        Context.RedisConfig.hash_set("configitem", "game:2:match.normal.config", Context.json_dumps(match_normal_config))

        Context.RedisConfig.hash_set('configitem', 'update.time', Time.current_ts())
        Context.Configure.reload()
        cmd = Message.MSG_SYS_UPDATE_MATCH_CONFIG | Message.ID_REQ
        Context.GData.send_to_entity(1000001, mi, cmd=cmd, gid=gid)
        return MsgPack(0)


    def update_picture_version(self, gid, mi, request):
        picture_name = mi.get_param('pn')
        picture_url = mi.get_param('pu')
        if picture_name and picture_url:
            max_picture_version = Context.RedisMix.hash_incrby('picture:version_num', 'max_picture_version', 1)
            dat = {'pn': picture_name, 'pu': picture_url}
            Context.RedisMix.hash_set('picture:version_record', max_picture_version, Context.json_dumps(dat))
        return MsgPack(0)

    def pay_rank(self, gid, mi, request):
        pid = mi.get_param('pid')
        if pid == 1:
            ret = self.query_pay_rank(gid, mi, request)
        elif pid == 2:
            ret = self.modify_pay_rank(gid, mi, request)
        elif pid == 3:
            start_stamp = mi.get_param('start')
            end_stamp = mi.get_param('end')
            c = mi.get_param('channel')
            s = Time.str_to_timestamp(start_stamp)
            e = Time.str_to_timestamp(end_stamp)
            dat = PayRankActivity.query_background_pay_rank_record(s, e, c)
            ret = MsgPack(0)
            ret.set_param('ret', dat)
        else:
            return MsgPack.Error(0, 1, 'not exist pid')
        return ret

    def query_pay_rank(self, gid, mi, request):
        mo = MsgPack(0)
        cnf = PayRankActivity.activity_pay_rank_config()
        if cnf == None:cnf = {}
        mo.set_param('ret', cnf)
        return mo

    def modify_pay_rank(self, gid, mi, request):
        modify_cnf = mi.get_param('ret')

        if PayRankActivity.judge_pay_rank_activity_open():
            cnf = PayRankActivity.activity_pay_rank_config()
            if cnf.get('start') != modify_cnf.get('start'):
                return MsgPack.Error(0, 1, u'活动已开启，不可修改时间')
            channel = modify_cnf.get('channel')
            end = modify_cnf.get('end')
            end_ts = Time.str_to_timestamp(end)
            start = cnf.get('start')
            key = 'activity:%s:%s' % ('pay_rank', start[:10])
            Context.RedisActivity.hash_mset(key, 'refresh_time', end_ts, 'channel', Context.json_dumps(channel))

        Context.RedisActivity.set('pay_rank.activity.config', Context.json_dumps(modify_cnf))
        mou = MsgPack(Message.MSG_SYS_UPDATE_ACTIVITY_CONF | Message.ID_ACK)
        mou.set_param('model', 12)
        Context.GData.broadcast_to_system(mou)
        return MsgPack(0)

    def happy_shake(self, gid, mi, request):
        pid = mi.get_param('pid')
        if pid == 1:
            ret = self.query_happy_shake(gid, mi, request)
        elif pid == 2:
            ret = self.modify_happy_shake(gid, mi, request)
        elif pid == 3:
            ret = self.query_happy_shake_record(gid, mi, request)
        else:
            return MsgPack.Error(0, 1, 'not exist pid')
        return ret

    def query_happy_shake_record(self, gid, mi, request):
        mo = MsgPack(0)
        cnf = ShakeActivity.query_shake_record(mi)
        mo.set_param('ret', cnf)
        return mo

    def query_happy_shake(self, gid, mi, request):
        mo = MsgPack(0)
        cnf = ShakeActivity.activity_shake_config()
        if cnf == None:cnf = {}
        mo.set_param('ret', cnf)
        return mo

    def modify_happy_shake(self, gid, mi, request):
        modify_cnf = mi.get_param('ret')
        cnf = ShakeActivity.activity_shake_config()
        if cnf and cnf.has_key('detail') and cnf['detail'].has_key('way'):
            if not modify_cnf or not modify_cnf.has_key('detail') or not modify_cnf['detail'].has_key('way'):
                return MsgPack.Error(0, 1, 'not exist way')
            if modify_cnf['detail']['way'] != cnf['detail']['way']:
                count = Context.Activity.get_activity_data(gid, 'shake', 'count', 0)
                if count:
                    Context.Activity.set_activity_data(gid, 'shake', 'count', 0)

        Context.RedisActivity.set('shake.activity.config', Context.json_dumps(modify_cnf))
        mou = MsgPack(Message.MSG_SYS_UPDATE_ACTIVITY_CONF | Message.ID_ACK)
        mou.set_param('model', 11)
        Context.GData.broadcast_to_system(mou)
        return MsgPack(0)

    def get_channel_list(self, gid, mi, request):
        channel_list = Context.Configure.get_game_item_json(gid, 'channel.path.config', {})
        mo = MsgPack(0)
        mo.set_param('ret', channel_list)
        return mo

    def get_product_list(self, gid, mi, request):
        product_list = Context.Configure.get_game_item_json(gid, 'product.config', {})
        mo = MsgPack(0)
        mo.set_param('ret', product_list)
        return mo

    def receive_new_player_gift(self, gid, mi, request):
        mo = MsgPack(0)
        uid = Tool.to_int(mi.get_param('uid'), 0)
        if not uid:
            mo.set_param("ret", 0)
            return mo
        info = WxNewPlayerActivity.activity_receive_new_player_gift(gid, uid)
        if info:
            mo.set_param("ret", 1)
        else:
            mo.set_param("ret", 0)
        return mo

    def query_account_exist(self, gid, mi, request):
        uid = mi.get_param('uid', 0)
        uid = Tool.to_int(uid, 0)
        is_exist = Context.Data.exists_attr(uid, 'userName')
        mo = MsgPack(0)
        mo.set_param('result', is_exist)
        return mo


    def get_shop_tips(self, gid, mi, request):
        mo = MsgPack(0)
        info = Context.RedisMix.hash_get_json('game.%d.background' % gid, 'shop_tips', {})
        channel_dict = Context.Configure.get_game_item_json(gid, 'channel.path.config')
        channel = channel_dict.keys()
        cd = {}
        for i in channel:
            if info.has_key(i):
                cd[i] = info[i]
            else:
                cd[i] = ""
        mo.set_param("ret", cd)
        return mo

    def modify_shop_tips(self, gid, mi, request):
        # dz add record
        # Context.Log.debug("gm_recharge_add_gift:", mi)
        # Context.Record.add_record_recharge_add_gift(mi)
        info = mi.get_param("ret")
        Context.RedisMix.hash_set('game.%d.background' % gid, 'shop_tips', Context.json_dumps(info))
        cmd = Message.MSG_SYS_SHOP_TIPS_NOTICE | Message.ID_REQ
        mon = MsgPack(0)
        Context.GData.send_to_entity(1000001, mon, cmd=cmd, gid=gid)
        return MsgPack(0)


    def first_recharge_query(self, gid, mi, request):
        Context.Log.debug("first_recharge_query:", mi)
        Context.Record.add_record_first_recharge_query(mi)

        mo = MsgPack(0)
        info = DoubleActivity.get_recharge_date(gid)
        mo.set_param("ret", info)
        return mo

    def first_recharge_modify(self, gid, mi, request):
        Context.Log.debug("first_recharge_modify:", mi)
        Context.Record.add_record_first_recharge_modify(mi)

        dt = mi.get_param('rdd')
        Context.RedisActivity.set('recharge.double.config', Context.json_dumps(dt))
        mo = MsgPack(0)
        info = DoubleActivity.get_recharge_date(gid)
        mo.set_param("ret", info)

        mou = MsgPack(Message.MSG_SYS_UPDATE_ACTIVITY_CONF | Message.ID_ACK)
        mou.set_param('model', 8)
        Context.GData.broadcast_to_system(mou)

        return mo

    def vip_activity_query(self, gid, mi, request):
        Context.Log.debug("vip_activity_query:", mi)
        Context.Record.add_record_vip_activity_query(mi)

        mo = MsgPack(0)
        info = VipActivity.get_vip_activity_date(gid)
        mo.set_param("ret", info)
        return mo

    def vip_activity_modify(self, gid, mi, request):
        Context.Log.debug("vip_activity_modify:", mi)
        Context.Record.add_record_vip_activity_modify(mi)

        dt = mi.get_param('ret')
        Context.RedisActivity.set('vip.activity.config', Context.json_dumps(dt))
        mo = MsgPack(0)
        info = VipActivity.get_vip_activity_date(gid)
        mo.set_param("ret", info)

        mou = MsgPack(Message.MSG_SYS_UPDATE_ACTIVITY_CONF | Message.ID_ACK)
        mou.set_param('model', 9)
        Context.GData.broadcast_to_system(mou)

        return mo

    def wx_new_player_activity_query(self, gid, mi, request):
        Context.Log.debug("wx_new_player_activity_query_activity_query:", mi)
        Context.Record.add_record_wx_new_player_activity_query(mi)

        mo = MsgPack(0)
        info = WxNewPlayerActivity.get_wx_new_player_activity_date(gid)
        mo.set_param("ret", info)
        return mo

    def wx_new_player_activity_modify(self, gid, mi, request):
        Context.Log.debug("wx_new_player_activity_modify:", mi)
        Context.Record.add_record_wx_new_player_activity_modify(mi)

        dt = mi.get_param('ret')
        Context.RedisActivity.set('wx_new_player.activity.config', Context.json_dumps(dt))
        mo = MsgPack(0)
        info = WxNewPlayerActivity.get_wx_new_player_activity_date(gid)
        mo.set_param("ret", info)

        mou = MsgPack(Message.MSG_SYS_UPDATE_ACTIVITY_CONF | Message.ID_ACK)
        mou.set_param('model', 10)
        Context.GData.broadcast_to_system(mou)

        return mo

    def save_money_activity_query(self, gid, mi, request):
        Context.Log.debug("save_money_activity_query:", mi)
        Context.Record.add_record_save_money_activity_query(mi)

        mo = MsgPack(0)
        save_money_data = Context.RedisActivity.get('save.money.activity.config')
        if save_money_data == None:
            save_money_data = {}
        else:
            save_money_data = Context.json_loads(save_money_data)
        mo.set_param("ret", save_money_data)
        return mo

    def save_money_activity_modify(self, gid, mi, request):
        Context.Log.debug("save_money_activity_modify:", mi)
        Context.Record.add_record_save_money_activity_modify(mi)

        dt = mi.get_param('ret')
        Context.RedisActivity.set('save.money.activity.config', Context.json_dumps(dt))
        mo = MsgPack(0)

        return mo

    def year_monster_pool_query(self, gid, mi, request):
        Context.Log.debug("year_monster_pool_query:", mi)
        Context.Record.add_record_year_monster_pool_query(mi)

        mo = MsgPack(0)
        primary_key = 'game.2.year_monster'
        year_monster_pool_chip = Context.RedisMix.hash_get_int(primary_key, 'year_monster_pool', 0)
        mo.set_param("ret", year_monster_pool_chip)
        return mo

    def year_monster_pool_modify(self, gid, mi, request):
        Context.Log.debug("year_monster_pool_modify:", mi)
        Context.Record.add_record_year_monster_pool_modify(mi)

        dt = mi.get_param('ret')
        primary_key = 'game.2.year_monster'
        monster_pool = Context.RedisMix.hash_incrby(primary_key, 'year_monster_pool', int(dt))
        mo = MsgPack(0)
        mo.set_param('ret', monster_pool)
        return mo

    def alter_many_approve_status(self, gid, mi, request): #修改多个审核状态
        # tf add record
        Context.Log.debug("gm_many_approve_status:", mi)
        Context.Record.add_record_many_approve_status(mi)

        exchange_list = mi.get_param('exchange_list')
        for data in exchange_list:
            exchange_id = data.get("exchange_id")
            user_id = int(data.get("user_id"))
            self.approve_deal(gid, user_id, exchange_id)

        return MsgPack(0)

    def approve_deal(self,gid,uid,order_id):
        order = Context.Data.get_shop_attr(uid, 'shop:order', order_id)
        order_state = Context.json_loads(order)
        if order_state['stat'] !=0:
            return 0
        else:
            order_state['stat'] = 1
            Context.Data.set_shop_attr(uid, 'shop:order', order_id, Context.json_dumps(order_state))
            if order_state['good_type'] != 3:
                uid = order_state['uid']
                attrs = ['channelid']
                values = Context.Data.get_attrs(Tool.to_int(uid, 0), attrs)
                channelId = values[0]

                # 记录实物兑换
                pipe_args = []
                pipe_args.append(channelId + '.exchange.shop.real.cost')  # 实物兑换记录总消耗鸟券数
                pipe_args.append(order_state['price'])
                Context.Stat.mincr_daily_data(channelId, *pipe_args)  # 本日充值数据写入
                key = 'game.%d.info.hash' % gid
                pipe_args = []
                pipe_args.append(channelId + '.exchange.shop.real.cost')  # 本服充值总金额+cost
                pipe_args.append(order_state['price'])
                Context.RedisMix.hash_mincrby(key, *pipe_args)  # 服务器数据写入
            return 0

    def alter_point_shop_status(self, gid, mi, request): #修改多个审核状态
        order_data = mi.get_param('order_data')
        if order_data != None:
            for ord in order_data:
                uid = int(ord.get("uid"))
                order_id = ord.get("order_id")
                self.point_shop_deal(gid,uid, order_id)
        else:
            order_id = str(mi.get_param('order_id'))
            uid = int(mi.get_param('uid'))
            self.point_shop_deal(gid,uid,order_id)

        return MsgPack(0)

    def point_shop_deal(self,gid,uid,order_id):
        order = Context.Data.get_shop_attr(uid, 'point_shop:order', order_id)
        order_state = Context.json_loads(order)
        order_state['stat'] = 1
        Context.Data.set_shop_attr(uid, 'point_shop:order', order_id, Context.json_dumps(order_state))
        return 0

    def point_shopping_info(self, gid, mi, request): #发货信息
        order_id = mi.get_param('order_id')
        uid = int(mi.get_param('uid'))
        if order_id!=None:
            order = Context.Data.get_shop_attr(uid, 'point_shop:order', order_id)
            order_status = Context.json_loads(order)
            info = Context.Data.get_shop_all(uid, 'shop:user')
            info.update(order_status)
        else:
            info = Context.Data.get_shop_all(uid, 'shop:user')
        mo = MsgPack(0)
        mo.set_param('info', info)
        return mo

    def point_shopping_state(self, gid, mi, request): #发货状态
        order_id = str(mi.get_param('order_id'))
        order_info = mi.get_param('order_info')
        uid = int(mi.get_param('uid'))

        order = Context.Data.get_shop_attr(uid, 'point_shop:order', order_id)
        order_state = Context.json_loads(order)
        order_state['stat'] = 2
        # order_state['order_number'] = order_info
        order_state.update({'order_number':order_info })
        Context.Data.set_shop_attr(uid, 'point_shop:order', order_id, Context.json_dumps(order_state))
        return MsgPack(0)


    def get_recharge_add(self, gid, mi, request):
        mo = MsgPack(0)
        ret = {}
        info = Context.RedisMix.hash_get_json('game.%d.background' % gid, 'recharge_add_new', {})
        channel_dict = Context.Configure.get_game_item_json(gid, 'channel.path.config')
        channel = channel_dict.keys()
        for i in channel:
            if info.has_key(i):
                ret[i] = info[i]
            else:
                ret[i] = {"zhifubao": 0, "weixin": 0}
        mo.set_param("ret", ret)
        return mo

    def recharge_add_gift(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_recharge_add_gift:", mi)
        Context.Record.add_record_recharge_add_gift(mi)
        info = mi.get_param("ret")
        Context.RedisMix.hash_set('game.%d.background' % gid, 'recharge_add_new', Context.json_dumps(info))
        cmd = Message.MSG_SYS_SET_RECHARGE_PRESENT | Message.ID_REQ
        mon = MsgPack(0)
        Context.GData.send_to_entity(1000001, mon, cmd=cmd, gid=gid)
        return MsgPack(0)

    # 数据总览
    def data_summary(self, gid, mi, request):
        # tf add record
        Context.Log.debug("gm_query_data_summary:", mi)
        Context.Record.add_record_gm_query_overview(mi)

        # 数据总览
        mo = MsgPack(0)
        start = str(mi.get_param('start'))
        end = str(mi.get_param('end'))
        channelid = str(mi.get_param('channel_id'))
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')

        # 处理统计数据
        count_info = []
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            day_info = {}  # 本日时间记录
            channel_info = {}
            kvs = Context.Stat.get_day_data(channelid, fmt)  # 获取当天数据记录
            if len(kvs) == 0:  # 没有记录
                start_day = Time.next_days(start_day)
                continue
            channeldict = {}
            for keys, value in kvs.items():
                if keys.startswith('in.play_shot_gift_chip.'):
                    barrel = keys.split('.')[4]
                    channeldict["in.play_shot_gift_chip.{}".format(barrel)] = value

            key = '{}.pay.user.pay_total'.format(channelid)
            channeldict['pay_total'] = kvs.get(key, 0)

            key = '{}.sdk_pay.user.pay_total'.format(channelid)
            channeldict['sdk_pay_total'] = kvs.get(key, 0)
            # 获取兑换码充值额度
            key = '{}.cdkey_pay.user.pay_total'.format(channelid)
            channeldict['cdkey_pay_total'] = kvs.get(key, 0)
            # 获取微信充值额度
            key = '{}.weixin_pay.user.pay_total'.format(channelid)
            channeldict['weixin_pay_total'] = kvs.get(key, 0)
            # 获取支付宝充值额度
            key = '{}.ali_pay.user.pay_total'.format(channelid)
            channeldict['ali_pay_total'] = kvs.get(key, 0)
            # 获取gm充值额度
            key = '{}.gm_pay.user.pay_total'.format(channelid)
            channeldict['gm_pay_total'] = kvs.get(key, 0)

            # 打出鸟蛋
            key = 'out.chip.game.shot.bullet.200'
            channeldict[key] = kvs.get(key, 0)
            key = 'out.chip.game.shot.bullet.201'
            channeldict[key] = kvs.get(key, 0)
            key = 'out.chip.game.shot.bullet.202'
            channeldict[key] = kvs.get(key, 0)
            key = 'out.chip.game.shot.bullet.203'
            channeldict[key] = kvs.get(key, 0)
            key = 'out.chip.game.shot.bullet.209'
            channeldict[key] = kvs.get(key, 0)
            # 产出
            key = 'in.chip.catch.bird.200'
            channeldict[key] = kvs.get(key, 0)
            key = 'in.chip.catch.bird.201'
            channeldict[key] = kvs.get(key, 0)
            key = 'in.chip.catch.bird.202'
            channeldict[key] = kvs.get(key, 0)
            key = 'in.chip.catch.bird.203'
            channeldict[key] = kvs.get(key, 0)
            key = 'in.chip.catch.bird.209'
            channeldict[key] = kvs.get(key, 0)
            key = 'daily.pay.active.player'  #
            channeldict[key] = kvs.get(key, 0)

            # 商城成本
            channeldict['exchange_shop_real_cost'] = kvs.get(channelid + '.exchange.shop.real.cost', 0)
            # 当日登录用户数,活跃用户
            channeldict['login_user_count'] = kvs.get(channelid + '.login.user.count', 0)
            # 当日充值人数
            channeldict['pay_user_count'] = kvs.get(channelid + '.pay.user.count', 0)
            # 当日充值次数
            channeldict['user_pay_times'] = kvs.get(channelid + '.user.pay.times', 0)
            # 付费总额度
            channeldict['pay_user_pay_total'] = kvs.get(channelid + '.pay.user.pay_total', 0)
            # 新增用户数
            channeldict['new_user_count'] = kvs.get(channelid + '.new.user.count', 0)
            # 新增设备
            channeldict['new_device_count'] = kvs.get(channelid + '.new.device.count', 0)

            # 新增付费总额度
            key = '{}.new.pay.user.pay_total'.format(channelid)
            channeldict['day_new_pay_user_pay_total'] = Tool.to_int(Context.Stat.get_day_data(channelid, fmt, key),0)
            # 新增付费总次数
            key = '{}.new.pay_user.pay_times'.format(channelid)
            channeldict['day_new_pay_user_pay_times'] = Tool.to_int(Context.Stat.get_day_data(channelid, fmt, key),0)
            # 新增付费人数
            key = '{}.new.pay.user.count'.format(channelid)
            channeldict['day_new_pay_user_count'] = Tool.to_int(Context.Stat.get_day_data(channelid, fmt, key), 0)

            # 新增次留
            channeldict['login_level_1'] = kvs.get('login_level_1', 0)
            # 新增三留
            channeldict['login_level_2'] = kvs.get('login_level_2', 0)
            # 新增七留
            channeldict['login_level_3'] = kvs.get('login_level_3', 0)
            # 新增三十留
            channeldict['login_level_4'] = kvs.get('login_level_4', 0)

            key = 'game.%d.info.hash' % gid
            field = '%s.new.user.count' % channelid
            # 总人数
            channeldict['total_user'] = Context.RedisMix.hash_get(key, field, 0)
            # 总设备数
            field = '%s.new.device.count' % channelid
            channeldict['total_device'] = Context.RedisMix.hash_get(key, field, 0)

            channel_info[channelid] = channeldict

            if len(channel_info) > 0:
                day_info.update({'time': {fmt: channel_info}})
                count_info.append(day_info)
            start_day = Time.next_days(start_day)
        mo.set_param("ret", count_info)
        return mo

    # 数据总览
    def query_overview(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_query_overview:", mi)
        Context.Record.add_record_gm_query_overview(mi)

        # 数据总览
        mo = MsgPack(0)
        start = str(mi.get_param('start'))
        end = str(mi.get_param('end'))
        # channel = str(mi.get_param('channel_id'))
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
                channeldict = {}
                for keys,value in kvs.items():
                    if keys.startswith('in.play_shot_gift_chip.'):
                        barrel = keys.split('.')[4]
                        channeldict["in.play_shot_gift_chip.{}".format(barrel)] = value

                key = '{}.pay.user.pay_total'.format(channelid)
                channeldict['pay_total'] = kvs.get(key, 0)

                key = '{}.sdk_pay.user.pay_total'.format(channelid)
                channeldict['sdk_pay_total'] = kvs.get(key, 0)
                # 获取兑换码充值额度
                key = '{}.cdkey_pay.user.pay_total'.format(channelid)
                channeldict['cdkey_pay_total'] = kvs.get(key, 0)
                # 获取微信充值额度
                key = '{}.weixin_pay.user.pay_total'.format(channelid)
                channeldict['weixin_pay_total'] = kvs.get(key, 0)
                # 获取支付宝充值额度
                key = '{}.ali_pay.user.pay_total'.format(channelid)
                channeldict['ali_pay_total'] = kvs.get(key, 0)
                # 获取gm充值额度
                key = '{}.gm_pay.user.pay_total'.format(channelid)
                channeldict['gm_pay_total'] = kvs.get(key, 0)

                # 打出鸟蛋
                key = 'out.chip.game.shot.bullet.200'
                channeldict[key] = kvs.get(key, 0)
                key = 'out.chip.game.shot.bullet.201'
                channeldict[key] = kvs.get(key, 0)
                key = 'out.chip.game.shot.bullet.202'
                channeldict[key] = kvs.get(key, 0)
                key = 'out.chip.game.shot.bullet.203'
                channeldict[key] = kvs.get(key, 0)
                key = 'out.chip.game.shot.bullet.209'
                channeldict[key] = kvs.get(key, 0)
                # 产出
                key = 'in.chip.catch.bird.200'
                channeldict[key] = kvs.get(key, 0)
                key = 'in.chip.catch.bird.201'
                channeldict[key] = kvs.get(key, 0)
                key = 'in.chip.catch.bird.202'
                channeldict[key] = kvs.get(key, 0)
                key = 'in.chip.catch.bird.203'
                channeldict[key] = kvs.get(key, 0)
                key = 'in.chip.catch.bird.209'
                channeldict[key] = kvs.get(key, 0)
                key = 'daily.pay.active.player' #
                channeldict[key] = kvs.get(key, 0)


                # 商城成本
                channeldict['exchange_shop_real_cost'] = kvs.get(channelid + '.exchange.shop.real.cost', 0)
                # 当日登录用户数,活跃用户
                channeldict['login_user_count'] = kvs.get(channelid + '.login.user.count', 0)
                # 当日充值人数
                channeldict['pay_user_count'] = kvs.get(channelid + '.pay.user.count', 0)
                # 当日充值次数
                channeldict['user_pay_times'] = kvs.get(channelid + '.user.pay.times', 0)
                # 付费总额度
                channeldict['pay_user_pay_total'] = kvs.get(channelid + '.pay.user.pay_total', 0)
                # 新增用户数
                channeldict['new_user_count'] = kvs.get(channelid + '.new.user.count', 0)
                # 新增设备
                channeldict['new_device_count'] = kvs.get(channelid + '.new.device.count', 0)

                # 新增付费总额度
                key = '{}.new.pay.user.pay_total'.format(channelid)
                channeldict['day_new_pay_user_pay_total'] = Tool.to_int(Context.Stat.get_day_data(channelid, fmt, key), 0)
                # 新增付费总次数
                key = '{}.new.pay_user.pay_times'.format(channelid)
                channeldict['day_new_pay_user_pay_times'] = Tool.to_int(Context.Stat.get_day_data(channelid, fmt, key), 0)
                # 新增付费人数
                key = '{}.new.pay.user.count'.format(channelid)
                channeldict['day_new_pay_user_count'] = Tool.to_int(Context.Stat.get_day_data(channelid, fmt, key), 0)

                # 新增次留
                channeldict['login_level_1'] = kvs.get('login_level_1', 0)
                # 新增三留
                channeldict['login_level_2'] = kvs.get('login_level_2', 0)
                # 新增七留
                channeldict['login_level_3'] = kvs.get('login_level_3', 0)
                # 新增三十留
                channeldict['login_level_4'] = kvs.get('login_level_4', 0)

                key = 'game.%d.info.hash' % gid
                field = '%s.new.user.count' % channelid
                # 总人数
                channeldict['total_user'] = Context.RedisMix.hash_get(key, field, 0)
                # 总设备数
                field = '%s.new.device.count' % channelid
                channeldict['total_device'] = Context.RedisMix.hash_get(key, field, 0)

                channel_info[channelid] = channeldict

            if len(channel_info) > 0:
                day_info.update({'time': {fmt: channel_info}})
                count_info.append(day_info)
            start_day = Time.next_days(start_day)
        mo.set_param("ret", count_info)
        return mo

    def request_verify_code(self, gid, mobile):
        config = Context.Configure.get_game_item_json(gid, 'sms.config')
        rest = CCPRestSDK.REST(config['serverIP'], config['serverPort'], config['softVersion'])
        rest.setAccount(config['accountSid'], config['accountToken'])
        rest.setAppId(config['appId'])

        verifyCode = random.randint(100000, 999999)

        for tempId in config['tempId_arr']:
            result = rest.sendTemplateSMS(mobile, [str(verifyCode), '30'], tempId)
            Context.Log.debug('---------sms', result, 'code:', verifyCode)
            if result['statusCode'] == '000000':
                return verifyCode

        return 0

    def request_verify_Messages(self, gid, mobile,goods):
        config = Context.Configure.get_game_item_json(gid, 'sms.config')
        rest = CCPRestSDK.REST(config['serverIP'], config['serverPort'], config['softVersion'])
        rest.setAccount(config['accountSid'], config['accountToken'])
        rest.setAppId(config['appId'])
        if len(goods) >= 5:
            if goods == "美的多功能电烤箱":
                data_info = ["美的电烤箱",""]
            else:
                data_info = [goods[:5],goods[5:]]
        else:
            data_info = [goods,""]

        result = rest.sendTemplateSMS(mobile, data_info, "468540")
        Context.Log.debug('---------sms', result, 'goods:', goods)
        if result['statusCode'] == '000000':
            return result
        return 0


    def tmp_fun(self):
        info = {
            '18712805553': [1077441, '18805085381'],
            '15032995908': [1036848, '13139913123'],
        }
        #for k, v in info.items():
        #    keys = 'username:1004:13:%s' % k
        #    userId = Context.RedisMix.hash_get_int(keys, 'userId', 0)
        #    if userId == v[0]:
        #        Context.RedisMix.delete(keys)
        #        kes = 'username:1004:13:%s' % v[1]
        #        Context.RedisMix.hash_set(kes, 'userId', userId)

        for k, v in info.items():
            keys = 'username:1004:13:%s' % v[1]
            userId = Context.RedisMix.hash_get_int(keys, 'userId', 0)
            if userId == v[0]:
                Context.Data.set_attr(int(userId), 'userName', v[1])

    def getMVerifyCode(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_getm_verifycode:", mi)
        Context.Record.add_record_getm_verifycode(mi)
        mobile = mi.get_param('mobile', '0')
        Context.Log.debug("getMVerifyCode", mobile)

        if not Entity.checkMobile(mobile):
            return MsgPack.Error(0, 1, 'mobile invalid')
        verifyCode = self.request_verify_code(gid, mobile)
        if verifyCode == 0:
            return MsgPack.Error(0, 3, 'send failed')

        mo = MsgPack(0)
        mo.set_param('result', 1)
        mo.set_param('code', verifyCode)

        return mo

    def getMVerify_Messages(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_get_verify_messages:", mi)
        Context.Record.add_record_get_verifymessages(mi)
        mobile = mi.get_param('mobile', '0')
        goods = mi.get_param('goods', '0')
        Context.Log.debug("getMVerifyMessages", mobile,goods)

        if not Entity.checkMobile(mobile):
            return MsgPack.Error(0, 1, 'mobile invalid')
        messages = self.request_verify_Messages(gid, mobile,goods)
        if messages == 0:
            return MsgPack.Error(0, 3, 'send failed')

        mo = MsgPack(0)
        mo.set_param('result', 1)
        return mo

    def get_barrel_pool_config(self, gid, mi, request):
        # TF add record
        Context.Log.debug("gm_get_barrel_pool_config:", mi)
        Context.Record.add_record_barrel_pool_config(mi)

        common_barrel_pool, new_barrel_pool, barrel_pool = [], [], {}
        pool_space = Context.Configure.get_game_item_json(gid, 'barrel_pool.config')
        for index, space in enumerate(pool_space["pool_space"]):
            level_chip, banker_chip = self.get_barrel_pool_info(gid, index+1)
            common_barrel_pool.append({str(index): space["space"], "level_chip": level_chip, "banker_chip": banker_chip})

            new_level_chip, new_banker_chip = self.get_barrel_pool_info(gid, index + 1001)
            new_barrel_pool.append({str(index + 1001): space["space"], "new_level_chip": new_level_chip, "new_banker_chip": new_banker_chip})
        barrel_pool.update({"common_barrel": common_barrel_pool, "new_barrel": new_barrel_pool})
        mo = MsgPack(0)
        mo.set_param('ret', barrel_pool)
        return mo

    def alter_barrel_pool_config(self, gid, mi, request):
        # tf add record
        Context.Log.debug("gm_alter_barrel_pool_config:", mi)
        Context.Record.add_record_alter_barrel_pool_config(mi)

        barrel_pool = mi.get_param('barrel_info')
        for pool_id, value in enumerate(barrel_pool):
            real_pool_id = int(pool_id) + 3
            key = 'game.%d.info.barrel_pool:%d' % (gid, real_pool_id)
            pool_barrel = 'pool.barrel_level_chip.%d' % real_pool_id
            values = long(value)
            Context.Log.debug('alter_barrel_pool_configxxxxx', values)
            Context.RedisMix.hash_incrby(key, pool_barrel, values)
        mo = MsgPack(0)
        mo.set_param("result", 0)
        return mo

    # 获取炮倍池配置
    def get_barrel_pool_info(self, gid, pool_id):
        key = 'game.%d.info.barrel_pool:%d' % (gid, pool_id)
        level_key,banker_key = 'pool.barrel_level_chip.{}'.format(pool_id),'pool.banker_chip'
        level_chip = Tool.to_int(Context.RedisMix.hash_get(key, level_key, 0))
        banker_chip = Tool.to_int(Context.RedisMix.hash_get(key, banker_key, 0))
        return level_chip,banker_chip


    def freeze_user(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_freeze_user:", mi)
        Context.Record.add_record_freeze(mi)

        uid = int(mi.get_param('userId'))
        if not Context.UserAttr.check_exist(uid, gid):
            return MsgPack.Error(0, 1, 'not exist')

        days = mi.get_param('days')
        mo = MsgPack(0)
        if days is None:
            Context.RedisMix.hash_del('game.%d.freeze.user' % gid, uid)
        else:
            end_ts = Time.current_ts() + days * 3600 * 24
            Context.RedisMix.hash_set('game.%d.freeze.user' % gid, uid, end_ts)
            mo.set_param('end_ts', end_ts)

            cmd = Message.MSG_SYS_USER_DEAL | Message.ID_REQ
            mon = MsgPack(0)
            mon.set_param('deal', 1)
            Context.GData.send_to_entity(uid, mon, cmd=cmd, gid=gid)
        return mo

    def set_kill_chip(self, gid, mi, request):
        # tf add record
        Context.Log.debug("gm_user_kill_chip:", mi)
        Context.Record.add_record_kill_chip(mi)

        uid = int(mi.get_param('uid'))
        if not Context.UserAttr.check_exist(uid, gid):
            return MsgPack.Error(0, 1, 'not exist')

        kill_chip = int(mi.get_param('kill_chip'))
        chip_rate = mi.get_param('chip_rate')
        Context.UserAttr.incr_kill_chip(uid, gid,kill_chip,'kill.incr')
        Context.UserAttr.set_kill_chip_rate(uid, gid, chip_rate)
        return MsgPack(0)

    def set_give_chip(self, gid, mi, request):
        # tf add record
        Context.Log.debug("gm_user_give_chip:", mi)
        Context.Record.add_record_give_chip(mi)

        uid = int(mi.get_param('uid'))
        if not Context.UserAttr.check_exist(uid, gid):
            return MsgPack.Error(0, 1, 'not exist')

        give_chip = mi.get_param('give_chip')
        multiple = mi.get_param('multiple')
        give_rate = mi.get_param('give_rate')

        Context.UserAttr.incr_give_chip(uid, gid, give_chip, 'give.incr')
        Context.UserAttr.set_give_chip_rate(uid, gid, give_rate)
        Context.UserAttr.set_give_chip_effect_bm(uid, gid, multiple)
        return MsgPack(0)

    def limit_shop_open(self, gid, mi, request):
        open = mi.get_param('open')
        limit_shop = Context.RedisMix.get('limit.shop.open')
        limit_shop_open = Tool.to_int(limit_shop)
        mo = MsgPack(0)
        if open == limit_shop_open:
            return MsgPack.Error(0, 1, 'not has modify')
        else:
            cmd = Message.MSG_SYS_LIMIT_SHOP_OPEN | Message.ID_REQ
            mon = MsgPack(0)
            mon.set_param('open', open)
            Context.GData.send_to_entity(1000001, mon, cmd=cmd, gid=gid)
        return mo

    def limit_raffle_open(self, gid, mi, request):
        mo = MsgPack(0)
        open = mi.get_param('open')
        limit_raffle_open = Context.RedisMix.hash_get_int('limit.raffle.open', 0)
        if open == limit_raffle_open:
            return MsgPack.Error(0, 1, 'not has modify')
        else:
            cmd = Message.MSG_SYS_LIMIT_RAFFLE_OPEN | Message.ID_REQ
            mon = MsgPack(0)
            mon.set_param('open', open)
            Context.GData.send_to_entity(1000001, mon, cmd=cmd, gid=gid)
        return mo

    def gm_add_mail(self, gid, mi, request): #系统邮件
        # dz add record
        Context.Log.debug("gm_add_mail:", mi)
        Context.Record.add_record_mail(mi)

        nType = mi.get_param('t', None)
        reward = mi.get_param('r')
        useId = mi.get_param('u', 0)
        title = mi.get_param('tl')
        if nType == None:
            return MsgPack.Error(0, 1, 'not has type')
        if not reward:
            return MsgPack.Error(0, 2, 'not has reward')
        if not title:
            return MsgPack.Error(0, 3, 'not has title')
        if nType == 0:
            ret = Context.RedisCluster.hget_keys('game:2:*')
            for i in ret:
                uid = int(i.split('game:2:')[1])
                if uid <= 1000000:
                    continue
                times = Time.current_ts()
                ret = Mail.add_mail(uid, gid, times, 9, reward, -10, title)
                if ret:
                    Mail.send_mail_list(uid, gid)

        elif nType == 1:
            if useId <= 0:
                return MsgPack.Error(0, 4, 'not has useId')
            times = Time.current_ts()
            ret = Mail.add_mail(useId, gid, times, 9, reward, -10, title)
            if ret:
                Mail.send_mail_list(useId, gid)
        d = {'nType': nType, 'reward': reward, 'title': title}

        return MsgPack(0)

    def modifyDropCoupon(self, gid, mi, request):
        uid = mi.get_param('uid')
        drop_coupon = mi.get_param('f')
        if not uid or drop_coupon == None:
            return MsgPack.Error(0, 1, 'info error')
        d = Context.Data.get_game_attr_int(uid, gid, 'drop_coupon', 0)
        if Tool.to_int(drop_coupon) != d:
            Context.Data.set_game_attr(uid, gid, 'drop_coupon', drop_coupon)
            key = 'location:%d:%d' % (gid, uid)
            sid = Context.RedisCache.hash_get_int(key, 'serverId', 0)
            if sid > 0:
                mon = MsgPack(Message.MSG_SYS_MODIFY_DROP_COUPON | Message.ID_REQ)
                mon.set_param('drop_coupon', drop_coupon)
                mon.set_param('gameId', gid)
                Context.GData.send_to_game(uid, mon, sid, gid=gid)
        mo = MsgPack(0)
        mo.set_param('result', 0)
        return mo

    def gm_add_notice(self, gid, mi, request): #更新公告
        # dz add record
        Context.Log.debug("gm_add_notice:", mi)
        Context.Record.add_record_add_notice(mi)

        context = mi.get_param('c')
        if not context:
            return MsgPack.Error(0, 1, 'not has context')
        context = Context.json_dumps(context)
        Context.RedisCache.set('game.2.notice', context)
        max_notice_id = Context.RedisMix.hash_get_int('global.info.hash', 'max.notice.id', 0)
        Context.RedisMix.hash_set('global.info.hash', 'max.notice.id', max_notice_id+1)
        return MsgPack(0)

    def gm_notice_config(self, gid, mi, request):#获取公告信息
        context = Context.RedisCache.get('game.2.notice')
        max_notice_id = Context.RedisMix.hash_get_int('global.info.hash', 'max.notice.id', 0)
        info = {}
        c = []
        if context:
            context = Context.json_loads(context)
            for i in context:
                notice_dict = {}
                notice_dict.update({"t": i[0], "c": i[1]})
                c.append(notice_dict)
        info['c'] = c
        info['id'] = max_notice_id
        mo = MsgPack(0)
        mo.set_param('ret', info)
        return mo

    def gm_reward_vip(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_reward_vip:", mi)
        Context.Record.add_record_reward_vip(mi)

        uid = mi.get_param('userId')
        rmb = mi.get_param('rmb')
        if not isinstance(rmb, int):
            return MsgPack.Error(0, 1, 'int please')

        if not Context.UserAttr.check_exist(uid, gid):
            return MsgPack.Error(0, 2, 'not exist')

        if rmb < 0:
            pay_total = Context.Data.get_game_attr_int(uid, gid, 'pay_total', 0)
            if pay_total < -rmb:
                return MsgPack.Error(0, 3, 'too much')

        final = BirdProps.incr_pay(uid, gid, rmb, 'gm.reward')
        level = BirdAccount.get_vip_level(uid, gid, final)
        mo = MsgPack(0)
        mo.set_param('level', level)
        mo.set_param('pay_total', final)
        return mo

    def gm_push_info(self, gid, mi, request):
        msg = mi.get_param('msg') #公告内容
        cycle = mi.get_param('cycle') #循环次数
        interval = mi.get_param('interval', 0) #间隔时间(秒)
        bulletin = mi.get_param('bulletin') #公告类型(C:3,B:2,A:1)
        priority = mi.get_param('priority') #优先级(正常:0,紧急:1)
        start_hour = str(mi.get_param('start_hour', 0))
        end_hour = str(mi.get_param('end_hour', 0))
        # end_hour = mi.get_param('color', 0)#显示颜色
        if priority == 1:
            if int(cycle) > 1:
                i = 0
                while i < int(cycle):
                    mo = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
                    mo.set_param('game', {'msg': msg, 'ts': start_hour, 'bulletin': bulletin})
                    Context.GData.broadcast_to_system(mo)
                    i = i + 1
            else:
                mo = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
                mo.set_param('game', {'msg': msg, 'ts': start_hour, 'bulletin': bulletin})
                Context.GData.broadcast_to_system(mo)
        #有效期
        if start_hour == '0' and end_hour == '0':
            return MsgPack.Error(0, 1, 'start_hour or end_hour error')
        start_hour = Time.str_to_timestamp(start_hour)
        end_hour = Time.str_to_timestamp(end_hour)

        date_time = Time.timestamp_to_datetime(Time.current_ts())

        uid = Context.GData.get_new_led_id()
        today = int(''.join(str(datetime.date.today()).split('-')))

        led = {'msg': msg, 'cycle': cycle, 'interval': interval, 'bulletin': bulletin,  'start_hour': start_hour, 'end_hour': end_hour}
        Context.RedisCache.hash_set('game.led.%d' % today, uid, Context.json_dumps(led))

        return MsgPack(0)

    def remove_special_packet(self, gid, mi, request): #特殊红包
        # tf add record
        Context.Log.debug("gm_remove_special_red_packet:", mi)
        Context.Record.add_record_remove_special_red_packet(mi)
        special_id = mi.get_param('special_id')
        # day_stamp = Time.current_ts() - 3600 * 24
        Context.Data.set_red_packet_attrs(100, 'red_packet:special_timer', special_id,['stop_state'], [2])
        mo = MsgPack(0)
        mo.set_param('result', 0)
        return mo


    def send_special_packet_info(self, gid, mi, request):  # 特殊红包配置
        # dz add record
        Context.Log.debug("gm_send_special_packet_info:", mi)
        Context.Record.add_record_special_red_packet(mi)

        ntype = mi.get_param('type')
        random_packet = mi.get_param('number')
        send_gold = mi.get_param('total_price')
        now = Time.current_ts()

        if ntype == 1:
            st = mi.get_param('st')
            et = mi.get_param('nt')
            sh = mi.get_param('sh')
            eh = mi.get_param('eh')
            it = mi.get_param('it')
            dct = {'start_today': st, 'end_today': et, 'start_hours': sh, 'end_hours': eh, 'interval_time': it,'red_packet_type': 1,'packet_sum':random_packet, 'send_gold':send_gold,'send_packet_list':[],'stop_state':1, 'get_money':0, 'surplus':send_gold,"special_id":now}
            Context.Data.set_red_packet_dict(100, 'red_packet:special_timer', now, dct)
        else:

            Context.Data.set_red_packet_dict(100, 'red_packet:special', now, {'red_packet_type': 0,'packet_sum':random_packet, 'send_gold':send_gold, 'get_money':0, 'surplus':send_gold,"special_id":now})
            cmd = Message.MSG_SYS_SPECIA_RED_PACKET | Message.ID_REQ
            mon = MsgPack(0)
            mon.set_param('now', now)
            Context.GData.send_to_entity(1000001, mon, cmd=cmd, gid=gid)

    def coupon_event(self, gid, mi, request):
        uid = mi.get_param('userId')
        event_list = Context.Data.get_coupon_event_all(uid)
        name = Context.Data.get_attr(uid, 'nick', '')
        mo = MsgPack(0)
        for k,v in event_list.items():
            v = Context.json_loads(v)
            td = {}
            if len(v) >= 7:
                td['times'] = v[3]
                td['server'] = u'无'
                td['name'] = name
                td['event'] = v[0]
                td['num'] = v[1]
                td['detail'] = "%d, %d, %d"%(int(v[4]), int(v[5]), int(v[6]))
            mo.set_param(k, td)
        return mo

    def gm_reward_card(self, gid, mi, request):
        uid = mi.get_param('userId')
        days = mi.get_param('days')
        if days <= 0:
            return MsgPack.Error(0, 1, 'error days')

        if not Context.UserAttr.check_exist(uid, gid):
            return MsgPack.Error(0, 2, 'not exist')

        state, days = BirdProps.incr_vip(uid, gid, days, 'gm.reward')
        mo = MsgPack(0)
        mo.set_param('days', days)
        return mo

    def gm_reward_prop(self, gid, mi, request):
        uid = mi.get_param('userId')
        _id = mi.get_param('id')
        _count = mi.get_param('count')
        if _id not in (201, 202, 203, 204, 205, 211, 212, 213, 214, 215, 216, 217, 218, 219, 224, 225) and \
            _id < 10000000:
            return MsgPack.Error(0, 1, 'error id')

        if not Context.UserAttr.check_exist(uid, gid):
            return MsgPack.Error(0, 3, 'user not exist')

        real, final = BirdProps.incr_props(uid, gid, _id, _count, 'gm.reward')
        mo = MsgPack(0)
        mo.set_param('delta', real)
        mo.set_param('id', _id)
        mo.set_param('count', final)
        return mo

    def gm_poke_mole_chip(self, gid, mi, request):
        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')

        t_all = 0
        t_chip = 0
        t_hammer = 0
        res = Context.Stat.get_daily_data(gid, 'poke_mole:chip', 'poke_mole:mp_chip', 'poke_mole:mp_hammer')
        now_all, now_chip, now_hammer = res
        now_all = Tool.to_int(now_all, 0)
        now_chip = Tool.to_int(now_chip, 0)
        now_hammer = Tool.to_int(now_hammer, 0)

        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            res = Context.Stat.get_day_data(gid, fmt, 'poke_mole:chip', 'poke_mole:mp_chip', 'poke_mole:mp_hammer')
            _all, _chip, _hammer = res
            t_all += Tool.to_int(_all, 0)
            t_chip += Tool.to_int(_chip, 0)
            t_hammer += Tool.to_int(_hammer, 0)
            start_day = Time.next_days(start_day)

        mo = MsgPack(0)
        mo.set_param('now_all', now_all)
        mo.set_param('now_chip', now_chip)
        mo.set_param('now_hammer', now_hammer)
        mo.set_param('t_all', t_all)
        mo.set_param('t_chip', t_chip)
        mo.set_param('t_hammer', t_hammer)
        return mo

    def gm_exchange_phone(self, gid, mi, request):
        uid = mi.get_param('userId')
        seq = mi.get_param('seq')
        state = Context.RedisCluster.hash_get_int(uid, 'history:%d:%d' % (gid, uid), seq)
        if state is None:
            return MsgPack.Error(0, 1, 'error seq')
        if state == 1:
            return MsgPack.Error(0, 2, 'already exchange')
        Context.RedisCluster.hash_set(uid, 'history:%d:%d' % (gid, uid), seq, 1)
        return MsgPack(0)

    def gm_account_block(self, gid, mi, request):
        uid = mi.get_param('userId')
        odds = mi.get_param('odds')
        if odds is None:
            Context.Data.del_game_attrs(uid, gid, 'block')
        else:
            if not Context.UserAttr.check_exist(uid, gid):
                return MsgPack.Error(0, 1, 'not exist')
            if odds <= 0 or odds > 1:
                return MsgPack.Error(0, 2, 'odds limit (0, 1]')
            Context.Data.set_game_attr(uid, gid, 'block', odds)
        return MsgPack(0)

    def gm_village_can_buy(self, gid, mi, request):
        uid = mi.get_param('userId')
        key = 'village_exp_can_buy:%d' % gid
        Context.RedisMix.hash_set(key, uid, 1)
        return MsgPack(0)

    def gm_broadcast_set(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_broadcast_set:", mi)
        Context.Record.add_record_gm_broadcast_set(mi)

        keys = mi.get_param('keys')
        if keys != None:
            Context.RedisCache.delete('notice:%d:%s'%(gid, keys))
            return MsgPack(0)

        led = mi.get_param('led')
        start = mi.get_param('start')
        end = mi.get_param('end')
        interval = Tool.to_int(mi.get_param('interval'), 0)

        if interval%60 != 0:
            return MsgPack.Error(0, 1, 'interval error')

        if interval == 0:
            if start != end:
                return MsgPack.Error(0, 1, 'interval error')
        bulletin = mi.get_param('bulletin')
        now_ts = Time.current_ts()
        if now_ts > end or (now_ts > start and (now_ts + interval) > end):
            return MsgPack.Error(0, 2, 'times error')

        Context.RedisCache.hash_mset('notice:%s:%d'%(gid, Time.current_ms()), 'led', led, 'start', start, 'end', end,
                                          'interval', interval, 'bulletin', bulletin)

        return MsgPack(0)

    def gm_broadcast_query(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_broadcast_query:", mi)
        Context.Record.add_record_gm_broadcast_query(mi)

        mo = MsgPack(0)
        keys = 'notice:%d:'%gid
        broadcast_keys = Context.RedisCache.hget_keys('%s*' % keys)
        if not broadcast_keys or len(broadcast_keys) <= 0:
            return mo
        info = {}
        for i in broadcast_keys:
            k = i.split(keys)[1]
            v = Context.RedisCache.hash_getall(i)
            info[k] = v
        mo.set_param('ret', info)
        return mo
    # def do_notice(self, led):
    #     TaskManager.add_simple_task(self._do_notice, led)
    #
    # def _do_notice(self, led):
    #     now_ts = Time.current_ts()
    #     mo = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
    #     bulletin = led.get('bulletin', 3)
    #     msg = led.get('led', '')
    #     mo.set_param('game', {'msg': msg, 'ts': now_ts, 'bulletin': bulletin})
    #     version = led.get('version', 0)
    #     version_db = Context.RedisCache.hash_get_int('global.notice', 'version', 0)
    #     interval = led.get('interval')
    #     end = led.get('end')
    #     if version == version_db and (now_ts + interval) < (end+5):
    #         TaskManager.set_timeout(self.do_notice, interval,
    #                         {'led': msg, 'end': end, 'interval': interval, 'version': version, 'bulletin': bulletin})
    #     Context.GData.broadcast_to_system(mo)

    def gm_modify_groupbuy_num(self, gid, mi, request):
        num = mi.get_param('num')
        now_dt = Time.datetime()
        prefix = Time.datetime_to_str(now_dt, '%Y-%m-%d')
        key = 'group_buy:%d:%s' % (gid, prefix)
        Context.RedisMix.hash_set(key, 'total', num)
        return MsgPack(0)

    def query_history_phone(self, gid, mi, request):
        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        uid_seq_map, all_seq_list = {}, []
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            records = Context.RedisStat.hash_getall('history:%d:%s' % (gid, fmt))
            for seq, uid in records.iteritems():
                if uid not in uid_seq_map:
                    uid_seq_map[uid] = []
                uid_seq_map[uid].append(int(seq))
                all_seq_list.append(int(seq))
            start_day = Time.next_days(start_day)

        _list = []
        if all_seq_list:
            seq_record_map = Context.RedisMix.hash_mget_as_dict('game.%d.exchange.record' % gid, *all_seq_list)
            for uid, seq_list in uid_seq_map.iteritems():
                states = Context.RedisCluster.hash_mget(uid, 'history:%d:%s' % (gid, uid), *seq_list)
                for seq, state in zip(seq_list, states):
                    if state is not None and seq in seq_record_map:
                        record = Context.json_loads(seq_record_map[seq])
                        if record['type'] == 'exchange' and record['to'] == 'phone':
                            record = {
                                'uid': int(uid),
                                'ts': record['ts'],
                                'count': record['count'],
                                'phone': record['phone'],
                                'state': int(state),
                                'seq': seq,
                            }
                            _list.append(record)

        mo = MsgPack(0)
        mo.set_param('exchange', _list)
        return mo

    def query_chip_consume(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_query_chip_consume:", mi)
        Context.Record.add_record_query_chip_consume(mi)

        room_types = (201, 202, 203, 211, 231)
        mini_games = (10002, 10003, 10004)
        fields = ['out.chip.attack']
        for room_type in room_types:
            fields.append('out.chip.game.shot.bullet.%d' % room_type)
        for game in mini_games:
            fields.append('out.chip.game.%d' % game)
        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        mo = MsgPack(0)
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            chips = Context.Stat.get_day_data(gid, fmt, *fields)
            attack = Tool.to_int(chips[0], 0)
            info = []
            for chip in chips[1:]:
                if chip:
                    info.append(int(chip))
                else:
                    info.append(0)
            info[2] += attack
            mo.set_param(fmt, info)
            start_day = Time.next_days(start_day)
        return mo

    def query_chip_produce(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_query_chip_produce:", mi)
        Context.Record.add_record_query_chip_produce(mi)

        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        mo = MsgPack(0)
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            kvs = Context.Stat.get_day_data(gid, fmt)
            task_total, catch_total = 0, 0
            _kvs = {}
            for k, v in kvs.iteritems():
                if k.startswith('in.chip.'):
                    if k.startswith('in.chip.task.get'):
                        task_total += int(v)
                    elif k.startswith('in.chip.catch.bird.'):
                        catch_total += int(v)
                    else:
                        _kvs[k] = int(v)
            _kvs['in.chip.task.reward'] = task_total
            _kvs['in.chip.catch.bird'] = catch_total
            _kvs['in.chip.buy.product'] = int(kvs.get('in.chip.buy.product', 0))
            mo.set_param(fmt, _kvs)
            start_day = Time.next_days(start_day)
        return mo

    # def query_shit_consume(self, gid, mi, request):
    #     room_types = (201, 202, 203, 211, 231)
    #     mini_games = (10002, 10003, 10004)
    #     fields = ['out.shit.attack']
    #     for room_type in room_types:
    #         fields.append('out.shit.game.shot.bullet.%d' % room_type)
    #     for game in mini_games:
    #         fields.append('out.shit.game.%d' % game)
    #     start = mi.get_param('start')
    #     end = mi.get_param('end')
    #     start_day = Time.str_to_datetime(start, '%Y-%m-%d')
    #     end_day = Time.str_to_datetime(end, '%Y-%m-%d')
    #     mo = MsgPack(0)
    #     while start_day <= end_day:
    #         fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
    #         shits = Context.Stat.get_day_data(gid, fmt, *fields)
    #         attack = Tool.to_int(shits[0], 0)
    #         info = []
    #         for shit in shits[1:]:
    #             if shit:
    #                 info.append(int(shit))
    #             else:
    #                 info.append(0)
    #         info[2] += attack
    #         mo.set_param(fmt, info)
    #         start_day = Time.next_days(start_day)
    #     return mo
    #
    # def query_shit_produce(self, gid, mi, request):
    #     start = mi.get_param('start')
    #     end = mi.get_param('end')
    #     start_day = Time.str_to_datetime(start, '%Y-%m-%d')
    #     end_day = Time.str_to_datetime(end, '%Y-%m-%d')
    #     mo = MsgPack(0)
    #     while start_day <= end_day:
    #         fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
    #         kvs = Context.Stat.get_day_data(gid, fmt)
    #         task_total, catch_total = 0, 0
    #         _kvs = {}
    #         for k, v in kvs.iteritems():
    #             if k.startswith('in.shit.'):
    #                 if k.startswith('in.shit.task.reward.'):
    #                     task_total += int(v)
    #                 elif k.startswith('in.shit.catch.bird.'):
    #                     catch_total += int(v)
    #                 else:
    #                     _kvs[k] = int(v)
    #         _kvs['in.shit.task.reward'] = task_total
    #         _kvs['in.shit.catch.bird'] = catch_total
    #         _kvs['in.shit.buy.product'] = int(kvs.get('in.shit.buy.product', 0))
    #         mo.set_param(fmt, _kvs)
    #         start_day = Time.next_days(start_day)
    #     return mo

    def query_diamond_consume(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_query_diamond_consume:", mi)
        Context.Record.add_record_query_diamond_consume(mi)

        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        mo = MsgPack(0)
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            kvs = Context.Stat.get_day_data(gid, fmt)
            _kvs, total = {}, 0
            for k, v in kvs.iteritems():
                if k.startswith('out.diamond.'):
                    if k.startswith('out.diamond.inner.buy.'):
                        k = 'out.diamond.buy.' + k[-3:]
                    elif k.startswith('out.diamond.table.buy.'):
                        k = 'out.diamond.buy.' + k[-3:]
                    if k in _kvs:
                        _kvs[k] += int(v)
                    else:
                        _kvs[k] = int(v)
                    total += int(v)
            _kvs['total'] = total
            mo.set_param(fmt, _kvs)
            start_day = Time.next_days(start_day)
        return mo

    def query_diamond_produce(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_query_diamond_produce:", mi)
        Context.Record.add_record_query_diamond_produce(mi)

        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        mo = MsgPack(0)
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            kvs = Context.Stat.get_day_data(gid, fmt)
            _kvs = {}
            total, task_total, fall_total = 0, 0, 0
            for k, v in kvs.iteritems():
                if k.startswith('in.diamond.'):
                    if k.startswith('in.diamond.task.reward.'):
                        task_total += int(v)
                    elif k.startswith('in.diamond.bird.fall.'):
                        fall_total += int(v)
                    else:
                        _kvs[k] = int(v)
                    total += int(v)
            _kvs['in.diamond.task.reward'] = task_total
            _kvs['in.diamond.bird.fall'] = fall_total
            _kvs['in.diamond.buy.product'] = int(kvs.get('in.diamond.buy.product', 0))
            _kvs['total'] = total
            mo.set_param(fmt, _kvs)
            start_day = Time.next_days(start_day)
        return mo

    def query_egg_fall(self, gid, mi, request):
        room_types = (201, 202, 203, 211, 231)
        props_ids = (211, 212, 213)
        fields = []
        for pid in props_ids:
            for room_type in room_types:
                fields.append('in.props.%d.bird.fall.%d' % (pid, room_type))

        cnt_fields = []
        for pid in props_ids:
            cnt_fields.append('user.count.get.props.%d' % pid)

        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        mo = MsgPack(0)
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            eggs = Context.Stat.get_day_data(gid, fmt, *fields)
            props_info = []
            for i in range(0, len(eggs), len(room_types)):
                fall = 0
                for j in range(len(room_types)):
                    if eggs[i+j]:
                        fall += int(eggs[i+j])
                props_info.append(fall)

            gets = Context.Stat.get_day_data(gid, fmt, *cnt_fields)
            get_total = 0
            for cnt in gets:
                if cnt:
                    get_total += int(cnt)
            mo.set_param(fmt, {'fall': props_info, 'get': get_total})
            start_day = Time.next_days(start_day)
        return mo

    def query_shot(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_query_shot:", mi)
        Context.Record.add_record_query_shot(mi)

        room_types = (201, 202, 203, 211)
        fields = []
        for room_type in room_types:
            fields.append('shot.times.%d' % room_type)
        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        mo = MsgPack(0)
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            values = Context.Stat.get_day_data(gid, fmt, *fields)
            info = []
            for v in values:
                if v:
                    info.append(int(v))
                else:
                    info.append(0)
            mo.set_param(fmt, info)
            start_day = Time.next_days(start_day)
        return mo

    def query_raffle(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_query_raffle:", mi)
        Context.Record.add_record_query_raffle(mi)

        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        eggs = (211, 212, 213, 214)
        fileds = ['in.chip.bonus.raffle', 'in.diamond.bonus.raffle', 'in.coupon.bonus.raffle']
        for egg in eggs:
            fileds.append('in.props.%d.bonus.raffle' % egg)
        mo = MsgPack(0)
        while start_day <= end_day:
            kvs = {}
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            values = Context.Stat.get_day_data(gid, fmt, *fileds)
            kvs['chip'] = Tool.to_int(values[0], 0)
            kvs['diamond'] = Tool.to_int(values[1], 0)
            kvs['coupon'] = Tool.to_int(values[2], 0)
            egg_list = []
            for egg in values[3:]:
                egg_list.append(Tool.to_int(egg, 0))
            kvs['egg'] = egg_list
            mo.set_param(fmt, kvs)
            start_day = Time.next_days(start_day)
        return mo

    def query_room_211(self, gid, mi, request):
        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        pids = (201, 203)
        eggs = (211, 212, 213, 214)
        fileds = ['in.diamond.match.task.101', 'out.chip.game.shot.bullet.211', 'in.chip.catch.bird.211']
        for pid in pids:
            fileds.append('out.props.%d.game.use.211' % pid)
        for egg in eggs:
            fileds.append('in.props.%d.match.award' % egg)
        mo = MsgPack(0)
        while start_day <= end_day:
            kvs = {}
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            values = Context.Stat.get_day_data(gid, fmt, *fileds)
            kvs['in.diamond'] = Tool.to_int(values[0], 0)
            kvs['out.chip'] = Tool.to_int(values[1], 0)
            kvs['in.chip'] = Tool.to_int(values[2], 0)

            props_list = []
            for prop in values[3:3 + len(pids)]:
                props_list.append(Tool.to_int(prop, 0))
            kvs['props'] = props_list
            egg_list = []
            for egg in values[-len(eggs):]:
                egg_list.append(Tool.to_int(egg, 0))
            kvs['egg'] = egg_list
            mo.set_param(fmt, kvs)
            start_day = Time.next_days(start_day)
        return mo


    # 获取所有玩家数据
    def all_player_data(self, gid, mi, request):
        # TF add record
        Context.Log.debug("gm_query_all_player_data:", mi)
        Context.Record.add_record_query_all_user_info(mi)
        user_info = []
        online = []
        sort_uid = []
        ret = Context.RedisCluster.hget_keys('user:*')
        if not ret:
            return MsgPack.Error(0, 2, 'not exist')
        for item in ret:
            user_id = item.split(':')[1]
            play_recharge = self.pay_total_sort(user_id, gid)
            online.append(play_recharge)
        online.sort()
        for uid_dict in online:
            sort_uid.append(uid_dict["uid"])
        sort_uid.sort()

        for uid in sort_uid:
            kvs = self.new_player_info(int(uid), gid)
            if len(kvs) > 0:
                user_info.append(kvs)
            else:
                continue
        mo = MsgPack(0)
        mo.set_param("info", user_info)
        return mo


    def pay_total_sort(self,uid,gid):
        play_recharge = {}
        pay_total = Context.Data.get_game_attr_int(int(uid), gid, 'pay_total', 0)
        play_recharge.update({"uid": int(uid), "pay_total": pay_total})
        return play_recharge


    #新玩家总览
    def new_player_info(self, uid, gid, start_time, end_time):
        user_attrs = ['createTime', 'nick','idType','userName','createIp','channelid', 'platform']
        kvs = Context.Data.get_attrs_dict(uid, user_attrs)
        game_attrs = ['pay_total', 'session_login','barrel_level','inviter','target_coupon', 'chip', 'diamond',
                      'in_props_211', 'in_props_212', 'in_props_213', 'in_props_214', 'out_props_211', 'out_props_212',
                      'out_props_213', 'out_props_214','coupon', 'in_coupon','coupon_pool_private','bonus_pool']
        _kvs = Context.Data.get_game_attrs_dict(uid, gid, game_attrs)
        if not _kvs or not kvs:
            return {}

        kvs.update(_kvs)
        channel_id = kvs.get("channelid")
        phone = Context.Data.get_shop_attr(uid, 'shop:user', 'phone')
        if not phone:
            kvs['exchange_phone'] = 0
        else:
            kvs['exchange_phone'] = phone

        # 用户的所有数据
        in_chip_free = 0   # 总免费鸟蛋
        in_target_coupon_total = 0  # 获取靶卷总数

        user_data = Context.RedisStat.hash_getall('user:2:%d' % (uid))
        for k, v in user_data.items():
            # 获取微信充值额度
            if k.endswith('.weixin_pay.user.pay_total'):
                kvs['weixin_pay_total'] = int(v)
            # 获取兑换码充值额度
            elif k.endswith('.cdkey_pay.user.pay_total'):
                kvs['cdkey_pay_total'] = int(v)
            # 获取支付宝充值额度
            elif k.endswith('.ali_pay.user.pay_total'):
                kvs['ali_pay_total'] = int(v)

            elif k.startswith('in.target_coupon.'):
                in_target_coupon_total += int(v)

            if k.endswith('in.chip.day.activity.value.receive') \
                    or k.endswith('in.chip.exp.upgrade') or k.endswith('in.chip.bind.rewards') or k.endswith('in.chip.activity.task.reward.total') \
                    or k.endswith('in.chip.online.reward') or k.endswith('in.chip.signin.reward') \
                    or k.endswith('in.chip.task.get') or k.endswith('in.chip.unlock.barrel') \
                    or k.endswith('in.chip.vip_receive') or k.endswith('in.chip.week.activity.value.receive') \
                    or k.endswith('in.chip.activity.login.reward') or k.endswith('in.chip.boss.rank.get') \
                    or k.endswith('in.chip.primary.rank.get') or k.endswith('in.chip.middle.rank.get') \
                    or k.endswith('in.chip.high.rank.get') or k.endswith('in.chip.activity.pay.raffle') \
                    or k.endswith('in.chip.activity.login.reward') or k.endswith('in.chip.activity.task.reward.receive') \
                    or k.endswith('in.chip.activity.rank.config') or k.endswith('in.chip.game.startup') or k.endswith('in.chip.cdkey.reward.free'):
                in_chip_free += int(v)

            #鸟蛋产出
            if k.startswith('in.chip.'):
                kvs[k] = v  # tf

            # 鸟蛋消耗
            if k.startswith('out.chip.'):
                kvs[k] = v  # tf

        #用户当天的数据
        day_in_chip_free,day_in_diamond_free,day_award_rate = 0,0,0 # 当天免费鸟蛋、当天免费钻石和当日出奖率
        day_bird_in_coupon, day_in_coupon, day_out_coupon = 0,0,0 #鸟券产出和鸟券消耗

        # 鸟券
        deal_coupon = 0
        if start_time:
            start_date, end_date = str(start_time), str(end_time)
            if start_date != end_date:
                day_time = Time.current_time('%Y-%m-%d')
                deal_coupon = 1
            else:
                day_time = start_date
        else:
            day_time = Time.current_time('%Y-%m-%d')

        user_day = Context.RedisStat.hash_getall('user_daily:%s:%s:%s' % (channel_id, day_time, str(uid)))
        for k, v in user_day.items():

            # 今日鸟场鸟券产出
            if k.startswith('in.coupon.coupon_pool.hit.bird'):
                day_bird_in_coupon += int(v)
            # 今日鸟券产出
            if k.startswith('in.coupon.'):
                day_in_coupon += int(v)

            # 获取今日充值
            if k.endswith('.pay.user.pay_total'):
                kvs['day_pay_total'] = str(v)
            # 获取今日兑换码充值额度
            elif k.endswith('.cdkey_pay.user.pay_total'):
                kvs['day_cdkey_pay_total'] = str(v)

            # 获取今日兑换码充值额度
            elif k.startswith('person_bonus_pool'):
                kvs['person_bonus_pool'] = str(v)

            # 获取今日登录次数
            elif k.startswith('login.times'):
                kvs['day_login_time'] = str(v)

            # 今日鸟券消耗
            elif k.startswith('out.coupon.'):
                day_out_coupon += int(v)

            #今日免费鸟蛋
            elif k.endswith('in.chip.day.activity.value.receive') \
                    or k.endswith('in.chip.exp.upgrade') or k.endswith('in.chip.bind.rewards') or k.endswith('in.chip.activity.task.reward.total') \
                    or k.endswith('in.chip.online.reward') or k.endswith('in.chip.signin.reward') \
                    or k.endswith('in.chip.task.get') or k.endswith('in.chip.unlock.barrel') \
                    or k.endswith('in.chip.vip_receive') or k.endswith('in.chip.week.activity.value.receive') \
                    or k.endswith('in.chip.activity.login.reward') or k.endswith('in.chip.boss.rank.get') \
                    or k.endswith('in.chip.primary.rank.get') or k.endswith('in.chip.middle.rank.get') \
                    or k.endswith('in.chip.high.rank.get') or k.endswith('in.chip.activity.pay.raffle') \
                    or k.endswith('in.chip.activity.login.reward') or k.endswith('in.chip.activity.task.reward.receive') \
                    or k.endswith('in.chip.activity.rank.config') or k.endswith('in.chip.game.startup') or k.endswith('in.chip.cdkey.reward.free'):
                day_in_chip_free += int(v)

            # 今日免费钻石
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
                day_in_diamond_free += int(v)

        # 计算免费抽奖池相对前一天的值
        kvs['bonus_pool_space'] = str(int(kvs.get('bonus_pool', 0)) - int(kvs.get('person_bonus_pool', 0)))

        #总鸟蛋消耗
        kvs['day_coupon_info'] = 0
        kvs['event_coupon_cost'] = 0
        kvs['login_time'] = 0

        kvs['new_weixin_pay_total'] = 0
        kvs['new_ali_pay_total'] = 0
        kvs['new_cdkey_pay_total'] = 0
        kvs['new_sdk_pay_total'] = 0
        create_time = Context.Data.get_attr(int(uid), 'createTime')
        start_day = Time.str_to_datetime(create_time[:10], '%Y-%m-%d')
        end_day = Time.str_to_datetime(Time.current_time('%Y-%m-%d'), '%Y-%m-%d')
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')

            kvs['days_login_time'] = 0

            user_day = Context.RedisStat.hash_getall('user_daily:%s:%s:%s' % (channel_id, fmt, str(uid)))
            for k, v in user_day.items():
                # 获取总登录次数
                if k.startswith('login.times'):
                    kvs['days_login_time'] = int(v)
            kvs['login_time'] += kvs['days_login_time']
            start_day = Time.next_days(start_day)

        if deal_coupon == 1:
            start_day = Time.str_to_datetime(start_time, '%Y-%m-%d')
            end_day = Time.str_to_datetime(end_time, '%Y-%m-%d')
            coupon_total, day_pay_total = 0, 0
            while start_day <= end_day:
                fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
                user_day = Context.RedisStat.hash_getall('user_daily:{}:{}:{}'.format(channel_id, fmt, uid))
                for keys, values in user_day.items():
                    # 区间鸟券产出
                    if keys.startswith('in.coupon.'):
                        coupon_total = coupon_total + int(values)
                    # 当日充值
                    if keys.startswith('{}.pay.user.pay_total'.format(channel_id)):
                        day_pay_total = day_pay_total + int(values)
                start_day = Time.next_days(start_day)
            kvs['day_pay_total'] = day_pay_total
            kvs['day_in_coupon'] = coupon_total
        else:
            kvs['day_in_coupon'] = day_in_coupon

        user_pay = self.get_user_all_pay(gid,uid)
        kvs['new_weixin_pay_total'],kvs['new_sdk_pay_total'] = user_pay["weixin_pay"],user_pay["sdk_pay"]
        kvs['new_cdkey_pay_total'],kvs['new_ali_pay_total'] = user_pay["cdkey_pay"],user_pay["ali_pay"]
        kvs['day_event_coupon_cost'] = str(0)
        #虚拟兑换消耗
        virtual_coupon = 0 #兑换虚拟道具
        data = Context.Data.get_shop_all(uid, 'shop:order')
        for k, v in data.items():
            record_json = Context.json_loads(v)
            if int(record_json["good_type"]) == 3:
                virtual_coupon += int(record_json["price"])

        kvs['weixin_pay_total'] = kvs.get('weixin_pay_total', 0)
        kvs['cdkey_pay_total'] = kvs.get('cdkey_pay_total', 0)
        kvs['ali_pay_total'] = kvs.get('ali_pay_total', 0)
        kvs['target_coupon_total'] = in_target_coupon_total
        #用户的所有免费鸟蛋
        kvs['in_chip_free'] = str(in_chip_free)

        kvs['day_login_time'] = kvs.get('day_login_time', 0)
        kvs['day_pay_total'] = kvs.get('day_pay_total', 0)
        # kvs['person_bonus_pool'] = kvs.get('person_bonus_pool', 0)
        kvs['day_cdkey_pay_total'] = kvs.get('day_cdkey_pay_total', 0)
        kvs['day_in_chip_free'] = str(day_in_chip_free)
        kvs['day_in_diamond_free'] = str(day_in_diamond_free)
        # kvs['day_in_coupon'] = day_in_coupon
        kvs['day_bird_in_coupon'] = day_bird_in_coupon

        kvs['nick'] = kvs.get('nick', "")
        kvs['target_coupon'] = int(kvs.get('target_coupon', 0))
        kvs['createIp'] = kvs.get('createIp', 0)
        kvs['chip'] = int(kvs.get('chip', 0))
        kvs['inviter'] = int(kvs.get('inviter', 0))
        kvs['target_coupon'] = int(kvs.get('target_coupon', 0))
        kvs['uid'] = uid

        kvs['diamond'] = int(kvs.get('diamond', 0))
        kvs['in_props_211'] = int(kvs.get('in_props_211', 0))
        kvs['in_props_212'] = int(kvs.get('in_props_212', 0))
        kvs['in_props_213'] = int(kvs.get('in_props_213', 0))
        kvs['in_props_214'] = int(kvs.get('in_props_214', 0))

        kvs['out_props_211'] = int(kvs.get('out_props_211', 0))
        kvs['out_props_212'] = int(kvs.get('out_props_212', 0))
        kvs['out_props_213'] = int(kvs.get('out_props_213', 0))
        kvs['out_props_214'] = int(kvs.get('out_props_214', 0))

        kvs['coupon'] = int(kvs.get('coupon', 0))
        kvs['in_coupon'] = int(kvs.get('in_coupon', 0))

        kvs['in_kind_coupon'] = int(kvs.get('in_coupon', 0)) - virtual_coupon - int(kvs.get('coupon', 0))
        kvs['virtual_coupon'] = virtual_coupon

        dt = Time.str_to_datetime(kvs['createTime'], '%Y-%m-%d %X.%f')
        kvs['createTime'] = Time.datetime_to_str(dt, '%Y-%m-%d %X')

        dt = Time.str_to_datetime(kvs['session_login'], '%Y-%m-%d %X.%f')
        login_time = Time.datetime_to_str(dt, '%Y-%m-%d %X')
        kvs['session_login'] = login_time

        last_time = Time.yesterday_time(Time.str_to_timestamp(login_time[:10], "%Y-%m-%d"))
        result = Context.Stat.get_daily_user_data(kvs["channelid"], uid, last_time)
        if len(result) > 0:
            fix_own_chip = int(result.get("fix_own_chip",0))
        else:
            fix_own_chip = 0

        kvs['fix_own_chip'] = fix_own_chip
        if day_time != Time.current_time('%Y-%m-%d'):
            result = Context.Stat.get_daily_user_data(kvs["channelid"], uid, day_time)
            if len(result) > 0:
                day_own_chip = int(result.get("fix_own_chip", 0))
            else:
                day_own_chip = 0

            kvs['chip'] = day_own_chip

        # 今日新增鸟蛋剩余
        now_chip = int(kvs.get('chip', 0))
        # fix_own_chip = int(kvs.get('fix_own_chip', 0))
        if now_chip < 1 or now_chip < fix_own_chip:
            day_add_chip = 0
        else:
            day_add_chip = now_chip - fix_own_chip

        kvs['day_add_chip'] = day_add_chip
        #当日出奖率
        day_surplus_chip = int(kvs.get('day_pay_total', 0)) + float(fix_own_chip/5000)
        if day_surplus_chip == 0:
            kvs['day_award_rate'] = '%.2f' % (day_in_coupon + float(day_add_chip/5000))
        else:
            kvs['day_award_rate'] = '%.2f' % ((day_in_coupon + float(day_add_chip/5000)) / float(day_surplus_chip))

        end_ts = Context.RedisMix.hash_get_int('game.%d.freeze.user' % gid, uid, 0)
        if end_ts != 0:
            if end_ts > Time.current_ts():
                kvs['freeze_user'] = end_ts
            else:
                Context.RedisMix.hash_del('game.%d.freeze.user' % gid, uid)
                kvs['freeze_user'] = 0
        else:
            kvs['freeze_user'] = end_ts

        if int(kvs.get('idType', 0)) == 13:
            kvs['phone'] = kvs['userName']
        else:
            kvs['phone'] = 0

        kill_info = Context.UserAttr.get_kill_chip(uid, gid)#玩家当前杀分额度
        if not kill_info:
            kvs['kill_chip'] = 0
        else:
            kvs['kill_chip'] = kill_info

        rate_info = Context.UserAttr.get_kill_chip_rate(uid, gid)  # 收分比例
        if not rate_info:
            kvs['chip_rate'] = [0,0]
        else:
            kvs['chip_rate'] = rate_info

        # 送分比例
        give_chip_rate = Context.UserAttr.get_give_chip_rate(uid, gid, [0, 0])
        kvs['give_chip_rate'] = give_chip_rate

        # 送分区间炮倍
        give_chip_effect_bm = Context.UserAttr.get_give_chip_effect_bm(uid, gid, [0, 0])
        kvs['give_chip_effect'] = give_chip_effect_bm

        give_info = Context.UserAttr.get_give_chip(uid, gid)  # 玩家当前送分额度
        if not give_info:
            kvs['give_chip'] = 0
        else:
            kvs['give_chip'] = give_info

        #历史收分
        key = 'user:{}:{}'.format(gid,uid)
        history_kill_chip = Context.RedisStat.hash_get(key, 'out.kill_chip.kill_chip.triggle', 0)
        kvs['history_kill_chip'] = history_kill_chip

        # 历史送分
        key = 'user:{}:{}'.format(gid, uid)
        history_give_chip = Context.RedisStat.hash_get(key, 'out.give_chip.give_chip.triggle', 0)
        kvs['history_give_chip'] = history_give_chip

        user_sign = Context.Data.get_game_attr_int(int(uid), gid, "p_protected.flag_bad_guy", 0)
        kvs['user_sign'] = user_sign

        min_percent = Context.UserAttr.get_user_min_cost_percent_flag(uid, gid)
        kvs['min_percent'] = min_percent

        kvs['pay_total'] = int(kvs.get('pay_total', 0))
        barrel_level = int(kvs.get('barrel_level', 0))
        kvs['barrel_multiple'] = BirdAccount.trans_barrel_level(gid, barrel_level)
        l = (201, 202, 203, 204, 205, 211, 212, 213, 214, 215, 216, 217, 218, 219)
        _list = BirdProps.get_props_list(uid, gid, l)
        props_map = dict(_list)
        props_list = []
        for i in l:
            count = props_map.get(i, 0)
            props_list.append(count)
        # kvs['props'] = props_list
        kvs['props_201'],kvs['props_202'],kvs['props_203'],kvs['props_204'],kvs['props_205'],kvs['props_211']= props_list[0],props_list[1],props_list[2],props_list[3],props_list[4],props_list[5]
        kvs['props_212'], kvs['props_213'], kvs['props_214'], kvs['props_215'], kvs['props_216'] = props_list[6],props_list[7],props_list[8],props_list[9],props_list[10]
        kvs['props_217'], kvs['props_218'], kvs['props_219'] = props_list[11],props_list[12],props_list[13]
        return kvs

    def wechat_bind(self, gid, mi, request):
        _name = mi.get_param('username')
        _pw = mi.get_param('password')
        _id = mi.get_param('ID')
        _weixin = mi.get_param('openid')
        channelid = mi.get_param('channelid')
        idType = Const.IDTYPE_USERNAME
        userId = Account.getUserIDByUserName(_name, idType, channelid)
        if not userId:
            return MsgPack.Error(0, 1, u'用户不存在')

        token, weixin = Context.Data.get_attrs(userId, ['token', 'weixin'])
        if weixin:
            if weixin != _weixin:
                return MsgPack.Error(0, 2, u'已经绑定其他微信号')
            return MsgPack(0)

        md5_pass = Entity.encodePassword(_name, _pw)
        if md5_pass != token:
            return MsgPack.Error(0, 3, u'昵称或密码错误')

        keys = ['weixin']
        values = [_weixin]
        if _id:
            keys.append('ID')
            values.append(_id)
        Context.Data.set_attrs(userId, keys, values)

        key = 'weixin:' + str(_weixin)
        Context.RedisMix.hash_setnx(key, _name, userId)
        return MsgPack(0)

    def wechat_unbind(self, gid, mi, request):
        _name = mi.get_param('username')
        _pw = mi.get_param('password')
        _id = mi.get_param('ID')
        _weixin = mi.get_param('openid')
        channelid = mi.get_param('channelid')
        idType = Const.IDTYPE_USERNAME
        userId = Account.getUserIDByUserName(_name, idType, channelid)
        if not userId:
            return MsgPack.Error(0, 1, u'用户不存在')

        token, weixin, id_card = Context.Data.get_attrs(userId, ['token', 'weixin', 'ID'])
        if weixin and weixin != _weixin:
            return MsgPack.Error(0, 2, u'已经绑定其他微信号')

        if id_card and id_card != _id:
            return MsgPack.Error(0, 3, u'身份证号不正确')

        md5_pass = Entity.encodePassword(_name, _pw)
        if md5_pass != token:
            return MsgPack.Error(0, 4, u'昵称或密码错误')

        Context.Data.del_attrs(userId, 'weixin', 'ID')

        key = 'weixin:' + str(_weixin)
        Context.RedisMix.hash_del(key, _name)
        return MsgPack(0)

    def wechat_modify_password(self, gid, mi, request):
        _name = mi.get_param('username')
        _weixin = mi.get_param('openid')
        _pw = mi.get_param('password')
        channelid = mi.get_param('channelid')
        idType = Const.IDTYPE_USERNAME
        userId = Account.getUserIDByUserName(_name, idType, channelid)
        if not userId:
            return MsgPack.Error(0, 1, u'用户不存在')

        weixin = Context.Data.get_attr(userId, 'weixin')
        if not weixin:
            return MsgPack.Error(0, 2, u'该用户未绑定')
        elif weixin != _weixin:
            return MsgPack.Error(0, 3, u'已经绑定其他微信号')

        if not Entity.checkPassword(_pw):
            return MsgPack.Error(0, 4, u'密码不合法')

        md5_pass = Entity.encodePassword(_name, _pw)
        Context.Data.set_attr(userId, 'token', md5_pass)
        Context.Data.del_attrs(userId, 'accessToken')
        return MsgPack(0)

    def query_pay_detail(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_query_pay_detail:", mi)
        Context.Record.add_record_query_pay_detail(mi)

        conf = Context.Configure.get_game_item_json(gid, 'product.config')
        pids = []
        for pid in conf.iterkeys():
            pids.append('product_' + pid)
        start = mi.get_param('start')
        end = mi.get_param('end')
        start_day = Time.str_to_datetime(start, '%Y-%m-%d')
        end_day = Time.str_to_datetime(end, '%Y-%m-%d')
        mo = MsgPack(0)
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            times = Context.Stat.get_day_data(gid, fmt, *pids)
            kvs = {}
            for k, v in zip(pids, times):
                pid = k.replace('product_', '')
                kvs[k] = Tool.to_int(v, 0)
            mo.set_param(fmt, kvs)
            start_day = Time.next_days(start_day)
        return mo

    def update_shop_info(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_update_shop_info:", mi)
        Context.Record.add_record_update_shop_info(mi)

        channel_id = mi.get_param('cid')
        ntype = int(mi.get_param('ntype'))
        gids = str(mi.get_param('gids'))
        name = mi.get_param('name')
        count = mi.get_param('count')

        # prop_limit = mi.get_param('prop_limit')
        limit_num = mi.get_param('limit_num')
        price = mi.get_param('price')
        goods_type = mi.get_param('goods_type')
        vip_limit = mi.get_param('vip_limit')
        money_type = mi.get_param('money_type')
        line = mi.get_param('line')
        # uptime = mi.get_param('uptime')
        if ntype == 1:
            limit_config = Context.Configure.get_game_item_json(gid, 'limit.shop.config')
            cid = channel_id
            if not limit_config.has_key(cid):
                cid = '1001_0'
            shop_config = limit_config.get(cid, None)
        else:
            shop_config = Context.Configure.get_game_item_json(gid, 'exchange.config')
        if not shop_config:
            return MsgPack.Error(0, 2, 'not config')
        update = Context.RedisConfig.hash_get_int('configitem', 'update.time')
        if not update:
            return MsgPack.Error(0, 3, 'not update time')
        update_config = {}

        for k, v in shop_config.items():
            good_id = str(k)
            if good_id == gids:
                v[0] = str(name)
                v[1] = goods_type
                if v[2].has_key('props'):
                    v[2]['props'][0]['count'] = count
                else:
                    keys = v[2].keys()[0]
                    v[2][keys] = count
                v[3] = money_type
                v[4] = price
                v[5] = vip_limit
                v[6][1]['num'] = limit_num
                v[8] = line
                info = [v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], v[8]]
                update_config[gids] = info
                continue
            update_config[k] = v
        if ntype == 1:
            shop_config = Context.Configure.get_game_item_json(gid, 'limit.shop.config')
            shop_config[channel_id] = update_config
            Context.RedisConfig.hash_set("configitem", "game:2:limit.shop.config", Context.json_dumps(shop_config))
        else:
            Context.RedisConfig.hash_set("configitem", "game:2:exchange.config", Context.json_dumps(update_config))

        Context.RedisConfig.hash_set('configitem', 'update.time', Time.current_ts())
        Context.Configure.reload()
        cmd = Message.MSG_SYS_UPDATE_SHOP_CONFIG | Message.ID_REQ
        Context.GData.send_to_entity(1000001, mi, cmd=cmd, gid=gid)

    def exchange_record(self, gid, mi, request):
        # dz add record
        Context.Log.debug("gm_exchange_record:", mi)
        Context.Record.add_record_exchange_record(mi)
        ret = Context.RedisCluster.hget_keys('shop:order:*')
        if not ret:
            return MsgPack.Error(0, 1, 'not exist')
        record_info = []
        input_data = mi.get_param('input_data')
        start = mi.get_param('start')
        end = mi.get_param('end')
        if input_data != None:
            screen_info = mi.get_param('screen_info')
            if screen_info == "uid":
                uid = int(input_data)
                channelid = Context.Data.get_attr(uid, 'channelid')
                if channelid == None:
                    return MsgPack.Error(0, 2, 'not uid')
                other_coupon, pay_total, in_coupon, coupon = self.shop_virtual_coupon(uid, gid)
                all_pay = self.all_exchange_data(uid=uid,start=start,end=end)
                user_pay = self.get_user_all_pay(gid,uid)
                data = Context.Data.get_shop_all(int(input_data), 'shop:order')

                for stamp, value in data.items():
                    days = int(stamp) / 1000
                    day_time = Time.timestamp_to_str(days,'%Y-%m-%d')
                    day_total,day_cdkey = self.get_everyday_data(uid,day_time)
                    value = Context.json_loads(value)
                    value.update(user_pay)
                    value.update({"day_total":day_total,"day_cdkey":day_cdkey,"channelid":channelid,"pay_total":pay_total,"all_pay": all_pay,"in_coupon":in_coupon,"coupon":coupon,"other_coupon":other_coupon})
                    record_info.append({stamp: value})
            else:
                for item in ret:
                    uid = int(item.split(':')[2])
                    nick = Context.Data.get_attr(uid, 'nick')
                    if nick == input_data:
                        channelid = Context.Data.get_attr(uid, 'channelid')
                        other_coupon, pay_total, in_coupon, coupon = self.shop_virtual_coupon(uid, gid)
                        all_pay = self.all_exchange_data(uid=uid,start=start,end=end)
                        user_pay = self.get_user_all_pay(gid, uid)
                        data = Context.Data.get_shop_all(uid, 'shop:order')
                        for stamp, value in data.items():
                            days = int(stamp) / 1000
                            day_time = Time.timestamp_to_str(days, '%Y-%m-%d')
                            day_total, day_cdkey = self.get_everyday_data(uid, day_time)
                            value = Context.json_loads(value)
                            value.update(user_pay)
                            value.update({"day_total":day_total,"day_cdkey":day_cdkey,"channelid": channelid, "pay_total": pay_total,"all_pay": all_pay, "in_coupon": in_coupon,"coupon": coupon,"other_coupon":other_coupon})
                            record_info.append({stamp: value})
        else:
            start_stamp = Time.str_to_timestamp(start)
            end_stamp = Time.str_to_timestamp(end)

            for item in ret:
                uid = int(item.split(':')[2])
                channelid = Context.Data.get_attr(uid, 'channelid')
                other_coupon, pay_total, in_coupon, coupon = self.shop_virtual_coupon(uid, gid)
                all_pay = self.all_exchange_data(uid=uid,start=start,end=end)
                user_pay = self.get_user_all_pay(gid, uid)
                data = Context.Data.get_shop_all(uid, 'shop:order')
                for stamp, value in data.items():
                    value = Context.json_loads(value)
                    days = int(stamp) /1000
                    if days >= start_stamp and days <= end_stamp:
                        day_time = Time.timestamp_to_str(days, '%Y-%m-%d')
                        day_total, day_cdkey = self.get_everyday_data(uid, day_time)
                        value.update(user_pay)
                        value.update({"day_total":day_total,"day_cdkey":day_cdkey,"channelid": channelid, "pay_total": pay_total,"all_pay": all_pay, "in_coupon": in_coupon, "coupon": coupon,"other_coupon":other_coupon})
                        record_info.append({stamp: value})
                    else:
                        continue
        mo = MsgPack(0)
        mo.set_param('ret', record_info)
        return mo

    def get_everyday_data(self,user_id,day):
        channel = Context.Data.get_attr(user_id, 'channelid')
        result = Context.RedisStat.hash_getall('user_daily:{}:{}:{}'.format(channel, day, user_id))
        if len(result) > 0:
            day_total, day_cdkey = 0, 0
            for k, v in result.items():
                if k.startswith('{}.pay.user.pay_total'.format(channel)):
                    day_total = int(v)
                if k.startswith('{}.cdkey_pay.user.pay_total'.format(channel)):
                    day_cdkey = int(v)
            day_total += day_cdkey
        else:
            day_total, day_cdkey = 0, 0
        return day_total,day_cdkey

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
        pay_info['weixin_pay'],pay_info['sdk_pay'],pay_info['ali_pay'],pay_info['cdkey_pay'] = weixin_pay,sdk_pay,ali_pay,cdkey_pay
        return pay_info

    def point_exchange_record(self, gid, mi, request):
        # dz add record
        # Context.Log.debug("gm_exchange_record:", mi)
        # Context.Record.add_record_exchange_record(mi)
        ret = Context.RedisCluster.hget_keys('point_shop:order:*')
        if not ret:
            return MsgPack.Error(0, 1, 'not exist')
        record_info = []
        start = mi.get_param('start')
        end = mi.get_param('end')
        input_data = mi.get_param('input_data')
        if input_data != None:
            screen_info = mi.get_param('screen_info')
            if screen_info == "uid":
                uid = int(input_data)
                channelid = Context.Data.get_attr(uid, 'channelid')
                if channelid == None:
                    return MsgPack.Error(0, 2, 'not uid')
                pay_total = Context.Data.get_game_attr_int(uid, gid, 'pay_total', 0)
                all_pay = self.all_exchange_data(uid=uid,start=start,end=end)
                data = Context.Data.get_shop_all(int(input_data), 'point_shop:order')
                for stamp, v in data.items():
                    v = Context.json_loads(v)
                    aid = v.get('ak')
                    total_point, use_point, surplus_point = PointShopActivity.get_activity_point(uid, aid)
                    v.update({"channelid": channelid, "pay_total": pay_total, "all_pay": all_pay,
                              "total_point": total_point, "use_point": use_point, "surplus_point": surplus_point})
                    record_info.append({stamp: v})
            else:
                for item in ret:
                    uid = int(item.split(':')[2])
                    nick = Context.Data.get_attr(uid, 'nick')
                    if nick == input_data:
                        channelid = Context.Data.get_attr(uid, 'channelid')
                        pay_total = Context.Data.get_game_attr_int(uid, gid, 'pay_total', 0)
                        all_pay = self.all_exchange_data(uid=uid,start=start,end=end)
                        data = Context.Data.get_shop_all(uid, 'point_shop:order')
                        for stamp, v in data.items():
                            v = Context.json_loads(v)
                            aid = v.get('ak')
                            total_point, use_point, surplus_point = PointShopActivity.get_activity_point(uid, aid)
                            v.update({"channelid": channelid, "pay_total": pay_total, "all_pay": all_pay,
                                      "total_point": total_point, "use_point": use_point,
                                      "surplus_point": surplus_point})
                            record_info.append({stamp: v})
        else:
            start_stamp = Time.str_to_timestamp(start)
            end_stamp = Time.str_to_timestamp(end)
            for item in ret:
                uid = int(item.split(':')[2])
                channelid = Context.Data.get_attr(uid, 'channelid')
                pay_total = Context.Data.get_game_attr_int(uid, gid, 'pay_total', 0)
                all_pay = self.all_exchange_data(uid=uid,start=start,end=end)
                data = Context.Data.get_shop_all(uid, 'point_shop:order')
                for stamp, v in data.items():
                    v = Context.json_loads(v)
                    days = int(stamp) /1000
                    if days >= start_stamp and days <= end_stamp:
                        aid = v.get('ak')
                        total_point, use_point, surplus_point = PointShopActivity.get_activity_point(uid, aid)
                        v.update({"channelid": channelid, "pay_total": pay_total, "all_pay": all_pay,
                                  "total_point": total_point, "use_point": use_point, "surplus_point": surplus_point})
                        record_info.append({stamp: v})
        mo = MsgPack(0)
        mo.set_param('ret', record_info)
        return mo

    def shop_virtual_coupon(self,uid,gid):
        #虚拟兑换消耗
        virtual_coupon = 0 #兑换虚拟道具
        data = Context.Data.get_shop_all(uid, 'shop:order')
        for k, v in data.items():
            record_json = Context.json_loads(v)
            if int(record_json["good_type"]) == 3:
                virtual_coupon += int(record_json["price"])
        pay_total, in_coupon, coupon = Context.Data.get_game_attrs(uid, gid, ['pay_total', 'in_coupon', 'coupon'])
        if pay_total:
            pay_total = pay_total
        else:
            pay_total = 0

        if in_coupon:
            in_coupon = int(in_coupon)
        else:
            in_coupon = 0

        if coupon:
            coupon = int(coupon)
        else:
            coupon = 0
        other_coupon = in_coupon - virtual_coupon - coupon
        return other_coupon,pay_total,in_coupon,coupon

    def all_exchange_data(self,uid,start,end):
        new_pay_user_total = 0
        channel_id = Context.Data.get_attr(int(uid), 'channelid')
        start_day = Time.str_to_datetime(start[:10], '%Y-%m-%d')
        end_day = Time.str_to_datetime(end[:10], '%Y-%m-%d')
        while start_day <= end_day:
            fmt = Time.datetime_to_str(start_day, '%Y-%m-%d')
            user_pay_total = 0
            user_day = Context.RedisStat.hash_getall('user_daily:%s:%s:%s' % (channel_id, fmt, str(uid)))
            for k, v in user_day.items():
                # 获取充值额度
                if k.startswith('{}.pay.user.pay_total'.format(channel_id)):
                    user_pay_total = int(v)
            new_pay_user_total += user_pay_total
            start_day = Time.next_days(start_day)
        return new_pay_user_total

    def get_red_packet_info(self, gid, mi, request):
        # TF add record
        Context.Log.debug("gm_get_red_packet_info:", mi)
        Context.Record.add_record_get_red_packet_info(mi)
        red_type = int(mi.get_param('red_type'))
        start_time = mi.get_param('start')
        end_time = mi.get_param('end')
        start_stamp = Time.str_to_timestamp(start_time)
        end_stamp = Time.str_to_timestamp(end_time)

        if red_type == 0:
            packet_type = "special"
        else:
            packet_type = "special_timer"

        special = []
        ret = Context.RedisCluster.hget_keys('red_packet:{}:*'.format(packet_type))
        if not ret:
            return MsgPack.Error(0, 2, '{} not exist'.format(packet_type))

        times_list = []
        for item in ret:
            times_stamp = int(item.split(':')[2])
            if times_stamp >= start_stamp and times_stamp <= end_stamp:
                times_list.append(str(times_stamp))
        times_list.sort()

        if red_type == 0:
            for now in times_list:  # 全服普通红包
                red_packet = Context.Data.get_red_packet_all(1000001, 'red_packet:{}'.format(packet_type), now)
                red_packet_type = int(red_packet.get("red_packet_type",0))
                if red_packet_type == 0:
                    new_red_packet = self.verify_red_packet(red_packet)
                    new_red_packet.update({"day_time": Time.timestamp_to_str(int(now))})
                    special.append(new_red_packet)
                else:
                    continue
        else:
            for new_now in times_list:  # 全服定时红包
                special_dict = {}
                special_conf = Context.Data.get_red_packet_all(1000001, 'red_packet:{}'.format(packet_type), new_now)
                packet_str = special_conf.get("send_packet_list")

                special_list = []
                packet_list = Context.json_loads(packet_str)
                for now in packet_list:
                    red_packet = Context.Data.get_red_packet_all(1000001, 'red_packet:special', now)
                    new_red_packet = self.verify_red_packet(red_packet)
                    special_list.append(new_red_packet)
                # special_dict = copy.deepcopy(special_conf)
                special_dict.update(special_conf)

                special_dict.update({"red_info": special_list})
                special.append(special_dict)

        mo = MsgPack(0)
        mo.set_param(packet_type, special)
        return mo


    def verify_red_packet(self,red_packet):
        if red_packet.has_key('packet_list'):
            del red_packet["packet_list"]
        if red_packet.has_key('surplus_list'):
            del red_packet["surplus_list"]
        if red_packet.has_key('rank_money'):
            del red_packet["rank_money"]
        return red_packet

    def old_config(self, gid, mi, request):
        aid = mi.get_param('aid')
        if aid == 1:
            pid = mi.get_param('pid')
            if pid == 1:
                mo = MsgPack(0)
                cnf = PayActivity.activity_pay_config()
                if cnf == None: cnf = {}
                mo.set_param('ret', cnf)
                mo.set_param('aid', aid)
                mo.set_param('pid', pid)
                return mo
            elif pid == 2:
                ret = mi.get_param('ret')
                Context.RedisConfig.hash_set("configitem", "game:2:activity.pay.config", Context.json_dumps(ret))

                Context.RedisConfig.hash_set('configitem', 'update.time', Time.current_ts())
                Context.Configure.reload()
                cmd = Message.MSG_SYS_UPDATE_ACTIVITY_CONFIG | Message.ID_REQ
                Context.GData.send_to_entity(1000001, mi, cmd=cmd, gid=gid)
            else:
                return MsgPack.Error(0, 1, 'not exist pid')
        elif aid == 2:
            pid = mi.get_param('pid')
            if pid == 1:
                mo = MsgPack(0)
                cnf = TaskActivity.activity_task_config()
                if cnf == None: cnf = {}
                mo.set_param('ret', cnf)
                mo.set_param('aid', aid)
                mo.set_param('pid', pid)
                return mo
            elif pid == 2:
                ret = mi.get_param('ret')
                Context.RedisConfig.hash_set("configitem", "game:2:activity.task.config", Context.json_dumps(ret))

                Context.RedisConfig.hash_set('configitem', 'update.time', Time.current_ts())
                Context.Configure.reload()
                cmd = Message.MSG_SYS_UPDATE_ACTIVITY_CONFIG | Message.ID_REQ
                Context.GData.send_to_entity(1000001, mi, cmd=cmd, gid=gid)
            else:
                return MsgPack.Error(0, 2, 'not exist pid')
        elif aid == 3:
            pid = mi.get_param('pid')
            if pid == 1:
                mo = MsgPack(0)
                cnf = RankActivity.activity_rank_config()
                if cnf == None: cnf = {}
                mo.set_param('ret', cnf)
                mo.set_param('aid', aid)
                mo.set_param('pid', pid)
                return mo
            elif pid == 2:
                ret = mi.get_param('ret')
                Context.RedisConfig.hash_set("configitem", "game:2:activity.rank.config", Context.json_dumps(ret))

                Context.RedisConfig.hash_set('configitem', 'update.time', Time.current_ts())
                Context.Configure.reload()
                cmd = Message.MSG_SYS_UPDATE_ACTIVITY_CONFIG | Message.ID_REQ
                Context.GData.send_to_entity(1000001, mi, cmd=cmd, gid=gid)
            else:
                return MsgPack.Error(0, 3, 'not exist pid')
        elif aid == 4:
            pid = mi.get_param('pid')
            if pid == 1:
                mo = MsgPack(0)
                cnf = LoginActivity.activity_login_config()
                if cnf == None: cnf = {}
                mo.set_param('ret', cnf)
                mo.set_param('aid', aid)
                mo.set_param('pid', pid)
                return mo
            elif pid == 2:
                ret = mi.get_param('ret')
                Context.RedisConfig.hash_set("configitem", "game:2:activity.login.config", Context.json_dumps(ret))

                Context.RedisConfig.hash_set('configitem', 'update.time', Time.current_ts())
                Context.Configure.reload()
                cmd = Message.MSG_SYS_UPDATE_ACTIVITY_CONFIG | Message.ID_REQ
                Context.GData.send_to_entity(1000001, mi, cmd=cmd, gid=gid)
            else:
                return MsgPack.Error(0, 4, 'not exist pid')
        elif aid == 5:
            pid = mi.get_param('pid')
            if pid == 1:
                mo = MsgPack(0)
                cnf = ShareActivity.activity_share_config()
                if cnf == None: cnf = {}
                mo.set_param('ret', cnf)
                mo.set_param('aid', aid)
                mo.set_param('pid', pid)
                return mo
            elif pid == 2:
                ret = mi.get_param('ret')
                Context.RedisConfig.hash_set("configitem", "game:2:activity.share.config", Context.json_dumps(ret))

                Context.RedisConfig.hash_set('configitem', 'update.time', Time.current_ts())
                Context.Configure.reload()
                cmd = Message.MSG_SYS_UPDATE_ACTIVITY_CONFIG | Message.ID_REQ
                Context.GData.send_to_entity(1000001, mi, cmd=cmd, gid=gid)
            else:
                return MsgPack.Error(0, 5, 'not exist pid')
        elif aid == 6:
            pid = mi.get_param('pid')
            if pid == 1:
                mo = MsgPack(0)
                cnf = DiscountActivity.activity_discount_config()
                if cnf == None: cnf = {}
                mo.set_param('ret', cnf)
                mo.set_param('aid', aid)
                mo.set_param('pid', pid)
                return mo
            elif pid == 2:
                ret = mi.get_param('ret')
                product = ret.get('product')[0]
                product_id = product.get('product_id')
                weapon_id = product.get('id')
                weapon_config = Context.Configure.get_game_item_json(gid, 'weaponshop.config')
                if weapon_config.has_key(str(weapon_id)):
                    nid = weapon_config.get(str(weapon_id))[4]
                    if len(nid) >= 4:
                        activity_shop_config = Context.Configure.get_game_item_json(gid, 'activity_shop.config')
                        info = [{'a_pid': product_id, 'pid': nid}]
                        activity_shop_config['weapon'] = info
                        Context.RedisConfig.hash_set("configitem", "game:2:activity_shop.config",
                                                     Context.json_dumps(activity_shop_config))
                        Context.RedisConfig.hash_set('configitem', 'update.time', Time.current_ts())
                        Context.Configure.reload()
                    else:
                        return MsgPack.Error(0, 9, 'not product')
                else:
                    return MsgPack.Error(0, 10, 'not weapon_id')

                Context.RedisConfig.hash_set("configitem", "game:2:activity.discount.config", Context.json_dumps(ret))

                Context.RedisConfig.hash_set('configitem', 'update.time', Time.current_ts())
                Context.Configure.reload()
                cmd = Message.MSG_SYS_UPDATE_ACTIVITY_CONFIG | Message.ID_REQ
                Context.GData.send_to_entity(1000001, mi, cmd=cmd, gid=gid)
            else:
                return MsgPack.Error(0, 6, 'not exist pid')
        elif aid == 7:
            pid = mi.get_param('pid')
            if pid == 1:
                mo = MsgPack(0)
                cnf = GiveActivity.activity_give_config()
                if cnf == None: cnf = {}
                mo.set_param('ret', cnf)
                mo.set_param('aid', aid)
                mo.set_param('pid', pid)
                return mo
            elif pid == 2:
                ret = mi.get_param('ret')
                Context.RedisConfig.hash_set("configitem", "game:2:activity.give.config", Context.json_dumps(ret))

                Context.RedisConfig.hash_set('configitem', 'update.time', Time.current_ts())
                Context.Configure.reload()
                cmd = Message.MSG_SYS_UPDATE_ACTIVITY_CONFIG | Message.ID_REQ
                Context.GData.send_to_entity(1000001, mi, cmd=cmd, gid=gid)
            else:
                return MsgPack.Error(0, 7, 'not exist pid')
        else:
            return MsgPack.Error(0, 8, 'not exist aid')
        return

BirdShell = BirdShell()
