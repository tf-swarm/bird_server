#!/usr/bin/env python
# -*- coding=utf-8 -*-

import random
import time
import datetime
import copy
from pet import BirdPet
from task import BirdTask
from const import Message
from rank import BirdRank
from match import BirdMatch
from share import BirdShare
from props import BirdProps
from account import BirdAccount
from activity import BirdActivity
from comm import BirdComm
from mail import Mail, MailRecord
from red_packet import Red_Packet
from shop import Shop
from target import Target
from newrank import NewRank
from framework.context import Context
from framework.util.tool import Tool
from framework.util.tool import Time
from framework.util.tool import Algorithm
from framework.entity.msgpack import MsgPack
from lemon.entity.upgrade import Upgrade
from lemon.entity.gametimer import GameTimer
from newtask import NewTask
from fanfanle import BirdFanFanLe
from newactivity import *
from giftactivity import *
from richman import RichMan

class BirdEntity(object):
    def __init__(self):
        from lemon.tasklet.entity import EntityTasklet
        self.timer = GameTimer(EntityTasklet)

    def onMessage(self, cmd, uid, gid, mi):
        mo = None
        if cmd == Message.MSG_SYS_ROOM_LIST | Message.ID_REQ:
            self.on_room_list(uid, gid, mi)
        elif cmd == Message.MSG_SYS_RANK_LIST | Message.ID_REQ:
            mo = BirdRank.get_ranks(uid, gid, mi)
        elif cmd == Message.MSG_SYS_BENEFIT | Message.ID_REQ:
            mo = self.on_benefit(uid, gid, mi)
        elif cmd == Message.MSG_SYS_SIGN_IN | Message.ID_REQ:
            mo = self.on_sign_in(uid, gid, mi)
        elif cmd == Message.MSG_SYS_CONFIG | Message.ID_REQ:
            mo = self.on_get_config(uid, gid, mi)
        elif cmd == Message.MSG_SYS_PROPS_LIST | Message.ID_REQ:
            mo = self.on_props_list(uid, gid, mi)
        elif cmd == Message.MSG_SYS_USE_PROPS | Message.ID_REQ:
            mo = self.on_use_props(uid, gid, mi)
        elif cmd == Message.MSG_SYS_RAFFLE | Message.ID_REQ:
            mo = self.on_raffle(uid, gid, mi)
        elif cmd == Message.MSG_SYS_TASK_LIST | Message.ID_REQ:
            mo = BirdTask.on_task_list(uid, gid, mi)
        elif cmd == Message.MSG_SYS_TARGET_RANGE | Message.ID_REQ: #靶场
            mo = Target.target_room_date(uid, gid, mi)
        elif cmd == Message.MSG_SYS_RAFFLE_CONFIG | Message.ID_REQ:  # 抽奖配置
            mo = self.get_raffle_config(uid, gid, mi)
        elif cmd == Message.MSG_SYS_CONSUME_TASK | Message.ID_REQ:
            mo = BirdTask.on_consume_task(uid, gid, mi)
        elif cmd == Message.MSG_SYS_PRESENT | Message.ID_REQ:
            mo = self.on_present(uid, gid, mi)
        elif cmd == Message.MSG_SYS_EXCHANGE | Message.ID_REQ:
            mo = self.on_exchange(uid, gid, mi)
        elif cmd == Message.MSG_SYS_INNER_BUY | Message.ID_REQ:
            mo = self.on_inner_buy(uid, gid, mi)
        elif cmd == Message.MSG_SYS_CONSUME_CDKEY | Message.ID_REQ:
            mo = self.on_consume_cdkey(uid, gid, mi)
        elif cmd == Message.MSG_SYS_ACTIVITY_LIST | Message.ID_REQ:
            mo = BirdActivity.get_activity_list(uid, gid, mi)
        elif cmd == Message.MSG_SYS_CONSUME_ACTIVITY | Message.ID_REQ:
            mo = BirdActivity.consume_activity(uid, gid, mi)
        elif cmd == Message.MSG_SYS_SHARE_INFO | Message.ID_REQ:
            mo = BirdShare.get_share_info(uid, gid, mi)
        elif cmd == Message.MSG_SYS_SHARE | Message.ID_REQ:
            mo = BirdShare.on_share(uid, gid, mi)
        elif cmd == Message.MSG_SYS_BIND_INVITER | Message.ID_REQ:
            mo = BirdShare.on_bind_inviter(uid, gid, mi)
        elif cmd == Message.MSG_SYS_INVITE_INFO | Message.ID_REQ:
            mo = BirdShare.get_invite_info(uid, gid, mi)
        elif cmd == Message.MSG_SYS_INVITE_REWARD | Message.ID_REQ:
            mo = BirdShare.get_invite_reward(uid, gid, mi)
        elif cmd == Message.MSG_SYS_UP_BARREL | Message.ID_REQ:
            mo = self.on_up_barrel(uid, gid, mi)
        elif cmd == Message.MSG_SYS_RESOLVE_STONE | Message.ID_REQ:
            mo = self.on_resolve_stone(uid, gid, mi)
        elif cmd == Message.MSG_SYS_SWITCH_INFO | Message.ID_REQ:
            mo = self.switch_info(uid, gid, mi)
        # elif cmd == Message.MSG_SYS_MATCH_ENTRY | Message.ID_REQ:
        #     mo = BirdMatch.on_match_entry(uid, gid, mi)
        # elif cmd == Message.MSG_SYS_AWARD_LIST | Message.ID_REQ:
        #     mo = self.on_award_list(uid, gid, mi)
        # elif cmd == Message.MSG_SYS_CONSUME_AWARD | Message.ID_REQ:
        #     mo = self.on_consume_award(uid, gid, mi)
        elif cmd == Message.MSG_SYS_HATCH_EGG | Message.ID_REQ:
            mo = BirdPet.hatch_egg(uid, gid, mi)
        elif cmd == Message.MSG_SYS_HATCH_QUICKEN | Message.ID_REQ:
            mo = BirdPet.hatch_quicken(uid, gid, mi)
        elif cmd == Message.MSG_SYS_PET_INFO | Message.ID_REQ:
            mo = BirdPet.pet_info(uid, gid, mi)
        elif cmd == Message.MSG_SYS_PET_COMPOSE | Message.ID_REQ:
            mo = BirdPet.compose(uid, gid, mi)
        elif cmd == Message.MSG_SYS_PET_UP | Message.ID_REQ:
            mo = BirdPet.up(uid, gid, mi)
        elif cmd == Message.MSG_SYS_PET_CHOICE | Message.ID_REQ:
            mo = BirdPet.choice(uid, gid, mi)
        # elif cmd == Message.MSG_SYS_MATCH_TASK_LIST | Message.ID_REQ:
        #     mo = BirdMatch.get_task_list(uid, gid, mi)

        elif cmd == Message.MSG_SYS_BIND_REWARD | Message.ID_REQ:
            mo = self.on_consume_bind_reward(uid, gid, mi)

        elif cmd == Message.MSG_SYS_MAIL_LIST | Message.ID_REQ:
            mo = Mail.send_mail_list(uid, gid, open = 1)
        elif cmd == Message.MSG_SYS_MAIL_RECORD_LIST | Message.ID_REQ:
            mo = MailRecord.send_mail_record(uid, gid)
        elif cmd == Message.MSG_SYS_MAIL_RECEIVE | Message.ID_REQ:
            mo = Mail.receive_present(uid, gid, mi)
        elif cmd == Message.MSG_SYS_MAIL_DELETE_RECORD | Message.ID_REQ:
            mo = Mail.del_mail(uid, gid, mi)

        elif cmd == Message.MSG_SYS_RANK | Message.ID_REQ:
            mo = NewRank.send_rank(gid, uid, mi)
        elif cmd == Message.MSG_SYS_WBRANK_LIST | Message.ID_REQ:
            mo = NewRank.send_world_boss_rank_list( uid, gid)
        # 商城协议
        elif cmd == Message.MSG_SYS_SHOP_BUY | Message.ID_REQ:
            mo = Shop.buy(uid, gid, mi)
        elif cmd == Message.MSG_SYS_LIMIT_SHOP | Message.ID_REQ:
            mo = Shop.on_limit_shop_timer(gid, uid)
        elif cmd == Message.MSG_SYS_SHOP_USER_INFO | Message.ID_REQ:
            mo = Shop.set_user_info(uid, gid, mi)
        elif cmd == Message.MSG_SYS_SHOP_RECORD | Message.ID_REQ:
            mo = Shop.get_record_info(uid, gid)
        elif cmd == Message.MSG_SYS_BUY_WEAPON | Message.ID_REQ:
            mo = Shop.on_buy_weapon(uid, gid, mi)
        elif cmd == Message.MSG_SYS_USE_WEAPON | Message.ID_REQ:
            mo = Shop.on_use_weapon(uid, gid, mi)
        elif cmd == Message.MSG_SYS_PROPS_RECOVERY | Message.ID_REQ:
            mo = Shop.recovery_limit_props(uid, gid, mi)

        elif cmd == Message.MSG_SYS_VIP_RECEIVE_RECORD | Message.ID_REQ:
            mo = self.vip_record_list(uid, gid)
        elif cmd == Message.MSG_SYS_VIP_RECEIVE | Message.ID_REQ:
            mo = self.vip_receive(uid, gid, mi)
        # 任务协议
        elif cmd == Message.MSG_SYS_NEW_TASK_LIST | Message.ID_REQ:
            mo = NewTask.send_task_list(uid)
        elif cmd == Message.MSG_SYS_RECEIVE_TASK_REWARD | Message.ID_REQ:
            mo = NewTask.complete_task(uid, mi)
        elif cmd == Message.MSG_SYS_ACTIVITY_RECEIVE | Message.ID_REQ:
            mo = NewTask.activity_value_receive(uid, mi)
        elif cmd == Message.MSG_SYS_TABLE_TASK_LIST | Message.ID_REQ:
            mo = NewTask.send_task_room(uid, mi)
        # 活动协议
        elif cmd == Message.MSG_SYS_NEW_ACTIVITY_LIST | Message.ID_REQ:
            mo = Activity.get_activity_list(uid)
        elif cmd == Message.MSG_SYS_NEW_ACTIVITY_CONFIG | Message.ID_REQ:
            mo = Activity.get_activity_info(uid, gid, mi)
        elif cmd == Message.MSG_SYS_NEW_ACTIVITY_PAY_RAFFLE | Message.ID_REQ:
            mo = PayActivity.on_raffle(uid)
        elif cmd == Message.MSG_SYS_NEW_ACTIVITY_PAY_SEND_RECORD | Message.ID_REQ:
            mo = PayActivity.send_raffle_record(uid)
        elif cmd == Message.MSG_SYS_NEW_ACTIVITY_TASK_REWARD | Message.ID_REQ:
            mo = TaskActivity.receive_reward_task(uid, mi)
        elif cmd == Message.MSG_SYS_NEW_ACTIVITY_TASK_REWARD_TOTAL | Message.ID_REQ:
            mo = TaskActivity.receive_reward_total(uid)
        elif cmd == Message.MSG_SYS_NEW_ACTIVITY_LOGIN_REWARD | Message.ID_REQ:
            mo = LoginActivity.receive_login_reward(uid, mi)
        elif cmd == Message.MSG_SYS_NEW_ACTIVITY_GIVE_REWARD | Message.ID_REQ:
            mo = GiveActivity.on_receive_reward(uid, mi)
        elif cmd == Message.MSG_SYS_NEW_ACTIVITY_VIP_RECEIVE | Message.ID_REQ:
            mo = VipActivity.vip_activity_recevie(uid, mi)
        elif cmd == Message.MSG_SYS_NEW_ACTIVITY_SAVE_MONEY_DATA | Message.ID_REQ:
            mo = SaveMoneyActivity.get_save_money_activity_data(uid, gid, mi)
        elif cmd == Message.MSG_SYS_NEW_ACTIVITY_SAVE_MONEY_RECEIVE | Message.ID_REQ:
            mo = SaveMoneyActivity.receive_save_money_reward(uid, gid, mi)
        # 红包协议
        elif cmd == Message.MSG_SYS_OPEN_SPECIAL_ENVELOPE | Message.ID_REQ: #打开特殊红包
            mo = Red_Packet.open_special_envelope(uid, mi)
        elif cmd == Message.MSG_SYS_SPECIAL_ENVELOPE_RECORD | Message.ID_REQ: #特殊红包记录
            mo = Red_Packet.special_envelope_record(uid, mi)
        elif cmd == Message.MSG_SYS_SPECIA_RED_PACKET | Message.ID_REQ:  # 后台发送全服红包
            mo = self.gm_send_red_packet(uid, gid, mi)

        # 翻翻乐
        elif cmd == Message.MSG_SYS_FFL_CONFIG | Message.ID_REQ: # 配置
            BirdFanFanLe.send_config(uid, gid)
        elif cmd == Message.MSG_SYS_FFL_START | Message.ID_REQ: # 开始玩
            BirdFanFanLe.start_game(uid, gid, mi)
        elif cmd == Message.MSG_SYS_FFL_CHANGE | Message.ID_REQ: # 换牌
            BirdFanFanLe.change_card(uid, gid, mi)
        elif cmd == Message.MSG_SYS_FFL_REWARD | Message.ID_REQ: # 领取奖励
            BirdFanFanLe.send_reward(uid, gid)
        elif cmd == Message.MSG_SYS_FFL_OPEN | Message.ID_REQ:   #打开翻翻乐
            BirdFanFanLe.open_game(uid, gid)

        elif cmd == Message.MSG_SYS_UPDATE_SHOP_CONFIG | Message.ID_REQ: #修改服务器配置
            mo = self.update_shop_info(uid, gid, mi)

        elif cmd == Message.MSG_SYS_SWITCH_SHOP | Message.ID_REQ: #修改限时商城开关
            mo = self.shop_switch(uid, gid, mi)

        elif cmd == Message.MSG_SYS_FILL_POINT | Message.ID_REQ: #修改填分配置
            mo = self.alter_chip_trigger_give(uid, gid, mi)

        elif cmd == Message.MSG_SYS_POOL_LOOP_WAVE | Message.ID_REQ: #池子循环波动处理
            self.modify_pool_loop_wave(uid, gid, mi)

        elif cmd == Message.MSG_SYS_PLAYER_PROTECTED | Message.ID_REQ: #玩家游戏体验保护机制
            self.modify_player_protected(uid, gid, mi)

        elif cmd == Message.MSG_SYS_MONTH_REWARD | Message.ID_REQ: #月卡领取
            mo = self.on_month_card(uid, gid)

        elif cmd == Message.MSG_SYS_USER_DEAL | Message.ID_REQ:     #后台对玩家的处理
            mo = self.on_user_deal(uid, gid, mi)

        elif cmd == Message.MSG_SYS_LIMIT_SHOP_OPEN | Message.ID_REQ:   #后台修改限时商城的开启和关闭
            mo = self.on_deal_limit_shop_open(gid, mi)

        elif cmd == Message.MSG_SYS_LIMIT_RAFFLE_OPEN | Message.ID_REQ:   #后台奖金抽奖的开启和关闭
            mo = self.on_deal_raffle_open(gid, mi)

        elif cmd == Message.MSG_SYS_SEND_RAFFLE_OPEN | Message.ID_REQ:   #后台奖金抽奖的开启和关闭
            mo = self.on_send_raffle_open(uid, gid, mi)

        elif cmd == Message.MSG_SYS_SET_RECHARGE_PRESENT | Message.ID_REQ:   #后台修改微信支付宝充值修改知客户端请求新数据
            mo = self.on_set_recharge_present(uid, gid, mi)

        elif cmd == Message.MSG_SYS_SHOP_TIPS_NOTICE | Message.ID_REQ:      #后台修改商城tips通知客户端请求新数据
            mo = self.on_set_shop_tips(uid, gid, mi)

        elif cmd == Message.MSG_SYS_SHOP_TIPS_SEND | Message.ID_REQ:        #客户端获取商城tips
            mo = self.on_get_shop_tips(uid, gid, mi)

        elif cmd == Message.MSG_SYS_SHOP_BROADCAST_RECORD_LIST | Message.ID_REQ:        #客户端获取商城tips
            mo = Shop.shop_broadcast_record_list(uid, gid)

        elif cmd == Message.MSG_SYS_ACTIVITY_SHAKE_GET | Message.ID_REQ:         # 获取开心摇一摇的金币数
            mo = ShakeActivity.get_shake_money(uid, gid, mi)
        elif cmd == Message.MSG_SYS_ACTIVITY_SHAKE_RECV | Message.ID_REQ:        # 领取开心摇一摇的金币数
            mo = ShakeActivity.recv_shake_money(uid, gid, mi)
        elif cmd == Message.MSG_SYS_UPDATE_PICTURE | Message.ID_REQ:
            mo = self.update_picture(uid, gid, mi)
        elif cmd == Message.MSG_SYS_UPDATE_MATCH_CONFIG | Message.ID_REQ: #修改服务器配置
            mo = self.update_match_info(uid, gid, mi)
        elif cmd == Message.MSG_SYS_GET_GAME_OPEN | Message.ID_REQ:
            mo = self.get_game_open(uid, gid, mi)
        elif cmd == Message.MSG_SYS_RICH_MAN | Message.ID_REQ:
            mo = RichMan.on_message(uid, gid, mi)
        elif cmd == Message.MSG_SYS_ACTIVITY_GIFT_BOX_CAN | Message.ID_REQ:
            mo = self.gift_activity_message(uid, gid, mi)
        elif cmd == Message.MSG_SYS_UPDATE_ACTIVITY_CONFIG | Message.ID_REQ:
            mo = self.update_old_activity_config(uid, gid, mi)
        elif cmd == Message.MSG_SYS_UPDATE_POINT_SHOP_CONFIG | Message.ID_REQ:
            self.update_point_shop_config(uid, gid, mi)
        elif cmd == Message.MSG_SYS_GET_POINT_SHOP_CONFIG | Message.ID_REQ:
            mo = PointShopActivity.get_point_shop_config(uid, gid)
        elif cmd == Message.MSG_SYS_GET_POINT_SHOP_EXCHANGE | Message.ID_REQ:
            mo = Shop.get_point_shop_record_info(uid, gid)
        elif cmd == Message.MSG_SYS_ACTIVITY_SMASH_EGG_START | Message.ID_REQ:
            mo = SmashEggActivity.start_game(uid, gid, mi)
        elif cmd == Message.MSG_SYS_ACTIVITY_SMASH_EGG_ACTION | Message.ID_REQ:
            mo = SmashEggActivity.smash_egg(uid, gid, mi)
        elif cmd == Message.MSG_SYS_ACTIVITY_SMASH_EGG_REWARD | Message.ID_REQ:
            mo = SmashEggActivity.deal_reward(uid, gid, mi)
        elif cmd == Message.MSG_SYS_ACTIVE_USER_COUNT | Message.ID_REQ:
            mo = self.deal_active_user_count(gid, mi)
        elif cmd == Message.MSG_SYS_DRAGON_BOAT_RECV | Message.ID_REQ:
            mo = DragonBoatActivity.exchange_reward(uid, gid, mi)
        elif cmd == Message.MSG_SYS_SMART_GAME_TOKEN | Message.ID_REQ:
            mo = self.smart_game_token(uid, gid, mi)

        elif cmd == Message.MSG_SYS_BURYING_POINT | Message.ID_REQ:
            mo = self.deal_burying_point(uid, mi)
        elif cmd == Message.MSG_SYS_SHOP_GIFT_CONFIG | Message.ID_REQ:
            mo = Shop.get_gift_config(uid, gid)
        elif cmd == Message.MSG_SYS_SHOP_GIFT_BUY | Message.ID_REQ:
            mo = Shop.gift_shop_buy(uid, gid, mi)
        elif cmd == Message.MSG_SYS_NEW_MONTH_CARD_BUY | Message.ID_REQ:
            mo = Shop.new_month_card_buy(uid, gid, mi)
        elif cmd == Message.MSG_SYS_NEW_MONTH_CARD_RECV | Message.ID_REQ:
            mo = self.on_new_month_card(uid, gid, mi)
        elif cmd == Message.MSG_SYS_ACTIVITY_TOTAL_PAY_RECV | Message.ID_REQ:
            mo = TotalPayActivity.on_recv_reward(uid, mi)
        elif cmd == Message.MSG_INNER_TIMER:
            self.__on_timer(cmd, uid, gid, mi)

        if isinstance(mo, MsgPack):
            Context.GData.send_to_connect(uid, mo)

    def smart_game_leave(self, uid, game_id):
        mo = MsgPack(Message.MSG_SYS_SMART_GAME_LEAVE | Message.ID_ACK)
        mo.set_param('mgid', game_id)
        Context.GData.send_to_connect(uid, mo)
        return MsgPack(0, {'ret': 0})

    def smart_game_token(self, uid, gid, mi):
        gameId = mi.get_param('gid')
        mo = MsgPack(Message.MSG_SYS_SMART_GAME_TOKEN | Message.ID_ACK)
        channel_id = Context.Data.get_attr(uid, 'loginChannelId', '1001_0')
        if channel_id in ['1005_0']:
            return mo.set_error(1, u'您的渠道暂时未开通斗地主')
        vip_level = BirdAccount.get_vip_level(uid, gid)
        if vip_level < 1:
            return mo.set_error(4, u'vip等级不足')
        status = Context.RedisCache.hash_get_int('smart_game:%d' % uid, 'status', 0)
        if status > 0:
            game_info = Context.RedisCache.hash_get_json('smart_game:%d' % uid, 'game_info')
            if game_info:
                if gameId == game_info.get('gid', 0):
                    token = Context.RedisCache.hash_get('smart_game:%d' % uid, 'token')
                else:
                    return mo.set_error(2, u'您正在进行其他第三方游戏！')
            else:
                return mo.set_error(3, u'第三方小游戏数据错误，请联系客服帮您解决！')
        else:
            ms = Time.current_ms()
            token_str = 'gameId=%d&ts=%d'%(gameId, ms)
            token = Algorithm.base64_encode(token_str)
            Context.RedisCache.hash_set('smart_game:%d' % uid, 'status', 0)
            Context.RedisCache.hash_set('smart_game:%d' % uid, 'token', token)

        url = Context.Configure.get_game_item(gid, 'smart_game_ddz.config')
        mo.set_param('url', url)
        mo.set_param('gid', gameId)
        mo.set_param('token', token)
        return mo

    def deal_burying_point(self, uid, mi):
        pid = mi.get_param('pid')
        if pid == 1:
            m_str = 'open_guide_info'
        elif pid == 2:
            m_str = 'open_activity_info'
        elif pid == 3:
            m_str = 'open_shop_info'
        elif pid == 4:
            m_str = 'set_coupon_info'
        else:
            return


    def gift_activity_message(self, uid, gid, mi):
        pid = mi.get_param('pid')
        if pid == 1:
            mo = GiftBox1Activity.activity_can_buy(uid, gid, mi)
        elif pid == 2:
            mo = GiftBox2Activity.activity_can_buy(uid, gid, mi)
        elif pid == 3:
            mo = GiftBox3Activity.activity_can_buy(uid, gid, mi)
        elif pid == 4:
            mo = GiftBox4Activity.activity_can_buy(uid, gid, mi)
        else:
            return
        return mo

    def on_deal_raffle_open(self, gid, mi):
        open = mi.get_param('open')
        open_flag = Context.RedisMix.get('limit.raffle.open')
        if open != open_flag:
            Context.RedisMix.set('limit.raffle.open', open)
            mo = MsgPack(Message.MSG_SYS_SEND_RAFFLE_OPEN | Message.ID_ACK)
            mo.set_param('open', open)
            Context.GData.broadcast_to_system(mo)
        return

    def on_deal_limit_shop_open(self, gid, mi):
        open = mi.get_param('open')
        open_flag = Context.RedisMix.get('limit.shop.open')
        if open != open_flag:
            Context.RedisMix.set('limit.shop.open', open)
            Shop.on_limit_shop_timer(gid, background=True)
        return

    def on_send_raffle_open(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_SEND_RAFFLE_OPEN | Message.ID_ACK)
        open_flag = Context.RedisMix.hash_get_int('limit.raffle.open', 0)
        mo.set_param('open', open_flag)
        return mo

    def on_user_deal(self, uid, gid, mi):
        deal = mi.get_param('deal')
        mo = MsgPack(Message.MSG_SYS_USER_DEAL | Message.ID_ACK)
        if deal == 1:
            mo.set_param('deal', 1)
            mo.set_param('msg', u'该玩家账号异常被封冻，如有疑问请联系客服。')
        return mo

    def on_set_recharge_present(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_SET_RECHARGE_PRESENT | Message.ID_NTF)
        # conf = self.get_recharge_add_config(gid)
        # mo.set_param('recharge_add', conf)
        Context.GData.broadcast_to_system(mo)
        return

    def on_set_shop_tips(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_SHOP_TIPS_NOTICE | Message.ID_NTF)
        Context.GData.broadcast_to_system(mo)
        return

    def on_get_shop_tips(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_SHOP_TIPS_SEND | Message.ID_ACK)
        conf = Context.RedisMix.hash_get_json('game.%d.background' % gid, 'shop_tips', {})
        channel_id = Context.Data.get_attr(uid, 'loginChannelId', '1001_0')
        if conf.has_key(channel_id):
            cf = conf[channel_id]
        else:
            cf = ""
        mo.set_param('c', cf)
        Context.GData.send_to_connect(uid, mo)
        return

    def vip_record_list(self, uid, gid):
        vip_level = BirdAccount.get_vip_level(uid, gid)
        vip_record = []
        mo = MsgPack(Message.MSG_SYS_VIP_RECEIVE_RECORD | Message.ID_ACK)
        if vip_level <= 0:
            mo.set_param('record', Context.json_dumps(vip_record))
            return mo
        vip_record = self.get_vip_record_list(uid, gid, vip_level)
        Context.Data.set_game_attr(uid, gid, 'vip_record', Context.json_dumps(vip_record))
        mo.set_param('record', Context.json_dumps(vip_record))
        return mo

    def vip_receive(self, uid, gid, mi):
        idx = mi.get_param('idx')
        vip_level = BirdAccount.get_vip_level(uid, gid)
        mo = MsgPack(Message.MSG_SYS_VIP_RECEIVE | Message.ID_ACK)
        if vip_level < idx:
            return mo.set_error(1, u'你的vip等级还不足以领取此礼包')

        vip_record = self.get_vip_record_list(uid, gid, vip_level)
        if vip_record[idx - 1] == 1:
            return mo.set_error(1, u'你已经领取了此礼包')
        vipConfig = Context.Configure.get_game_item_json(gid, 'vip.config')
        gift1 = dict(vipConfig[idx - 1].get('gift1', {}))
        gift2 = dict(vipConfig[idx - 1].get('gift2', {}))
        if gift1.has_key('name'):
            del gift1['name']
        if gift2.has_key('name'):
            del gift2['name']
        reward = dict(gift1.items()+gift2.items())
        BirdProps.issue_rewards(uid, gid, reward, "vip_receive", True)
        final_info = BirdProps.convert_reward(reward)
        vip_record[idx - 1] = 1
        Context.Data.set_game_attr(uid, gid, 'vip_record', Context.json_dumps(vip_record))

        mo.set_param('reward', final_info)
        if vipConfig[idx - 1].has_key('weaponId'):
            wpid = int(vipConfig[idx - 1]['weaponId'])
            weapon_buy_dict = Context.Data.get_game_attr_json(uid, gid, 'weapon_buy_dict')
            weapon_buy_dict[str(wpid)] = 1
            Context.Data.set_game_attr(uid, gid, 'weapon_buy_dict', Context.json_dumps(weapon_buy_dict))

            mo1 = MsgPack(Message.MSG_SYS_USE_WEAPON | Message.ID_ACK)
            weapon_use_dict = Context.Data.get_game_attr_int(uid, gid, 'weapon_use_dict', 0)
            if weapon_use_dict != int(wpid):
                Context.Data.set_game_attr(uid, gid, 'weapon_use_dict', wpid)
                info = {}
                info['weapon'] = wpid
                info['success'] = 1
                mo1.update_param(info)
                Context.GData.send_to_connect(uid, mo1)

            name = 'weaponshop'
            mou = MsgPack(Message.MSG_SYS_CONFIG | Message.ID_ACK)
            conf = Shop.get_weaponshop_config(uid, gid)
            mou.set_param(name, conf)
            Context.GData.send_to_connect(uid, mou)

        mo2 = MsgPack(Message.MSG_SYS_VIP_RECEIVE_RECORD | Message.ID_ACK)
        mo2.set_param('record', Context.json_dumps(vip_record))
        Context.GData.send_to_connect(uid, mo2)

        return mo

    def get_vip_record_list(self, uid, gid, vip_level):
        vip_record = Context.Data.get_game_attr(uid, gid, 'vip_record', None)
        if vip_record:
            vip_record = Context.json_loads(vip_record)
            if len(vip_record) < vip_level:
                tmp_list = []
                for i in xrange(vip_level - len(vip_record)):
                    tmp_list.append(0)
                vip_record.extend(tmp_list)
        else:
            vip_record = []
            for i in xrange(vip_level):
                vip_record.append(0)
        return vip_record

    def on_startup(self, gid):
        if Context.Global.is_first():
            # self.timer.setInterval(1, {'gameId': gid, 'action': 'report'})
            self.timer.setTimeout(1, {'gameId': gid, 'action': 'minute_deal'})
            self.timer.setTimeout(1, {'gameId': gid, 'action': 'online'})
            self.add_timer_active_count(gid)
            self.handle_script()
            self.set_limit_timer(gid)
            BirdMatch.deal_reboot_server(gid)
            ts = Time.tomorrow_start_ts() - Time.current_ts()
            next_ftm = Time.timestamp_to_str(Time.tomorrow_start_ts() - 1, '%Y-%m-%d')
            self.timer.setTimeout(ts, {'gameId': gid, 'action': 'daily', 'ftm': next_ftm})
            # BirdMatch.install_match_event(gid)

    def add_timer_active_count(self, gid):
        ts = int(time.time())
        now_tm = time.localtime(ts)
        inv = 3600 - now_tm.tm_min * 60 - now_tm.tm_sec
        self.timer.setTimeout(inv, {'gameId': gid, 'action': 'hour_deal'})
        return

    def add_task_to_manage(self, gid, ftm):
        from framework.entity.manager import TaskManager
        TaskManager.add_simple_task(self.set_daily_date, gid, ftm)

    def handle_script(self):
        kvs = {
            'seat0': 0,
            'seat1': 0,
            'seat2': 0,
            'seat3': 0,
        }
        table_keys = Context.RedisCache.hget_keys('relax_table:2:*')
        for key in table_keys:
            Context.RedisCache.hash_mset(key, **kvs)


        #kvs1 = {
        #    '200': 37500,
        #    '201': 312500,
        #    '202': 1875000,
        #    '203': 12500000,
        #    '209': 12500000,
        #}
        #for key in table_keys:
        #    room_type = Context.RedisCache.hash_get_int(key, 'room_type', 0)
        #    if room_type in [200, 201, 202, 203, 209]:
        #        Context.RedisCache.hash_set(key, 'table_pool', kvs1.get(str(room_type)))

        Context.RedisMix.hash_setnx('game.2.share', 'ffl_pool_0_level_1', 250000)
        Context.RedisMix.hash_setnx('game.2.share', 'ffl_pool_0_level_2', 6000000)
        Context.RedisMix.hash_setnx('game.2.share', 'ffl_pool_0_level_3', 10000000)

        Context.RedisMix.hash_setnx('game.2.share', 'ffl_pool_1_level_1', 2500000)
        Context.RedisMix.hash_setnx('game.2.share', 'ffl_pool_1_level_2', 10000000)
        Context.RedisMix.hash_setnx('game.2.share', 'ffl_pool_1_level_3', 20000000)

        Context.RedisMix.hash_setnx('game.2.RichMan_pool', 'RichMan_pool_1', 5000000)
        Context.RedisMix.hash_setnx('game.2.RichMan_pool', 'RichMan_pool_2', 15000000)
        Context.RedisMix.hash_setnx('game.2.RichMan_pool', 'RichMan_pool_3', 25000000)


    def set_limit_timer(self, gid):
        limit_timer = Context.Data.get_timer_all(10000, gid)
        if limit_timer and len(limit_timer) <= 0:
            return
        for k,v in limit_timer.items():

            userId = int(k.split('_')[0])
            propsId = int(k.split('_')[1])
            limit_times = v
            ts = Time.current_ts()
            if ts > int(limit_times):
                self.deal_props_limit(userId, gid, propsId)
            else:
                limit_time = int(limit_times) - ts
                self.timer.setTimeout(limit_time,{'gameId': gid, 'userId': userId, 'propsId': propsId, 'action': 'limit_props'})
        return


    def __on_timer(self, cmd, uid, gid, msg):
        action = msg.get_param('action')
        now_ts = Time.datetime()
        now_seconds = now_ts.second
        # if action == 'report':
        #     server_url = Context.Configure.get_game_item(gid, 'stat.server.url')
        #     if not server_url:
        #         Context.Log.warn('no stat.server.url found')
        #         return
        #     game_room = Context.GData.map_room_type.get(gid)
        #     room_types = sorted(game_room.keys())
        #     # pool.chip
        #     pool_chip = []
        #     for room_type in room_types:
        #         fields = ['pool.shot.%d' % room_type, 'pool.reward.%d' % room_type,
        #                   'official.macro.control.%d' % room_type,
        #                   'buff.pool.shot.%d' % room_type]
        #         _shot, _reward, _control, _buff = Context.RedisMix.hash_mget('game.%d.info.hash' % gid, *fields)
        #         _shot = Tool.to_int(_shot, 0)
        #         _reward = Tool.to_int(_reward, 0)
        #         _control = Tool.to_int(_control, 0)
        #         _buff = Tool.to_int(_buff, 0)
        #         pool_chip.append(_buff + _shot - _reward + _control)
        #
        #     # red.pool.chip
        #     _shot, _reward = Context.RedisMix.hash_mget('game.%d.info.hash' % gid, 'red.pool.shot.203', 'red.pool.reward.203')
        #     _shot = Tool.to_int(_shot, 0)
        #     _reward = Tool.to_int(_reward, 0)
        #     red_pool_chip = _shot - _reward
        #
        #     # red.pool.chip
        #     _shot, _reward = Context.RedisMix.hash_mget('game.%d.info.hash' % gid, 'red.pool.shot.231', 'red.pool.reward.231')
        #     _shot = Tool.to_int(_shot, 0)
        #     _reward = Tool.to_int(_reward, 0)
        #     n_red_pool_chip = _shot - _reward
        #
        #     now_ts = Time.current_ts()
        #     mo = MsgPack(0)
        #     mo.set_param('gameId', gid)
        #     mo.set_param('ts', now_ts)
        #     mo.set_param('pool', pool_chip)
        #     mo.set_param('red.pool', [red_pool_chip, n_red_pool_chip])
        #     Context.WebPage.wait_for_page(server_url + '/pond_stat/add', postdata={'pond_data': mo.pack()})
        #     # online
        #     onlines = Context.Online.get_online(gid, *room_types)
        #     online_list = []
        #     for _online in onlines:
        #         _online = Tool.to_int(_online, 0)
        #         online_list.append(_online)
        #     mo.remove_param('pool')
        #     mo.set_param('online', online_list)
        #     Context.WebPage.wait_for_page(server_url + '/show_online/add', postdata={'online_data': mo.pack()})
        if action == 'minute_deal': #整分钟的处理
            self.timer.setTimeout(60 - now_seconds, {'gameId': gid, 'action': 'minute_deal'})
            NewRank.on_rank_timer(gid)
            RankActivity.on_rank_timer()
            PayRankActivity.on_pay_rank_timer()
            PointShopActivity.on_point_shop_timer()
            Shop.on_shop_goods_timer(gid)
            Shop.on_limit_shop_timer(gid)
            Red_Packet.special_red_packet(gid)
            Red_Packet.bulletin_info()
            BirdMatch.on_match_room_timer(gid)
            self.on_broadcast_timer(gid)
            # Context.MysqlData.on_timer_daily_data()
        elif action == 'online':
            self.timer.setTimeout(600, {'gameId': gid, 'action': 'online'})
            Context.Stat.on_online_timer(gid)
        elif action == 'hour_deal':
            self.timer.setTimeout(3600, {'gameId': gid, 'action': 'hour_deal'})
            self.send_to_active_user_msg(gid)
        elif action == 'daily':
            ts = Time.tomorrow_start_ts() - Time.current_ts()
            next_ftm = Time.timestamp_to_str(Time.tomorrow_start_ts() - 1, '%Y-%m-%d')
            self.timer.setTimeout(ts, {'gameId': gid, 'action': 'daily', 'ftm': next_ftm})
            ftm = msg.get_param('ftm')
            self.update_daily_info()
            self.add_task_to_manage(gid, ftm)
        elif action == 'limit_props':
            userId = msg.get_param('userId')
            propsId = msg.get_param('propsId')
            self.deal_props_limit(userId, gid, propsId)
        elif action == 'deal_shake':
            ShakeActivity.deal_reward(msg)
        # else:
        #     BirdMatch.on_match_event(gid, action, msg)

    def send_to_active_user_msg(self, gid):
        cmd = Message.MSG_SYS_ACTIVE_USER_COUNT | Message.ID_REQ
        mo = MsgPack(Message.MSG_SYS_ACTIVE_USER_COUNT | Message.ID_REQ)
        Context.GData.send_to_connect(1000000, mo, cmd=cmd, gid=gid, pipe = 1)
        return

    def deal_active_user_count(self, gid, mi):
        ids = mi.get_param('ids')
        # count = len(ids)
        ts = int(time.time())
        hour = time.localtime(ts).tm_hour
        if hour == 0:
            hour = 24
        format = '%Y-%m-%d'
        ftm = Time.current_time(format)

        dat = {}
        for uid in ids:
            channel_id = Context.Data.get_attr(int(uid), 'loginChannelId', '1004_0')
            info = dat.get(channel_id, {})
            online = info.get('online', 0)
            online += 1
            online_vip = info.get('online_vip', 0)
            vip_level = BirdAccount.get_vip_level(uid, gid)
            if vip_level > 0:
                online_vip += 1
            online_pay = info.get('online_pay', 0)
            pay = Context.Daily.get_daily_data(uid, gid, 'pay_times')
            if pay:
                online_pay += 1
            dat[channel_id] = {'online':online, 'online_vip':online_vip, 'online_pay':online_pay}
        for k,v in dat.items():
            for i, j in v.items():
                Context.RedisStat.hash_set('statistics:%s:%s:%s'%(k, ftm, i), hour, j)

        return

    def update_daily_info(self):
        mo = MsgPack(Message.MSG_SYS_UPDATE_DAILY_INFO | Message.ID_NTF)
        Context.GData.broadcast_to_system(mo)

    def has_barrel_pool_chip_date(self, pool_id):
        key = 'game.%d.info.barrel_pool:%d' % (2, pool_id)
        pool_barrel = 'pool.barrel_level_chip.%d' % pool_id
        pool_chip = Context.RedisMix.hash_get(key, pool_barrel, None)
        if pool_chip == None:
            return False
        return True

    #def get_barrel_pool_chip(self, pool_id):
    #    key = 'game.%d.info.barrel_pool:%d' % (2, pool_id)
    #    pool_barrel = 'pool.barrel_level_chip.%d' % pool_id
    #    pool_chip = Context.RedisMix.hash_get(key, pool_barrel, 0)

    #    return Tool.to_int(pool_chip)

    #def get_barrel_pool_win_chip(self, gid):
    #    barrel_pool_config = Context.Configure.get_game_item_json(gid, 'barrel_pool.config')
    #    pool_space_config = barrel_pool_config['pool_space']
    #    index = 0
    #    max_index = len(pool_space_config)#

    #    total_fill = 0
    #    cur_pool_chip = 0
    #    for pool in pool_space_config:
    #        max_multiple = pool['space'][len(pool['space']) - 1]
    #        index += 1#

    #        cur_pool_chip += self.get_barrel_pool_chip(index)
    #    if not self.has_barrel_pool_chip_date(1):
    #        return total_fill, total_fill

        #Context.Log.debug('获取炮倍池输赢状况,cur_pool_chip:', cur_pool_chip, 'total_fill:', total_fill )
    #    return cur_pool_chip, total_fill

    def save_own_chip(self, ftm):
        key = 'user_daily:*:%s:*' % ftm
        ret = Context.RedisStat.hget_keys(key)
        for daily_key in ret:
            uid = int(daily_key.split(':')[3])
            chipArr = Context.Data.get_game_attrs(uid, 2, ['chip'])
            chip = chipArr[0]

            arr_keys = daily_key.split(':')
            day_time = arr_keys[2]
            cur_ts = Time.str_to_datetime(day_time, '%Y-%m-%d')
            next_day = Time.next_days(cur_ts)
            next_day = Time.datetime_to_str(next_day, '%Y-%m-%d')
            next_key = 'user_daily:%s:%s:%s' % (arr_keys[1], next_day, arr_keys[3])
            p_daily_data = Context.RedisStat.hash_getall(next_key)
            total_in_chip = 0
            total_out_chip = 0
            for k, v in p_daily_data.items():
                if k.startswith('in.chip.'):
                    total_in_chip += int(v)
                elif k.startswith('out.chip.'):
                    total_out_chip += int(v)
            own_chip = Tool.to_int(chip, 0) + total_out_chip - total_in_chip
            Context.RedisStat.hash_set(daily_key, 'fix_own_chip', own_chip)
            Context.Log.debug('save_own_chip', own_chip)

            p_daily_data = Context.RedisStat.hash_getall(daily_key)
            total_in_chip = 0
            total_out_chip = 0
            for k, v in p_daily_data.items():
                if k.startswith('in.chip.'):
                    total_in_chip += int(v)
                elif k.startswith('out.chip.'):
                    total_out_chip += int(v)
            own_chip = own_chip + total_out_chip - total_in_chip
            Context.RedisStat.hash_set(daily_key, 'fix_last_own_chip', own_chip)
            Context.Log.debug('fix_last_own_chip', own_chip)

    # 获取新手赠分
    def get_new_p_gift_chip(self, daily_data_key):
        p_daily_data = Context.RedisStat.hash_getall(daily_data_key)
        new_p_gift_chip = (int(p_daily_data.get('out.chip_pool_new_gift.new_player_hit_bird', 0)) - int(
            p_daily_data.get('in.chip_pool_new_gift.new_player_hit_bird', 0)))
        return new_p_gift_chip

    def set_daily_date(self, gid, ftm, nextTimer=True):
        # 这里如果调用的时间是昨日之前的数据的话会有问题
        Context.Log.debug('set_daily_date:', gid, ftm)
        Context.Record.add_record_save_user_daily_data(ftm)

        ret = Context.RedisCluster.hget_keys('game:2:*')

        self.save_own_chip(ftm)

        barrel_pool_play_gift_config = Context.Configure.get_game_item_json(gid, 'barrel_pool_play_gift.config')
        #len_gift_pool = len(barrel_pool_play_gift_config['data'])  # 赠送池的个数

        date_dict = {}
        for i in ret:
            uid = int(i.split('game:2:')[1])
            if uid <= 1000000:
                continue
            channel_id = Context.Data.get_attr(uid, 'channelid', '1001_0')
            if not date_dict.has_key(channel_id):
                date_dict[channel_id] = {'chip': 0, 'diamond': 0, 'coupon': 0, 'target': 0, 'bonus_pool':0, 'pool_left':0, 'gift_chip':0, 'recharge_gift_chip': 0, 'chip_pool_new_gift': 0,
                                         '202': 0, '203': 0, '204': 0, '205': 0,
                                         '211': 0, '212': 0, '213': 0, '214': 0,
                                        '215': 0, '216': 0, '217': 0, '218': 0, '219': 0}
            chip, diamond, coupon, target, bonus_pool, pool_left, gift_chip, recharge_gift_chip, chip_pool_new_gift = Context.Data.get_game_attrs(uid, gid, ['chip', 'diamond', 'coupon', 'target_coupon', 'bonus_pool', 'pool_left', 'gift_chip', 'recharge_gift_chip', 'chip_pool_new_gift'])
            props = Context.RedisCluster.hash_mget(uid, 'props:%d:%d'%(gid, uid),
                                                   '202', '203', '204', '205', '211', '212', '213', '214', '215', '216', '217', '218', '219')



            #Context.Log.debug('xxxxxxxx')
            #for i in range(len_gift_pool):
            #    key_play_shot_gift = 'play_shot_gift.%d' % i
            #    date_dict[channel_id][key_play_shot_gift] = Tool.to_int(date_dict[channel_id].get(key_play_shot_gift, 0)) + Context.UserAttr.get_play_shot_gift_chip(uid, gid, i, 0)
                #Context.Log.debug('xxxxxxxx222')

            chips = Tool.to_int(chip, 0)
            pool_left = Tool.to_int(pool_left, 0)
            bonus_pool = Tool.to_int(bonus_pool, 0)
            gift_chip = Tool.to_int(gift_chip, 0)
            recharge_gift_chip = Tool.to_int(recharge_gift_chip, 0)
            chip_pool_new_gift = Tool.to_int(chip_pool_new_gift, 0)
            if chip_pool_new_gift > 0:
                chip_pool_new_gift = 100000 - Tool.to_int(chip_pool_new_gift, 0)
            date_dict[channel_id]['chip'] += chips
            date_dict[channel_id]['pool_left'] += pool_left
            date_dict[channel_id]['gift_chip'] += gift_chip
            date_dict[channel_id]['chip_pool_new_gift'] += chip_pool_new_gift
            date_dict[channel_id]['recharge_gift_chip'] += recharge_gift_chip
            date_dict[channel_id]['bonus_pool'] += bonus_pool

            date_dict[channel_id]['diamond'] += Tool.to_int(diamond, 0)
            date_dict[channel_id]['coupon'] += Tool.to_int(coupon, 0)
            date_dict[channel_id]['target'] += Tool.to_int(target, 0)

            date_dict[channel_id]['202'] += Tool.to_int(props[0], 0)
            date_dict[channel_id]['203'] += Tool.to_int(props[1], 0)
            date_dict[channel_id]['204'] += Tool.to_int(props[2], 0)
            date_dict[channel_id]['205'] += Tool.to_int(props[3], 0)
            date_dict[channel_id]['211'] += Tool.to_int(props[4], 0)
            date_dict[channel_id]['212'] += Tool.to_int(props[5], 0)
            date_dict[channel_id]['213'] += Tool.to_int(props[6], 0)
            date_dict[channel_id]['214'] += Tool.to_int(props[7], 0)
            date_dict[channel_id]['215'] += Tool.to_int(props[8], 0)
            date_dict[channel_id]['216'] += Tool.to_int(props[9], 0)
            date_dict[channel_id]['217'] += Tool.to_int(props[10], 0)
            date_dict[channel_id]['218'] += Tool.to_int(props[11], 0)
            date_dict[channel_id]['219'] += Tool.to_int(props[12], 0)

        for k,v in date_dict.items():
            #Context.Log.debug('xxxxxxxx333')
            #for i in range(len_gift_pool):
            #    Context.Log.debug('xxxxxxxx444')
            #    key_play_shot_gift = 'play_shot_gift.%d' % i
            #    Context.Stat.set_daily_data(k, ftm, key_play_shot_gift, v.get(key_play_shot_gift, 0))

            Context.Stat.set_daily_data(k, ftm, 'server_chip', v.get('chip', 0))
            Context.Stat.set_daily_data(k, ftm, 'server_gift_chip', v.get('gift_chip', 0))
            Context.Stat.set_daily_data(k, ftm, 'server_recharge_gift_chip', v.get('recharge_gift_chip', 0))
            Context.Stat.set_daily_data(k, ftm, 'server_chip_pool_new_gift', v.get('chip_pool_new_gift', 0))
            Context.Stat.set_daily_data(k, ftm, 'server_diamond', v.get('diamond', 0))
            Context.Stat.set_daily_data(k, ftm, 'server_coupon', v.get('coupon', 0))
            Context.Stat.set_daily_data(k, ftm, 'server_target', v.get('target', 0))
            Context.Stat.set_daily_data(k, ftm, 'server_bonus_pool', v.get('bonus_pool', 0))
            Context.Stat.set_daily_data(k, ftm, 'server_pool_left', v.get('pool_left', 0))
            Context.Stat.set_daily_data(k, ftm, 'server_props_202', v.get('202', 0))
            Context.Stat.set_daily_data(k, ftm, 'server_props_203', v.get('203', 0))
            Context.Stat.set_daily_data(k, ftm, 'server_props_204', v.get('204', 0))
            Context.Stat.set_daily_data(k, ftm, 'server_props_205', v.get('205', 0))
            Context.Stat.set_daily_data(k, ftm, 'server_props_211', v.get('211', 0))
            Context.Stat.set_daily_data(k, ftm, 'server_props_212', v.get('212', 0))
            Context.Stat.set_daily_data(k, ftm, 'server_props_213', v.get('213', 0))
            Context.Stat.set_daily_data(k, ftm, 'server_props_214', v.get('214', 0))
            Context.Stat.set_daily_data(k, ftm, 'server_props_215', v.get('215', 0))
            Context.Stat.set_daily_data(k, ftm, 'server_props_216', v.get('216', 0))
            Context.Stat.set_daily_data(k, ftm, 'server_props_217', v.get('217', 0))
            Context.Stat.set_daily_data(k, ftm, 'server_props_218', v.get('218', 0))
            Context.Stat.set_daily_data(k, ftm, 'server_props_219', v.get('219', 0))

        # coupon_pool_free, coupon_pool_vip, target_pool, coupon_pool_spacial = Context.RedisMix.hash_mget('game.2.share',
        #                                                                                                  'coupon_pool_free',
        #                                                                                                  'coupon_pool_vip',
        #                                                                                                  'target_pool',
        #                                                                                                  'coupon_pool_spacial')
        # Context.Stat.set_daily_data(gid, ftm, 'coupon_pool_free', Tool.to_int(coupon_pool_free, 0))
        # Context.Stat.set_daily_data(gid, ftm, 'coupon_pool_vip', Tool.to_int(coupon_pool_vip, 0))
        # Context.Stat.set_daily_data(gid, ftm, 'target_pool', Tool.to_int(target_pool, 0))
        # Context.Stat.set_daily_data(gid, ftm, 'coupon_pool_spacial', Tool.to_int(coupon_pool_spacial, 0))

        ## 保存每天炮倍池状态
        #strWin, strFill = self.get_barrel_pool_win_chip(gid)
        #Context.Stat.set_daily_data(gid, ftm, 'win_barrel_chip', Tool.to_int(strWin, 0))

        return

    def deal_props_limit(self, userId, gid, propsId):
        weapon_buy_dict = Context.Data.get_game_attr_json(userId, gid, 'weapon_buy_dict')
        es = Context.Data.get_timer_attr(10000, gid, "%d_%d" % (userId, propsId))
        if es == None or int(es) > Time.current_ts():
            return
        if int(weapon_buy_dict[str(propsId)]) <= 1:
            Context.Data.del_timer_attr(10000, gid, '%d_%d' % (userId, propsId))
            return
        Context.Data.del_timer_attr(10000, gid, '%d_%d' % (userId, propsId))
        weapon_use_dict = Context.Data.get_game_attr_int(userId, gid, 'weapon_use_dict', 0)

        if weapon_use_dict == int(propsId):
            Context.Data.set_game_attr(userId, gid, 'weapon_use_dict', 20000)
            weapon_use = 20000
        else:
            weapon_use = Context.Data.get_game_attr_int(userId, gid, 'weapon_use_dict', 0)
        weapon_buy_dict = Context.Data.get_game_attr_json(userId, gid, 'weapon_buy_dict')
        if weapon_buy_dict[str(propsId)] != 1:
            weapon_buy_dict[str(propsId)] = 0
        Context.Data.set_game_attr(userId, gid, 'weapon_buy_dict', Context.json_dumps(weapon_buy_dict))

        mo = MsgPack(Message.MSG_SYS_WEAPON_EXPIRE | Message.ID_ACK)
        info = {}
        info['lose'] = propsId
        info['use'] = weapon_use
        mo.update_param(info)
        Context.GData.send_to_connect(userId, mo)

    def on_sign_in(self, uid, gid, mi):
        vip_level = BirdAccount.get_vip_level(uid, gid)
        vipConfig = Context.Configure.get_game_item_json(gid, 'vip.config')

        # 签到奖励
        mo = MsgPack(Message.MSG_SYS_SIGN_IN | Message.ID_ACK)
        conf = copy.deepcopy(Context.Configure.get_game_item_json(gid, 'login.reward'))
        if not conf:
            Context.Log.error('miss config')
            return mo.set_error(1, 'miss config')

        now_day, last_login, ns_login, np_login = BirdAccount.get_login_info(uid, gid)
        create_day = Context.Data.get_uid_create_day(uid)
        channel_id = Context.Data.get_attr(uid, 'channelid', '1004_0')
        if channel_id not in ['1000_0', '1003_0', '1004_0','1005_0','1007_0','1008_0'] or create_day > 7 : #非新手签到
            if now_day == last_login:
                return mo.set_error(2, u'今日奖励已领取')
            elif now_day == last_login + 1 and create_day != 8:  # 连续登陆
                ns_login += 1
            else:
                ns_login = 0
            conf = conf['common']
            days = ns_login % len(conf)
            reward = conf[days]
            reward1 = reward[0]
            reward2 = reward[1]
            BirdAccount.set_login_info(uid, gid, now_day, ns_login)
            if vip_level and vipConfig[vip_level -1].has_key('day_sign_times') and reward1.has_key('chip'):
                reward1['chip'] = vipConfig[vip_level -1]['day_sign_times'][days]
        else:           #新手签到

            if now_day == last_login:
                return mo.set_error(2, u'今日奖励已领取，第七日拥有神秘奖励，一定要记得每天来签到领取哦~')
            elif np_login + 1 == 7 and Context.Data.get_game_attr_int(uid, gid, 'bind_mobile', 0) == 0:
                return mo.set_error(3, u'你需要绑定手机，才可领取此神秘大奖')
            else:
                BirdAccount.set_login_info(uid, gid, now_day, ns_login, create_day)

            conf = conf['new']
            reward = conf[np_login]
            reward1 = reward[0]
            reward2 = reward[1]
        realChip = reward1['chip']
        rewards_info = BirdProps.issue_rewards(uid, gid, reward1, 'signin.reward', True)
        if len(reward2) > 0:
            _rewards = BirdProps.issue_rewards(uid, gid, reward2, 'signin.reward', True)
            rewards_info = BirdProps.merge_reward_result(True, rewards_info, _rewards)


        # vip 登录赠送 day_gift
        # if vip_level:
        #     day_gift = vipConfig[vip_level - 1].get('day_gift', 0)
        #     if day_gift:
        #         vip_gift_reward = BirdProps.issue_rewards(uid, gid, reward2, 'vip.gift.reward', True)
        #         rewards_info = BirdProps.merge_reward_result(True, rewards_info, vip_gift_reward)

        finalChip = 0
        finalDiamond = 0
        finalCoupon = 0
        if rewards_info.get('chip', 0):
            finalChip = rewards_info['chip']
        if rewards_info.get('diamond', 0):
            finalDiamond = rewards_info['diamond']
        if rewards_info.get('coupon', 0):
            finalCoupon = rewards_info['coupon']

        pipe_args = []
        delta_chip = realChip

        pipe_args.append('login.carrying.volume.chip')
        pipe_args.append(delta_chip)
        pipe_args.append('carrying.volume.chip')
        pipe_args.append(delta_chip)
        Context.Daily.mincr_daily_data(uid, gid, *pipe_args)
        NewTask.get_sign_in_task(uid)

        if finalChip:
            mo.set_param('chip', finalChip)
        if finalCoupon:
            mo.set_param('coupon', finalCoupon)
        if finalDiamond:
            mo.set_param('diamond', finalDiamond)
        return mo

    def on_month_card(self, uid, gid):
        # 领取月卡奖
        mo = MsgPack(Message.MSG_SYS_MONTH_REWARD | Message.ID_ACK)
        success, left_days = BirdProps.use_vip(uid, gid)
        if success:
            conf = self.get_month_card_reward(uid, gid)
            reward = BirdProps.issue_rewards(uid, gid, conf, 'month.card.reward', True)
            mo.set_param('final', reward)
            return mo
        return mo.set_error(1, 'failed')

    def on_new_month_card(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_NEW_MONTH_CARD_RECV | Message.ID_ACK)
        pid = mi.get_param('gid')
        if pid == 1:
            month_id = 14
            product_id = '102001'
        else:
            month_id = 15
            product_id = '102002'

        success, left_days = BirdProps.use_new_month_card(uid, gid, month_id)
        mo.set_param('pid', pid)
        if success:
            product_config = Context.Configure.get_game_item_json(gid, 'product.config')
            product_info = product_config.get(product_id)
            rw = product_info.get('content')
            reward = BirdProps.issue_rewards(uid, gid, rw, 'month.card.reward', True)
            mo.set_param('final', reward)
            return mo
        return mo.set_error(1, 'failed')

    def on_room_list(self, uid, gid, mi):
        room_config = Context.Configure.get_room_config(gid)
        if not room_config:
            Context.Log.error(uid, 'req room list, but no config fetch')
            return False

        conf = Context.copy_json_obj(room_config)
        vip_room_list = []
        for i in conf: #新手场的处理
            if i['room_type'] in [200,209]:
                conf.remove(i)
                if i['room_type'] == 209:
                    vip_room_list.append(i)
        mo = MsgPack(Message.MSG_SYS_ROOM_LIST | Message.ID_ACK)
        mo.set_param('room_list', conf)
        mo.set_param('vip_room_list', vip_room_list)
        match = mi.get_param('match', 0)
        if match:
            _match = Context.Configure.get_match_config(gid)
            conf.append(_match)
        #     session_ver = Context.Data.get_game_attr(uid, gid, 'session_ver')
        #     if Upgrade.cmp_version(session_ver, '1.2.0') >= 0:

        village_room = mi.get_param('village_room', 0)
        if village_room:
            _village_room = Context.Configure.get_game_item_json(gid, 'village_room.config')
            conf.insert(0, _village_room)

        return Context.GData.send_to_connect(uid, mo)

    def on_benefit(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_BENEFIT | Message.ID_ACK)
        conf = Context.Configure.get_game_item_json(gid, 'benefit.config')
        vip_level = BirdAccount.get_vip_level(uid, gid)
        total_times = conf['reward'][vip_level]['times']
        benefit_times, bankrupt_ts = Context.Daily.get_daily_data(uid, gid, 'benefit_times', 'bankrupt_ts')
        benefit_times = Tool.to_int(benefit_times, 0)
        if benefit_times >= total_times:
            return mo.set_error(1, 'none')
        now_ts = Time.current_ts()
        if not bankrupt_ts or int(bankrupt_ts) > now_ts:
            return mo.set_error(2, 'wait')

        benefit_chip = conf['reward'][vip_level]['max']  #min(conf['base'] * barrel_multi, conf['reward'][vip_level]['max'])
        reward = [benefit_chip] * conf['reward'][vip_level]['times']
        #Context.Log.report('on_benefit:', benefit_chip)
        result = BirdAccount.issue_benefit(uid, gid, reward)
        Context.Log.report('on_benefit result:', result)
        if not result:
            return mo.set_error(3, 'failed')

        Context.Daily.del_daily_data(uid, gid, 'bankrupt_ts')
        Context.Data.set_game_attrs_dict(uid, gid, {'bankrupt_chip_ts': now_ts})
        mo.update_param(result)
        return mo

    def on_get_config(self, uid, gid, mi):
        which = mi.get_param('which')
        if isinstance(which, (str, unicode)):
            which = [which]

        mo = MsgPack(Message.MSG_SYS_CONFIG | Message.ID_ACK)
        for name in which:
            if name == 'vip':
                conf = self.get_vip_config(uid, gid)
            elif name == 'shop':
                conf = self.get_shop_config(uid, gid)
            elif name == 'weaponshop':
                conf = Shop.get_weaponshop_config(uid, gid)
            elif name == 'weapon':
                conf = Shop.get_weapon_config(uid, gid)
            elif name == 'weaponeff':
                conf = Shop.get_weaponeff_config(uid, gid)
            elif name == 'props_shop':
                conf = Shop.get_props_shop_info(uid,gid)
            elif name == 'limit_time':
                conf = Shop.get_limit_time_info(gid)
            elif name == 'limit_shop':
                conf = Shop.get_limit_shop_info(uid, gid, 1)
            # elif name == 'raffle':
            #     conf = self.get_raffle_config(uid, gid)
            elif name == 'props':
                conf = BirdProps.get_props_config(gid)
            elif name == 'unlock':
                conf = self.get_unlock_config(uid, gid)
            elif name == 'barrel':
                conf = self.get_barrel_config(uid, gid)
            elif name == 'exchange':
                #self.get_exchange_config(uid, gid)
                conf = Shop.get_limit_shop_info(uid, gid, 2)
            elif name == 'benefit':
                conf = self.get_benefit_config(uid, gid)
            elif name == 'html':
                conf = self.get_html_config(uid, gid)
            elif name == 'exp':
                conf = self.get_exp_config(uid, gid)
            elif name == 'share':
                conf = self.get_share_config(gid)
            elif name == 'upbrrel':
                conf = self.get_upbrrel_config(uid, gid)
            elif name == 'match':
                conf = BirdMatch.get_config(gid)
            elif name == 'pet':
                conf = BirdPet.config(uid, gid)
            elif name == 'target': # 靶场
                conf = Target.get_target_config(uid, gid)
            elif name == 'tips':
                tips_version = mi.get_param('version')
                conf = self.get_tips_config(gid, tips_version)
            elif name == 'global_flag':#全局标记，（现已有：修改昵称次数标记，绑定手机标记）
                conf = self.get_golbalflag_config(uid, gid)
            elif name == 'notice':
                conf = self.get_notice_config(gid)
            elif name == 'vip_room':
                conf = self.get_vip_room_config(gid)
            elif name == 'recharge_add':
                conf = self.get_recharge_add_config(uid, gid)
            else:
                continue
            mo.set_param(name, conf)
        return mo

    def get_recharge_add_config(self, uid, gid):
        conf = Context.RedisMix.hash_get_json('game.%d.background' % gid, 'recharge_add_new', {})
        channel_id = Context.Data.get_attr(uid, 'loginChannelId', '1004_0')
        if conf.has_key(channel_id):
            cf = conf[channel_id]
        else:
            cf = {"zhifubao": 0, "weixin": 0}
        return cf

    def get_vip_room_config(self, gid):
        conf = {}
        vip_room_config = Context.Configure.get_game_item_json(gid, 'vip_room.config')
        vip_room_price = Tool.to_int(vip_room_config.get('vip_room_price'))
        vip_room_level = Tool.to_int(vip_room_config.get('vip_room_level'))
        conf['vip_room_price'] = vip_room_price
        conf['vip_room_level'] = vip_room_level
        return conf

    def get_notice_config(self, gid):
        context = Context.RedisCache.get('game.2.notice')
        max_notice_id = Context.RedisMix.hash_get_int('global.info.hash', 'max.notice.id', 0)
        info = {}
        c = []
        if context:
            context = Context.json_loads(context)
            for i in context:
                c.append([i[0],i[1]])
        info['c'] = c
        info['id'] = max_notice_id
        return info

    def get_tips_config(self, gid, tips_version=-1):
        tips_conf = Context.Configure.get_game_item_json(gid, 'tips.config')
        if str(tips_version) != tips_conf[0]:
            return tips_conf
        return {}

    def get_vip_config(self, uid, gid):
        vip = Context.Configure.get_game_item_json(gid, 'vip.config')
        benefitCfg = Context.Configure.get_game_item_json(gid, 'benefit.config')
        nIdx = 1
        for vipAtr in vip:
            vipAtr['Benefit'] = benefitCfg['reward'][nIdx]['max']
            vipAtr['BenefitTimes'] = benefitCfg['reward'][nIdx]['times']
            nIdx += 1

        # session_ver = Context.Data.get_game_attr(uid, gid, 'session_ver')
        # if Upgrade.cmp_version(session_ver, '1.1.0') < 0:
        #     return vip[:-2]
        return vip

    #全局的通用配置，标记可以加在这个位置发送给客户端（已有修改昵称，绑定手机的标记）
    def get_golbalflag_config(self, uid, gid):
        changenick = Context.Configure.get_game_item_json(gid, 'nickname.diamoncost.config')
        times = Context.Data.get_game_attr_int(uid, gid, 'change_nick_times',0)
        conf = {}
        nickDict = {}
        nickDict['list'] = changenick
        nickDict['times'] = times
        conf['change_nick'] = nickDict
        bind_mobile = Context.Data.get_game_attr_int(uid, gid, 'bind_mobile', 0)
        conf['bind_mobile'] = bind_mobile
        return conf

    def get_share_config(self, gid):
        _conf = Context.Configure.get_game_item_json(gid, 'share.config')
        conf = Context.copy_json_obj(_conf)
        for x in range(len(conf['friend_reward'])):
            conf['friend_reward'][x]['reward'] = BirdProps.convert_reward(conf['friend_reward'][x]['reward'])
        for x in range(len(conf['welfare'])):
            conf['welfare'][x]['reward'] = BirdProps.convert_reward(conf['welfare'][x]['reward'])
        return conf


    def get_shop_config(self, uid, gid):
        product_config = Context.Configure.get_game_item_json(gid, 'product.config')
        shop_config = Context.Configure.get_game_item_json(gid, 'shop.config')
        if not shop_config or not product_config:
            return {}

        product_config = Context.copy_json_obj(product_config)
        attrs = []
        reg_channel_id = Context.Data.get_attr(int(uid), 'channelid', '1001_0')
        if reg_channel_id == '1001_0':
            for pid in list(shop_config['chip']):
                if int(pid) > 110000:
                    attrs.append(pid)
        else:
            for pid in list(shop_config['chip']):
                if int(pid) < 110000:
                    attrs.append(pid)

        if reg_channel_id == '1001_0':
            for pid in list(shop_config['diamond']):
                if int(pid) > 110000:
                    attrs.append(pid)
        else:
            for pid in list(shop_config['diamond']):
                if int(pid) < 110000:
                    attrs.append(pid)

        attrs.extend(shop_config['first'])
        fileds = []
        for attr in attrs:
            fileds.append('product_%s' % attr)
            fileds.append('reset_%s' % attr)

        counts = Context.Data.get_game_attrs(uid, gid, fileds)
        kvs = Tool.make_dict(attrs, counts[::2])
        reset_kvs = Tool.make_dict(attrs, counts[1::2])
        info = {}
        for k, pids in shop_config.iteritems():
            group = []
            for pid in pids:

                if k in ['chip', 'diamond'] and pid not in attrs:
                    continue
                product = product_config[pid]

                del product['name']
                if k in ('chip', 'diamond'):
                    if product.has_key('content'):
                        del product['content']
                if 'first' in product:
                    if product.has_key('first'):
                        del product['first']
                if k in ['chip', 'diamond', 'first'] and (kvs[str(pid)] is None or reset_kvs[str(pid)]):
                    product['first'] = 1
                product['id'] = pid
                group.append(product)
            info[k] = group
        #info['card'] = info['card'][0]      # 只要一个
        info['new_card'] = info['card'][1:]
        card_info = self.get_month_card_info(uid, gid)
        if card_info:
            product_card = info['card'][0]
            product_card['price'] = card_info.get('price')
            product_card['content'] = card_info.get('rw')
            info['card'] = product_card
        else:
            info['card'] = info['card'][0]

        if Context.Data.get_uid_create(uid) >= 1315:
            info['new_first'] = info['first'][1]  # 新6元礼包
        info['first'] = info['first'][0]  # 老首冲

        # dz add 武器商城配置信息
        weapon_config = Context.Configure.get_game_item_json(gid, 'weaponShop.config')
        if weapon_config:
            info['weapon'] = weapon_config
        # dz add end

        return info

    def get_month_card_info(self, uid, gid):
        version = Context.Data.get_game_attr_int(uid, gid, 'month_card_version', 0)
        if version == 0:
            state, left_days = props.BirdProps.get_vip(uid, gid)
            if left_days > 0:
                return None
            else:
                version = Context.RedisMix.hash_get_int('game.%d.background' % gid, 'month_card.max.version', 0)
        cnf = Context.RedisMix.hash_get_json('game:%d:month_card_version' % gid, str(version))
        return cnf

    def get_month_card_reward(self, uid, gid):
        version = Context.Data.get_game_attr_int(uid, gid, 'month_card_version', 0)
        if version != 0:
            conf = Context.RedisMix.hash_get_json('game:%d:month_card_version' % gid, str(version))
            rw = conf.get('rw')
        else:
            rw = Context.Configure.get_game_item_json(gid, 'month.card.reward')
        return rw


    def get_raffle_config(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_RAFFLE_CONFIG | Message.ID_ACK)
        raffle_config = Context.Configure.get_game_item_json(gid, 'raffle.config')
        raffle_config = Context.copy_json_obj(raffle_config)
        loop_config = raffle_config['loop']
        raffle_config = raffle_config['config']
        for item in raffle_config:
            item['reward'] = []
            item['reward'].append(item['coupon_reward']['reward'])
            for reward in item['other_reward']:
                item['reward'].append(reward['reward'])
            del item['coupon_reward']
            del item['other_reward']

        class_pool, loop_times = Context.Daily.get_daily_data(uid, gid, 'fake.bonus.count', 'bonus.loop.times')
        class_pool = Tool.to_int(class_pool, 0)
        loop_times = Tool.to_int(loop_times, 0)

        if loop_times > len(loop_config) - 1:
            this_count = loop_config[-1]
        else:
            this_count = loop_config[loop_times]
        info = {'config': raffle_config}
        bonus_pool = Context.Data.get_game_attr_int(uid, gid, 'bonus_pool', 0)
        info['pool'] = bonus_pool
        info['progress'] = [class_pool, this_count]
        mo.set_param("info", info)
        return mo

    def get_upbrrel_config(self, uid, gid):
        """
        发一个
        """
        config = Context.Configure.get_game_item_json(gid, 'barrel.unlock.config')
        barrel_level = Context.Data.get_game_attr_int(uid, gid, 'barrel_level', 1)
        strong_conf = Context.Configure.get_game_item_json(gid, 'barrel.unlock.strong')
        level = barrel_level + 1
        conf = {}
        if strong_conf[0] <= level <= strong_conf[1]:
            conf = config[level-1]
        return conf

    def get_unlock_config(self, uid, gid):
        """
        前端显示5个
        """
        return Context.Configure.get_game_item_json(gid, 'barrel.unlock.config')


    def get_barrel_config(self, uid, gid):
        return Context.Configure.get_game_item_json(gid, 'barrel.level.config')

    def get_exchange_config(self, uid, gid):
        return Context.Configure.get_game_item_json(gid, 'exchange.config')

    def get_benefit_config(self, uid, gid):
        conf = Context.Configure.get_game_item_json(gid, 'benefit.config')
        benefit_times, bankrupt_ts = Context.Daily.get_daily_data(uid, gid, 'benefit_times', 'bankrupt_ts')
        benefit_times = int(benefit_times) if benefit_times else 0

        barrel_level = Context.Data.get_game_attr_int(uid, gid, 'barrel_level', 1)
        barrel_multi = BirdAccount.trans_barrel_level(gid, barrel_level)
        vip_level = BirdAccount.get_vip_level(uid, gid)
        benefit_chip = min(conf['base'] * barrel_multi, conf['reward'][vip_level]['max'])
        reward = []
        for i in range(conf['reward'][vip_level]['times']):
            reward.append({'chip': benefit_chip, 'wait': conf['wait'][i]})
        _info = {
            'which': benefit_times,      # 已领取几次
            'conf': reward
        }
        if bankrupt_ts is not None:
            now_ts = Time.current_ts()
            bankrupt_ts = int(bankrupt_ts)
            if now_ts > bankrupt_ts:
                _info['wait'] = 0
            else:
                _info['wait'] = bankrupt_ts - now_ts
        return _info

    def on_props_list(self, uid, gid, mi):
        BirdPet.up_hatch(uid, gid)
        props_list = BirdProps.get_props_list(uid, gid)
        info = {
            'c': Context.UserAttr.get_chip(uid, gid, 0),
            'd': Context.UserAttr.get_diamond(uid, gid, 0),
            'o': Context.UserAttr.get_coupon(uid, gid, 0)
        }
        if props_list:
            info['p'] = BirdProps.filter_props_by_version(uid, gid, props_list)

        # 升级礼包
        conf = Context.Configure.get_game_item_json(gid, 'exp.level.reward')
        level, _ = BirdAccount.get_exp_info(uid, gid)
        if level < len(conf):
            info['up'] = BirdProps.convert_reward(conf[level])

        # 宠物蛋孵化信息
        eIds = BirdProps.pet_egg_ids()
        hTimeInfo = []
        now_ts = Time.current_ts()
        for eId in eIds:
            hTime = BirdPet.get_egg_hTime(uid, gid, eId)
            if hTime:
                egg_conf = BirdProps.get_config_by_id(gid, eId)
                _t = egg_conf['hTime'] - (now_ts-hTime)
                hTimeInfo.append([eId, _t])
        if hTimeInfo:
            info['h'] = hTimeInfo

        mo = MsgPack(Message.MSG_SYS_PROPS_LIST | Message.ID_ACK)
        mo.update_param(info)
        return mo

    # 绑定手机赠送礼包
    def on_consume_bind_reward(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_BIND_REWARD | Message.ID_ACK)
        if Context.Data.get_game_attr_int(uid, gid, 'bind_mobile', 0) != 1:
            return
        conf = Context.Configure.get_game_item_json(gid, 'bindPhone.reward')
        info = {}
        BirdProps.issue_rewards(uid, gid, conf[0], 'bind.rewards', True)
        info['reward'] = BirdProps.convert_reward(conf[0])
        Context.Data.set_game_attr(uid, gid, 'bind_mobile', 2)
        mo.update_param(info)
        return mo

    def on_use_props(self, uid, gid, mi):
        _id = mi.get_param('id')
        _count = mi.get_param('count')
        mo = MsgPack(Message.MSG_SYS_USE_PROPS | Message.ID_ACK)
        if _id not in [BirdProps.PROP_EGG_BRONZE, BirdProps.PROP_EGG_SILVER,
                       BirdProps.PROP_EGG_GOLD, BirdProps.PROP_EGG_COLOR] and _id < 10000*1000:
            return mo.set_error(1, 'can not use')

        if not isinstance(_count, int) or _count <= 0:
            return mo.set_error(2, 'count error')
        if _id > 10000*1000:
            return self.use_limit_props(uid, gid, _id, _count)

        lock = BirdAccount.check_global_lock(uid, 0)
        if _id in [211, 212, 213, 214] and lock and lock['gid'] == 10005:
            return mo.set_error(5, u'您当前正在斗地主游戏中，此功能暂不可用')

        conf = BirdProps.get_config_by_id(gid, _id)
        if not conf:
            Context.Log.error('not found props:', uid, gid, _id, _count)
            return mo.set_error(4, 'not found props')

        real, final = BirdProps.incr_props(uid, gid, _id, -_count, 'entity.use')
        if real != -_count:
            return mo.set_error(3, '道具不足，无法使用')

        if _count == 1:
            reward = conf['content']
        else:
            reward = BirdProps.merge_reward(*[conf['content']] * _count)
        reward = Context.copy_json_obj(reward)
        reward = self.deal_reward(reward)
        reward = BirdProps.issue_rewards(uid, gid, reward, 'entity.use')
        reward = BirdProps.convert_reward(reward)

        # 个人 宝盒 统计
        Context.Data.hincr_game(uid, gid, 'out_props_'+str(_id), _count)

        mo.update_param(reward)

        return mo

    def use_limit_props(self, uid, gid, idx, count): #使用道具
        mo = MsgPack(Message.MSG_SYS_USE_PROPS | Message.ID_ACK)
        if not isinstance(idx, int):
            return mo.set_error(6, 'id error')
        props_id = int(idx/1000)
        days = int(idx%1000)

        weapon_buy_dict = Context.Data.get_game_attr_json(uid, gid, 'weapon_buy_dict')
        if int(weapon_buy_dict[str(props_id)]) == 1:
            return mo.set_error(6, 'weapon error')

        real, final = BirdProps.incr_props(uid, gid, idx, -count, 'props.use')
        if real != -count:
            return mo.set_error(3, '道具不足，无法使用')
        #20000-30000是限时炮
        if props_id > 20000 and props_id <= 30000:
            es = Context.Data.get_timer_attr(10000, gid, "%d_%d" % (uid, props_id))
            end_ts = Time.current_ts() + days * 24 * 3600
            if es != None and int(weapon_buy_dict[str(props_id)]) > 1:
                end_ts = int(es) + days * 24 * 3600
            last_time = end_ts - Time.current_ts()
            weapon_buy_dict[str(props_id)] = end_ts
            Context.Data.set_game_attr(uid, gid, 'weapon_buy_dict', Context.json_dumps(weapon_buy_dict))
            Context.Data.set_timer_attr(10000, gid, "%d_%d"%(uid, props_id), end_ts)
            self.timer.setTimeout(last_time, {'gameId': gid, 'userId': uid, 'propsId': props_id, 'action': 'limit_props'})
        return mo.set_param('final', 1)


    def deal_reward(self, rewards):
        if not rewards:
            return {}
        props = rewards.get('props')
        if not props:
            return rewards

        _props = []
        for prop in props:
            count = prop['count']
            if 'dRate' in prop:
                count = 0
                for _ in range(prop['count']):
                    if random.random() <= prop.get('dRate'):
                        count += 1
            if count:
                _props.append({'id': prop['id'], 'count': count})
        rewards['props'] = _props
        return rewards

    def on_raffle(self, uid, gid, mi):
        _id = mi.get_param('i')
        _button = mi.get_param('bt')
        mo = MsgPack(Message.MSG_SYS_RAFFLE | Message.ID_ACK)
        raffle_config = Context.Configure.get_game_item_json(gid, 'raffle.config')
        raffle_config = Context.copy_json_obj(raffle_config)
        loop_config = raffle_config['loop']
        raffle_config = raffle_config['config']
        class_pool, loop_times = Context.Daily.get_daily_data(uid, gid, 'fake.bonus.count', 'bonus.loop.times')
        class_pool = Tool.to_int(class_pool, 0)
        loop_times = Tool.to_int(loop_times, 0)
        if loop_times > len(loop_config) - 1:
            this_count = loop_config[-1]
        else:
            this_count = loop_config[loop_times]
        if class_pool < this_count:
            return mo.set_error(1, 'lack bird')

        reward = None
        for item in raffle_config:
            if item['id'] != _id:
                continue

            bonus_pool = Context.Data.get_game_attr_int(uid, gid, 'bonus_pool', 0)
            if bonus_pool < item['limit']:
                return mo.set_error(2, 'lack chip')
            coupon_reward = item.get('coupon_reward')
            other_reward = item.get('other_reward')
            rate = coupon_reward.get('rate')
            reward_c = coupon_reward.get('reward')
            price = BirdProps.get_props_price(reward_c)
            #pool_free = Context.RedisMix.hash_get('game.2.share', 'coupon_pool_free', default=0)
            P = random.random()
            if bonus_pool > price and P < rate: #and pool_free > reward_c['coupon'] :
                #Context.RedisMix.hash_incrby('game.2.share', 'coupon_pool_free', reward_c['coupon'])
                reward = reward_c
                index = 0
            else:
                weight_dict = {}
                weight_total = 0
                for k,v in enumerate(other_reward):
                    weight_f = v.get('weight_f')
                    reward_o = v.get('reward')
                    price = BirdProps.get_props_price(reward_o)

                    value = (price - bonus_pool)/5000
                    if value == 0:
                        value = 1

                    weight = 1/float(abs(value)) * weight_f
                    weight_total += weight
                    weight_dict[k] = weight
                index = 0
                rate_vale = 0
                rdm = random.random()
                for k,v in weight_dict.items():

                    rate_vale += v / float(weight_total)
                    if rdm < rate_vale:
                        reward = other_reward[k]['reward']
                        index = k
                        break
                index += 1

            Context.Data.hincr_game(uid, gid, 'bonus_pool', -bonus_pool)
            Context.Data.hincr_pool_cycle(uid, 'raffle_chip_pool', 'in.bonus.raffle', bonus_pool)

            diamond = reward.get('diamond', 0)
            if diamond > 0:
                diamond_pool_cycle = Context.RedisMix.hash_get_int('game.2.share', 'diamond_pool_cycle')
                if diamond_pool_cycle < diamond:
                    reward = other_reward[-1]['reward']
                    index = len(other_reward)

            chip = reward.get('chip', 0)
            if chip > 0:
                raffle_chip_pool = Context.RedisMix.hash_get_int('game.2.share', 'raffle_chip_pool')
                if raffle_chip_pool < chip:
                    reward = other_reward[-1]['reward']
                    index = len(other_reward)
            if reward.has_key('diamond'):
                Context.Data.hincr_pool_cycle(uid, 'raffle_chip_pool', 'out.bonus.raffle.diamond', -diamond*500)
            elif reward.has_key('coupon'):
                Context.Data.hincr_pool_cycle(uid, 'raffle_chip_pool', 'out.bonus.raffle.coupon', -reward['coupon']*5000)
            else:
                p = BirdProps.get_props_price(reward)
                Context.Data.hincr_pool_cycle(uid, 'raffle_chip_pool', 'out.bonus.raffle', -p)
            reward = BirdProps.issue_rewards(uid, gid, reward, 'bonus.raffle')
            mo.set_param('bt', _button)
            mo.set_param('i', index + 1)
            rw = BirdProps.convert_reward(reward)
            mo.update_param(rw)
            # 重置数据
            pipe_args = ['fake.bonus.count', -class_pool, 'bonus.loop.times', 1]
            Context.Daily.mincr_daily_data(uid, gid, *pipe_args)
            if _id >= 3:
                bulletin = 3
                nick = Context.Data.get_attr(uid, 'nick')
                nick = Context.hide_name(nick)
                room_name = item.get('name')

                rw_str = u''
                rwe = rw['w']
                if rwe.has_key('c'):
                    rw_str += u'鸟蛋*%d' % rwe['c']
                if rwe.has_key('d'):
                    rw_str += u'钻石*%d' % rwe['d']
                if rwe.has_key('o'):
                    rw_str += u'鸟券*%d' % rwe['o']
                if rwe.has_key('p'):
                    for i in rwe['p']:
                        rw_str += u'%s*%d' % (BirdProps.get_props_desc(i[0]), i[1])
                led = u'幸运爆表！玩家<color=#00FF00FF>%s</color>通过<color=#00FF00FF>%s</color>获得<color=#FFFF00FF>%s</color>！' % (
                    nick, room_name, rw_str)
                mou = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
                mou.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
                Context.GData.broadcast_to_system(mou)

            return mo

        return mo.set_error(3, 'error id')


    #赠送礼物
    def on_present(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_PRESENT | Message.ID_ACK)
        # 赠送功能增加vip限制  以及赠送次数限制
        vip_level = BirdAccount.get_vip_level(uid, gid)
        if vip_level:
            vip_config = Context.Configure.get_game_item_json(gid, 'vip.config')
            sendTimesTotal = vip_config[vip_level-1].get('send_t', 0)
            if sendTimesTotal > 0:
                present_times = Context.Daily.get_daily_data(uid, gid, 'present_times',)
                present_times = Tool.to_int(present_times, 0)
                if present_times >= sendTimesTotal:
                    return mo.set_error(10, 'no times')

            else:
                return mo.set_error(9, 'vip limit')
        else:
            return mo.set_error(9, 'vip limit')

        # 指定用户不能赠送
        if uid in (20014, 20016, 20017, 29713):
            return mo.set_error(8, 'limit account')
        # 直播号不能赠送
        exist = Context.RedisMix.set_ismember('game.%d.live.telecast.user' % gid, uid)
        if exist:
            return mo.set_error(8, 'limit account')

        _id = mi.get_param('id')
        if not isinstance(_id, int):
            return mo.set_error(1, 'error param')
        _count = mi.get_param('count')
        if not isinstance(_count, int) or _count <= 0:
            return mo.set_error(2, 'error param')
        if _id not in [201, 202, 203, 204, 205, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 224, 225]:
            return mo.set_error(3, 'error id')
        # 斗地主锁
        # u'您当前正在%s游戏中，请稍后再试' % lock['name']
        lock = BirdAccount.check_global_lock(uid, 0)
        if _id in [211, 212, 213, 214] and lock and lock['gid'] == 10005:
            return mo.set_error(8, u'您当前正在斗地主游戏中，此功能暂不可用')
        BirdPet.up_hatch(uid, gid)
        if _id in BirdPet.pet_ids()['s']:
            hTime = BirdPet.get_egg_hTime(uid, gid, _id)
            if hTime:
                return mo.set_error(3, 'error id')
        ta = mi.get_param('ta')
        if ta < 0 or not Context.UserAttr.check_exist(ta, gid):
            return mo.set_error(4, 'error uid')
        conf = BirdProps.get_config_by_id(gid, _id)
        if conf:
            if 'count' in conf:
                if _count % conf['count'] != 0:
                    return mo.set_error(5, 'error count')
            if 'present' in conf:
                pay_total = Context.Data.get_game_attr_int(uid, gid, 'pay_total', 0)
                if conf['present']['pay'] > pay_total:
                    return mo.set_error(7, 'pay limit')
            real, final = BirdProps.incr_props(uid, gid, _id, -_count, 'present.props', ta=ta)
            if real != -_count:
                return mo.set_error(6, '道具不足，无法赠送')

            times = time.time()
            reward = {'props':[{'id':_id, 'count': _count}]}
            #def add_mail(self, uid, gid, times, nType, reward, sender):
            ret = Mail.add_mail(ta, gid, times, 1, reward, uid)
            if not ret:
                return mo.set_error(9, 'add mail fail')
            Mail.send_mail_list(ta, gid)
            mo.set_param('id', _id)
            mo.set_param('count', final)
            #BirdProps.incr_props(ta, gid, _id, _count, 'present.props', ta=uid)

            # 赠送成功 修改本日赠送次数
            present_times += _count
            Context.Daily.set_daily_data(uid, gid, 'present_times', present_times)
            return mo

        Context.Log.error('no props config found', _id)
        return mo.set_error(7, 'unknown')

    def on_exchange(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_EXCHANGE | Message.ID_ACK)
        _id = mi.get_param('id')
        if not isinstance(_id, int):
            return mo.set_error(1, 'error param')

        conf = Context.Configure.get_game_item_json(gid, 'exchange.config')
        if _id >= len(conf):
            return mo.set_error(1, 'error id')

        info = conf[_id]
        to_type = info['type']
        if to_type not in ('diamond', 'props', 'phone'):
            raise Exception(str(to_type) + '<----error type, please check config')

        real, final = Context.UserAttr.incr_coupon(uid, gid, -info['cost'], 'exchange.' + to_type)
        if real != -info['cost']:
            return mo.set_error(2, '鸟券不足，无法兑换')
        mo.set_param('coupon', final)
        record = {
            'uid': uid,
            'type': 'exchange',
            'ts': Time.current_ts(),
            'from': 'coupon',
            'to': to_type,
            'cost': info['cost'],
            'count': info['count'],
            'desc': info['desc']
        }
        if info['type'] == 'diamond':   # 兑换钻石
            real, final = Context.UserAttr.incr_diamond(uid, gid, info['count'], 'exchange.diamond')
            if info['count'] > 0:
                NewTask.get_diamond_task(uid, info['count'], 'exchange.diamond')
            mo.set_param('diamond', final)
            state = 1
        elif info['type'] == 'props':   # 兑换道具
            real, final = BirdProps.incr_props(uid, gid, info['id'], info['count'], 'exchange.props')
            mo.set_param('id', info['id'])
            mo.set_param('count', final)
            state = 1
            record['id'] = info['id']
        elif info['type'] == 'phone':
            state = 0
            record['phone'] = mi.get_param('phone')
        else:
            raise Exception('something error, please check config')

        seq_num = Context.RedisMix.hash_incrby('game.%d.info.hash' % gid, 'exchange.history.seq', 1)
        Context.RedisCluster.hash_set(uid, 'history:%d:%d' % (gid, uid), seq_num, state)

        record = Context.json_dumps(record)
        Context.RedisMix.hash_mset('game.%d.exchange.record' % gid, seq_num, record)
        fmt = Time.current_time('%Y-%m-%d')
        Context.RedisStat.hash_set('history:%d:%s' % (gid, fmt), seq_num, uid)
        return mo

    def on_inner_buy(self, uid, gid, mi):

        mo = MsgPack(Message.MSG_SYS_INNER_BUY | Message.ID_ACK)
        _id = mi.get_param('id')
        if not isinstance(_id, int):
            return mo.set_error(1, 'error param')
        _count = mi.get_param('count')
        if not isinstance(_count, int) or _count <= 0:
            return mo.set_error(2, 'error param')
        if _id not in [201, 202, 203, 204, 205]:
            return mo.set_error(3, 'error id')

        level = Context.Data.get_game_attr_int(uid, gid, 'barrel_level', 1)
        barrel_unlock_use = Tool.to_int(Context.Configure.get_game_item_json(gid, 'barrel.unlock.use'), 3)
        if level < barrel_unlock_use:
            return mo.set_error(4, u'解锁10倍炮才能购买')
        conf = BirdProps.get_config_by_id(gid, _id)
        if conf:
            if 'count' in conf:
                if _count % conf['count'] != 0:
                    return mo.set_error(5, 'error count')
            real, final = Context.UserAttr.incr_diamond(uid, gid, -conf['diamond'], 'inner.buy.%d' % _id)
            if real != -conf['diamond']:
                return mo.set_error(6, '钻石不足，无法购买')
            NewTask.get_diamond_consume_task(uid, conf['diamond'])
            mo.set_param('diamond', final)
            real, final = BirdProps.incr_props(uid, gid, _id, _count, 'inner.buy')
            mo.set_param('id', _id)
            mo.set_param('count', final)
            return mo

        Context.Log.error('no props config found', _id)
        return mo.set_error(7, 'unknown')

    def on_consume_cdkey(self, uid, gid, mi):
        code = mi.get_param('code')
        imei = mi.get_param('imei')
        data = {'appId': 1002, 'code': code, 'userChannel': 0, 'imei': imei, 'userId': uid}
        cdkey_server_url = Context.Configure.get_game_item(gid, 'cdkey.server.url')
        cdkey_access_key = Context.Configure.get_global_item('cdkey.access_key')
        ts = Time.current_ts()
        s = 'gameId=%d&token=%s&ts=%d' % (gid, cdkey_access_key, ts)
        sign = Algorithm.md5_encode(s)
        data['sign'] = sign
        data['gameId'] = gid
        data['ts'] = ts

        result = Context.WebPage.wait_for_json(cdkey_server_url, postdata=Context.json_dumps(data))
        mo = MsgPack(Message.MSG_SYS_CONSUME_CDKEY | Message.ID_ACK)
        if result['result'] != 1:  # 失败
            if result['result'] == 2:
                mo.set_error(u'今日已达领取上限')
            else:
                mo.set_error(result['result'])
        else:
            try:
                # dz add record
                Context.Log.debug("game_exchange_cdkey:", mi)
                Context.Record.add_record_game_exchange_cdkey(mi)

                rewards = result['desc']
                tag = 'cdkey.reward.free'
                if rewards.has_key('pool'):#兑换码里面的pool相当于是充值
                    tag = 'cdkey.reward'

                    cost = int(rewards['pool'])
                    del rewards['pool']

                    today_cdkey_pay_times, _ = Context.Daily.mincr_daily_data(uid, gid, 'cdkey_pay_times', 1, 'cdkey_pay_total', cost)  # 本日cdkey使用次数,本日cdkey总额度
                    cdkey_pay_total = BirdProps.incr_cdkey_pay(uid, gid, cost, 'exchange_cdkey')     # 将本次兑换cost值存入个人记录中，并返回总值

                    channel_id = Context.RedisCluster.hash_get(uid, 'user:%s' % uid, 'channelid')
                    pipe_args = []
                    if today_cdkey_pay_times == 1:  # today first pay                    # 本日首次使用cdkey
                        pipe_args.append(channel_id + '.cdkey_pay.user.count')           # 本日cdkey 使用用户数+1
                        pipe_args.append(1)
                    pipe_args.append(channel_id + '.cdkey_pay.user.pay_total')           # 本日cdkey使用金额+cost
                    pipe_args.append(cost)
                    pipe_args.append(channel_id + '.user.cdkey_pay.times')               # 本日cdkey使用总次数+1
                    pipe_args.append(1)

                    if cdkey_pay_total == cost:  # life first pay                              # 如果为首次使用cdkey
                        pipe_args.append(channel_id + '.new.cdkey_pay.user.count')        # 本日新增cdkey使用用户数+1
                        pipe_args.append(1)

                        Context.Daily.mincr_daily_data(uid, gid, 'new_cdkey_pay_user', 1)    # 此用户标记为新增使用cdkey用户
                        new_pay_user = 1
                    else:
                        new_pay_user = Context.Daily.get_daily_data(uid, gid, 'new_cdkey_pay_user')

                    if new_pay_user:                                                         # 如果此用户为新增使用cdkey用户
                        pipe_args.append(channel_id + '.new.cdkey_pay.user.pay_total')       # 本日新增使用cdkey 金额+cost
                        pipe_args.append(cost)
                        pipe_args.append(channel_id + '.new.cdkey_pay.user.pay_times')            # 新增用户充值次数+1
                        pipe_args.append(1)

                    Context.Stat.mincr_daily_data(channel_id, *pipe_args)                         # 本日cdkey数据写入
                    Context.Stat.mincr_daily_user_data(channel_id, uid, *pipe_args)
                    Context.Stat.mincr_user_data(uid, gid, *pipe_args)
                    key = 'game.%d.info.hash' % gid
                    pipe_args = []
                    if cdkey_pay_total == cost:                                                   # 首次使用cdkey
                        pipe_args.append(channel_id + '.cdkey_pay.user.count')                    # 本服本渠道使用cdkey用户+1
                        pipe_args.append(1)

                    pipe_args.append(channel_id + '.cdkey_pay.user.pay_total')                    # 本服本渠道cdkey总金额+cost
                    pipe_args.append(cost)
                    pipe_args.append(channel_id + '.user.cdkey_pay.times')                        # 本服本渠道cdkey总使用次数+1
                    pipe_args.append(1)
                    Context.RedisMix.hash_mincrby(key, *pipe_args)                                # 数据写入

                    Context.Data.hincr_rank(101, gid, '%d' % uid, cost)                           # cdkey金额算入排行榜
                    PayActivity.pay_set(uid, cost)                                                # 支付活动
                    GiveActivity.pay_set(uid, cost)
                    ShakeActivity.pay_set(uid, cost)

                rewards = BirdProps.issue_rewards(uid, gid, rewards, tag, True)                         # cdkey奖励发放
                _rewards = BirdProps.convert_reward(rewards)

                mo.update_param(_rewards)
            except:
                Context.Log.exception(uid, gid, result)
                return
        return mo

    def get_html_config(self, uid, gid):
        html_conf = Context.Configure.get_game_item_json(gid, 'html.config.new')
        # ver = Context.Data.get_game_attr(uid, gid, 'session_ver')
        # if Upgrade.cmp_version(ver, '1.1.0') >= 0:
        #     html_conf = Context.Configure.get_game_item_json(gid, 'html.config.new')
        # else:
        #     html_conf = Context.Configure.get_game_item_json(gid, 'html.config.old')
        #     kvs = Context.Data.get_game_attrs_dict(uid, gid, ['channel', 'platform'])
        #     if 'channel' not in kvs:
        #         kvs['channel'] = 'qifan'
        #     if 'platform' not in kvs:
        #         kvs['platform'] = 'android'
        #     html_conf = Context.copy_json_obj(html_conf)
        #     for k, v in html_conf.iteritems():
        #         html_conf[k] = v % kvs
        return html_conf

    def get_exp_config(self, uid, gid):
        return Context.Configure.get_game_item_json(gid, 'exp.level')

    def on_product_deliver(self, uid, gid, mi):
        orderId = mi.get_param('orderId')
        productId = mi.get_param('productId')
        payType = mi.get_param('paytype', '0')
        channel = mi.get_param('channel')
        cost = mi.get_param('cost')
        channel_id = Context.RedisCluster.hash_get(uid, 'user:%s' %uid, 'channelid')
        if int(cost) < 1:
            cost = 1
        cost = int(cost)
        param = {
            'orderId': orderId,
            'productId': productId,
            'paytype': payType,
            'channel': channel,
            'cost': cost
        }
        Context.Log.report('product.issue: [%d, %d, %s, %s]' % (uid, gid, orderId, param))
        all_product = Context.Configure.get_game_item_json(gid, 'product.config')
        shop_config = Context.Configure.get_game_item_json(gid, 'shop.config')
        if productId not in all_product:
            if int(productId) >= 1000000:
                gift_product_config = Shop.get_gift_config_from_db()
                Shop.on_gift_product_deliver(uid, gid, int(productId), gift_product_config)
                product = gift_product_config[productId]
            else:
                Context.Log.error('productId not exist', orderId, productId, all_product)
                return MsgPack.Error(0, 1, 'no product found')
        else:
            product = all_product[productId]
        now_ts = Time.current_ts()
        pipe_args = []
        # 记录商品, 排行榜
        if productId in shop_config['activity']:
            if int(productId) == 101111:
                GiftBox1Activity.activity_buy_gift_box_1(uid, gid, productId)
            elif int(productId) == 101112:
                GiftBox2Activity.activity_buy_gift_box_2(uid, gid, productId)
            elif int(productId) == 101113:
                GiftBox3Activity.activity_buy_gift_box_3(uid, gid, productId)
            elif int(productId) == 101114:
                GiftBox4Activity.activity_buy_gift_box_4(uid, gid, productId)
            pipe_args = ['product_%s' % productId, 1]

        elif productId in shop_config['weapon']:  # dz 武器购买成功处理 后期文忠处理
            weaponId = product['weaponid']
            if weaponId > 0:
                weapon_buy_dict = Context.Data.get_game_attr_json(uid, gid, 'weapon_buy_dict')
                weapon_buy_dict[str(weaponId)] = 1
                Context.Data.set_game_attr(uid, gid, 'weapon_buy_dict', Context.json_dumps(weapon_buy_dict))
                Context.Log.report('buyweapon:', [uid, gid, productId, 'buy.product'])
                pipe_args = ['product_%s' % productId, 1]

        elif productId in shop_config['card']:
            if productId == '100808':
                state, days = BirdProps.incr_vip(uid, gid, 30, 'buy.product', orderId=orderId)
                if state == 0:  # 今日未领取
                    success, left_days = BirdProps.use_vip(uid, gid)
                    if success:
                        version = Context.RedisMix.hash_get_int('game.%d.background' % gid, 'month_card.max.version', 0)
                        Context.Data.set_game_attr(uid, gid, 'month_card_version', version)
                        conf = self.get_month_card_reward(uid, gid)
                        final = BirdProps.issue_rewards(uid, gid, conf, 'month.card.reward', True)
                        mon = MsgPack(Message.MSG_SYS_SHOP_REWARD_INFO | Message.ID_REQ)
                        mon.set_param('f', final)
                        Context.GData.send_to_connect(uid, mon)
            else:
                month_id = 0
                if productId == '102001': #黄金月卡
                    month_id = 14
                elif productId == '102002': #至尊月卡
                    month_id = 15
                if month_id > 0:
                    BirdProps.incr_new_month_card(uid, gid, 30, month_id)
                    first_content = product.get('first_content')
                    final = props.BirdProps.issue_rewards(uid, gid, first_content, 'new.month.card' + str(productId), True)
                    Context.Daily.set_daily_data(uid, gid, 'new_month_state_%d' % month_id, 1)
                    mon = MsgPack(Message.MSG_SYS_SHOP_REWARD_INFO | Message.ID_REQ)
                    mon.set_param('f', final)
                    Context.GData.send_to_connect(uid, mon)
        else:
            pipe_args = ['product_%s' % productId, 1]
        times = Context.Data.hincr_game(uid, gid, 'product_%s' % productId, 1)

        # 记录充值相关字段
        Context.Data.set_game_attrs(uid, gid, ['last_pay', 'last_pay_ts'], [cost, now_ts])
        pay_total = BirdProps.incr_pay(uid, gid, cost, 'buy.product', orderId=orderId)
        today_pay_times, _ = Context.Daily.mincr_daily_data(uid, gid, 'pay_times', 1, 'pay_total', cost)
        is_reset_chance, is_first_double = False, False
        if productId in shop_config['chip'] or productId in shop_config['diamond'] :
            if times == 1:
                is_first_double = True
            else:
                reset_choice = Context.Data.get_game_attr_int(uid, gid, 'reset_' + str(productId), 0)
                if reset_choice:
                    is_reset_chance = True

        if is_reset_chance and product.has_key('first') and product.has_key('content'):  # reset chance
            reward = self.__rebate_reward(gid, pay_total, product['content'], channel)
            BirdProps.issue_rewards(uid, gid, reward, 'buy.product', True, orderId=orderId, reset=1)
            final = BirdProps.issue_rewards(uid, gid, product['first'], 'buy.product.extra', True)
            self.deal_recharge_add(uid, gid, reward, payType, final)
            Context.Data.del_game_attrs(uid, gid, 'reset_' + str(productId))
            flag, double = DoubleActivity.get_activity_can_buy(uid, gid, productId)
            final = self.deal_recharge_double(uid, gid, reward, flag, double, final)
            mon = MsgPack(Message.MSG_SYS_SHOP_REWARD_INFO | Message.ID_REQ)
            mon.set_param('f', final)
            Context.GData.send_to_connect(uid, mon)
        elif is_first_double and product.has_key('first') and product.has_key('content'):
            reward = self.__rebate_reward(gid, pay_total, product['content'], channel)
            BirdProps.issue_rewards(uid, gid, reward, 'buy.product', True, orderId=orderId, first=1)
            final = BirdProps.issue_rewards(uid, gid, product['first'], 'buy.product.extra', True)
            self.deal_recharge_add(uid, gid, reward, payType, final)
            flag, double = DoubleActivity.get_activity_can_buy(uid, gid, productId)
            final = self.deal_recharge_double(uid, gid, reward, flag, double, final)
            mon = MsgPack(Message.MSG_SYS_SHOP_REWARD_INFO | Message.ID_REQ)
            mon.set_param('f', final)
            Context.GData.send_to_connect(uid, mon)
        elif product.has_key('content') and productId not in shop_config['card']:
            if productId == '102003':
                first_content = product.get('content')
                final = props.BirdProps.issue_rewards(uid, gid, first_content, 'new.month.card' + str(productId), True)
                mon = MsgPack(Message.MSG_SYS_SHOP_REWARD_INFO | Message.ID_REQ)
                mon.set_param('f', final)
                Context.GData.send_to_connect(uid, mon)
            else:
                reward = self.__rebate_reward(gid, pay_total, product['content'], channel)
                final=BirdProps.issue_rewards(uid, gid, reward, 'buy.product', True, orderId=orderId)
                if productId in shop_config['chip'] or productId in shop_config['diamond']:
                    self.deal_recharge_add(uid, gid, reward, payType, final)
                    flag, double = DoubleActivity.get_activity_can_buy(uid, gid, productId)
                    final = self.deal_recharge_double(uid, gid, reward, flag, double, final)
                mon = MsgPack(Message.MSG_SYS_SHOP_REWARD_INFO | Message.ID_REQ)
                mon.set_param('f', final)
                Context.GData.send_to_connect(uid, mon)

        #if productId in shop_config['chip'] or productId in shop_config['diamond']: #发红包
        #    mon = MsgPack(Message.BIRD_MSG_RED_ENVELOPE | Message.ID_REQ)
        #    chip = 0
        #    if product['content'].has_key('chip'):
        #        chip += product['content']['chip']
        #    elif product['content'].has_key('diamond'):
        #        chip += (product['content']['diamond']*500)
        #    if chip > 100:
        #        mon.set_param('reg', {'chip': chip})
        #        key = 'location:%d:%d' % (gid, uid)
        #        sid = Context.RedisCache.hash_get_int(key, 'serverId', 0)
        #        if sid > 0:
        #            ret, moc = Red_Packet.red_packet(uid, mon)
        #            if ret:
        #                player_list = self.rand_get_table_player_list()
        #                for player_id in player_list:
        #                    Context.GData.send_to_connect(int(player_id), moc)

        if today_pay_times == 1:      # today first pay              # 如果是本日首次充值
            pipe_args.append(channel_id + '.pay.user.count')        # 本日充值用户数+1
            pipe_args.append(1)
        pipe_args.append(channel_id + '.pay.user.pay_total')        # 本日充值总数 + cost
        key = 'user_daily:%s:%s:%s' % (channel_id, Time.current_time('%Y-%m-%d'), str(uid))
        cdkey_pay_total = Context.Data.get_game_attr_int(uid, gid, 'cdkey_pay_total', 0)
        Context.RedisStat.hash_set(key, 'his_pay_total', pay_total - cdkey_pay_total)  # 本日历史充值数据写入
        pipe_args.append(cost)

        if payType == '1':
            pipe_args.append(channel_id + '.weixin_pay.user.pay_total')  # 微信本日充值总数 + cost
            pipe_args.append(cost)
        elif payType == '2':
            pipe_args.append(channel_id + '.ali_pay.user.pay_total')  # 支付宝本日充值总数 + cost
            pipe_args.append(cost)
        elif payType == '3':
            pipe_args.append(channel_id + '.sdk_pay.user.pay_total')  # sdk支付本日充值总数 + cost
            pipe_args.append(cost)
        else:
            pipe_args.append(channel_id + '.gm_pay.user.pay_total')  # gm本日充值总数 + cost
            pipe_args.append(cost)

        pipe_args.append(channel_id + '.user.pay.times')            # 本日充值次数+1
        pipe_args.append(1)
        pipe_args.append(str(payType) + '.pay.user.pay_total')  # 本日充值总数 + cost
        pipe_args.append(cost)
        pipe_args.append(str(payType) + '.user.pay.times')  # 本日充值次数+1
        pipe_args.append(1)

        if pay_total == cost:   # life first pay                    # 玩家首冲
            pipe_args.append(channel_id + '.new.pay.user.count')    # 本日新进充值玩家+1
            pipe_args.append(1)
            #pipe_args.append('new_pay_user')                        # 本日新增付费用户+1
            #pipe_args.append(1)

            Context.Daily.mincr_daily_data(uid, gid, 'new_pay_user', 1)  # 此用户标记为今日新增付费用户

            new_pay_user = 1
        else:
            new_pay_user = Context.Daily.get_daily_data(uid, gid, 'new_pay_user')    # 查询是否是本日新增支付用户

        if new_pay_user:            # 如果是本日新增支付用户
            pipe_args.append(channel_id + '.new.pay.user.pay_total')      # 新增支付用户总充值金额+cost
            pipe_args.append(cost)
            pipe_args.append(channel_id + '.new.pay_user.pay_times')      # 新增用户充值次数+1
            pipe_args.append(1)

        Context.Stat.mincr_daily_data(channel_id, *pipe_args)                    # 本日充值数据写入
        Context.Stat.mincr_daily_user_data(channel_id, uid, *pipe_args)

        Context.Stat.mincr_user_data(uid, gid, *pipe_args)
        key = 'game.%d.info.hash' % gid
        pipe_args = []
        if pay_total == cost:                                              # 如果是首冲
            pipe_args.append(channel_id + '.pay.user.count')               # 本服充值用户+1
            pipe_args.append(1)
            vip_level = BirdAccount.get_vip_level(uid, gid)
            if vip_level > 0:
                Context.Stat.incr_daily_data(channel_id, 'daily.pay.active.player', 1)

        pipe_args.append(channel_id + '.pay.user.pay_total')               # 本服充值总金额+cost
        pipe_args.append(cost)
        pipe_args.append(channel_id + '.user.pay.times')                    # 本服充值次数+1
        pipe_args.append(1)
        pipe_args.append(str(payType) + '.pay.user.pay_total')              # 本服充值总金额+cost
        pipe_args.append(cost)
        pipe_args.append(str(payType) + '.user.pay.times')                  # 本服充值次数+1
        pipe_args.append(1)
        Context.RedisMix.hash_mincrby(key, *pipe_args)                      # 服务器数据写入

        if payType in ['1', '2']:
            self.incr_active_recharge_count(uid, gid, channel_id)

        Context.Data.hincr_rank(101, gid, '%d' % uid, cost)
        PayActivity.pay_set(uid, cost)
        GiveActivity.pay_set(uid, cost)
        ShakeActivity.pay_set(uid, cost)
        TotalPayActivity.pay_set(uid, cost)
        PayRankActivity.incr_user_pay_rank_value(uid, cost)
        PointShopActivity.incr_user_recharge(uid, cost)
        SmashEggActivity.pay_set(uid, cost)

        # 记录用户状态
        Context.UserAttr.set_user_pay_flag(uid, gid, 1, Time.current_ts() + 4 * 24 * 60 * 60)
        loginChannelId = Context.Data.get_attr(uid, 'loginChannelId', '1001_0')
        if (loginChannelId == '1004_0' or loginChannelId == '1005_0' or loginChannelId == '1003_0' \
                or loginChannelId == '1007_0' or loginChannelId == '1007_2' or loginChannelId == '1008_0') \
                and channel != 'gm':
            Context.Data.set_attr(uid, 'pay_channel_flag', "forbit")
        return MsgPack(0, {'msg': u'已到货'})

    def incr_active_recharge_count(self, uid, gid, channel_id):
        recharge_time_slot = Context.Data.get_game_attr_int(uid, gid, 'recharge_time_slot', 0)
        ts = Time.current_ts()
        if recharge_time_slot == 0:
            hour = time.localtime(ts).tm_hour
            if hour == 0:
                hour = 24
            ftm = Time.current_time('%Y-%m-%d')
            Context.RedisStat.hash_incrby('statistics:%s:%s:%s' % (channel_id, ftm, 'pay_count'), hour, 1)
            Context.Data.set_game_attr(uid, gid, 'recharge_time_slot', ts)
        else:
            tm1 = time.localtime(ts)
            tm2 = time.localtime(recharge_time_slot)
            if tm1.tm_yday == tm2.tm_yday and tm1.tm_hour == tm2.tm_hour:
                return
            else:
                ftm = Time.current_time('%Y-%m-%d')
                hour = tm1.tm_hour
                if hour == 0:
                    hour = 24
                Context.RedisStat.hash_incrby('statistics:%s:%s:%s' % (channel_id, ftm, 'pay_count'), hour, 1)
                Context.Data.set_game_attr(uid, gid, 'recharge_time_slot', ts)
        return


    def rand_get_table_player_list(self):
        ret = Context.RedisCache.hget_keys('table:2:*')
        roomkey = []
        for i in ret:
            dat = Context.RedisCache.hash_getall(i)
            roomtype = Tool.to_int(dat.get('room_type'))
            seat0 = Tool.to_int(dat.get('seat0'))
            seat1 = Tool.to_int(dat.get('seat1'))
            seat2 = Tool.to_int(dat.get('seat2'))
            seat3 = Tool.to_int(dat.get('seat3'))
            if roomtype in [201,202,203,209] and (seat0 > 1000000 or seat1 > 1000000 or seat2 > 1000000 or seat3 > 1000000):
                roomkey.append(i)

        if len(roomkey) > 5:
            roomkey = random.sample(roomkey, 5)
        player_list = []
        for j in roomkey:
            seat0, seat1, seat2, seat3 = Context.RedisCache.hash_mget(j, 'seat0', 'seat1', 'seat2', 'seat3')
            seat0 = Tool.to_int(seat0)
            seat1 = Tool.to_int(seat1)
            seat2 = Tool.to_int(seat2)
            seat3 = Tool.to_int(seat3)
            if seat0 > 1000000:
                player_list.append(seat0)
            if seat1 > 1000000:
                player_list.append(seat1)
            if seat2 > 1000000:
                player_list.append(seat2)
            if seat3 > 1000000:
                player_list.append(seat3)
        return player_list


    def deal_recharge_add(self, uid, gid, reward, payType, final):
        add_dict = self.get_recharge_add_config(uid, gid)
        ret = final
        if payType == '1':
            percent = add_dict.get('weixin', 0)
            if float(percent) > 0.0:
                _reward = BirdProps.reward_doubling(reward, percent)
                ret = BirdProps.issue_rewards(uid, gid, _reward, 'buy.product.recharge_add')
        elif payType == '2':
            percent = add_dict.get('zhifubao', 0)
            if float(percent) > 0.0:
                _reward = BirdProps.reward_doubling(reward, percent)
                ret = BirdProps.issue_rewards(uid, gid, _reward, 'buy.product.recharge_add')
        return ret

    def deal_recharge_double(self, uid, gid, reward, flag, double, final):
        ret = final
        if flag:
            mou = MsgPack(Message.MSG_SYS_UPDATE_ACTIVITY_CONF | Message.ID_ACK)
            mou.set_param('model', 8)
            Context.GData.broadcast_to_system(mou)
            if double > 0:
                _reward = BirdProps.reward_doubling(reward, float(double))
                ret = BirdProps.issue_rewards(uid, gid, _reward, 'buy.product.recharge_double')
        return ret

    def __rebate_reward(self, gid, pay_total, reward, channel):
        reward = Context.copy_json_obj(reward)
        if 'chip' in reward:
            vip_config = Context.Configure.get_game_item_json(gid, 'vip.config')
            if vip_config:
                for item in reversed(vip_config):
                    if pay_total > item['pay'] and 'rebate' in item:
                        rebate = item['rebate']
                        reward['chip'] += int(reward['chip'] * rebate)
                        break

        #if channel in ('weixin', 'alipay'):
        #    if 'chip' in reward:
        #        reward['chip'] += int(reward['chip'] * 0.2)
        #    if 'diamond' in reward:
        #        reward['diamond'] += int(reward['diamond'] * 0.2)

        return reward

    @classmethod
    def get_barrel_multi(self, gid, level):
        conf = Context.Configure.get_game_item_json(gid, 'barrel.unlock.config')
        return conf[level - 1]['multiple']

    def on_up_barrel(self, uid, gid, mi):
        # 强化万倍炮
        # up type 1 石头 2 精华
        ret = 0
        mo = MsgPack(Message.MSG_SYS_UP_BARREL | Message.ID_ACK)
        up_type = mi.get_param('up_ty')
        conf = Context.Configure.get_game_item_json(gid, 'barrel.unlock.config')
        if not conf:
            return mo.set_error(1, 'system error')

        next_level = Context.Data.get_game_attr_int(uid, gid, 'barrel_level', 1) + 1
        # if next_level > len(conf):
        strong_conf = Context.Configure.get_game_item_json(gid, 'barrel.unlock.strong')
        if next_level < strong_conf[0] or next_level > strong_conf[1]:
            return mo.set_error(2, 'level error')
        level_conf = conf[next_level - 1]

        diamond_count = level_conf['diamond']
        real, final = Context.UserAttr.incr_diamond(uid, gid, -diamond_count, 'up.barrel')
        if real != -diamond_count:
            return mo.set_error(3, 'lack diamond')
        NewTask.get_diamond_consume_task(uid, diamond_count)
        if up_type == 1:
            count = -level_conf['stone']
            if not BirdProps.mincr_props(uid, gid, 'on_up_barrel', 215, count,
                                         216, count, 217, count, 218, count):
                Context.UserAttr.incr_diamond(uid, gid, diamond_count,
                                              'up.barrel.error')
                return mo.set_error(3, 'lack stone')
            res, gem = self.do_up_barrel(level_conf)
            if res:
                ret = self.up_barrel_led(uid, gid, next_level)
            else:
                BirdProps.mincr_props(uid, gid, 'on_up_barrel.fail_reurn', 219, gem)
                mo.set_param('num', gem)
        elif up_type == 2:
            count = -level_conf['stone']
            count_gem = -level_conf['gem']
            if not BirdProps.mincr_props(uid, gid, 'on_up_barrel', 215, count,
                                         216, count, 217, count, 218, count,
                                         219, count_gem):
                Context.UserAttr.incr_diamond(uid, gid, diamond_count,
                                              'up.barrel.error')
                return mo.set_error(3, 'lack item')
            ret = self.up_barrel_led(uid, gid, next_level)
        else:
            return mo.set_error(4, 'type error')

        Context.GData.send_to_connect(uid, mo)
        return ret

    def up_barrel_led(self, uid, gid, next_level):
        Context.Data.set_game_attr(uid, gid, 'barrel_level', next_level)
        conf = Tool.to_int(Context.Configure.get_game_item_json(gid, 'barrel.unlock.led'), 33)
        if next_level > int(conf):
            bulletin = 3
            barrel_multi = self.get_barrel_multi(gid, next_level)
            nick = Context.Data.get_attr(uid, 'nick')
            nick = Context.hide_name(nick)
            led = u'玩家<color=#00FF00FF>%s</color>成功强化到<color=#FFFF00FF>%d</color>倍的炮倍，战斗力立马爆表！' % (nick, barrel_multi)
            mou = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
            mou.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
            Context.GData.broadcast_to_system(mou)
        return next_level

    def do_up_barrel(self, conf):
        if random.random() <= conf['ratio']:
            return 1, 0
        else:
            return 0, random.randint(conf['fail_gem'][0], conf['fail_gem'][1])

    def on_resolve_stone(self, uid, gid, mi):
        # 分解强化石
        mo = MsgPack(Message.MSG_SYS_RESOLVE_STONE | Message.ID_ACK)

        stone_id = mi.get_param('id')
        double = mi.get_param('dle', 1)
        if stone_id not in [215, 216, 217, 218]:
            return mo.set_error(1, 'id error')
        conf = BirdProps.get_config_by_id(gid, stone_id)
        count = -(conf['count']*double)
        if not BirdProps.mincr_props(uid, gid, 'on_resolve_stone', stone_id, count):
            return mo.set_error(2, 'lack stone')
        gem_count = random.randint(conf['resolve'][0], conf['resolve'][1])
        BirdProps.mincr_props(uid, gid, 'on_resolve_stone', 219, gem_count*int(double))
        mo.set_param('num', gem_count)
        mo.set_param('dle', double)
        return mo

    def switch_info(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_SWITCH_INFO | Message.ID_ACK)
        conf = Context.Configure.get_game_item_json(gid, 'switch.config')
        mo.set_param('is_review', 0)
        mo.set_param('pay_type', 0)
        mo.set_param('more_game', 1)

        kvs = Context.Data.get_game_attrs_dict(uid, gid, ['session_ver', 'session_channel'])
        version = kvs['session_ver']
        channel = kvs['session_channel']
        if channel == 'appstore':
            mo.set_param('pay_type', 1)
        for _conf in conf:
            if 'version' in _conf and Upgrade.cmp_version(version, _conf['version']) != 0:
                continue
            if 'channel' in _conf and channel != _conf['channel']:
                continue

            if 'is_review' in _conf:
                mo.set_param('is_review', _conf['is_review'])
            if 'pay_type' in _conf:
                mo.set_param('pay_type', _conf['pay_type'])
            if 'more_game' in _conf:
                mo.set_param('more_game', _conf['more_game'])

        return mo

    # def on_award_list(self, uid, gid, mi):
    #     _list = mi.get_param('list')
    #     mo = MsgPack(Message.MSG_SYS_AWARD_LIST | Message.ID_ACK)
    #     if 'match' in _list:
    #         match = BirdMatch.get_award_list(uid, gid)
    #         if match:
    #             mo.set_param('match', match)
    #     return mo

    # def on_consume_award(self, uid, gid, mi):
    #     aid = mi.get_param('id')
    #     return BirdMatch.consume_award(uid, gid, aid, mi)

    def update_shop_info(self, uid, gid, mi):
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
            # if flag:
            #     mo = MsgPack(Message.MSG_SYS_CONFIG | Message.ID_ACK)
            #     conf = Shop.get_limit_shop_info(uid, gid, 1)
            #     mo.set_param('limit_shop', conf)
            #     Context.GData.broadcast_to_system(mo)
        else:
            Context.RedisConfig.hash_set("configitem", "game:2:exchange.config", Context.json_dumps(update_config))
        return MsgPack(0)

    def update_match_info(self, uid, gid, mi):
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
        if open == 0:
            BirdMatch.deal_match_end_cache(gid)

        mo = MsgPack(Message.MSG_SYS_CONFIG | Message.ID_ACK)
        conf = BirdMatch.get_config(gid)
        mo.set_param('match', conf)
        Context.GData.broadcast_to_system(mo)

        return MsgPack(0)

    def shop_switch(self, uid, gid, mi):
        start_time = int(mi.get_param('start_time'))
        end_time = int(mi.get_param('end_time'))
        limit_time = Context.Configure.get_game_item_json(gid, 'limit.time.config')
        if not limit_time:
            return MsgPack.Error(0, 2, 'not config')

        limit_time[0] = start_time
        limit_time[1] = end_time
        Context.RedisConfig.hash_set("configitem", "game:2:limit.time.config", limit_time)
        return MsgPack(0)

    def alter_chip_trigger_give(self, uid, gid, mi):
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
        Context.RedisConfig.hash_set("configitem", "game:2:barrel_pool_play_gift.config",Context.json_dumps(barrel_pool_config))

        Context.RedisConfig.hash_set('configitem', 'update.time', Time.current_ts())
        Context.Configure.reload()

        return MsgPack(0)

    def gm_send_red_packet(self, uid, gid, mi):
        now = mi.get_param('now')
        Red_Packet.special_packets(uid=uid, now=now,red_type=True)


    def on_broadcast_timer(self, gid):
        broadcast_keys = Context.RedisCache.hget_keys('notice:%d:*'%gid)
        if not broadcast_keys or len(broadcast_keys) <= 0:
            return
        for i in broadcast_keys:
            start_ts, end_ts, interval, bulletin, led = Context.RedisCache.hash_mget(i,
                                                'start', 'end', 'interval', 'bulletin', 'led')
            current_ts = Time.current_ts()
            start_ts = Tool.to_int(start_ts)
            end_ts = Tool.to_int(end_ts)
            interval = Tool.to_int(interval)
            bulletin = Tool.to_int(bulletin)
            if current_ts < start_ts - 5:
                continue
            if current_ts > end_ts + 5:
                if current_ts > end_ts + 30*24*3600:
                    Context.RedisCache.delete(i) # 要不要删看策划
                continue
            if (interval == 0 and current_ts > start_ts - 5 and current_ts < start_ts + 5) or \
                    (interval != 0 and (current_ts - start_ts) % interval < 5):
                mo = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
                mo.set_param('game', {'msg': led, 'ts': current_ts, 'bulletin': bulletin})
                Context.GData.broadcast_to_system(mo)
        return

    def update_picture(self, uid, gid, mi):
        version = mi.get_param('v')
        mo = MsgPack(Message.MSG_SYS_UPDATE_PICTURE | Message.ID_ACK)
        # max_picture_version = Context.RedisMix.hash_incrby('picture:version_num', 'max_picture_version', 1)
        # dat = {'pn': picture_name, 'pu': picture_url}
        # Context.RedisMix.hash_set('picture:version_record', max_picture_version, Context.json_dumps(dat))
        max_picture_version = Context.RedisMix.hash_get_int('picture:version_num', 'max_picture_version', 0)
        mo.set_param('max', max_picture_version)
        update = []
        if max_picture_version <= version:
            mo.set_param('update', update)
            return mo
        tmp = {}
        while max_picture_version >= version:
            dat = Context.RedisMix.hash_get_json('picture:version_record', max_picture_version, {})
            if dat and dat.has_key('pu') and dat.has_key('pn'):
                pn = dat['pn']
                pu = dat['pu']
                if not tmp.has_key(pn):
                    tmp[pn] = pu
                    update.append({'pu':pu, 'pn':pn})
            max_picture_version = max_picture_version-1
        mo.set_param('update', update)
        return mo

    def get_game_open(self, uid, gid, mi):
        sid = mi.get_param('sid')
        mo = MsgPack(Message.MSG_SYS_GET_GAME_OPEN | Message.ID_ACK)
        if sid == 1: #靶场
            dat = self.get_target_open_config(gid)
            mo.set_param('sid', sid)
            mo.set_param('ret', dat)
        elif sid == 2:
            dat = self.get_fanfanle_open_config(gid)
            mo.set_param('sid', sid)
            mo.set_param('ret', dat)
        elif sid == 3:
            dat = self.get_rich_man_open_config(gid)
            mo.set_param('sid', sid)
            mo.set_param('ret', dat)
        else:
            MsgPack.Error(0, 2, 'not sid, config')
        return mo

    def get_target_open_config(self, gid):
        dat = Context.RedisMix.hash_get_json('game.%d.background' % gid, 'target.config', {})
        open = 1
        vlm = 0
        vlp = 0
        vlh = 0
        if dat.has_key('open'):
            open = Tool.to_int(dat.get('open'), 1)
        if dat.has_key('vlp'):
            vlp = Tool.to_int(dat.get('vlp'), 0)
        if dat.has_key('vlm'):
            vlm = Tool.to_int(dat.get('vlm'), 0)
        if dat.has_key('vlh'):
            vlh = Tool.to_int(dat.get('vlh'), 0)
        dat = {'open': open, 'vlp': vlp, 'vlm': vlm, 'vlh': vlh}
        return dat

    def get_fanfanle_open_config(self, gid):
        dat = Context.RedisMix.hash_get_json('game.%d.background' % gid, 'fanfanle.config', {})
        open = 1
        vip_limit = 0
        if dat.has_key('open'):
            open = Tool.to_int(dat.get('open'), 1)
        if dat.has_key('vip_limit'):
            vip_limit = Tool.to_int(dat.get('vip_limit'), 1)
        dat = {'open': open, 'vip_limit': vip_limit}
        return dat

    def get_rich_man_open_config(self, gid):
        dat = Context.RedisMix.hash_get_json('game.%d.background' % gid, 'rich_man.config', {})
        open = 1
        vip_limit = 0
        if dat.has_key('open'):
            open = Tool.to_int(dat.get('open'), 1)
        if dat.has_key('vip_limit'):
            vip_limit = Tool.to_int(dat.get('vip_limit'), 1)
        dat = {'open': open, 'vip_limit': vip_limit}
        return dat

    def update_old_activity_config(self, uid, gid, mi):
        aid = mi.get_param('aid')
        if aid == 1:
            pid = mi.get_param('pid')
            if pid == 2:
                ret = mi.get_param('ret')
                Context.RedisConfig.hash_set("configitem", "game:2:activity.pay.config", Context.json_dumps(ret))
                Context.RedisConfig.hash_set('configitem', 'update.time', Time.current_ts())
                Context.Configure.reload()
                mou = MsgPack(Message.MSG_SYS_UPDATE_ACTIVITY_CONF | Message.ID_ACK)
                mou.set_param('model', 1)
                Context.GData.broadcast_to_system(mou)
            else:
                return MsgPack.Error(0, 1, 'not exist pid')
        elif aid == 2:
            pid = mi.get_param('pid')
            if pid == 2:
                ret = mi.get_param('ret')
                Context.RedisConfig.hash_set("configitem", "game:2:activity.task.config", Context.json_dumps(ret))
                Context.RedisConfig.hash_set('configitem', 'update.time', Time.current_ts())
                Context.Configure.reload()
                mou = MsgPack(Message.MSG_SYS_UPDATE_ACTIVITY_CONF | Message.ID_ACK)
                mou.set_param('model', 2)
                Context.GData.broadcast_to_system(mou)
            else:
                return MsgPack.Error(0, 2, 'not exist pid')
        elif aid == 3:
            pid = mi.get_param('pid')
            if pid == 2:
                ret = mi.get_param('ret')
                Context.RedisConfig.hash_set("configitem", "game:2:activity.rank.config", Context.json_dumps(ret))
                Context.RedisConfig.hash_set('configitem', 'update.time', Time.current_ts())
                Context.Configure.reload()
                mou = MsgPack(Message.MSG_SYS_UPDATE_ACTIVITY_CONF | Message.ID_ACK)
                mou.set_param('model', 3)
                Context.GData.broadcast_to_system(mou)
            else:
                return MsgPack.Error(0, 3, 'not exist pid')
        elif aid == 4:
            pid = mi.get_param('pid')
            if pid == 2:
                ret = mi.get_param('ret')
                Context.RedisConfig.hash_set("configitem", "game:2:activity.login.config", Context.json_dumps(ret))
                Context.RedisConfig.hash_set('configitem', 'update.time', Time.current_ts())
                Context.Configure.reload()
                mou = MsgPack(Message.MSG_SYS_UPDATE_ACTIVITY_CONF | Message.ID_ACK)
                mou.set_param('model', 4)
                Context.GData.broadcast_to_system(mou)
            else:
                return MsgPack.Error(0, 4, 'not exist pid')
        elif aid == 5:
            pid = mi.get_param('pid')
            if pid == 2:
                ret = mi.get_param('ret')
                Context.RedisConfig.hash_set("configitem", "game:2:activity.share.config", Context.json_dumps(ret))
                Context.RedisConfig.hash_set('configitem', 'update.time', Time.current_ts())
                Context.Configure.reload()
                mou = MsgPack(Message.MSG_SYS_UPDATE_ACTIVITY_CONF | Message.ID_ACK)
                mou.set_param('model', 5)
                Context.GData.broadcast_to_system(mou)
            else:
                return MsgPack.Error(0, 5, 'not exist pid')
        elif aid == 6:
            pid = mi.get_param('pid')
            if pid == 2:
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
                mou = MsgPack(Message.MSG_SYS_UPDATE_ACTIVITY_CONF | Message.ID_ACK)
                mou.set_param('model', 6)
                Context.GData.broadcast_to_system(mou)
            else:
                return MsgPack.Error(0, 6, 'not exist pid')
        elif aid == 7:
            pid = mi.get_param('pid')
            if pid == 2:
                ret = mi.get_param('ret')
                Context.RedisConfig.hash_set("configitem", "game:2:activity.give.config", Context.json_dumps(ret))
                Context.RedisConfig.hash_set('configitem', 'update.time', Time.current_ts())
                Context.Configure.reload()
                mou = MsgPack(Message.MSG_SYS_UPDATE_ACTIVITY_CONF | Message.ID_ACK)
                mou.set_param('model', 7)
                Context.GData.broadcast_to_system(mou)
            else:
                return MsgPack.Error(0, 7, 'not exist pid')
        else:
            return MsgPack.Error(0, 8, 'not exist aid')

    def update_point_shop_config(self, uid, gid, mi):
        cnf = mi.get_param('cnf')
        Context.RedisConfig.hash_set("configitem", "game:2:point.shop.config", Context.json_dumps(cnf))
        Context.RedisConfig.hash_set('configitem', 'update.time', Time.current_ts())
        Context.Configure.reload()
        return

BirdEntity = BirdEntity()
