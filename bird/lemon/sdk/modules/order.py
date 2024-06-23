#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-16

from sdk.const import Const
from sdk.modules.entity import Entity
from framework.context import Context
from framework.util.tool import Time
from framework.util.tool import Algorithm
from framework.entity.msgpack import MsgPack
from random import Random
from lemon.entity.upgrade import Upgrade
from framework.entity.globals import Global


order_wait = 0   # 订单等待中，等待一段时间再次校验
order_fail = -1   # 订单不存在或者是失败订单
order_success = 1  # 订单成功

class Order(object):
    invalid_product = 1
    invalid_channel = 2
    invalid_order = 3
    unknown_error = 4
    time_error = 5
    already_buy = 6
    appstore_limit = 7
    village_ts = 8
    village_can = 9
    love_max_times = 10
    first_limit = 11

    state_timeout = 0
    state_create = 1
    state_verify_success = 2
    state_verify_failed_id = 3
    state_verify_failed_sign = 4
    state_pre_deliver = 5
    state_deliver_success = 6
    state_deliver_failed = 7

    current_version = 2000   # dz 老版本高兑优化版 id设置为2000

    @classmethod
    def get_new_order_id(cls, appId, dt):
        """
        orderId采用62进制, 16个字符, 由5个字段标记: <1位版本号><3位应用id><3位预留><6位时间戳><3位序列号>
        """
        attr = 'max.order.id.%s' % cls.current_version
        seq_number = Context.RedisMix.hash_incrby('global.info.hash', attr, 1)
        api_ver = Context.Strutil.to_str62(cls.current_version, 1)
        app_id = Context.Strutil.to_str62(appId, 3)
        unused = Context.Strutil.to_str62(0, 3)
        seq_number = Context.Strutil.to_str62(seq_number, 3)
        ts = Context.Strutil.to_str62(int(dt.strftime('%s')), 6)
        return api_ver + app_id + unused + ts + seq_number

    @classmethod
    def get_short_order_id(cls, orderId):
        short_order_id = Context.RedisMix.hash_incrby('global.info.hash', 'max.short.order.id', 1)
        short_order_id = str(100000 + short_order_id)[-6:]
        Context.Log.report('order.map:', short_order_id, orderId)
        Context.RedisMix.hash_set('global.short.order.id.map', short_order_id, orderId)
        return short_order_id

    @classmethod
    def get_order_id(cls, shortOrderId):
        return Context.RedisMix.hash_get('global.short.order.id.map', shortOrderId)

    @classmethod
    def parse_order(cls, orderId):
        if isinstance(orderId, (str, unicode)) and len(orderId) == 16:
            api_ver = Context.Strutil.to_int10(orderId[0:1])
            app_id = Context.Strutil.to_int10(orderId[1:4])
            # unused = Context.Strutil.to_int10(orderId[4:7])
            ts = Context.Strutil.to_int10(orderId[7:13])
            seq_number = Context.Strutil.to_int10(orderId[13:16])
            return {'version': api_ver, 'appId': app_id, 'ts': ts, 'seq': seq_number}

    @classmethod
    def __create_order(cls, uid, gid, channel, productId, **kwargs):
        all_product = Context.Configure.get_game_item_json(gid, 'product.config')
        gift_config = Context.RedisActivity.get('gift_shop:product_config')
        if gift_config:
            gift_config = Context.json_loads(gift_config)
        else:
            gift_config = {}

        if productId not in all_product:
            if not gift_config.has_key(str(productId)):
                return cls.invalid_product, 'invalid productId'
            product = gift_config[productId]
        else:
            product = all_product[productId]

        if 'week' in product and product['week'] != Time.weekday():
            return cls.invalid_product, 'invalid productId'
        shop_config = Context.Configure.get_game_item_json(gid, 'shop.config')
        product_name = product.get('name', '')
        product_content = product.get('content', {})
        product_price = product.get('price', 0)
        if productId in shop_config['first']:
            # 首充只能一次
            first_product = Context.Data.get_game_attr(uid, gid, 'product_%s' % productId)
            if first_product:
                return cls.first_limit, u'已购买过首充礼包，无法再次购买'

        elif productId in shop_config['weapon']:
            product_content['weaponid'] = product.get('weaponid')

        elif productId in shop_config['activity']:
            if int(productId) == 101111:
                from lemon.games.bird.giftactivity import GiftBox1Activity
                cnf = GiftBox1Activity.activity_gift_box_config()
                product_content = cnf.get('gift1', {})
                product_name = cnf.get('name', '')
                product_price = cnf.get('price', 0)
            elif int(productId) == 101112:
                from lemon.games.bird.giftactivity import GiftBox2Activity
                cnf = GiftBox2Activity.activity_gift_box_config()
                product_content = cnf.get('gift2', {})
                product_name = cnf.get('name', '')
                product_price = cnf.get('price', 0)
            elif int(productId) == 101113:
                from lemon.games.bird.giftactivity import GiftBox3Activity
                cnf = GiftBox3Activity.activity_gift_box_config()
                product_content = cnf.get('gift', {})
                product_name = cnf.get('name', '')
                product_price = cnf.get('price', 0)
            elif int(productId) == 101114:
                from lemon.games.bird.giftactivity import GiftBox4Activity
                cnf = GiftBox4Activity.activity_gift_box_config()
                product_content = cnf.get('gift', {})
                product_name = cnf.get('name', '')
                product_price = cnf.get('price', 0)
            else:
                return cls.invalid_product, 'invalid productId'
        elif productId in shop_config['card']:
            if int(productId) == 100808:
                version = Context.RedisMix.hash_get_int('game.%d.background' % gid, 'month_card.max.version', 0)
                if version == 0:
                    card_info = None
                else:
                    card_info = Context.RedisMix.hash_get_json('game:%d:month_card_version' % gid, str(version))
                if card_info:
                    product_price = card_info.get('price', 0)
                    product_content = card_info.get('rw', {})
        elif gift_config.has_key(str(productId)):   # 礼包商城
            gift_info = gift_config.get(str(productId))
            product_content = gift_info.get('reward', {})
            product_name = gift_info.get('name', '')
            product_price = gift_info.get('price', 0)

        dt = Time.datetime()
        order_id = cls.get_new_order_id(gid, dt)
        kvs = {'userId': uid, 'gameId': gid, 'channel': channel, 'productId': productId, 'cost': product_price,
               'state': cls.state_create, 'createTime': Time.datetime_to_str(dt, '%Y-%m-%d %X.%f'), 'context': Context.json_dumps(product_content)}
        kvs.update(kwargs)
        Context.Log.report('order.create: [%d, %d, %s, %s]' % (uid, gid, order_id, kvs))
        Context.RedisPay.hash_mset('order:' + order_id, **kvs)
        Context.RedisStat.list_rpush('order:%d:%d:user' % (gid, uid), order_id)
        Context.RedisStat.list_rpush('order:%d:%s:daily' % (gid, dt.strftime('%Y-%m-%d')), order_id)

        info = {
            'orderId': order_id,
            'productId': productId,
            'title': product_name,
            'desc': '',
            'cost': product_price,
            'price': product_price,
        }
        if channel == 'meizu':
            openid = Context.Data.get_attr(uid, 'openid')
            special_info = cls.meizu_create_order(order_id, productId, openid, product['name'], product_price)
            info['special_info'] = Context.json_dumps(special_info)
        elif channel == 'vivo':
            openid = Context.Data.get_attr(uid, 'openid')
            special_info = cls.vivo_create_order(order_id, productId, openid, product['name'], product_price)
            info['special_info'] = Context.json_dumps(special_info)
        elif channel == 'baidu':
            info['shortOrderId'] = Order.get_short_order_id(order_id)
        elif channel == 'huawei':
            openid = Context.Data.get_attr(uid, 'openid')
            special_info = cls.huawei_create_order(order_id, productId, openid, product['name'], product_price)
            info['special_info'] = special_info

        return 0, info

    @classmethod
    def huawei_create_order(cls, order_id, productId, openid, name, price):
        param = {'userID': Const.HUAWEI_USERID,
                 'applicationID': Const.HUAWEI_APPID,
                 'amount': '%.2f' % price,
                 'productName': name,
                 'requestId': order_id,
                 'productDesc': name,
                 }
        sign = Entity.huawei_get_sign(param)
        return sign

    @classmethod
    def vivo_create_order(cls, order_id, productId, openid, name, price):
        if type(name) == unicode:
            name = name.encode('utf8')
        orderAmount = '%.2f' % float(price)
        data = {
            "version": '1',
            "signMethod": 'MD5',
            "storeId": Const.VIVO_CPID,
            "appId": Const.VIVO_APPID,
            "storeOrder": order_id,
            "notifyUrl": Context.Global.http_sdk() + '/v1/third/callback/vivo/pay',
            "orderTime": str(Time.datetime_now('%Y%m%d%H%M%S')),
            "orderAmount": orderAmount,
            "orderTitle": name,
            "orderDesc": name,
        }
        sign = Entity.vivo_get_sign(data)
        data['signature'] = sign
        res = Context.WebPage.wait_for_json(Const.VIVO_URL, postdata=data)
        param = {
            "respCode": res.get('respCode', ''),
            "respMsg": res.get('respMsg', ''),
            "signMethod": res.get('signMethod', ''),
            "signature": res.get('signature', ''),
            "vivoSignature": res.get('vivoSignature', ''),
            "vivoOrder": res.get('vivoOrder', ''),
            "orderAmount": res.get('orderAmount', ''),
        }
        sign = Entity.vivo_get_sign(param)
        if sign == param['signature']:
            return {"vivoSignature": param['vivoSignature'], "vivoOrder": param['vivoOrder']}
        return {}

    @classmethod
    def meizu_create_order(cls, order_id, productId, openid, name, price):
        # app_id=464013&buy_amount=1&cp_order_id=2680&create_time=139868782768&pay_type=0&product_body= &product_id=0&product_per_price=1.0&product_subject= 购买 500 枚鸟蛋 &product_unit= &total_price=1.0&uid=5535004&user_info=:appSecret
        param = {
            "app_id": Const.MEIZU_APPID,
            "buy_amount": 1,
            "cp_order_id": order_id,
            "create_time": Time.current_ts(),
            "pay_type": 0,
            "product_body": name,
            "product_id": productId,
            "product_per_price": str(float(price)),
            "product_subject": name,
            "product_unit": '',
            "total_price": str(float(price)),
            "uid": openid,
            "user_info": '',
            "sign_type": 'md5',
        }
        sign = Entity.meizu_get_sign(param)
        param['sign'] = sign

        return param

    @classmethod
    def getOrderInfo(cls, orderId, *args):
        if not args:
            return Context.RedisPay.hash_getall('order:' + orderId)
        if len(args) == 1:
            return Context.RedisPay.hash_get('order:' + orderId, args[0])
        else:
            return Context.RedisPay.hash_mget('order:' + orderId, *args)

    def deliver_product(self, userId, gameId, orderId, orderInfo, productId, payType):
        deliver_url = Context.Global.http_game() + '/v1/game/product/deliver'
        param = {
            'userId': userId,
            'gameId': gameId,
            'orderId': orderId,
            'productId': productId,
            'cost': float(orderInfo['cost']),
            'paytype': payType,
            'channel': orderInfo['channel']
        }
        appKey = Context.Configure.get_game_item(gameId, 'appKey', '')
        data = '%s-%s-%s' % (orderId, appKey, productId)
        sign = Algorithm.md5_encode(data)
        param['sign'] = sign
        Context.Log.report('product.deliver: [%d, %d, %s, %s]' % (userId, gameId, orderId, param))
        mo = MsgPack(0, param)
        Context.Log.debug(deliver_url)
        result = Context.WebPage.wait_for_json(deliver_url, postdata=mo.pack(), timeout=60)
        Context.Log.info('========deliver_product===========', result)
        return 'error' not in result

    def orderquery(self, orderId, payType, channelid = '0', token=''):
        if channelid == '1000_0':
            if '192.168.0.' in Global.local_ip():
                return order_success
            else:
                return order_fail
        if payType == '1':        # 微信
            from sdk.third import weixin
            return weixin.orderquery(orderId)
        elif payType == '2':
            from sdk.third import ali
            return ali.orderquery(orderId)
        elif payType == '3':
            if channelid in ['1007_0', '1007_2']:
                from sdk.third import vivo
                return vivo.orderquery(orderId)
            elif channelid == '1100_0': # apple pay
                from sdk.third import applepay
                return applepay.orderquery(orderId, token)
            elif channelid == '1008_0':
                return order_wait
            else:
                Context.Log.debug('sdk pay query')
            return order_wait

        return 0

    @classmethod
    def updateOrder(cls, orderId, **kwargs):
        return Context.RedisPay.hash_mset('order:' + orderId, **kwargs)

    def otherCreateOrder(self, gameId, userId, productId, channel, platform):
        #if productId == '100808':
        #    return MsgPack.Error(0, self.invalid_product, 'invalid productId')

        code, desc = self.__create_order(userId, gameId, channel, productId, platform=platform)
        if code != 0:
            Context.Log.debug('-------, otherCreateOrder:', code)
            return MsgPack.Error(0, code, desc)
        return MsgPack(0, desc)

    def createOrder(self, mi, request):
        gameId = mi.get_param('gameId')
        channel = mi.get_param('channel', Global.channel_name)
        platform = mi.get_param('platform', 'android')
        productId = mi.get_param('productId')

        if not Entity.logined(request):
            return MsgPack.Error(0, Const.E_NOT_LOGIN, Const.ES_NOT_LOGIN)

        userId = request.getSession().userId

        switch_conf = Context.Configure.get_game_item_json(gameId, 'switch.config')
        session_ver = Context.Data.get_game_attr(userId, gameId, 'session_ver')
        for _switch_conf in switch_conf:
            if session_ver == _switch_conf['version'] and channel == _switch_conf['channel']:
                if channel == 'appstore':
                    if 'is_review' not in _switch_conf or 1 != _switch_conf['is_review']:
                        times = Context.Daily.incr_daily_data(userId, gameId, 'appstore.order.times', 1)
                        if times != 1:
                            return MsgPack.Error(0, self.appstore_limit, u'不会充值？充值失败？无法使用APP充值？请添加微信公众号“LaoYouBuNiao”获得帮助！')
                if 'pay_type' in _switch_conf and 3 == _switch_conf['pay_type']:
                    return MsgPack.Error(0, self.appstore_limit, u'暂未开启充值')
                if 'pay_type' in _switch_conf and 4 == _switch_conf['pay_type']:
                    return MsgPack.Error(0, self.appstore_limit, u'不会充值？充值失败？无法使用APP充值？请添加微信公众号“LaoYouBuNiao”获得帮助！')

        code, desc = self.__create_order(userId, gameId, channel, productId, platform=platform)
        if code != 0:
            return MsgPack.Error(0, code, desc)
        return MsgPack(0, desc)

    def deliverOrder(self, mi, request):
        gid = mi.get_param('gameId')
        order_list = mi.get_param('orders')
        token_list = mi.get_param('tokens')
        if not Entity.logined(request):
            return MsgPack.Error(0, Const.E_NOT_LOGIN, Const.ES_NOT_LOGIN)

        uid = request.getSession().userId
        orders = []
        idx = 0

        for orderId in order_list:
            orderInfo = self.getOrderInfo(orderId)
            if not orderInfo:
                continue

            userId = int(orderInfo['userId'])
            gameId = int(orderInfo['gameId'])
            state = int(orderInfo['state'])
            if userId != uid:
                Context.Log.warn('userId not match', userId, uid, orderId)
                continue

            if gameId != gid:
                Context.Log.warn('gameId not match', gameId, gid, orderId)
                continue

            if state == self.state_create:
                channelid = Context.Data.get_attr(uid, 'channelid')
                token = None
                if token_list is not None:
                    token = token_list[idx]
                resCode = Order.orderquery(orderId, orderInfo['paytype'], channelid, token)
                if resCode == order_success:  # 订单验证成功发布奖励
                    kvs = {
                        'payTime': Time.current_time(),
                        'deliverTime': Time.current_time(),
                    }

                    Order.updateOrder(orderId, state=Order.state_pre_deliver)

                    if Order.deliver_product(userId, gameId, orderId, orderInfo, orderInfo['productId'], orderInfo['paytype']):
                        kvs['state'] = Order.state_deliver_success
                    else:
                        kvs['state'] = Order.state_deliver_failed
                    Order.updateOrder(orderId, **kvs)
                    state = self.state_deliver_success

                elif resCode == order_fail:
                    state = self.state_verify_failed_id
                elif resCode == order_wait:
                    create_ts = Time.str_to_timestamp(orderInfo['createTime'], '%Y-%m-%d %X.%f')
                    now_ts = Time.current_ts()
                    if now_ts - create_ts > 3600:
                        state = self.state_timeout

            orders.append({'id': orderId, 'state': state})
            idx += 1
        return MsgPack(0, {'orders': orders})

    def random_str(self, randomlength=8):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
        random = Random()
        return "".join([chars[random.randint(0, len(chars) - 1)] for i in range(randomlength)])

    def judge_exist_product_id(self, gid, product_id):
        product_config = Context.Configure.get_game_item_json(gid, 'product.config')
        gift_config = Context.RedisActivity.get('gift_shop:product_config')
        if gift_config:
            gift_config = Context.json_loads(gift_config)
        else:
            gift_config = {}
        if product_id not in product_config and product_id not in gift_config:
            return False
        return True

Order = Order()
