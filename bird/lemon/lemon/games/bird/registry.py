#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-26

from const import Enum
from framework.context import Context


class BirdRegistry(object):
    def get_table(self, tid):
        return Context.GData.online_table.get(tid)

    def create_table(self, gid, tid, playMode, level = 0, match_id = 0, table_index =0):
        if tid not in Context.GData.online_table:
            if playMode == Enum.play_mode_match:
                from match_table import MatchBirdTable as Table
                t = Table(gid, tid, level, match_id, table_index)
            else:
                from table import BirdTable as Table
                t = Table(gid, tid, playMode)
            if not t.on_init():
                return None
            Context.GData.online_table[tid] = t

        return Context.GData.online_table[tid]

    def remove_table(self, tid):
        Context.Log.info('remove_table', tid, Context.GData.online_table)
        if tid in Context.GData.online_table:
            del Context.GData.online_table[tid]
            Context.Log.info('remove_table1', Context.GData.online_table)

    def get_player(self, uid):
        return Context.GData.online_user.get(uid)

    def create_player(self, uid):
        if uid not in Context.GData.online_user:
            from player import BirdPlayer
            p = BirdPlayer(uid)
            if not p.on_init():
                return None
            Context.GData.online_user[uid] = p

        return Context.GData.online_user[uid]

    def remove_player(self, uid):
        if uid in Context.GData.online_user:
            Context.Log.info('remove_player', uid)
            del Context.GData.online_user[uid]


BirdRegistry = BirdRegistry()
