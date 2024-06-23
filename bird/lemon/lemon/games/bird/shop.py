#!/usr/bin/env python
# -*- coding=utf-8 -*-



import time
import json
import sys
from const import Message
from framework.entity.msgpack import MsgPack
from framework.context import Context
from framework.util.tool import Time, Tool
from sdk.modules.mobile import Mobile
import props
from account import BirdAccount
import newtask
from newactivity import *


if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf8')

class Shop(object):

    def get_limit_shop_config(self, uid, gid):
        limit_config = Context.Configure.get_game_item_json(gid, 'limit.shop.config')
        channel_id = Context.Data.get_attr(uid, 'loginChannelId', '1001_0')
        if not limit_config.has_key(channel_id):
            channel_id = '1001_0'
        shop_config = limit_config.get(channel_id)
        return shop_config

    def get_point_shop_config(self, gid):
        limit_config = Context.Configure.get_game_item_json(gid, 'point.shop.config', {})
        return limit_config

    def get_all_channel_list(self, gid):
        channel_list = Context.Configure.get_game_item_json(gid, 'channel.path.config', {})
        channel_id_list = channel_list.keys()
        channel_id_list.append('2')
        return channel_list

    def buy(self, uid, gid, mi):
        nType = mi.get_param('type')
        if nType == 3:#道具商城
            return self.props_shop_buy(uid, gid, mi)
        if nType == 5:#实物商城
            return self.goods_shop_buy(uid, gid, mi)
        if nType == 6:#限时商城
            return self.limit_shop_buy(uid, gid, mi)
        if nType == 7:#积分商城
            return self.point_shop_buy(uid, gid, mi)

    def get_props_shop_info(self, uid, gid):
        props_shop_config = Context.Configure.get_game_item_json(gid, 'props.shop.config')
        if not props_shop_config:
            return {}
        info = []
        for k,v in props_shop_config.items():
            limit = []
            for i in v[5]:
                buy_num = self.get_buy_num(uid, str(k), int(i['type']), int(i['num']), '2')
                limit.append({'buy_limit':int(i['type']), 'limit_num':int(i['num']), 'buy_num':int(buy_num)})
            prop = {
                'id': int(k),
                'name': str(v[0]),
                'goods': props.BirdProps.convert_reward(v[1]),
                'buy_type': int(v[2]),
                'price': int(v[3]),
                'vip_limit': int(v[4]),
                'limit': limit,
                'desc': str(v[6]),
                'pid': str(v[7]),
            }
            info.append(prop)
        return info

    def get_limit_time_info(self, gid):
        limit_time_config = Context.Configure.get_game_item_json(gid, 'limit.time.config')
        return limit_time_config

    def is_in_limit_time(self, gid):
        limit_time_config = Context.Configure.get_game_item_json(gid, 'limit.time.config')
        if isinstance(limit_time_config, list) and len(limit_time_config) >= 2:
            now_ts = Time.datetime()
            if now_ts.hour >= limit_time_config[0] and now_ts.hour < limit_time_config[0]:
                return True
        return False

    def get_target_limit(self, gid, vip):
        vip_config = Context.Configure.get_game_item_json(gid, 'vip.config')
        vip_date = vip_config[vip - 1]
        if vip_date.has_key('target_exchange'):
            return vip_date['target_exchange']
        return 0


    def get_limit_shop_info(self, uid, gid, ntype):
        if ntype == 1:
            shop_config = self.get_limit_shop_config(uid, gid)
        else:
            shop_config = Context.Configure.get_game_item_json(gid, 'exchange.config')
        if not shop_config:
            return {}
        info = []
        vip_level = BirdAccount.get_vip_level(uid, gid)
        for k,v in shop_config.items():
            if int(v[8]) <= 0:
                continue
            limit = []
            vip = int(v[5])
            for i in v[6]:
                if int(k) == 40014 and int(i['type']) == 1:
                    limit_num = 0
                    if vip_level >= vip:
                        double = self.get_target_limit(gid, vip_level)
                        limit_num = double * int(i['num'])
                    channel_id = Context.Data.get_attr(uid, 'loginChannelId', '1001_0')
                    buy_num = self.get_buy_num(uid, str(k), int(i['type']), limit_num, channel_id)
                    limit.append({'buy_limit': int(i['type']), 'limit_num': limit_num, 'buy_num': int(buy_num)})
                else:
                    channel_id = Context.Data.get_attr(uid, 'loginChannelId', '1001_0')
                    buy_num = self.get_buy_num(uid, str(k), int(i['type']), int(i['num']), channel_id)
                    limit.append({'buy_limit': int(i['type']), 'limit_num': int(i['num']), 'buy_num': int(buy_num)})
            prop = {
                'id': int(k),
                'name': str(v[0]),
                'goods_type': int(v[1]),
                'goods': props.BirdProps.convert_reward(v[2]),
                'buy_type': int(v[3]),
                'price': int(v[4]),
                'vip_limit': int(v[5]),
                'limit': limit,
                'desc': str(v[7])}
            info.append(prop)
        return info

    def get_point_shop_info(self, uid, gid):
        shop_config = self.get_point_shop_config(gid)
        if not shop_config:
            return {}
        info = []
        vip_level = BirdAccount.get_vip_level(uid, gid)
        for k,v in shop_config.items():
            if int(v[8]) <= 0:
                continue
            limit = []
            vip = int(v[5])
            for i in v[6]:
                if int(k) == 40014 and int(i['type']) == 1:
                    limit_num = 0
                    if vip_level >= vip:
                        double = self.get_target_limit(gid, vip_level)
                        limit_num = double * int(i['num'])
                    channel_id = Context.Data.get_attr(uid, 'loginChannelId', '1001_0')
                    buy_num = self.get_buy_num(uid, str(k), int(i['type']), limit_num, channel_id)
                    limit.append({'buy_limit': int(i['type']), 'limit_num': limit_num, 'buy_num': int(buy_num)})
                else:
                    channel_id = Context.Data.get_attr(uid, 'loginChannelId', '1001_0')
                    buy_num = self.get_buy_num(uid, str(k), int(i['type']), int(i['num']), channel_id)
                    limit.append({'buy_limit': int(i['type']), 'limit_num': int(i['num']), 'buy_num': int(buy_num)})
            prop = {
                'id': int(k),
                'name': str(v[0]),
                'goods_type': int(v[1]),
                'goods': props.BirdProps.convert_reward(v[2]),
                'buy_type': int(v[3]),
                'price': int(v[4]),
                'vip_limit': int(v[5]),
                'limit': limit,
                'desc': str(v[7])}
            info.append(prop)
        return info

    # 获取玩家限时商城特殊充值额度  # 需要找时间做成通用函数 table get_limit_shop_pay
    def check_limit_shop_pay(self, uid, gid, pid, price):
        limit_pay = Context.UserAttr.get_limit_special_pay(uid, gid, -1)
        limit_cost_pay_config = Context.Configure.get_game_item_json(gid, 'limit_coupon_cost_pay.config')
        if limit_pay == -1:
            data = Context.Data.get_shop_all(uid, 'shop:order')
            limit_pay = 0
            for k, v in data.items():
                record_json = Context.json_loads(v)
                if int(record_json["pid"]) in limit_cost_pay_config['as_pay']:
                    limit_pay += int(record_json['price'])
            Context.UserAttr.incr_limit_special_pay(uid, gid, limit_pay)

        limit_pay = Tool.to_int(limit_pay)
        if int(pid) in limit_cost_pay_config['as_pay']:
            limit_pay += int(price)
            Context.UserAttr.incr_limit_special_pay(uid, gid, int(price))
        Context.Log.debug('获取限时商城消耗', limit_pay)
        return Tool.to_int(limit_pay)

    def limit_shop_buy(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_SHOP_BUY | Message.ID_ACK)
        if self.is_in_limit_time(gid):
            return mo.set_error(6, u'限时商城还没开启')

        limit_shop_conf = self.get_limit_shop_config(uid, gid)
        productId = mi.get_param('productId')
        count = mi.get_param('count', 1)

        if not limit_shop_conf.has_key(str(productId)):
            return mo.set_error(1, u'商城没有此商品')

        #-------------通过oppo转服后 用户还用oppo渠道充值 则不能再转服渠道进行兑换----------------------
        channel_id = Context.Data.get_attr(uid, 'loginChannelId', '1001_0')
        if channel_id == '1004_1' or channel_id == '1005_1' or channel_id == '1003_1' \
                or channel_id == '1007_1' or channel_id == '1008_1':
            pay_channel_flag = Context.Data.get_attr(uid, 'pay_channel_flag')
            if pay_channel_flag == 'forbit':
                return mo.set_error(11, u'使用过非官方支付方式，不能再官方渠道进行兑换')
        # -------------通过oppo转服后 用户还用oppo渠道充值 则不能再转服渠道进行兑换----------------------

        product_info = limit_shop_conf[str(productId)]
        product_name = str(product_info[0])
        product_type = int(product_info[1])
        buy_type = int(product_info[3])
        price = int(product_info[4])
        vip = int(product_info[5])
        buy_limit = product_info[6]

        price = price * count

        vip_level = BirdAccount.get_vip_level(uid, gid)
        if vip_level < vip:
            return mo.set_error(2, u'VIP等级不足，是否前往充值')

        phone = Context.Data.get_shop_attr(uid, 'shop:user', 'phone')
        if not phone:
            return mo.set_error(3, u'请确认*号标记的信息都已完整后，再次提交')

        if self.check_address_info(uid,mi):
            return mo.set_error(10, u'您的地址信息已修改，请重新填写')

        if buy_type == 5: #鸟券兑换
            real, final = Context.UserAttr.incr_coupon(uid, gid, -price, 'limit.shop.buy')
            if real != -price:
                return mo.set_error(4, u'鸟券不足')

            limit_flag = True
            for i in buy_limit:
                limit_type = i.get('type', 0)
                limit_num = i.get('num', 0)
                if limit_num < 0:
                    return mo.set_error(9, u'此商品暂时不允许购买')
                if limit_type > 0 and limit_num > 0:
                    if int(productId) == 40014 and limit_type == 1:
                        double = self.get_target_limit(gid, vip_level)
                        limit_num = double * limit_num
                        ret = self.check_buy_num(uid, str(productId), limit_type, limit_num, count, channel_id)
                    else:
                        ret = self.check_buy_num(uid, str(productId), limit_type, limit_num, count, channel_id)
                    if not ret or ret <= 0:
                        limit_flag = False

            if not limit_flag:
                Context.UserAttr.incr_coupon(uid, gid, price, 'limit.shop.buy')
                return mo.set_error(5, u'兑换失败')
            else:
                for i in buy_limit:
                    limit_type = i.get('type', 0)
                    limit_num = i.get('num', 0)
                    if limit_type > 0 and limit_num > 0:
                        if productId == 40014:
                            double = self.get_target_limit(gid, vip_level)
                            limit_num = double * limit_num
                            self.set_buy_num(uid, str(productId), limit_type, limit_num, count, channel_id)
                        else:
                            self.set_buy_num(uid, str(productId), limit_type, limit_num, count, channel_id)

            mo.set_param('coupon', final)
            nick = Context.Data.get_attr(uid, 'nick')
            nicks = nick.decode('utf-8')
            info = {}
            info['pid'] = productId
            info['uid'] = uid
            info['good_name'] = product_name
            info['price'] = price
            info['nick'] = nicks
            info['shop'] = 6 #限时商城
            info['good_type'] = product_type
            info['pay_channel'] = channel_id
            if product_type == 3:
                info['stat'] = 2
                #Context.Log.debug('xxxx111')
                self.check_limit_shop_pay(uid, gid, productId, price)
            else:
                info['stat'] = 0  # 0 未审核 1 未发货 2 已发货
            info['count'] = count
            info['times'] = Time.datetime_to_str(Time.datetime(), '%Y-%m-%d')

            times = '{:.3f}'.format(time.time())
            times = times.replace('.', '')
            Context.Data.set_shop_attr(uid,'shop:order',times,Context.json_dumps(info))

            bulletin = 3
            nick = Context.Data.get_attr(uid, 'nick')
            nick = Context.hide_name(nick)
            led = u'<color=#FF0000FF>%s</color>经过不懈努力，终于在限时商城中成功兑换<color=#00FF00FF>%s*%d</color>。' % (nick, product_info[0], count)
            mou = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
            mou.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
            Context.GData.broadcast_to_system(mou)

            record_data = {'st': mi.get_param('type'), 'n': nick, 'pn': product_name, 'c': count}
            self.insert_exchange_record(uid, record_data)

            if product_type == 3:
                rewards = product_info[2]
                rewards = props.BirdProps.reward_doubling(rewards, count)
                final = props.BirdProps.issue_rewards(uid, gid, rewards, 'coupon.exchange', True)
                mo.set_param('rw', final)
            mo.set_param('final', 1)
            return mo

    def point_shop_buy(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_SHOP_BUY | Message.ID_ACK)
        if self.is_in_limit_time(gid):
            return mo.set_error(6, u'限时商城还没开启')

        point_shop_conf = self.get_point_shop_config(gid)
        productId = mi.get_param('productId')
        count = mi.get_param('count', 1)

        if not point_shop_conf.has_key(str(productId)):
            return mo.set_error(1, u'商城没有此商品')

        # #-------------通过oppo转服后 用户还用oppo渠道充值 则不能再转服渠道进行兑换----------------------
        #
        # if channel_id == '1004_1' or channel_id == '1005_1' or channel_id == '1003_1' \
        #         or channel_id == '1007_1' or channel_id == '1008_1':
        #     pay_channel_flag = Context.Data.get_attr(uid, 'pay_channel_flag')
        #     if pay_channel_flag == 'forbit':
        #         return mo.set_error(11, u'使用过非官方支付方式，不能再官方渠道进行兑换')
        # # -------------通过oppo转服后 用户还用oppo渠道充值 则不能再转服渠道进行兑换----------------------

        product_info = point_shop_conf[str(productId)]
        product_name = str(product_info[0])
        product_type = int(product_info[1])
        buy_type = int(product_info[3])
        price = int(product_info[4])
        vip = int(product_info[5])
        buy_limit = product_info[6]

        price = price * count

        vip_level = BirdAccount.get_vip_level(uid, gid)
        if vip_level < vip:
            return mo.set_error(2, u'VIP等级不足，是否前往充值')

        phone = Context.Data.get_shop_attr(uid, 'shop:user', 'phone')
        if not phone:
            return mo.set_error(3, u'请确认*号标记的信息都已完整后，再次提交')

        if self.check_address_info(uid,mi):
            return mo.set_error(10, u'您的地址信息已修改，请重新填写')

        if buy_type == 6: #积分兑换
            channel_id = Context.Data.get_attr(uid, 'loginChannelId', '1001_0')
            from newactivity import PointShopActivity
            point = PointShopActivity.get_point(uid)
            if price > point:
                return mo.set_error(4, u'积分不足')

            limit_flag = True
            for i in buy_limit:
                limit_type = i.get('type', 0)
                limit_num = i.get('num', 0)
                if limit_num < 0:
                    return mo.set_error(9, u'此商品暂时不允许购买')
                if limit_type > 0 and limit_num > 0:
                    if int(productId) == 40014 and limit_type == 1:
                        double = self.get_target_limit(gid, vip_level)
                        limit_num = double * limit_num
                        ret = self.check_buy_num(uid, str(productId), limit_type, limit_num, count, channel_id)
                    else:
                        ret = self.check_buy_num(uid, str(productId), limit_type, limit_num, count, channel_id)
                    if not ret or ret <= 0:
                        limit_flag = False

            if not limit_flag:
                return mo.set_error(5, u'兑换失败')
            else:
                point = PointShopActivity.incr_user_use_point(uid, price)
                for i in buy_limit:
                    limit_type = i.get('type', 0)
                    limit_num = i.get('num', 0)
                    if limit_type > 0 and limit_num > 0:
                        if productId == 40014:
                            double = self.get_target_limit(gid, vip_level)
                            limit_num = double * limit_num
                            self.set_buy_num(uid, str(productId), limit_type, limit_num, count, channel_id)
                        else:
                            self.set_buy_num(uid, str(productId), limit_type, limit_num, count, channel_id)

            mo.set_param('point', point)
            nick = Context.Data.get_attr(uid, 'nick')
            nicks = nick.decode('utf-8')
            activity_key = PointShopActivity.get_key()
            info = {}
            info['pid'] = productId
            info['uid'] = uid
            info['good_name'] = product_name
            info['price'] = price
            info['nick'] = nicks
            info['shop'] = 7 #限时商城
            info['good_type'] = product_type
            info['pay_channel'] = channel_id
            info['ak'] = activity_key
            if product_type == 3:
                info['stat'] = 2
            #     #Context.Log.debug('xxxx111')
            #     self.check_limit_shop_pay(uid, gid, productId, price)
            else:
                info['stat'] = 0  # 0 未审核 1 未发货 2 已发货
            info['count'] = count
            info['times'] = Time.datetime_to_str(Time.datetime(), '%Y-%m-%d')

            times = '{:.3f}'.format(time.time())
            times = times.replace('.', '')
            Context.Data.set_shop_attr(uid,'point_shop:order',times,Context.json_dumps(info))

            bulletin = 3
            nick = Context.Data.get_attr(uid, 'nick')
            nick = Context.hide_name(nick)
            led = u'<color=#FF0000FF>%s</color>经过不懈努力，终于在积分商城中成功兑换<color=#00FF00FF>%s*%d</color>。' % (nick, product_info[0], count)
            mou = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
            mou.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
            Context.GData.broadcast_to_system(mou)

            # record_data = {'st': mi.get_param('type'), 'n': nick, 'pn': product_name, 'c': count}
            # self.insert_exchange_record(uid, record_data)

            if product_type == 3:
                rewards = product_info[2]
                rewards = props.BirdProps.reward_doubling(rewards, count)
                final = props.BirdProps.issue_rewards(uid, gid, rewards, 'activity.point.exchange', True)
                mo.set_param('rw', final)
            mo.set_param('final', 1)
            return mo

    #实物商城的处理逻辑
    def goods_shop_buy(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_SHOP_BUY | Message.ID_ACK)

        goods_shop_conf = Context.Configure.get_game_item_json(gid, 'exchange.config')
        productId = mi.get_param('productId')
        count = mi.get_param('count', 1)

        product_info = goods_shop_conf[str(productId)]

        product_name = str(product_info[0])
        product_type = int(product_info[1])
        buy_type = int(product_info[3])
        price = int(product_info[4])
        vip = int(product_info[5])
        buy_limit = product_info[6]

        price = price*count
        if len(buy_limit) < 0:
            return mo.set_error(9, u'此商品暂时不允许购买')

        vip_level = BirdAccount.get_vip_level(uid, gid)
        if vip_level < vip:
            return mo.set_error(2, u'VIP等级不足，是否前往充值')

        phone = Context.Data.get_shop_attr(uid, 'shop:user', 'phone')
        if not phone:
            return mo.set_error(3, u'请确认*号标记的信息都已完整后，再次提交')

        if self.check_address_info(uid,mi):
            return mo.set_error(10, u'您的地址信息已修改，请重新填写')

        real, final = Context.UserAttr.incr_coupon(uid, gid, -price, 'goods.shop.buy')

        if real != -price :
            return mo.set_error(4, u'鸟券不足')

        limit_flag = True
        for i in buy_limit:
            limit_type = i.get('type', 0)
            limit_num = i.get('num', 0)
            if limit_num < 0:
                return mo.set_error(9, u'此商品暂时不允许购买')
            if limit_type > 0 and limit_num > 0:
                ret = self.check_buy_num(uid, str(productId), limit_type, limit_num, count, '2')
                if not ret or ret <= 0:
                    limit_flag = False

        if not limit_flag:
            Context.UserAttr.incr_coupon(uid, gid, price, 'goods.shop.buy')
            return mo.set_error(5, u'兑换失败')
        else:
            for i in buy_limit:
                limit_type = i.get('type', 0)
                limit_num = i.get('num', 0)
                if limit_type > 0 and limit_num > 0:
                    self.set_buy_num(uid, str(productId), limit_type, limit_num, count, '2')

        mo.set_param('coupon', final)
        nick = Context.Data.get_attr(uid, 'nick')
        nicks = nick.decode('utf-8')
        info = {}
        info['pid'] = productId
        info['uid'] = uid
        info['good_name'] = product_name
        info['price'] = price
        info['nick'] = nicks
        info['shop'] = 5 #实物商城
        info['stat'] = 0  # 0 未审核 1 未发货 2 已发货
        info['good_type'] = product_type
        info['count'] = count
        channel_id = Context.Data.get_attr(uid, 'loginChannelId', '1001_0')
        info['pay_channel'] = channel_id
        info['times'] = Time.datetime_to_str(Time.datetime(), '%Y-%m-%d')

        times = '{:.3f}'.format(time.time())
        times = times.replace('.', '')
        Context.Data.set_shop_attr(uid, 'shop:order', str(times), Context.json_dumps(info))

        bulletin = 3
        nick = Context.Data.get_attr(uid, 'nick')
        nick = Context.hide_name(nick)
        led = u'<color=#FF0000FF>%s</color>。经过不懈努力，终于在商城实物中成功兑换<color=#00FF00FF>%s*%d</color>。'%(nick, product_info[0], count)
        mou = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
        mou.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
        Context.GData.broadcast_to_system(mou)

        record_data = {'st': mi.get_param('type'), 'n': nick, 'pn': product_name, 'c':count}
        self.insert_exchange_record(uid, record_data)

        if product_type == 3:
            rewards = product_info[2]
            rewards = props.BirdProps.reward_doubling(rewards, count)
            final = props.BirdProps.issue_rewards(uid, gid, rewards, 'coupon.exchange', True)
            mo.set_param('rw', final)
        mo.set_param('final', 1)
        return mo

    def props_shop_buy(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_SHOP_BUY | Message.ID_ACK)
        props_shop_conf = Context.Configure.get_game_item_json(gid, 'props.shop.config')
        productId = mi.get_param('productId')
        count = mi.get_param('count', 1)
        if not props_shop_conf.has_key(str(productId)):
            return mo.set_error(1, u'商城没有此商品')
        product_info = props_shop_conf[str(productId)]
        buy_type = int(product_info[2])
        buy_price = int(product_info[3])
        vip_limit = int(product_info[4])
        buy_limit = product_info[5]
        rewards = product_info[1]
        if count >= 2:
            rewards = props.BirdProps.reward_doubling(rewards, count)
            buy_price = buy_price * count
        info = {}

        vip_level = BirdAccount.get_vip_level(uid, gid)
        if vip_level < vip_limit:
            return mo.set_error(2, u'VIP等级不足，是否前往充值')

        if buy_type == 1:
            status = Context.RedisCache.hash_get_int('smart_game:%d' % uid, 'status', 0)
            if status > 0:
                return mo.set_error(0, u"你正在进行第三方小游戏，无法购买此商品")

            real, final = Context.UserAttr.incr_chip(uid, gid, buy_price, 'props.shop.buy' + str(productId))
            if -real != buy_price:
                return mo.set_error(5, u'您的鸟蛋不足，无法购买此商品')
            info['chip'] = final

            limit_flag = True
            for i in buy_limit:
                limit_type = i.get('type', 0)
                limit_num = i.get('num', 0)
                if limit_num < 0:
                    return mo.set_error(9, u'此商品暂时不允许购买')
                if limit_type > 0 and limit_num > 0:
                    ret = self.check_buy_num(uid, str(productId), limit_type, limit_num, count, '2')
                    if not ret or ret <= 0:
                        limit_flag = False

            if not limit_flag:
                Context.UserAttr.incr_chip(uid, gid, buy_price, 'props.shop.buy' + str(productId))
                return mo.set_error(5, u'兑换失败')
            else:
                for i in buy_limit:
                    limit_type = i.get('type', 0)
                    limit_num = i.get('num', 0)
                    if limit_type > 0 and limit_num > 0:
                        self.set_buy_num(uid, str(productId), limit_type, limit_num, count, '2')
            event = 'chip.exchange'

        elif buy_type == 2:
            status = Context.RedisCache.hash_get_int('smart_game:%d' % uid, 'status', 0)
            if status > 0:
                return mo.set_error(0, u"你正在进行第三方小游戏，无法购买此商品")

            real, final = Context.UserAttr.incr_diamond(uid, gid, -buy_price, 'props.shop.buy' + str(productId))
            if -real != buy_price:
                return mo.set_error(8, u'您的钻石不足，请前往钻石商城购买')
            info['diamond'] = final

            limit_flag = True
            for i in buy_limit:
                limit_type = i.get('type', 0)
                limit_num = i.get('num', 0)
                if limit_num < 0:
                    return mo.set_error(9, u'此商品暂时不允许购买')
                if limit_type > 0 and limit_num > 0:
                    ret = self.check_buy_num(uid, str(productId), limit_type, limit_num, count, '2')
                    if not ret or ret <= 0:
                        limit_flag = False
            event = 'diamond.exchange'

            if not limit_flag:
                Context.UserAttr.incr_diamond(uid, gid, buy_price, 'props.shop.buy' + str(productId))
                return mo.set_error(5, u'兑换失败')
            else:
                newtask.NewTask.get_diamond_consume_task(uid, buy_price)
                for i in buy_limit:
                    limit_type = i.get('type', 0)
                    limit_num = i.get('num', 0)
                    if limit_type > 0 and limit_num > 0:
                        self.set_buy_num(uid, str(productId), limit_type, limit_num, count, '2')

        elif buy_type == 3:
            return mo.set_error(4, u'暂时不支持人民币购买')
        else:
            return mo.set_error(6, u'没有此购买类型')
        final = props.BirdProps.issue_rewards(uid, gid, rewards, event, True)
        mo.set_param('rw', final)
        if len(info) > 0:
            mo.set_param('info',info)
        mo.set_param('final', 1)
        return mo

    def check_address_info(self, uid, mi):
        name = mi.get_param('name', '')
        sex = mi.get_param('sex', 0)
        area = mi.get_param('area', '')
        address = mi.get_param('address', '')
        phone = mi.get_param('phone', '')
        ret = Context.Data.get_shop_all(uid, 'shop:user')
        if isinstance(ret, dict ) and ret.has_key('name') and ret.has_key('sex') and ret.has_key('area') and ret.has_key('address') and ret.has_key('phone'):
            if ret['name'] == name and int(ret['sex']) == int(sex) and ret['area'] == area and ret['address'] == address and ret['phone'] == phone:
                return False
        return True

    #设置兑换实物的个人信息
    def set_user_info(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_SHOP_USER_INFO | Message.ID_ACK)
        name = mi.get_param('name', '')
        sex = mi.get_param('sex', 0)
        area = mi.get_param('area', '')
        address = mi.get_param('address', '')
        phone = mi.get_param('phone', '')
        verify = mi.get_param('verify', '')
        mail = mi.get_param('mail', '')

        if not name or not area or not address or not phone or not verify:
            return mo.set_error(1, u'请确认*号标记的信息都已完整后，再次提交')
        if not Mobile.checkVerifyCode(gid, phone, verify):
            return mo.set_error(2, u'验证码不正确')
        info = {}
        info['name'] = name
        info['sex'] = sex
        info['area'] = area
        info['address'] = address
        info['phone'] = phone
        info['mail'] = mail
        Context.Data.set_shop_attrs_dict(uid, 'shop:user', info)
        mo.set_param('final', 1)
        return mo

    #获取兑换记录列表
    def get_record_info(self, uid, gid):
        mo = MsgPack(Message.MSG_SYS_SHOP_RECORD | Message.ID_ACK)
        ret = Context.Data.get_shop_all(uid, 'shop:order')
        info = []
        for k, v in ret.items():
            v = json.loads(v)

            shop = int(v["shop"])
            pid = str(v["pid"])
            state = int(v["stat"])
            count = int(v.get('count', 0))
            good_type = int(v["good_type"])
            name = ''
            if shop == 6:#限时商城
                limit_shop_conf = self.get_limit_shop_config(uid, gid)
                if not limit_shop_conf.has_key(pid):
                    continue
                name = limit_shop_conf[pid][0]
            elif shop == 5:#实物商城
                limit_shop_conf = Context.Configure.get_game_item_json(gid, 'exchange.config')
                if not limit_shop_conf.has_key(pid):
                    continue
                name = limit_shop_conf[pid][0]
          
            record = {
                'orderid': k,
                'times': v['times'],
                'state': state,
                'num': count,
                'name': name,
                'good_type':good_type,
            }
            if state == 2 and good_type != 3:
                record.update({'order_number': v["order_number"]})
            info.append(record)
        if len(info) > 0:
            mo.set_param('order', info)
        return mo

    # 获取兑换记录列表
    def get_point_shop_record_info(self, uid, gid):
        mo = MsgPack(Message.MSG_SYS_GET_POINT_SHOP_EXCHANGE | Message.ID_ACK)
        ret = Context.Data.get_shop_all(uid, 'point_shop:order')
        info = []
        for k, v in ret.items():
            v = json.loads(v)

            shop = int(v["shop"])
            pid = str(v["pid"])
            state = int(v["stat"])
            count = int(v.get('count', 0))
            good_type = int(v["good_type"])
            if shop == 7:  # 限时商城
                point_shop_conf = self.get_point_shop_config(gid)
                if not point_shop_conf.has_key(pid):
                    continue
                name = point_shop_conf[pid][0]
            else:
                continue

            record = {
                'orderid': k,
                'times': v['times'],
                'state': state,
                'num': count,
                'name': name,
                'good_type': good_type,
            }
            if state == 2 and good_type != 3:
                record.update({'order_number': v["order_number"]})
            info.append(record)
        if len(info) > 0:
            mo.set_param('order', info)
        return mo

    def set_buy_num(self, uid, product_id, buy_limit, limit_num, buy_num, channel_id):
        if int(buy_limit) == 1:#个人日限制
            info = Context.Data.get_shop_attr_json(10001, 'shop:%s:day'%channel_id, str(uid))
            if info and info.has_key(str(product_id)):
                info[str(product_id)] = int(info[str(product_id)]) + buy_num
            else:
                if info == None:
                    info = {}
                info[str(product_id)] = buy_num
            if not info or limit_num >= info[str(product_id)]:
                Context.Data.set_shop_attr(10001, 'shop:%s:day'%channel_id, str(uid), Context.json_dumps(info))
                return True
            else:
                return False

        elif int(buy_limit) == 2:#全服日限制
            info = Context.Data.get_shop_attr(10002, 'shop:%s:day'%channel_id, str(product_id))
            if info == None and buy_num <= limit_num:
                Context.Data.set_shop_attr(10002, 'shop:day', str(product_id), buy_num)
            elif info and int(info) >= ((buy_num + int(info)) <= limit_num):
                Context.Data.set_shop_attr(10002, 'shop:%s:day'%channel_id, str(product_id), int(info) + buy_num)
                return True
            else:
                return False

        elif int(buy_limit) == 3:#个人周限制
            info = Context.Data.get_shop_attr_json(10001, 'shop:%s:week'%channel_id, str(uid))
            if info and info.has_key(str(product_id)):
                info[str(product_id)] = int(info[str(product_id)]) + buy_num
            else:
                if info == None:
                    info = {}
                info[str(product_id)] = buy_num
            if not info or limit_num >= info[str(product_id)]:
                Context.Data.set_shop_attr(10001, 'shop:%s:week'%channel_id, str(uid), Context.json_dumps(info))
                return True
            else:
                return False

        elif int(buy_limit) == 4:#全服周限制
            info = Context.Data.get_shop_attr(10002, 'shop:%s:week'%channel_id, str(product_id))
            if info == None and buy_num <= limit_num:
                Context.Data.set_shop_attr(10002, 'shop:%s:week'%channel_id, str(product_id), buy_num)
            elif info and int(info) >= ((buy_num + int(info)) <= limit_num):
                Context.Data.set_shop_attr(10002, 'shop:%s:week'%channel_id, str(product_id), int(info) + buy_num)
                return True
            else:
                return False

        elif int(buy_limit) == 5:#个人月限制
            info = Context.Data.get_shop_attr_json(10001, 'shop:%s:month'%channel_id, str(uid))
            if info and info.has_key(str(product_id)):
                info[str(product_id)] = int(info[str(product_id)]) + buy_num
            else:
                if info == None:
                    info = {}
                info[str(product_id)] = buy_num
            if not info or limit_num >= info[str(product_id)]:
                Context.Data.set_shop_attr(10001, 'shop:%s:month'%channel_id, str(uid), Context.json_dumps(info))
                return True
            else:
                return False

        elif int(buy_limit) == 6:#全服月限制
            info = Context.Data.get_shop_attr(10002, 'shop:%s:month'%channel_id, str(product_id))
            if info == None and buy_num <= limit_num:
                Context.Data.set_shop_attr(10002, 'shop:%s:month'%channel_id, str(product_id), buy_num)
            elif info and int(info) >= ((buy_num + int(info)) <= limit_num):
                Context.Data.set_shop_attr(10002, 'shop:%s:month'%channel_id, str(product_id), int(info) + buy_num)
                return True
            else:
                return False

        return False

    #更改购买的限制数量
    def check_buy_num(self, uid, product_id, buy_limit, limit_num, buy_num, channel_id):
        if int(buy_limit) == 1:#个人日限制
            info = Context.Data.get_shop_attr_json(10001, 'shop:%s:day'%channel_id, str(uid))
            if info and info.has_key(str(product_id)):
                info[str(product_id)] = int(info[str(product_id)]) + buy_num
            else:
                info= {}
                info[str(product_id)] = buy_num
            if not info or limit_num >= info[str(product_id)]:
                return True
            else:
                return False

        elif int(buy_limit) == 2:#全服日限制
            info = Context.Data.get_shop_attr(10002, 'shop:%s:day'%channel_id, str(product_id))
            if info == None and buy_num <= limit_num:
                return True
            if info and ((buy_num - int(info)) <= limit_num):
                return True
            else:
                return False

        elif int(buy_limit) == 3:#个人周限制
            info = Context.Data.get_shop_attr_json(10001, 'shop:%s:week'%channel_id, str(uid))
            if info and info.has_key(str(product_id)):
                info[str(product_id)] = int(info[str(product_id)]) + buy_num
            else:
                info = {}
                info[str(product_id)] = buy_num
            if not info or limit_num >= info[str(product_id)]:
                return True
            else:
                return False

        elif int(buy_limit) == 4:#全服周限制
            info = Context.Data.get_shop_attr(10002, 'shop:%s:week'%channel_id, str(product_id))
            if info == None and buy_num <= limit_num:
                return True
            if info and ((buy_num - int(info)) <= limit_num):
                return True
            else:
                return False

        elif int(buy_limit) == 5:#个人月限制
            info = Context.Data.get_shop_attr_json(10001, 'shop:%s:month'%channel_id, str(uid))
            if info and info.has_key(str(product_id)):
                info[str(product_id)] = int(info[str(product_id)]) + buy_num
            else:
                info = {}
                info[str(product_id)] = buy_num
            if not info or limit_num >= info[str(product_id)]:
                return True
            else:
                return False

        elif int(buy_limit) == 6:#全服月限制
            info = Context.Data.get_shop_attr(10002, 'shop:%s:month'%channel_id, str(product_id))
            if info == None and buy_num <= limit_num:
                return True
            if info and ((buy_num + int(info)) <= limit_num):
                return True
            else:
                return False
        return False

    #获取已经购买的数量
    def get_buy_num(self, uid, product_id, buy_limit, limit_num, channel_id):
        if int(buy_limit) == 1:
            info = Context.Data.get_shop_attr_json(10001, 'shop:%s:day'%channel_id, str(uid), {})
            if info and info.has_key(str(product_id)):
                return int(info[str(product_id)])
        elif int(buy_limit) == 2:
            info = Context.Data.get_shop_attr(10002, 'shop:%s:day'%channel_id, str(product_id))
            if info:
                return int(info)
        elif int(buy_limit) == 3:
            info = Context.Data.get_shop_attr_json(10001, 'shop:%s:week'%channel_id, str(uid), {})
            if info and info.has_key(str(product_id)):
                return int(info[str(product_id)])
        elif int(buy_limit) == 4:
            info = Context.Data.get_shop_attr(10002, 'shop:%s:week'%channel_id, str(product_id))
            if info:
                return int(info)
        elif int(buy_limit) == 5:
            info = Context.Data.get_shop_attr_json(10001, 'shop:%s:month'%channel_id, str(uid), {})
            if info and info.has_key(str(product_id)):
                return int(info[str(product_id)])
        elif int(buy_limit) == 6:
            info = Context.Data.get_shop_attr(10002, 'shop:%s:month'%channel_id, str(product_id))
            if info:
                return int(info)
        return 0

    #防止服务器更新时刷新商品的信息的判断函数
    def judge_refresh(self, type, times): #type = 1 日刷新，2周五刷新
        if times == None:
            return False
        if type == 1:
            today = Time.today_start_ts()
            if today > float(times):
                return True
        elif type == 2:
            week = Time.current_week_start_ts()
            if week > float(times):
                return True
        elif type == 3:
            month = Time.current_month_start_ts()
            if month > float(times):
                return False
        return False

    #获取全服刷新列表的更新数据
    # def get_shop_server(self, gid, type):
    #     props_shop_config = Context.Configure.get_game_item_json(gid, 'props.shop.config')
    #     limit_shop_config = limit_shop_conf = self.get_limit_shop_config(uid, gid)
    #     exchange_config = Context.Configure.get_game_item_json(gid, 'exchange.config')
    #     ret = {}
    #     if type == 1:#日刷新
    #         for k, v in props_shop_config.items():
    #             for i in v[5]:
    #                 limit_type = i.get('type', 0)
    #                 limit_num = i.get('num', 0)
    #                 if limit_type > 0 and limit_num > 0:
    #                     if limit_type == 2:#全服控制数量
    #                         ret[k] = limit_num
    #         for k, v in exchange_config.items():
    #             for i in v[6]:
    #                 limit_type = i.get('type', 0)
    #                 limit_num = i.get('num', 0)
    #                 if limit_type > 0 and limit_num > 0:
    #                     if limit_type == 2:#全服控制数量
    #                         ret[k] = limit_num
    #         for k, v in limit_shop_config.items():
    #             for i in v[6]:
    #                 limit_type = i.get('type', 0)
    #                 limit_num = i.get('num', 0)
    #                 if limit_type > 0 and limit_num > 0:
    #                     if limit_type == 2:#全服控制数量
    #                         ret[k] = limit_num
    #     elif type == 2:#z周刷新
    #         for k, v in props_shop_config.items():
    #             for i in v[5]:
    #                 limit_type = i.get('type', 0)
    #                 limit_num = i.get('num', 0)
    #                 if limit_type > 0 and limit_num > 0:
    #                     if limit_type == 4:#全服控制数量
    #                         ret[k] = limit_num
    #         for k, v in exchange_config.items():
    #             for i in v[6]:
    #                 limit_type = i.get('type', 0)
    #                 limit_num = i.get('num', 0)
    #                 if limit_type > 0 and limit_num > 0:
    #                     if limit_type == 4:#全服控制数量
    #                         ret[k] = limit_num
    #         for k, v in limit_shop_config.items():
    #             for i in v[6]:
    #                 limit_type = i.get('type', 0)
    #                 limit_num = i.get('num', 0)
    #                 if limit_type > 0 and limit_num > 0:
    #                     if limit_type == 4:#全服控制数量
    #                         ret[k] = limit_num
    #     elif type == 3:#月刷新
    #         for k, v in props_shop_config.items():
    #             for i in v[5]:#全服控制数量
    #                 limit_type = i.get('type', 0)
    #                 limit_num = i.get('num', 0)
    #                 if limit_type > 0 and limit_num > 0:
    #                     if limit_type == 6:  # 全服控制数量
    #                         ret[k] = limit_num
    #         for k, v in exchange_config.items():
    #             for i in v[6]:
    #                 limit_type = i.get('type', 0)
    #                 limit_num = i.get('num', 0)
    #                 if limit_type > 0 and limit_num > 0:
    #                     if limit_type == 6:#全服控制数量
    #                         ret[k] = limit_num
    #         for k, v in limit_shop_config.items():
    #             for i in v[6]:
    #                 limit_type = i.get('type', 0)
    #                 limit_num = i.get('num', 0)
    #                 if limit_type > 0 and limit_num > 0:
    #                     if limit_type == 6:#全服控制数量
    #                         ret[k] = limit_num
    #     return ret



    # 商城个人日限制数量的刷新
    def refresh_day_person(self, gid):
        channel_list = self.get_all_channel_list(gid)
        for channel_id in channel_list:
            refresh_time = Context.Data.get_shop_attr(10001, 'shop:%s:day'%channel_id, 'refresh_time')
            now_ts = Time.datetime()
            if not refresh_time or (now_ts.hour == 0 and now_ts.minute == 0) or self.judge_refresh(1, refresh_time):
                ret = Context.Data.get_shop_all(10001, 'shop:%s:day'%channel_id)
                for i in ret.keys():
                    Context.Data.del_shop_attrs(10001, 'shop:%s:day'%channel_id, i)
                Context.Data.set_shop_attr(10001, 'shop:%s:day'%channel_id, 'refresh_time', str(time.time()))
        return

    # 商城全服日限制数量的刷新
    def refresh_day_server(self, gid):
        channel_list = self.get_all_channel_list(gid)
        for channel_id in channel_list:
            refresh_time = Context.Data.get_shop_attr(10002, 'shop:%s:day'%channel_id, 'refresh_time')
            now_ts = Time.datetime()
            if not refresh_time or (now_ts.hour == 0 and now_ts.minute == 0 ) or self.judge_refresh(1,refresh_time):
                ret = Context.Data.get_shop_all(10002, 'shop:%s:day'%channel_id)
                for i in ret.keys():
                    Context.Data.del_shop_attrs(10002, 'shop:%s:day'%channel_id, i)
                Context.Data.set_shop_attr(10002, 'shop:%s:day'%channel_id, 'refresh_time', str(time.time()))
            # shop_server_dict = self.get_shop_server(gid, 1)
            # for k, v in shop_server_dict.items():
            #     Context.Data.set_shop_attr(10002, 'shop:day', str(k), v)
        return


    #商城个人周限制数量的刷新
    def refresh_week_person(self, gid):
        channel_list = self.get_all_channel_list(gid)
        for channel_id in channel_list:
            refresh_time = Context.Data.get_shop_attr(10001, 'shop:%s:week'%channel_id, 'refresh_time')
            now_ts = Time.datetime()
            if not refresh_time or (now_ts.weekday() == 0 and now_ts.hour == 0 and now_ts.minute == 0 ) or self.judge_refresh(2, refresh_time):
                ret = Context.Data.get_shop_all(10001, 'shop:%s:week'%channel_id)
                for i in ret.keys():
                    Context.Data.del_shop_attrs(10001, 'shop:%s:week'%channel_id, i)
                Context.Data.set_shop_attr(10001, 'shop:%s:week'%channel_id, 'refresh_time', str(time.time()))
        return

    #商城全服周限制数量的刷新
    def refresh_week_server(self, gid):
        channel_list = self.get_all_channel_list(gid)
        for channel_id in channel_list:
            refresh_time = Context.Data.get_shop_attr(10002, 'shop:%s:week'%channel_id, 'refresh_time')
            now_ts = Time.datetime()
            if not refresh_time or (now_ts.weekday() == 0 and now_ts.hour == 0 and now_ts.minute == 0) or self.judge_refresh(2, refresh_time):
                ret = Context.Data.get_shop_all(10002, 'shop:%s:week'%channel_id)
                for i in ret.keys():
                    Context.Data.del_shop_attrs(10002, 'shop:%s:week'%channel_id, i)
                Context.Data.set_shop_attr(10002, 'shop:%s:week'%channel_id, 'refresh_time', str(time.time()))
            # shop_server_dict = self.get_shop_server(gid, 2)
            # for k, v in shop_server_dict.items():
            #     Context.Data.set_shop_attr(10002, 'shop:week', str(k), v)
        return

    #商城个人月限制数量的刷新
    def refresh_month_person(self, gid):
        channel_list = self.get_all_channel_list(gid)
        for channel_id in channel_list:
            refresh_time = Context.Data.get_shop_attr(10001, 'shop:%s:month'%channel_id, 'refresh_time')
            now_ts = Time.datetime()
            if not refresh_time or (now_ts.day == 1 and now_ts.hour == 0 and now_ts.minute == 0) or self.judge_refresh(3, refresh_time):
                ret = Context.Data.get_shop_all(10001, 'shop:%s:month'%channel_id)
                for i in ret.keys():
                    Context.Data.del_shop_attrs(10001, 'shop:%s:month'%channel_id, i)
                Context.Data.set_shop_attr(10001, 'shop:%s:month'%channel_id, 'refresh_time', str(time.time()))
        return

    #商城全服月限制数量的刷新
    def refresh_month_server(self, gid):
        channel_list = self.get_all_channel_list(gid)
        for channel_id in channel_list:
            refresh_time = Context.Data.get_shop_attr(10002, 'shop:%s:month'%channel_id, 'refresh_time')
            now_ts = Time.datetime()
            if not refresh_time or (now_ts.day == 1 and now_ts.hour == 0 and now_ts.minute == 0) or self.judge_refresh(3, refresh_time):
                ret = Context.Data.get_shop_all(10002, 'shop:%s:month'%channel_id)
                for i in ret.keys():
                    Context.Data.del_shop_attrs(10002, 'shop:%s:month'%channel_id, i)
                Context.Data.set_shop_attr(10002, 'shop:%s:month'%channel_id, 'refresh_time', str(time.time()))
            # shop_server_dict = self.get_shop_server(gid, 3)
            # for k, v in shop_server_dict.items():
            #     Context.Data.set_shop_attr(10002, 'shop:month', str(k), v)
        return

    #用于处理商品限购数量的定时器
    def on_shop_goods_timer(self, gid):
        self.refresh_day_person(gid)
        self.refresh_day_server(gid)
        self.refresh_week_person(gid)
        self.refresh_week_server(gid)
        self.refresh_month_person(gid)
        self.refresh_month_server(gid)
        return

    #用于处理限时商城开启和关闭的定时器
    def on_limit_shop_timer(self, gid, uid = None, background = False):
        conf = self.get_limit_time_info(gid)
        open_time = int(conf[0])
        close_time = int(conf[1])
        now_ts = Time.datetime()
        limit_shop = Context.RedisMix.get('limit.shop.open')
        limit_shop_open = Tool.to_int(limit_shop)
        if not limit_shop_open:
            if now_ts.hour >= open_time and now_ts.hour < close_time:
                if now_ts.hour == open_time and now_ts.minute == 0 and not uid:
                    mo = MsgPack(Message.MSG_SYS_LIMIT_SHOP | Message.ID_NTF)
                    mo.set_param('open', 1)
                    Context.GData.broadcast_to_system(mo)
                    led = u'尊敬的各位玩家，当前<color=#00FF00FF>限时商城</color>已<color=#00FF00FF>开启</color>，一大批奖励正在冲您招手！'
                    self.send_broadcast_to_system(led)
                    return
                elif now_ts.hour >= open_time and now_ts.hour < close_time:
                    mo = MsgPack(Message.MSG_SYS_LIMIT_SHOP | Message.ID_ACK)
                    mo.set_param('open', 1)
                    mo.set_param('s', 3600 * (close_time - now_ts.hour) - now_ts.minute * 60 - now_ts.second)
                    if background:
                        Context.GData.broadcast_to_system(mo)
                        led = u'尊敬的各位玩家，当前<color=#00FF00FF>限时商城</color>已<color=#00FF00FF>开启</color>，一大批奖励正在冲您招手！'
                        self.send_broadcast_to_system(led)
                        return
                    if uid:
                        Context.GData.send_to_connect(uid, mo)
                        return
            if now_ts.hour == close_time and now_ts.minute == 0 and not uid:
                mo = MsgPack(Message.MSG_SYS_LIMIT_SHOP | Message.ID_NTF)
                mo.set_param('open', 2)
                Context.GData.broadcast_to_system(mo)
                led = u'尊敬的各位玩家，当前<color=#00FF00FF>限时商城</color>已<color=#00FF00FF>关闭</color>，如有疑问，请联系客服小妹。'
                self.send_broadcast_to_system(led)
                return
        else:
            mo = MsgPack(Message.MSG_SYS_LIMIT_SHOP | Message.ID_ACK)
            mo.set_param('open', 2)
            if background:
                Context.GData.broadcast_to_system(mo)
                led = u'尊敬的各位玩家，当前<color=#00FF00FF>限时商城</color>因临时维护已被<color=#00FF00FF>关闭</color>，如有疑问，请联系客服小妹。'
                self.send_broadcast_to_system(led)
                return
            if uid:
                Context.GData.send_to_connect(uid, mo)

            return

    def send_broadcast_to_system(self, led):
        bulletin = 3
        mo = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
        mo.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
        Context.GData.broadcast_to_system(mo)
        return

    #获取炮塔的特效信息
    def get_weaponeff_config(self,uid,gid):
        wpshop_config = Context.Configure.get_game_item_json(gid, 'weaponeff.config')
        if not wpshop_config:
            return {}

        info = []
        for k in wpshop_config:
            weapon = {
            'id':int(k['id']),
            'prob':k['prob'],
            'coeff':k['coeff'],
            'addi':k['addi'],
            'desc': k['desc'],
            }
            info.append(weapon)
        return info

    #获取炮塔信息
    def get_weapon_config(self, uid, gid):
        wpshop_config = Context.Configure.get_game_item_json(gid, 'weapon.config')
        if not wpshop_config:
            return {}

        info = []
        for k in wpshop_config:
            weapon = {
            'id':int(k['id']),
            'speed':k['speed'],
            'rebound':k['rebound'],
            'pene':k['pene'],
            'shut': k['shut'],
            'desc': k['desc'],
            }
            info.append(weapon)
        return info

    # 检查是否活动商品，如果是返回True 和 活动商品id
    def check_activity_weapon_shop(self, gid, pid):
        from newactivity import DiscountActivity
        if DiscountActivity.judge_discount_activity_open():
            str_pid = str(pid)
            activity_shop_config = Context.Configure.get_game_item_json(gid, 'activity_shop.config')
            weapon_activity_config = activity_shop_config['weapon']
            for data in weapon_activity_config:
                if data['pid'] == str_pid:
                    return True, data['a_pid']

        return False, 0

    #获取商店信息
    def get_weaponshop_config(self, uid, gid):
        wpshop_config = Context.Configure.get_game_item_json(gid, 'weaponshop.config')
        all_product = Context.Configure.get_game_item_json(gid, 'product.config')
        if not wpshop_config:
            return {}
        info = []
        wp_config = Context.Configure.get_game_item_json(gid, 'weapon.config')
        weapon_buy_dict = self.get_weapon_buy_dict(uid, gid, wpshop_config)
        for k,v in wpshop_config.items():
            eflist = []
            for i in wp_config:
                if int(i['id']) == int(k):
                    eflist.extend(i['pene'])
            buy = int(weapon_buy_dict[str(k)])
            if buy > 1:
                buy -= Time.current_ts()

            w_pid = v[4]
            w_price = str(v[2])
            use_new, new_pid = self.check_activity_weapon_shop(gid, w_pid)
            if use_new:
                product_info = all_product[new_pid]
                w_pid = new_pid
                w_price = product_info['price']

            weapon = {
                'id': int(k),
                'name': v[0],
                'unlock': int(v[1]),
                'price': w_price,
                'special': eflist,
                'buy': buy,
                'pid': w_pid,
                'desc': v[3],
                'p':v[5]}
            info.append(weapon)
        return info


    #获取炮塔购买信息
    def get_weapon_buy_dict(self, uid, gid, wpshop_config):
        weapon_buy_dict = Context.Data.get_game_attr_json(uid, gid, 'weapon_buy_dict')
        w_buy_dict = {}
        if not weapon_buy_dict:
            weapon_buy_dict = {}
        for k,v in weapon_buy_dict.items():
            w_buy_dict[k] = v
        for k, v in wpshop_config.items():
            if not weapon_buy_dict.has_key(str(k)):
                w_buy_dict[str(k)] = 0
            # if int(v[1]) == 4:
            #     vip_level = BirdAccount.get_vip_level(uid, gid)
            #     if vip_level > int(v[2]):
            #         w_buy_dict[str(k)] = 1
        nFlag = True
        for k,v in w_buy_dict.items():
            if v != 0:
                nFlag = False
        if nFlag:
            w_buy_dict[str(20000)] = 1
        Context.Data.set_game_attr(uid, gid, 'weapon_buy_dict', Context.json_dumps(w_buy_dict))
        return w_buy_dict

    #购买炮
    def on_buy_weapon(self, uid, gid, mi):
        _id = mi.get_param('id')
        mo = MsgPack(Message.MSG_SYS_BUY_WEAPON | Message.ID_ACK)
        wpshop_config = Context.Configure.get_game_item_json(gid, 'weaponshop.config')
        if not wpshop_config.has_key(str(_id)):
            return mo.set_error(1, u'没有此类型的炮台')
        info = {}
        info['weapon'] = _id
        weapon_buy_type = wpshop_config[str(_id)][1]
        weapon_buy_price = wpshop_config[str(_id)][2]

        weapon_buy_dict = Context.Data.get_game_attr_json(uid, gid, 'weapon_buy_dict')
        for k, v in weapon_buy_dict.items():
            if int(k) == int(_id):
                if v == 1:
                    return mo.set_error(7, u'您已经购买了此类型的炮台了，无需再次购买')
                break

        if weapon_buy_type == 1:
            status = Context.RedisCache.hash_get_int('smart_game:%d' % uid, 'status', 0)
            if status > 0:
                return mo.set_error(0, u"你正在进行第三方小游戏，无法购买此商品")

            real, final = Context.UserAttr.incr_chip(uid, gid, (-1) * weapon_buy_price, 'chip.buy.weapon')
            if real != -weapon_buy_price:
                return mo.set_error(2, u'您的鸟蛋不足，无法购买此炮台')
            # NewTask.get_chip_task(uid, weapon_buy_price, 'diamond.buy.weapon')
            # final += Context.UserAttr.get_chip(uid, gid, 0)
            info['chip'] = final
        elif weapon_buy_type == 2:
            status = Context.RedisCache.hash_get_int('smart_game:%d' % uid, 'status', 0)
            if status > 0:
                return mo.set_error(0, u"你正在进行第三方小游戏，无法购买此商品")

            real, final = Context.UserAttr.incr_diamond(uid, gid, (-1) * weapon_buy_price, 'diamond.buy.weapon')
            if real != -weapon_buy_price:
                return mo.set_error(3, u'您的钻石不足，无法购买此炮台')
            newtask.NewTask.get_diamond_consume_task(uid, weapon_buy_price)
            info['diamond'] = final
        elif weapon_buy_type == 3:
            return mo.set_error(4, u'暂时不支持人民币购买')
        elif weapon_buy_type == 4:
            vip_level = BirdAccount.get_vip_level(uid, gid)
            if vip_level < weapon_buy_price:
                return mo.set_error(5, u'VIP等级不足，是否前往充值')
        else:
            return mo.set_error(6, u'没有购买此炮台的购买类型')
        info['success'] = 1
        mo.update_param(info)
        weapon_buy_dict[str(_id)] = 1
        Context.Data.set_game_attr(uid, gid, 'weapon_buy_dict', Context.json_dumps(weapon_buy_dict))
        return mo

    # 回收道具
    def recovery_limit_props(self, uid, gid, mi):
        idx= mi.get_param('idx')
        count = int(mi.get_param('count'))
        mo = MsgPack(Message.MSG_SYS_PROPS_RECOVERY | Message.ID_ACK)
        if not isinstance(idx, int):
            return mo.set_error(1, u'道具id错误')
        props_id = int(idx/1000)
        days = int(idx%1000)
        info = {}
        #20000-30000是限时炮
        if props_id > 20000 and props_id <= 30000:
            wpshop_config = Context.Configure.get_game_item_json(gid, 'weaponshop.config')
            if not wpshop_config.has_key(str(props_id)):
                return mo.set_error(2, u'没有此类型的炮台')
            price = wpshop_config[str(props_id)][5]
            real, final = props.BirdProps.incr_props(uid, gid, idx, -count, 'props.recovery')
            if real != -count:
                return mo.set_error(3, u'道具数量不足')
            reward_chip = count * price * days
            real1, final1 = Context.UserAttr.incr_chip(uid, gid, reward_chip, 'props.recovery')

            newtask.NewTask.get_chip_task(uid, count*price*days, 'props.recovery')
            info['props'] = {'id': idx, 'count': final}
            info['chip'] = final1
        if idx == 220:
            real, final = props.BirdProps.incr_props(uid, gid, idx, -count, 'props.recovery')
            if real != -count:
                return mo.set_error(3, u'道具数量不足')

            vip_room_config = Context.Configure.get_game_item_json(gid, 'vip_room.config')
            vip_card_price = Tool.to_int(vip_room_config.get('vip_card_price'))
            real1, final1 = Context.UserAttr.incr_chip(uid, gid, count * vip_card_price, 'props.recovery')

            newtask.NewTask.get_chip_task(uid, count * vip_card_price , 'props.recovery')
            info['props'] = {'id': idx, 'count': final}
            info['chip'] = final1
        mo.set_param('ret', info)
        return mo

    # 使用炮台
    def on_use_weapon(self, uid, gid, mi):
        _id = mi.get_param('id')
        mo = MsgPack(Message.MSG_SYS_USE_WEAPON | Message.ID_ACK)
        weapon_buy_dict = Context.Data.get_game_attr_json(uid, gid, 'weapon_buy_dict')
        for k, v in weapon_buy_dict.items():
            if int(k) == int(_id):
                if int(v) < 1:
                    return mo.set_error(1, u'您还没有购买此炮台，无法使用')
        weapon_use_dict = Context.Data.get_game_attr_int(uid, gid, 'weapon_use_dict', 0)
        if weapon_use_dict == int(_id):
            return mo.set_error(2, u'您已使用此炮台，无法操作')
        Context.Data.set_game_attr(uid, gid, 'weapon_use_dict', _id)
        info = {}
        info['weapon'] = _id
        info['success'] = 1
        mo.update_param(info)
        return mo

    def shop_broadcast_record_list(self, uid, gid):
        mun = MsgPack(Message.MSG_SYS_SHOP_BROADCAST_RECORD_LIST | Message.ID_ACK)
        record = Context.RedisCluster.hash_get_json(uid, "shop:record:list", 'list', [])
        mun.set_param('ret', record)
        return mun

    def insert_exchange_record(self, uid, info):
        record = Context.RedisCluster.hash_get_json(uid, "shop:record:list", 'list', [])
        record.append(info)
        if len(record) > 20:
            record = record[:20]
        Context.RedisCluster.hash_set(uid, "shop:record:list", 'list', Context.json_dumps(record))
        mun = MsgPack(Message.MSG_SYS_SHOP_BROADCAST_RECORD_SINGLE | Message.ID_ACK)
        mun.set_param('ret', info)
        Context.GData.broadcast_to_system(mun)
        return

    def gift_shop_buy(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_SHOP_GIFT_BUY | Message.ID_ACK)
        pid = mi.get_param('pid', 0)
        product_config = Context.RedisActivity.get('gift_shop:product_config')
        if product_config:
            product_config = Context.json_loads(product_config)
        else:
            product_config = {}
        if not product_config.has_key(str(pid)):
            return mo.set_error(1, u'该礼包已被下架，无法购买')
        gift_info = product_config.get(str(pid))

        if not self.judge_gift_time(gift_info):
            return mo.set_error(2, u'礼包已过期，无法购买')
        f, desc = self.judge_gift_vip(uid, gid, gift_info)
        if not f:
            return mo.set_error(3, desc)
        gift_record = Context.RedisActivity.hash_get_json('gift_shop:record:%d'%uid, pid, {})
        version = gift_info.get('version', 1000)
        record_version = gift_record.get('vs', 1000)
        if gift_record:
            if version != record_version:
                gift_record = {}
            else:
                flag = self.get_gift_buy_info(uid, gid, gift_info, gift_record)

                if flag == True:
                    count = gift_record.get('c', 0)
                    if count >= gift_info.get('limit_num'):
                        return mo.set_error(5, u'你已购买完此礼包，无法继续购买')
                else:
                    gift_record = {}

        price = gift_info.get('price')
        if price == 0:
            final = self.on_gift_get_reward(uid, gid, gift_info, gift_record, pid)
            mo.set_param('rw', final)
        mo.set_param('pid', pid)
        mo.set_param('success', 1)
        return mo

    def on_gift_product_deliver(self, uid, gid, pid, product_config):
        if not product_config.has_key(str(pid)):
            return False
        gift_info = product_config.get(str(pid))
        gift_record = Context.RedisActivity.hash_get_json('gift_shop:record:%d' % uid, pid, {})
        self.on_gift_get_reward(uid, gid, gift_info, gift_record, pid)
        return True

    def on_gift_get_reward(self, uid, gid, gift_conf, gift_record, pid):
        reward = gift_conf.get('reward')
        final = props.BirdProps.issue_rewards(uid, gid, reward, 'gift.buy.%d' % pid, True)
        count = gift_record.get('c', 0)
        count += 1
        version = gift_conf.get('version', 0)
        record = {'c': count, 'vs': version, 'ts':Time.current_ts(), 'rw':reward}
        Context.RedisActivity.hash_set('gift_shop:record:%d' % uid, pid, Context.json_dumps(record))
        # mou = MsgPack(Message.MSG_SYS_NOTICE_CLIENT_GIFT_SHOP | Message.ID_ACK)
        # Context.GData.broadcast_to_system(mou)
        return final

    def judge_gift_time(self, gift_info):
        start = gift_info.get('start')
        end = gift_info.get('end')
        start_ts = Time.str_to_timestamp(start)
        end_ts = Time.str_to_timestamp(end)
        ts = Time.current_ts()
        if ts < start_ts or ts > end_ts:
            return False
        return True

    def judge_gift_vip(self, uid, gid, gift_info):
        vip_type = gift_info.get('vip_type')
        vip_level = gift_info.get('vip_level')
        if vip_type != 0 and len(vip_level) >= 1:
            my_vip = BirdAccount.get_vip_level(uid, gid)
            if vip_type == 1 and len(vip_level):
                if my_vip < vip_level[0]:
                    return False, u'VIP等级不足，此礼包需要VIP%d才能购买' % (vip_level[0])
            else:
                if int(my_vip) not in vip_level:
                    vip_str = ','.join(list(map(lambda x: 'vip%d' % x, vip_level)))
                    return False, u'此礼包只有%s才能购买' % (vip_str)
        return True, ''

    def get_gift_config_from_db(self):
        product_config = Context.RedisActivity.get('gift_shop:product_config')
        if product_config:
            product_config = Context.json_loads(product_config)
        else:
            product_config = {}
        return product_config

    def get_gift_buy_info(self, uid, pid, gift_info, gift_record):
        flag = False
        open_type = gift_info.get('open_type')
        rts = gift_record.get('ts')
        if open_type == 1:  # 开放类型为日开放
            rts = Time.timestamp_to_str(rts)
            if Time.is_today(rts):
                flag = True
            else:
                if open_type == 5 and gift_record.get('c') > 0:
                    dat = Context.copy_obj(gift_record)
                    dat['c'] = 0
                    Context.RedisActivity.hash_set('gift_shop:record:%d' % uid, pid, Context.json_dumps(dat))

        elif open_type == 2:  # 开放类型为周开放
            wts = Time.current_week_start_ts()
            local_wts = Time.current_week_start_ts(rts)
            if wts == local_wts:
                flag = True

        elif open_type == 3:
            lts = Time.current_localtime()
            local_wts = Time.current_localtime(rts)
            if lts.tm_year == local_wts.tm_year and lts.tm_mon == local_wts.tm_mon:
                flag = True

        elif open_type == 4:
            flag = True
        return flag

    def get_gift_config(self, uid, gid):
        mo = MsgPack(Message.MSG_SYS_SHOP_GIFT_CONFIG | Message.ID_ACK)
        product_config = self.get_gift_config_from_db()
        info = []
        for pid, gift_info in product_config.items():
            gift_record = Context.RedisActivity.hash_get_json('gift_shop:record:%d' % uid, pid, {})
            version = gift_info.get('version', 1000)
            record_version = gift_record.get('vs', 1000)
            can_buy_flag = True
            if not self.judge_gift_time(gift_info):
                can_buy_flag = False
            if not self.judge_gift_vip(uid, gid, gift_info)[0]:
                can_buy_flag = False
            limit_num = gift_info.get('limit_num')
            if gift_record:
                if version == record_version:
                    flag = self.get_gift_buy_info(uid, pid, gift_info, gift_record)
                    if flag == True:
                        count = gift_record.get('c', 0)
                        if count >= gift_info.get('limit_num'):
                            can_buy_flag = False
                        else:
                            limit_num = gift_info.get('limit_num') - count
            #if not can_buy_flag:
            #    limit_num = 0
            d = {}
            d['id'] = int(pid)
            d['n'] = gift_info.get('name')
            d['h'] = gift_info.get('hot')
            d['i'] = gift_info.get('icon_type')
            d['ln'] = limit_num
            d['d1'] = u"剩余数量：%d"%limit_num
            d['d2'] = gift_info.get('detail_2')
            d['d3'] = gift_info.get('detail_3')
            d['p'] = gift_info.get('price')
            d['w'] = gift_info.get('worth')
            d['rw'] = gift_info.get('reward')
            if can_buy_flag:
                d['cb'] = 1
            else:
                d['cb'] = 0
            info.append(d)
        info = sorted(info, key=lambda x: x['p'], reverse=False)
        mo.set_param('conf', info)
        return mo

    def new_month_card_buy(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_NEW_MONTH_CARD_BUY | Message.ID_ACK)
        pid = mi.get_param('pid', 0)
        if pid == 1:
            product_id = '102001'
            month_id = 14
        else:
            product_id = '102002'
            month_id = 15
        today, create, life, state = props.BirdProps.get_new_month_card_info(uid, gid, month_id)
        if life - today + create >= 1:
            return mo.set_error(5, u'你已购完此月卡，无法继续购买')
        product_config = Context.Configure.get_game_item_json(gid, 'product.config')
        product_info = product_config.get(product_id)
        diamond_price = product_info.get('diamond_price')
        real, final = Context.UserAttr.incr_diamond(uid, gid, -diamond_price, 'new.month.card.buy' + str(product_id))
        if -real != diamond_price:
            mo.set_param('success', 0)
            return mo

        props.BirdProps.incr_new_month_card(uid, gid, 30, month_id)
        first_content = product_info.get('first_content')
        Context.Data.hincr_game(uid, gid, 'product_%s' % product_id, 1)
        Context.Daily.set_daily_data(uid, gid, 'new_month_state_%d' % month_id, 1)
        final = props.BirdProps.issue_rewards(uid, gid, first_content, 'new.month.card'+ str(product_id), True)
        mo.set_param('rw', final)
        mo.set_param('success', 1)
        return mo

Shop = Shop()