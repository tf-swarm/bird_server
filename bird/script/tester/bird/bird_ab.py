#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-07-17

from twisted.internet import defer
from twisted.internet import reactor

from bird_client import BirdClient
from framework.context import Context
from tester.HttpSdk import HttpSdk
from tester.PlayerClient import TcpClientFactory as ClientFactory
from tester.PlayerClient import connect_lost


def run_as_player(http, all_clients, dt, start):
    try:
        http.run_as_player()
    except:
        pass
    dt.remove(id(http))
    if not dt:
        login_sdk(all_clients, start)


def start_connect_game(clients):
    defer_list = []
    for http in clients:
        if http.has_login:
            tcp = BirdClient(http)
            d = defer.Deferred()
            d.addBoth(connect_lost)
            factory = ClientFactory(d, tcp)
            reactor.connectTCP(http.host, int(http.port), factory)
            defer_list.append(d)
    d = defer.DeferredList(defer_list, consumeErrors=True)
    d.addBoth(lambda err: TaskManager.end_loop())


def login_sdk(all_clients, start=0):
    if start >= len(all_clients):
        start_connect_game(all_clients)
    else:
        dt = set()
        for http in all_clients[start:start + 100]:
            dt.add(id(http))
            TaskManager.add_simple_task(run_as_player, http, all_clients, dt, start + 100)


def main():
    Context.Log.open_std_log()
    redis_key = '127.0.0.1:6379:0'
    Context.init_with_redis_key(redis_key)
    Context.load_lua_script()
    params = Context.Configure.get_global_item_json('params')
    http_sdk = params['server']['http.sdk']
    http_clients = []
    for i in range(0, 1):
        devId = 'ab1_bird_' + str(i)
        clientId = '1.1.0'
        devName = 'ab1_bird_' + str(i)
        http_client = HttpSdk(2, http_sdk, devId, clientId, devName)
        http_clients.append(http_client)

    login_sdk(http_clients)


if __name__ == '__main__':
    from framework.entity.manager import TaskManager

    TaskManager.add_simple_task(main)
    TaskManager.start_loop()
