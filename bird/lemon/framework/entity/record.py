#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: dz  后面需要考虑把这部分记录存放在mysql，以及保存时间限制，例如：超过30天的记录清理
# Create: 2015-08-03

from framework.interface import ICallable
from framework.interface import IContext
from framework.util.tool import Time

class Record(ICallable, IContext):

    ############### shell server ########################

    def add_record_mail(self, msg):
        key = 'shell:event:gm_mail'       # gm 操作邮件
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_freeze(self, msg):
        key = 'shell:event:gm_freeze_user'    # gm 操作冻结
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_disable(self, msg):
        key = 'shell:event:gm_disable_user'   # gm 操作封禁
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_kill_chip(self, msg):
        key = 'shell:event:gm_user_kill_chip'    # gm 操作收分
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_give_chip(self, msg):
        key = 'shell:event:gm_user_give_chip'    # gm 操作送分
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_recharge_add_gift(self, msg):
        key = 'shell:event:gm_recharge_add_gift'  # gm 充值加赠
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_pay(self, msg):
        key = 'shell:event:gm_pay'  # gm 模拟充值
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_query_summary(self, msg):
        key = 'shell:event:gm_query_summary'  # gm 查询数据
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_query_online_detail(self, msg):
        key = 'shell:event:gm_query_online_detail'  # gm 查询在线详情
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_query_money_count(self, msg):
        key = 'shell:event:gm_query_money_count'  # gm 货币统计-
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_gm_data_summarizing(self, msg):
        key = 'shell:event:gm_data_summarizing'  # gm 数据总览
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_gm_query_overview(self, msg):
        key = 'shell:event:gm_query_overview'  # gm 临时数据总览
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_query_coupon_output(self, msg):
        key = 'shell:event:gm_query_coupon_output'  # gm 货币统计-鸟卷
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_query_super_weapon_count(self, msg):
        key = 'shell:event:gm_query_super_weapon_count'  # gm 货币统计-超级武器
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_query_box_fall(self, msg):
        key = 'shell:event:gm_query_box_fall'  # gm 货币统计-宝箱掉落
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_query_carry_chip(self, msg):
        key = 'shell:event:gm_query_carry_chip'  # gm 查询携带金币
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_query_shop_info(self, msg):
        key = 'shell:event:gm_query_shop_info'  # gm 查询商城信息
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_exchange_record(self, msg):
        key = 'shell:event:gm_exchange_record'  # gm 查询兑换记录
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_many_approve_status(self, msg):
        key = 'shell:event:gm_approve_state'  # gm 修改多个审核状态
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_shipping_info(self, msg):
        key = 'shell:event:gm_shipping_info'  # gm 商城实物发货信息
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_shipping_state(self, msg):
        key = 'shell:event:gm_shipping_state'  # gm 商城实物发货状态
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_order_query(self, msg):
        key = 'shell:event:gm_order_query'  # gm 订单查询
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_reward_vip(self, msg):
        key = 'shell:event:gm_reward_vip'  # gm 赠送vip
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_gm_broadcast_set(self, msg):
        key = 'shell:event:gm_broadcast_set'  # gm 服务器广播
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_gm_broadcast_query(self, msg):
        key = 'shell:event:gm_broadcast_query'  # gm 服务器广播
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_query_chip_consume(self, msg):
        key = 'shell:event:gm_query_chip_consume'  # gm 查询鸟蛋消耗
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_query_chip_produce(self, msg):
        key = 'shell:event:gm_query_chip_produce'  # gm 查询鸟蛋产出
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_query_diamond_consume(self, msg):
        key = 'shell:event:gm_query_diamond_consume'  # gm 查询钻石消耗
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_query_diamond_produce(self, msg):
        key = 'shell:event:gm_query_diamond_produce'  # gm 查询钻石产出
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_update_shop_info(self, msg):
        key = 'shell:event:gm_update_shop_info'  # gm 更新商城信息
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_shop_switch(self, msg):
        key = 'shell:event:gm_shop_switch'  # gm 商城开关
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_query_shot(self, msg):
        key = 'shell:event:gm_query_shot'  # gm 发炮统计
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_query_raffle(self, msg):
        key = 'shell:event:gm_query_raffle'  # gm 抽奖统计
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_query_user_info(self, msg):
        key = 'shell:event:gm_query_user_info'  # gm 查询玩家信息
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_query_all_user_info(self, msg):
        key = 'shell:event:gm_query_all_player_data'  # gm 查询所有玩家信息
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_query_pay_detail(self, msg):
        key = 'shell:event:gm_query_pay_detail'  # gm 查询支付详细
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_add_notice(self, msg):
        key = 'shell:event:gm_add_notice'  # gm 版本公告处理
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_getm_verifycode(self, msg):
        key = 'shell:event:gm_getm_verifycode'  # gm 获取手机验证码
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_get_verifymessages(self, msg):
        key = 'shell:event:gm_get_verifymessages'  # gm 玩家短信通知
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_gm_add_cdkey(self, msg):
        key = 'shell:event:gm_add_cdkey'  # gm 增加cdkey
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_gm_export_cdkey(self, msg):
        key = 'shell:event:gm_export_cdkey'  # gm 导出cdkey
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_gm_alter_cdkey(self, msg):
        key = 'shell:event:gm_alter_cdkey'  # gm 修改cdkey失效
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_gm_query_user_daily_info(self, msg):
        key = 'shell:event:gm_query_user_daily_info'  # gm 查询玩家每日详情信息
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_gm_query_user_period_data(self, msg):
        key = 'shell:event:gm_query_user_period_data'  # gm (新)查询玩家每日详情信息
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_gm_calc_coupon_rate(self, msg):
        key = 'shell:event:gm_calc_coupon_rate'  # gm 计算出券率
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_gm_server_redis_data(self, msg):
        key = 'shell:event:gm_server_redis_data'  # gm 获取服务器Redis
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_gm_cdkey_exchange_query(self, msg):
        key = 'shell:event:gm_cdkey_exchange_query'  # gm 兑换记录查询
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_modify_pool_loop_wave(self, msg):
        key = 'shell:event:gm_modify_pool_loop_wave'  # gm 池子循环波动处理
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_set_player_sign(self, msg):
        key = 'shell:event:gm_set_player_sign'  # gm 设置玩家标记
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_modify_player_protected(self, msg):
        key = 'shell:event:gm_modify_player_protected'  # gm 玩家游戏体验保护机制
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_barrel_pool_config(self, msg):
        key = 'shell:event:gm_getm_barrel_pool_config'  # gm 获取炮倍池配置
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_alter_barrel_pool_config(self, msg):
        key = 'shell:event:gm_alter_barrel_pool_config'  # gm 修改炮倍池
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_get_chip_pool_config(self, msg):
        key = 'shell:event:gm_get_chip_pool_config'  # gm 获取鸟蛋池配置
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_alter_chip_fill_point(self, msg):
        key = 'shell:event:gm_alter_chip_pool'  # gm 修改鸟蛋池配置
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_alter_chip_trigger_give(self, msg):
        key = 'shell:event:gm_alter_chip_trigger_give'  # gm 更新赠送比
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_remove_special_red_packet(self, msg):
        key = 'shell:event:gm_remove_special_red_packet'  # gm 删除全服定时红包
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_special_red_packet(self, msg):
        key = 'shell:event:gm_special_red_packet'  # gm 发送全服红包
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_get_red_packet_info(self, msg):
        key = 'shell:event:gm_get_red_packet_info'  # gm 获取红包信息
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_query_game_data(self, msg):
        key = 'shell:event:gm_query_game_data'  # gm 小游戏总览
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_query_match_data(self, msg):
        key = 'shell:event:gm_query_match_data'  # gm 小游戏总览
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_query_game_particulars_data(self, msg):
        key = 'shell:event:gm_query_game_particulars_data'  # gm 小游戏详情
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_query_player_data(self, msg):
        key = 'shell:event:gm_query_player_data'  # gm 玩家兑换查询
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_unlock_player_info(self, msg):
        key = 'shell:event:gm_unlock_player_info'  # gm 玩家兑换解锁
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    ####################### cdkey server ########################
    def add_record_cdkey_exchange_cdkey(self, msg):
        key = 'cdkey:event:cdkey_exchange_cdkey'  # cdkey 兑换码兑换
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_cdkey_add_cdkey(self, msg):
        key = 'cdkey:event:cdkey_add_cdkey'  # cdkey 增加兑换码
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_cdkey_get_cdkey(self, msg):
        key = 'cdkey:event:cdkey_get_cdkey'  # cdkey 获取兑换码
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_cdkey_alter_cdkey(self, msg):
        key = 'cdkey:event:cdkey_alter_cdkey'  # cdkey 修改兑换码状态
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_cdkey_query_cdkey(self, msg):
        key = 'cdkey:event:cdkey_query_cdkey'  # cdkey 查询兑换码
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)


    ######################## game server ##########################

    def add_record_game_product_deliver(self, msg):
        key = 'game:event:game_product_deliver'  # 游戏服务器的 商品发放
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_game_exchange_cdkey(self, msg):
        key = 'game:event:game_exchange_cdkey'  # 游戏服务器的 兑换cdkey
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_first_recharge_query(self, msg):
        key = 'game:event:first_recharge_query'
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_first_recharge_modify(self, msg):
        key = 'game:event:first_recharge_modify'
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_vip_activity_query(self, msg):
        key = 'game:event:vip_activity_query'
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_vip_activity_modify(self, msg):
        key = 'game:event:vip_activity_modify'
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)


    def add_record_save_money_activity_query(self, msg):
        key = 'game:event:save_money_activity_query'
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_save_money_activity_modify(self, msg):
        key = 'game:event:save_money_activity_modify'
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_save_user_daily_data(self, msg):
        key = 'game:event:save_user_daily_data'
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_year_monster_pool_query(self, msg):
        key = 'game:event:year_monster_pool_query'
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_year_monster_pool_modify(self, msg):
        key = 'game:event:year_monster_pool_modify'
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_wx_new_player_activity_query(self, msg):
        key = 'game:event:wx_new_player_activity_query'
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_wx_new_player_activity_modify(self, msg):
        key = 'game:event:wx_new_player_activity_modify'
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_get_shop_tips(self, msg):
        key = 'game:event:get_shop_tip'
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    def add_record_modify_shop_tips(self, msg):
        key = 'game:event:modify_shop_tips'
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

    ######################## sdk server ##########################
    def add_record_reset_player_password(self, msg):
        key = 'sdk:event:reset_player_password'
        return self.ctx.RedisRecord.hash_set(key, Time.current_ts(), msg)

Record = Record()
