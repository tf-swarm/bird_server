#!/usr/bin/env python
# -*- coding=utf-8 -*-

import props
from const import Message
from framework.util.tool import Time, Tool
from framework.context import Context
from framework.entity.msgpack import MsgPack


class GiftBoxActivity(object):
    def __init__(self):
        self.gid = 2

    def activity_gift_box_config(self):
        return

    def check_activity_in(self, start, end, show):
        if show:
            return True
        start_ts = self.get_timer(start)
        end_ts = self.get_timer(end)
        now_ts = Time.current_ts()
        if start_ts < now_ts < end_ts:
            return True
        return False

    def judge_gift_box_activity_open(self):
        cnf = self.activity_gift_box_config()
        if not cnf:
            return False
        if not self.check_activity_in(cnf['start'], cnf['end'], 0):
            return False
        return True

    def get_detail(self):
        i = self.activity_gift_box_config()
        start = i['start']
        end = i['end']
        d = {}
        d['id'] = i['id']
        d['t'] = i['model']
        d['s'] = start
        d['e'] = end
        d['n'] = i['name']
        d['d'] = i['desc']
        d['pic'] = i['price']
        d['dic'] = i['discount']
        d['pid'] = i['productId']
        return i, d

    def query_gift_box(self, gid, mi):
        mo = MsgPack(0)
        cnf = self.activity_gift_box_config()
        if cnf == None:cnf = {}
        mo.set_param('ret', cnf)
        return mo

    def get_timer(self, times):
        aid = Time.str_to_timestamp(times)
        return aid


class GiftBox1Activity(GiftBoxActivity):
    def activity_gift_box_config(self):
        gift_box_activity_data = Context.RedisActivity.get('gift_box_1.activity.config')
        if gift_box_activity_data == None:
            gift_box_activity_data = None
        else:
            gift_box_activity_data = Context.json_loads(gift_box_activity_data)
        return gift_box_activity_data

    def get_gift_box_1_activity_config(self, uid, gid):
        if not self.judge_gift_box_activity_open():
            return {}
        i, d = self.get_detail()
        aid = self.get_timer(d.get('s'))
        d['g1'] = i['gift1']
        key = 'activity:%s:%s' % ('gift_box_1', aid)
        qut = Context.RedisActivity.hash_get_json(key, uid)
        if qut:
            d['g1_b'] = 1
        else:
            d['g1_b'] = 0
        return d

    def activity_can_buy(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_ACTIVITY_GIFT_BOX_CAN | Message.ID_ACK)
        if not self.judge_gift_box_activity_open():
            return mo.set_error(u'活动已关闭，无法购买')
        cnf = self.activity_gift_box_config()
        c_list = cnf.get('channel')
        cid = Context.Data.get_attr(uid, 'loginChannelId')
        if cid not in c_list:
            return mo.set_error(u'渠道错误')
        pid = mi.get_param('pid')
        if pid == 1:
            productId = 101111
        else:
            return mo.set_error('not, pid')
        mo.set_param('pid', productId)
        mo.set_param('price', cnf.get('price'))

        aid = self.get_timer(cnf['start'])
        key = 'activity:%s:%s' % ('gift_box_1', aid)
        qut = Context.RedisActivity.hash_get_json(key, uid)
        if qut:
            mo.set_param('ret', 0)
        else:
            mo.set_param('ret', 1)
        return mo

    def activity_buy_gift_box_1(self, uid, gid,  productId):
        conf = self.activity_gift_box_config()
        if int(productId) != 101111:
            return
        # reward = self.deal_spacial_reward(uid, gid, conf['gift1'])
        final_info = props.BirdProps.issue_rewards(uid, self.gid, conf['gift1'], 'activity.buy.gift_box_1', True)
        mon = MsgPack(Message.MSG_SYS_SHOP_REWARD_INFO | Message.ID_REQ)
        mon.set_param('f', final_info)
        Context.GData.send_to_connect(uid, mon)
        aid = self.get_timer(conf['start'])
        key = 'activity:%s:%s' % ('gift_box_1', aid)
        buy_info = {'price': conf['price'], 'rw': conf['gift1']}
        Context.RedisActivity.hash_set(key, uid, Context.json_dumps(buy_info))
        return

    def update_gift_box_1(self, gid, mi):
        modify_cnf = mi.get_param('ret')

        if self.judge_gift_box_activity_open():
            cnf = self.activity_gift_box_config()
            if cnf.get('start') != cnf.get('start'):
                return MsgPack.Error(0, 1, u'活动已开启，不可修改时间')

        Context.RedisActivity.set('gift_box_1.activity.config', Context.json_dumps(modify_cnf))
        mou = MsgPack(Message.MSG_SYS_UPDATE_ACTIVITY_CONF | Message.ID_ACK)
        mou.set_param('model', 13)
        Context.GData.broadcast_to_system(mou)
        return MsgPack(0)

class GiftBox2Activity(GiftBoxActivity):
    def activity_gift_box_config(self):
        gift_box_activity_data = Context.RedisActivity.get('gift_box_2.activity.config')
        if gift_box_activity_data == None:
            gift_box_activity_data = None
        else:
            gift_box_activity_data = Context.json_loads(gift_box_activity_data)
        return gift_box_activity_data

    def get_gift_box_2_activity_config(self, uid, gid):
        if not self.judge_gift_box_activity_open():
            return {}
        i, d = self.get_detail()
        d['g2'] = i['gift2']
        aid = self.get_timer(d.get('s'))
        key = 'activity:%s:%s' % ('gift_box_2', aid)
        qut = Context.RedisActivity.hash_get_json(key, uid)
        if qut:
            d['g2_b'] = 1
        else:
            d['g2_b'] = 0
        return d

    def activity_can_buy(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_ACTIVITY_GIFT_BOX_CAN | Message.ID_ACK)
        if not self.judge_gift_box_activity_open():
            return mo.set_error(u'活动已关闭，无法购买')
        cnf = self.activity_gift_box_config()
        c_list = cnf.get('channel')
        cid = Context.Data.get_attr(uid, 'loginChannelId')
        if cid not in c_list:
            return mo.set_error(u'渠道错误')

        pid = mi.get_param('pid')
        if pid == 2:
            productId = 101112
        else:
            return mo.set_error('not, pid')
        mo.set_param('pid', productId)
        mo.set_param('price', cnf.get('price'))

        aid = self.get_timer(cnf['start'])
        key = 'activity:%s:%s' % ('gift_box_2', aid)
        qut = Context.RedisActivity.hash_get_json(key, uid)
        if qut:
            mo.set_param('ret', 0)
        else:
            mo.set_param('ret', 1)
        return mo

    def activity_buy_gift_box_2(self, uid, gid, productId):
        conf = self.activity_gift_box_config()
        if int(productId) != 101112:
            return
        # reward = self.deal_spacial_reward(uid, gid, conf['gift2'])
        final_info = props.BirdProps.issue_rewards(uid, self.gid, conf['gift2'], 'activity.buy.gift_box_2', True)
        mon = MsgPack(Message.MSG_SYS_SHOP_REWARD_INFO | Message.ID_REQ)
        mon.set_param('f', final_info)
        Context.GData.send_to_connect(uid, mon)
        aid = self.get_timer(conf['start'])
        key = 'activity:%s:%s' % ('gift_box_2', aid)
        buy_info = {'price':conf['price'], 'rw':conf['gift2']}
        Context.RedisActivity.hash_set(key, uid, Context.json_dumps(buy_info))
        return

    def update_gift_box_2(self, gid, mi):
        modify_cnf = mi.get_param('ret')

        if self.judge_gift_box_activity_open():
            cnf = self.activity_gift_box_config()
            if cnf.get('start') != cnf.get('start'):
                return MsgPack.Error(0, 1, u'活动已开启，不可修改时间')

        Context.RedisActivity.set('gift_box_2.activity.config', Context.json_dumps(modify_cnf))
        mou = MsgPack(Message.MSG_SYS_UPDATE_ACTIVITY_CONF | Message.ID_ACK)
        mou.set_param('model', 14)
        Context.GData.broadcast_to_system(mou)
        return MsgPack(0)

class GiftBox3Activity(GiftBoxActivity):
    def activity_gift_box_config(self):
        gift_box_activity_data = Context.RedisActivity.get('gift_box_3.activity.config')
        if gift_box_activity_data == None:
            gift_box_activity_data = None
        else:
            gift_box_activity_data = Context.json_loads(gift_box_activity_data)
        return gift_box_activity_data

    def get_gift_box_3_activity_config(self, uid, gid):
        if not self.judge_gift_box_activity_open():
            return {}
        i, d = self.get_detail()
        d['g3'] = i['gift']
        aid = self.get_timer(d.get('s'))
        key = 'activity:%s:%s' % ('gift_box_3', aid)
        qut = Context.RedisActivity.hash_get_json(key, uid)
        if qut:
            d['g3_b'] = 1
        else:
            d['g3_b'] = 0
        return d

    def activity_can_buy(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_ACTIVITY_GIFT_BOX_CAN | Message.ID_ACK)
        if not self.judge_gift_box_activity_open():
            return mo.set_error(u'活动已关闭，无法购买')
        cnf = self.activity_gift_box_config()
        c_list = cnf.get('channel')
        cid = Context.Data.get_attr(uid, 'loginChannelId')
        if cid not in c_list:
            return mo.set_error(u'渠道错误')

        create_day = cnf.get('create_day')
        day = Context.Data.get_uid_create_day(uid)
        if day > create_day:
            return mo.set_error(u'您创建账号已经超过%d天, 无法购买该礼包'%create_day)

        pid = mi.get_param('pid')
        if pid == 3:
            productId = 101113
        else:
            return mo.set_error('not, pid')
        mo.set_param('pid', productId)
        mo.set_param('price', cnf.get('price'))

        aid = self.get_timer(cnf['start'])
        key = 'activity:%s:%s' % ('gift_box_3', aid)
        qut = Context.RedisActivity.hash_get_json(key, uid)
        if qut:
            mo.set_param('ret', 0)
        else:
            mo.set_param('ret', 1)
        return mo

    def activity_buy_gift_box_3(self, uid, gid, productId):
        conf = self.activity_gift_box_config()
        if int(productId) != 101113:
            return
        # reward = self.deal_spacial_reward(uid, gid, conf['gift'])
        final_info = props.BirdProps.issue_rewards(uid, self.gid, conf['gift'], 'activity.buy.gift_box_3', True)
        mon = MsgPack(Message.MSG_SYS_SHOP_REWARD_INFO | Message.ID_REQ)
        mon.set_param('f', final_info)
        Context.GData.send_to_connect(uid, mon)
        aid = self.get_timer(conf['start'])
        key = 'activity:%s:%s' % ('gift_box_3', aid)
        buy_info = {'price':conf['price'], 'rw':conf['gift']}
        Context.RedisActivity.hash_set(key, uid, Context.json_dumps(buy_info))
        return

    def update_gift_box_3(self, gid, mi):
        modify_cnf = mi.get_param('ret')

        if self.judge_gift_box_activity_open():
            cnf = self.activity_gift_box_config()
            if cnf.get('start') != cnf.get('start'):
                return MsgPack.Error(0, 1, u'活动已开启，不可修改时间')

        Context.RedisActivity.set('gift_box_3.activity.config', Context.json_dumps(modify_cnf))
        mou = MsgPack(Message.MSG_SYS_UPDATE_ACTIVITY_CONF | Message.ID_ACK)
        mou.set_param('model', 17)
        Context.GData.broadcast_to_system(mou)
        return MsgPack(0)

class GiftBox4Activity(GiftBoxActivity):
    def activity_gift_box_config(self):
        gift_box_activity_data = Context.RedisActivity.get('gift_box_4.activity.config')
        if gift_box_activity_data == None:
            gift_box_activity_data = None
        else:
            gift_box_activity_data = Context.json_loads(gift_box_activity_data)
        return gift_box_activity_data

    def get_gift_box_4_activity_config(self, uid, gid):
        if not self.judge_gift_box_activity_open():
            return {}
        i, d = self.get_detail()
        d['g4'] = i['gift']
        aid = self.get_timer(d.get('s'))
        key = 'activity:%s:%s' % ('gift_box_4', aid)
        qut = Context.RedisActivity.hash_get_json(key, uid)
        if qut:
            d['g4_b'] = 1
        else:
            d['g4_b'] = 0
        return d

    def activity_can_buy(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_ACTIVITY_GIFT_BOX_CAN | Message.ID_ACK)
        if not self.judge_gift_box_activity_open():
            return mo.set_error(u'活动已关闭，无法购买')
        cnf = self.activity_gift_box_config()
        c_list = cnf.get('channel')
        cid = Context.Data.get_attr(uid, 'loginChannelId')
        if cid not in c_list:
            return mo.set_error(u'渠道错误')

        vip_limit = cnf.get('vip_limit')
        import account
        vip_level = account.BirdAccount.get_vip_level(uid, 2)
        if vip_level < vip_limit:
            return mo.set_error(u'VIP等级不足，无法领取')

        pid = mi.get_param('pid')
        if pid == 4:
            productId = 101114
        else:
            return mo.set_error('not, pid')
        mo.set_param('pid', productId)
        mo.set_param('price', cnf.get('price'))

        aid = self.get_timer(cnf['start'])
        key = 'activity:%s:%s' % ('gift_box_4', aid)
        qut = Context.RedisActivity.hash_get_json(key, uid)
        if qut:
            mo.set_param('ret', 0)
        else:
            mo.set_param('ret', 1)
        return mo

    def activity_buy_gift_box_4(self, uid, gid, productId):
        conf = self.activity_gift_box_config()
        if int(productId) != 101114:
            return
        # reward = self.deal_spacial_reward(uid, gid, conf['gift'])
        final_info = props.BirdProps.issue_rewards(uid, self.gid, conf['gift'], 'activity.buy.gift_box_4', True)
        mon = MsgPack(Message.MSG_SYS_SHOP_REWARD_INFO | Message.ID_REQ)
        mon.set_param('f', final_info)
        Context.GData.send_to_connect(uid, mon)
        aid = self.get_timer(conf['start'])
        key = 'activity:%s:%s' % ('gift_box_4', aid)
        buy_info = {'price':conf['price'], 'rw':conf['gift']}
        Context.RedisActivity.hash_set(key, uid, Context.json_dumps(buy_info))
        return

    def update_gift_box_4(self, gid, mi):
        modify_cnf = mi.get_param('ret')

        if self.judge_gift_box_activity_open():
            cnf = self.activity_gift_box_config()
            if cnf.get('start') != cnf.get('start'):
                return MsgPack.Error(0, 1, u'活动已开启，不可修改时间')

        Context.RedisActivity.set('gift_box_4.activity.config', Context.json_dumps(modify_cnf))
        mou = MsgPack(Message.MSG_SYS_UPDATE_ACTIVITY_CONF | Message.ID_ACK)
        mou.set_param('model', 18)
        Context.GData.broadcast_to_system(mou)
        return MsgPack(0)

GiftBox1Activity = GiftBox1Activity()
GiftBox2Activity = GiftBox2Activity()
GiftBox3Activity = GiftBox3Activity()
GiftBox4Activity = GiftBox4Activity()