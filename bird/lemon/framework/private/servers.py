#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-10-26

from framework.private.service import Service
from framework.private.protocols import GameInnerServerProtocol
from framework.private.protocols import EntityInnerProtocol
from framework.private.protocols import ProxyInnerProtocol
from framework.private.protocols import ProxyOuterProtocol
from framework.private.protocols import QuickInnerProtocol
from framework.private.protocols import ConnectInnerProtocol
from framework.private.protocols import ConnectOuterProtocol
from framework.private.protocols import WSServerFactory
from framework.private.protocols import SdkHttpFactory
from framework.private.protocols import GameHttpFactory
from framework.private.protocols import InnerHttpProtocol
from framework.private.protocols import ShellHttpFactory
from framework.private.protocols import InnerShellProtocol
from framework.private.protocols import CDKeyHttpFactory
from framework.private.protocols import YYBHttpsFactory


def run_as_game(proto=None):
    service = Service(innerProtocol=GameInnerServerProtocol)
    service.start()


def run_as_entity(proto=None):
    service = Service(innerProtocol=EntityInnerProtocol)
    service.start()


def run_as_proxy(proto=None):
    service = Service(innerProtocol=ProxyInnerProtocol, outerProtocol=ProxyOuterProtocol)
    service.start()


def run_as_quick(proto=None):
    service = Service(innerProtocol=QuickInnerProtocol)
    service.start()


def run_as_connect(proto=None):
    if proto is None:
        service = Service(innerProtocol=ConnectInnerProtocol, outerProtocol=ConnectOuterProtocol)
    else:
        service = Service(innerProtocol=ConnectInnerProtocol, wsFactory=WSServerFactory)
    service.start()


def run_as_sdk(proto=None):
    service = Service(httpFactory=SdkHttpFactory)
    service.start()


def run_as_http(proto=None):
    service = Service(innerProtocol=InnerHttpProtocol, httpFactory=GameHttpFactory)
    service.start()


def run_as_shell(proto=None):
    service = Service(innerProtocol=InnerShellProtocol, httpFactory=ShellHttpFactory)
    service.start()

def run_as_cdkey(proto=None):
    service = Service(httpFactory=CDKeyHttpFactory)
    service.start()

def run_as_yyb(proto=None):
    service = Service(httpsFactory=YYBHttpsFactory)
    service.start()

