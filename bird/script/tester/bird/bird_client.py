#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-07-14

import sys
import time
import random
import threading
from tester.PlayerClient import PlayerClient
from lemon.games.bird.const import Message
from framework.entity.manager import TaskManager


class BirdClient(PlayerClient):
    gid = 2

    def __init__(self, http, shot_limit=None):
        super(BirdClient, self).__init__(http)
        self.bird = None
        self.bullet = 0
        self.shot_limit = shot_limit

    def run(self):
        PlayerClient.run(self)
        #self.req_config()
        # self.req_match_entry()
        # self.req_poke_mole_info()
        # self.req_poke_mole()
        # self.req_get_share_info()
        # self.req_share()
        # self.req_bind_inviter()
        # self.req_share_reward_info()
        # self.req_get_share_reward()

        # self.req_get_group_buy_info()
        # self.req_get_group_buy_reward()
        # self.req_props_list()
        # self.req_task_list()
        # self.req_rank_list()
        # self.req_activity_list()
        # self.req_consume_cdkey()
        # self.req_present()
        # self.req_hold(True)
        # self.put_led()
        # self.req_led()
        # self.req_up_barrel()
        # self.req_task_list()
        # self.req_task_room()
        self.req_quick_start()

    def req_task_list(self):
        msg = {
            'cmd': Message.MSG_SYS_NEW_TASK_LIST | Message.ID_REQ,
            'param': {}
        }
        return self.send_to_svrd(msg)

    def req_task_room(self):
        msg = {
            'cmd': Message.MSG_SYS_TABLE_TASK_LIST | Message.ID_REQ,
            'param': {'room':201}
        }
        return self.send_to_svrd(msg)

    def on_msg(self, cmd, param):
        if 'error' in param:
            self.close()
            return
        elif cmd == Message.MSG_SYS_SIT_DOWN | Message.ID_ACK:
            self.req_board_info()
        elif cmd == Message.BIRD_MSG_BOARD_INFO | Message.ID_ACK:
            self.req_move_barrel(param)
        elif cmd == Message.BIRD_MSG_MOVE_BARREL | Message.ID_NTF:
            if param['u'] == self.http.userId:
                self.req_shot_bullet()
        elif cmd == Message.BIRD_MSG_SHOT_BULLET | Message.ID_NTF:
            self.on_shot_bullet(param)
        elif cmd == Message.BIRD_MSG_CATCH_BIRD | Message.ID_NTF:
            self.on_catch_bird(param)
        elif cmd == Message.BIRD_MSG_DELTA_SCENE | Message.ID_ACK:
            pass
        else:
            PlayerClient.on_msg(self, cmd, param)

    def req_match_entry(self):
        msg = {
            'cmd': Message.MSG_SYS_MATCH_ENTRY | Message.ID_REQ,
            'param': {}
        }
        return self.send_to_svrd(msg)

    def req_up_barrel(self):
        msg = {
            'cmd': Message.MSG_SYS_UP_BARREL | Message.ID_REQ,
            'param': {
                'gameId': self.gid,
                'up_ty': 2,
            }
        }
        return self.send_to_svrd(msg)

    def req_quick_start(self):
        msg = {
            'cmd': Message.MSG_SYS_QUICK_START | Message.ID_REQ,
            'param': {
                'gameId': self.gid,
                'playMode': 2
            }
        }
        return self.send_to_svrd(msg)

    def req_board_info(self):
        msg = {
            'cmd': Message.BIRD_MSG_BOARD_INFO | Message.ID_REQ,
            'param': {
            }
        }
        return self.send_to_svrd(msg)

    def req_move_barrel(self, param):
        uptime = param['uptime']
        freeze_sum = param['freeze']['total']
        if 'start' in param['freeze']:
            from framework.util.tool import Time
            freeze_sum += Time.current_ts() - param['freeze']['start']
        birds = param['map'].get('birds')
        if birds:
            for bird in birds:
                if bird['n'] * 100 + freeze_sum > uptime:
                    self.bird = bird['i']
                    break

        tide = param['map'].get('tide')
        if tide:
            self.bird = tide['info'][-2]['id']

        msg = {
            'cmd': Message.BIRD_MSG_MOVE_BARREL | Message.ID_REQ,
            'param': {
                'a': 52
            }
        }
        return self.send_to_svrd(msg)

    def req_shot_bullet(self):
        if self.is_connected():
            if self.shot_limit and self.bullet >= self.shot_limit:
                self.close()
                return
            self.bullet += 1
            msg = {
                'cmd': Message.BIRD_MSG_SHOT_BULLET | Message.ID_REQ,
                'param': {
                    'b': self.bullet,
                }
            }
            if self.bullet % 15 == 0:
                msg['param']['a'] = random.randint(-60, 60)

            TaskManager.add_delay_task(0.30, self.req_shot_bullet)

            return self.send_to_svrd(msg)

    def on_shot_bullet(self, param):
        if param['u'] == self.http.userId:
            # if param['c'] < 1000:
            #     uid = param['u']
            #     TaskManager.add_simple_task(Context.UserAttr.incr_chip, uid, self.gid, 1000, 'robot.issue')

            # 模拟打中鸟
            self.req_hit_bird()

    def req_hit_bird(self):
        if self.is_connected():
            if self.bird is not None:
                msg = {
                    'cmd': Message.BIRD_MSG_HIT_BIRD | Message.ID_REQ,
                    'param': {
                        "i": self.bird,
                        "b": self.bullet,
                    }
                }
                return self.send_to_svrd(msg)

    def on_catch_bird(self, param):
        bird = param['i']
        self.bird = bird + 1

    def req_rank_list(self):
        msg = {
            'cmd': Message.MSG_SYS_RANK_LIST | Message.ID_REQ,
            'param': {
            }
        }

        which = random.choice(['love'])
        if which:
            msg['param']['rank'] = which

        return self.send_to_svrd(msg)

    def put_led(self):
        msg = {
            'cmd': Message.MSG_SYS_LED | Message.ID_REQ,
            'param': {
                'action': 'put',
                'msg': 'hello world',
            }
        }
        return self.send_to_svrd(msg)

    def req_room_list(self):
        msg = {
            'cmd': Message.MSG_SYS_ROOM_LIST | Message.ID_REQ,
            'param': {
                'gameId': self.gid,
                'match': 1
            }
        }
        return self.send_to_svrd(msg)

    def req_config(self):
        msg = {
            'cmd': Message.MSG_SYS_CONFIG | Message.ID_REQ,
            'param': {
                # 'which': ['vip', 'shop', 'raffle', 'props', 'barrel', 'exchange', 'record', 'html']
                'which': ['match']
            }
        }
        return self.send_to_svrd(msg)

    def req_present(self):
        msg = {
            'cmd': Message.MSG_SYS_PRESENT | Message.ID_REQ,
            'param': {
                'id': 201,
                'count': 200,
                'ta': 27200
            }
        }
        return self.send_to_svrd(msg)

    def req_props_list(self):
        msg = {
            'cmd': Message.MSG_SYS_PROPS_LIST | Message.ID_REQ,
            'param': {
            }
        }
        return self.send_to_svrd(msg)


    def req_activity_list(self):
        msg = {
            'cmd': Message.MSG_SYS_ACTIVITY_LIST | Message.ID_REQ,
            'param': {
            }
        }
        return self.send_to_svrd(msg)

    def req_consume_cdkey(self):
        msg = {
            'cmd': Message.MSG_SYS_CONSUME_CDKEY | Message.ID_REQ,
            'param': {
                'code': 'e12fbd7a1',
                'imei': 'test',
            }
        }
        return self.send_to_svrd(msg)

    def req_share(self):
        msg = {
            'cmd': Message.MSG_SYS_SHARE | Message.ID_REQ,
            'param': {
                'gameId': self.gid,
            }
        }
        return self.send_to_svrd(msg)

    def req_get_share_info(self):
        msg = {
            'cmd': Message.MSG_SYS_SHARE_INFO | Message.ID_REQ,
            'param': {
                'gameId': self.gid,
            }
        }
        return self.send_to_svrd(msg)

    def req_bind_inviter(self):
        msg = {
            'cmd': Message.MSG_SYS_BIND_INVITER | Message.ID_REQ,
            'param': {
                'gameId': self.gid,
                'invite_code': "200012187",
            }
        }
        return self.send_to_svrd(msg)

    def req_share_reward_info(self):
        msg = {
            'cmd': Message.MSG_SYS_INVITE_INFO | Message.ID_REQ,
            'param': {
                'gameId': self.gid,
            }
        }
        return self.send_to_svrd(msg)

    def req_get_share_reward(self):
        msg = {
            'cmd': Message.MSG_SYS_INVITE_REWARD | Message.ID_REQ,
            'param': {
                'gameId': self.gid,
                'id': 3,
                'invitee': 20002,
            }
        }
        return self.send_to_svrd(msg)

    def req_poke_mole_info(self):
        msg = {
            'cmd': Message.MSG_SYS_POKE_MOLE_INFO | Message.ID_REQ,
            'param': {
                'gameId': self.gid,
            }
        }
        return self.send_to_svrd(msg)

    def req_poke_mole(self):
        msg = {
            'cmd': Message.MSG_SYS_POKE_MOLE | Message.ID_REQ,
            'param': {
                'gameId': self.gid,
                'i': 1,
            }
        }
        return self.send_to_svrd(msg)

    def req_poke_mole_change(self):
        msg = {
            'cmd': Message.MSG_SYS_POKE_MOLE_CHANGE | Message.ID_REQ,
            'param': {
                'gameId': self.gid,
                's': 1,
            }
        }
        return self.send_to_svrd(msg)


def main(*args, **kwargs):
    from tester.PlayerClient import run_as_tcp as run_client
    print args, kwargs
    d = run_client(*args, **kwargs)
    d.addBoth(lambda err: TaskManager.end_loop())

if __name__ == '__main__':
    if len(sys.argv) < 5:
        sys.argv.extend(['192.168.0.199:6379:0', 'test', '1.1.0', 'test'])

    TaskManager.add_simple_task(main, sys.argv[1:5], BirdClient, [2000])
    TaskManager.start_loop()