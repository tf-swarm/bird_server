#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-10-26

from lemon.tasklet.game import GameTasklet
from lemon.tasklet.http import SdkTasklet
from lemon.tasklet.http import HttpTasklet
from lemon.tasklet.http import ShellTasklet
from lemon.tasklet.http import CDKeyTasklet
from lemon.tasklet.http import YYBTasklet
from lemon.tasklet.entity import EntityTasklet
from lemon.tasklet.proxy import ProxyTasklet
from lemon.tasklet.quick import QuickTasklet
from lemon.tasklet.connect import ConnectTasklet
from framework.core.protocol.tcp.server import InnerServerProtocol
from framework.core.protocol.tcp.server import OuterServerProtocol
from framework.core.protocol.tcp.server import ThreeOuterServerProtocol
from framework.core.protocol.http.server import BasicHttpProtocol
from framework.core.protocol.http.server import SdkHttpFactory
from framework.core.protocol.http.server import GameHttpFactory
from framework.core.protocol.http.server import ShellHttpFactory
from framework.core.protocol.http.server import CDKeyHttpFactory
from framework.core.protocol.http.server import YYBHttpsFactory
from framework.core.protocol.ws.ws import WSServerProtocol
from framework.core.protocol.ws.ws import WSServerFactory


class GameInnerServerProtocol(InnerServerProtocol):
    def makeTasklet(self, cmd, raw, connection):
        return GameTasklet(cmd, raw, connection)


class EntityInnerProtocol(InnerServerProtocol):
    def makeTasklet(self, cmd, raw, connection):
        return EntityTasklet(cmd, raw, connection)


class ProxyInnerProtocol(InnerServerProtocol):
    def makeTasklet(self, cmd, raw, connection):
        return ProxyTasklet(cmd, raw, connection)


class ProxyOuterProtocol(ThreeOuterServerProtocol):
    def makeTasklet(self, cmd, raw, connection):
        return ProxyTasklet(cmd, raw, connection)


class QuickInnerProtocol(InnerServerProtocol):
    def makeTasklet(self, cmd, raw, connection):
        return QuickTasklet(cmd, raw, connection)


class ConnectInnerProtocol(InnerServerProtocol):
    def makeTasklet(self, cmd, raw, connection):
        return ConnectTasklet(cmd, raw, connection)


class ConnectOuterProtocol(OuterServerProtocol):
    def makeTasklet(self, cmd, raw, connection):
        return ConnectTasklet(cmd, raw, connection)


class ConnectWSProtocol(WSServerProtocol):
    def makeTasklet(self, cmd, raw, connection):
        return ConnectTasklet(cmd, raw, connection)


WSServerFactory.protocol = ConnectWSProtocol


class SdkHttpProtocol(BasicHttpProtocol):
    def makeTasklet(self, request):
        return SdkTasklet(request)


SdkHttpFactory.protocol = SdkHttpProtocol


class InnerHttpProtocol(InnerServerProtocol):
    def makeTasklet(self, cmd, raw, connection):
        return HttpTasklet(None)


class GameHttpProtocol(BasicHttpProtocol):
    def makeTasklet(self, request):
        return HttpTasklet(request)


GameHttpFactory.protocol = GameHttpProtocol


class InnerShellProtocol(InnerServerProtocol):
    def makeTasklet(self, cmd, raw, connection):
        return ShellTasklet(None)


class ShellHttpProtocol(BasicHttpProtocol):
    def makeTasklet(self, request):
        return ShellTasklet(request)


ShellHttpFactory.protocol = ShellHttpProtocol

class CDKeyHttpProtocol(BasicHttpProtocol):
    def makeTasklet(self, request):
        return CDKeyTasklet(request)

CDKeyHttpFactory.protocol = CDKeyHttpProtocol

class YYBHttpProtocol(BasicHttpProtocol):
    def makeTasklet(self, request):
        return YYBTasklet(request)

YYBHttpsFactory.protocol = YYBHttpProtocol

