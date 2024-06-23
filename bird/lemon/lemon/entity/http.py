#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-04-11

from framework.context import Context
from framework.entity.msgpack import MsgPack
from framework.util.tool import Algorithm
from framework.util.exceptions import NotFoundException
from framework.util.exceptions import ForbiddenException
from sdk.modules.order import Order

class HttpGame(object):
    def __init__(self):
        self.json_path = {
            '/v1/game/product/deliver': self.product_deliver,
        }
        self.third_path = {
            '/v1/game/smart_game/leave': self.smart_game_leave,
        }

    def check_token(self, uid, gid, mi):
        session = mi.get_param('session')
        redis_session = Context.RedisCache.hash_get('token:%d' % uid, 'session')
        Context.Log.debug('session:', session)
        if redis_session != session:
            Context.Log.info('verify session key failed', session, redis_session)
            return False
        return True

    def check_third_token(self, mi):
        gid = mi.get_param('gameId')
        orderId = mi.get_param('orderId')
        productId = mi.get_param('productId')
        appKey = Context.Configure.get_game_item(gid, 'appKey', '')
        data = '%s-%s-%s' % (orderId, appKey, productId)
        _sign = Algorithm.md5_encode(data)
        sign = mi.get_param('sign')
        if sign != _sign:
            Context.Log.info('verify sign failed', _sign, sign)
            return False
        return True

    def onMessage(self, request):
        if request.method.lower() == 'post':
            data = request.raw_data()
            mi = MsgPack.unpack(0, data)
            Context.Log.debug('------', mi)
            gid = mi.get_param('gameId')
            if request.path in self.json_path:
                if not self.check_third_token(mi):
                    raise ForbiddenException('no permission access')
                with Context.GData.server_locker:
                    return self.json_path[request.path](gid, mi, request)
            if request.path in self.third_path:
                with Context.GData.server_locker:
                    return self.third_path[request.path](gid, mi, request)
            #else:
            #    from lemon import classMap
            #    if gid in classMap:
            #        http = classMap[gid].get('http')
            #        if http:
            #            Context.Log.debug('------', http.json_path)
            #            Context.Log.debug('------', request.path)
            #            if request.path in http.json_path:
            #                uid = mi.get_param('userId')
            #                if not self.check_token(uid, gid, mi):
            #                    raise ForbiddenException('no permission access')
            #                with Context.GData.user_locker[uid]:
            #                    return http.json_path[request.path](uid, gid, mi, request)
            #            elif request.path in http.three_json_path:
            #                if not self.check_third_token(mi):
            #                    raise ForbiddenException('no permission access')
            #                with Context.GData.server_locker:
            #                    return http.three_json_path[request.path](gid, mi, request)

        raise NotFoundException('Not Found')

    def product_deliver(self, gid, mi, request):
        # dz add record
        Context.Log.debug("game_product_deliver:", mi)
        Context.Record.add_record_game_product_deliver(mi)

        userId = mi.get_param('userId')
        orderId = mi.get_param('orderId')
        productId = mi.get_param('productId')
        appKey = Context.Configure.get_game_item(gid, 'appKey', '')
        data = '%s-%s-%s' % (orderId, appKey, productId)
        sign = Algorithm.md5_encode(data)
        if sign != mi.get_param('sign'):
            return MsgPack.Error(0, 1, 'error sign')

        # dz 增加安全性处理
        orderInfo = Order.getOrderInfo(orderId)
        Context.Log.debug('orderInfo-----', orderInfo)
        if not orderInfo:
            return MsgPack.Error(0, 1, 'error orderinfo')

        state = int(orderInfo['state'])
        if state != Order.state_pre_deliver:  # 可能并没有成功, 需要检查对单
            return MsgPack.Error(0, 1, 'error orderinfo')


        from lemon import classMap
        entity = classMap.get(gid, {}).get('entity')
        if not entity:
            Context.Log.error('game %d have no processor for order' % gid)
            return MsgPack.Error(0, 2, 'no processor')

        return entity.on_product_deliver(userId, gid, mi)


    def smart_game_leave(self, gid, mi, request):
        userId = mi.get_param('uid')
        mgid = mi.get_param('mgid')
        from lemon import classMap
        entity = classMap.get(gid, {}).get('entity')
        if not entity:
            return MsgPack.Error(0, 2, 'no processor')

        return entity.smart_game_leave(userId, mgid)


HttpGame = HttpGame()
