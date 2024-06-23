#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: dz
# Create: 2018-05-19

from framework.context import Context
from framework.util.exceptions import NotFoundException
from sdk.third import yyb

class HttpYYB(object):

    def __init__(self):

        # 第三方回调
        self.callback_path = {
            '/v2/third/callback/yyb/pay': yyb.pay_callback,
        }

    def onMessage(self, request):
        if request.path in self.callback_path:
            with Context.GData.server_locker:
                return self.callback_path[request.path](request)

        raise NotFoundException('Not Found')



HttpYYB = HttpYYB()
