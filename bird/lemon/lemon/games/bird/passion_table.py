#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-10-16

from const import Enum
from const import Message
from table import BirdTable
from builder import MapBuilder
from framework.util.tool import Time
from framework.entity.msgpack import MsgPack
from framework.context import Context


class PassionBirdTable(BirdTable):
    def __init__(self, gid, tid):
        super(PassionBirdTable, self).__init__(gid, tid)
        self.start_ts = 0
        self.end_ts = 0

    def reset_param(self, empty=True):
        BirdTable.reset_param(self, empty)
        if empty:
            self.start_ts = 0
            self.end_ts = 0

    def fetch_table_info(self):
        success = BirdTable.fetch_table_info(self)
        if success:
            now_dt = Time.datetime()
            now_ts = Time.current_ts(now_dt)
            for start, end in self.room_config['time']:
                start_ts = Time.timestamp_from_hms(start, now_dt)
                end_ts = Time.timestamp_from_hms(end, now_dt)
                if start_ts < now_ts < end_ts:
                    self.start_ts = start_ts
                    self.end_ts = end_ts
                    break
            else:
                success = False
        return success

    # def handle_red_dragon(self):
    #     if 301 in self.lj_info:
    #         del self.lj_info[301]
    #     if Time.current_ts() + self.room_config['gap'] < self.end_ts:
    #         self.set_timer('red_dragon', self.room_config['gap'])
    #
    #     self.red_dragon_task_state = Enum.task_state_pre
    #     rel_uptime, _, _ = self.relative_time()
    #     hunter = self.get_by_state(Enum.user_state_playing)
    #     start, show, ev_list, birds = self.map.make_red_dragon_alone(rel_uptime / 100, 10, hunter)
    #     self.delta_timer.cancel()
    #     self.switch_timer.cancel()
    #     self.set_timer('red_dragon_start', 10, show=show)
    #
    #     mo = MsgPack(Message.BIRD_MSG_RED_DRAGON_COME | Message.ID_NTF)
    #     if birds:
    #         mo.set_param('birds', birds)
    #     if ev_list:
    #         mo.set_param('events', ev_list)
    #     mo.set_param('uptime', rel_uptime)
    #     self.table_broadcast(mo)
    #     return 0

    def on_skill_super_weapon(self, uid, player, mi):
        return

    def on_skill_freeze(self, uid, player, mi):
        return

    def on_skill_portal(self, uid, player, mi):
        return

    def init_map_info(self, old_map=None):
        if not self.map:
            if old_map:
                for player in self.players:
                    if player:
                        player.switch_scene()
            if not self.check_in_red_dragon():
                self.map = MapBuilder(self.room_type)
                next_img = old_map.next_img if old_map else None
                hunter = self.get_by_state(Enum.user_state_playing)
                duration, _, _ = self.map.new_map(self.builder_info, hunter, next_img)
                self.set_timer('switch', self.map.total_ts + 0.5)
                self.set_timer('delta', duration - 6)

    def check_in_red_dragon(self):
        if self.loop_red_dragon_timer.IsActive():
            return False

        gap = self.room_config['gap']
        now_ts = Time.current_ts()
        offset_ts = (now_ts - self.start_ts) % gap
        if now_ts < self.start_ts + gap:
            self.set_timer('red_dragon', gap - offset_ts)
            return False

        show = MapBuilder.red_dragon_show_time()
        if offset_ts > 10 + show:  # 界面上是普通鸟
            if now_ts < self.end_ts - gap:
                self.set_timer('red_dragon', gap - offset_ts)
            return False

        # 界面中是红龙
        self.map = MapBuilder(self.room_type)
        self.update_builder_info()
        hunter = self.get_by_state(Enum.user_state_playing)
        self.map.new_map_with_red_dragon(now_ts - offset_ts, 0, 10, hunter)
        if now_ts < self.end_ts - gap:
            self.set_timer('red_dragon', gap - offset_ts)

        if offset_ts <= 10:
            self.red_dragon_task_state = Enum.task_state_pre
            self.set_timer('red_dragon_start', 10 - offset_ts, show=show)
        else:
            self.set_timer('red_dragon_end', show + 10 - offset_ts)
            for player in self.players:
                if player and player.state == Enum.user_state_playing:
                    self.set_timer('call_bird', 1, userId=player.uid, first=True)
            self.red_dragon_task_state = Enum.task_state_ing

        return True
