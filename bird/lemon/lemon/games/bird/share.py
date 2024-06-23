#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: cui

from mail import Mail
import time
from account import BirdAccount
from props import BirdProps
from lemon.entity.share import Share
from framework.util.tool import Time
from framework.context import Context
from framework.entity.msgpack import MsgPack
from framework.entity.const import Message


class BirdShare(Share):
    def get_invite_reward(self, uid, gid, mi):
        reward_id = mi.get_param('id')  #可得奖励ID #3
        invitee = mi.get_param('invitee') #分享邀请的ID
        mo = MsgPack(Message.MSG_SYS_INVITE_REWARD | Message.ID_ACK)

        conf = Context.Configure.get_game_item_json(gid, 'share.config')
        if type(reward_id) != int or reward_id < 0 or reward_id > len(conf.get("friend_reward")):
            return mo.set_error(1, 'error id')
        reward_info = conf.get("friend_reward")[reward_id -1]
        if not reward_info:
            return mo.set_error(1, 'reward id error')

        invitee_list = self.get_invitee(uid, gid)
        if invitee not in invitee_list:
            return mo.set_error(2, 'invitee error')

        max_barrel = Context.Data.get_game_attr_int(invitee, gid, 'barrel_level', 1)
        max_barrel_multi = BirdAccount.trans_barrel_level(gid, max_barrel)
        if max_barrel_multi < reward_info['barrel']:
            return mo.set_error(3, 'max_barrel_multi little')

        v = self.get_invitee_by_uid(uid, gid, invitee)
        if v and 'ids' in v and reward_id in v['ids']:
            return mo.set_error(4, 'already receive')

        reward_money = Context.Data.get_game_attr_int(uid, gid, 'reward_money')
        if not reward_money:
            Context.Data.set_game_attr(uid, gid, 'reward_money', 0)
            reward_money = Context.Data.get_game_attr_int(uid, gid, 'reward_money')

        if reward_money >= 1000:
            return mo.set_error(5, '很抱歉，你领取的奖励已达到上限')
        else:
            wallet = self.get_reward_limit(uid, gid, invitee, reward_id) #3
            Context.Data.hincr_game(uid, gid, 'reward_money', wallet)
        BirdProps.issue_rewards(uid, gid, reward_info['reward'], 'share.config.welfare', True, rid=reward_id)
        idl = []
        if reward_info['reward'].has_key('props'):
            for i in reward_info['reward']['props']:
                idl.append(i)
            for j in idl:
                if j['id'] in [211, 212, 213]:
                    bulletin = 1
                    nick = Context.Data.get_attr(uid, 'nick')
                    nick = Context.hide_name(nick)
                    props_name = BirdProps.get_props_desc(j['id'])
                    led = u'恭喜<color=#00FF00FF>%s</color>在福利分享中领取<color=#FFFF00FF>%s</color>奖励，还在等什么，快来瓜分吧！' % (nick, props_name)
                    mou = MsgPack(Message.MSG_SYS_LED | Message.ID_NTF)
                    mou.set_param('game', {'msg': led, 'ts': Time.current_ts(), 'bulletin': bulletin})
                    Context.GData.broadcast_to_system(mou)
                    break
        self.add_invitee(uid, gid, invitee, reward_id) #3
        return mo

    def get_reward_limit(self, uid, gid, invitee, reward_id): #奖励限制
        conf = Context.Configure.get_game_item_json(gid, 'share.config')
        reward_info = conf.get("friend_reward")[reward_id-1]
        key = 'share:%d:%d' % (gid, uid)
        invitee_info = Context.RedisCluster.hash_get(uid, key, invitee)
        invitee_info = Context.json_loads(invitee_info)

        if not invitee_info:
            return 0
        else:
            wallet = 0
            if reward_id not in invitee_info['ids']:
                result = BirdProps.convert_reward(reward_info['reward'])
                if result.has_key('p'):
                    if result['p'][0] == 211:
                        count = result['p'][0][1]
                        wallet = count * 30
                    else:
                        count = result['p'][0][1]
                        wallet = count * 50
                if result.has_key('d'):
                    count = result['d']
                    wallet = count * 3
            return wallet

    def get_invite_info(self, uid, gid, mi):
        share_reward = []
        invitee_info = self.get_invitee(uid, gid)

        for _uid, v in invitee_info.iteritems():
            max_barrel = Context.Data.get_game_attr_int(_uid, gid, 'barrel_level', 1)
            max_barrel_multi = BirdAccount.trans_barrel_level(gid, max_barrel)
            conf = Context.Configure.get_game_item_json(gid, 'share.config')
            if conf.has_key('friend_reward'):
                barrel1 = conf['friend_reward'][0]['barrel']
                barrel2 = conf['friend_reward'][1]['barrel']
                barrel3 = conf['friend_reward'][2]['barrel']
                if max_barrel_multi >= barrel1:
                    this_info = {'uid': _uid}
                    this_info['multi'] = barrel1
                    if v and 'ids' in v and 'ts' in v:
                        this_info["ids"] = v['ids']
                        this_info["ts"] = v['ts']

                    values = Context.Data.get_attrs(_uid, ['nick', 'sex', 'avatar'])
                    if values[0]:
                        this_info['nick'] = values[0]
                    if values[1]:
                        this_info['sex'] = values[1]
                    if values[2]:
                        this_info['avatar'] = values[2]
                    share_reward.append(this_info)

                    if max_barrel_multi >= barrel2:
                        this_info = {'uid': _uid}
                        this_info['multi'] = barrel2
                        if v and 'ids' in v and 'ts' in v:
                            this_info["ids"] = v['ids']
                            this_info["ts"] = v['ts']

                        values = Context.Data.get_attrs(_uid, ['nick', 'sex', 'avatar'])
                        if values[0]:
                            this_info['nick'] = values[0]
                        if values[1]:
                            this_info['sex'] = values[1]
                        if values[2]:
                            this_info['avatar'] = values[2]
                        share_reward.append(this_info)

                        if max_barrel_multi >= barrel3:
                            this_info = {'uid': _uid}
                            this_info['multi'] = barrel3
                            if v and 'ids' in v and 'ts' in v:
                                this_info["ids"] = v['ids']
                                this_info["ts"] = v['ts']

                            values = Context.Data.get_attrs(_uid, ['nick', 'sex', 'avatar'])
                            if values[0]:
                                this_info['nick'] = values[0]
                            if values[1]:
                                this_info['sex'] = values[1]
                            if values[2]:
                                this_info['avatar'] = values[2]
                            share_reward.append(this_info)

        share_reward_list = self.get_record_sort(share_reward)
        mo = MsgPack(Message.MSG_SYS_INVITE_INFO | Message.ID_ACK)
        mo.set_param('list', share_reward_list)
        return mo

    def get_record_sort(self, share_reward):
        sort1 = []
        sort2 = []
        for ns in share_reward:
            if len(ns['ids']):
                sort1.append(ns)
            else:
                sort2.append(ns)
        multi_sorted = sorted(sort1, key=lambda x: len(x['ids']))
        sort2.extend(multi_sorted)
        return sort2

    def on_bind_inviter(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_BIND_INVITER | Message.ID_ACK)
        invite_code = mi.get_param('invite_code')
        if not invite_code.isdigit():
            return mo.set_error(1, 'code error')
        invite_code = int(invite_code)
        conf = Context.Configure.get_game_item_json(gid, 'share.config')
        now_time = int(time.time())
        create_time = Context.Data.get_attr(uid, 'createTime')
        create_tamp = Time.str_to_timestamp(create_time[:19])
        day_second = now_time - create_tamp
        days = self.day_Time(day_second)
        if not days:
            days = 0
        # 有没有绑定过分享码
        inviter = Context.Data.get_game_attr_int(uid, gid, 'inviter', 0)
        if inviter or days > 3:
            return mo.set_error(2, 'already bound')

        # 分享码是否有效, 查询分享者的分享码与这个是否相符，
        _invite_code = Context.Data.get_game_attr_int(invite_code, gid, 'invite_code')

        if invite_code != _invite_code:
            return mo.set_error(1, 'code error')

        # 增加不允许绑定自己的处理 dz
        if invite_code == uid:
            return mo.set_error(1, 'code error')

        # 获取兑换卷，绑定分享者的id
        nType = 8
        for x in range(len(conf['welfare'])):
            times = time.time()
            ret = Mail.add_mail(uid, gid, times, nType, conf['welfare'][x]['reward'], invite_code)
            if not ret:
                return mo.set_error(3, 'add mail fail')
        Context.Data.set_game_attr(uid, gid, 'inviter', invite_code)

        # 给对方记录我的id
        if len(self.get_invitee(invite_code, gid)) < 5:
            self.add_invitee(invite_code, gid, uid)

        return mo

    def day_Time(self, allTime):
        day = 24 * 60 * 60
        if allTime > day:
            days = divmod(allTime, day)
            return int(days[0])

    def on_share(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_SHARE | Message.ID_ACK)

        #if not self.can_get_share_reward(uid, gid):
        #    return mo.set_error(1, 'already get')
        from lemon.games.bird.newtask import NewTask
        NewTask.get_share_task(uid)
        Context.Data.set_game_attr(uid, gid, 'last_share_reward_ts', Time.current_ts())
        mo.set_param('share', {})
        return mo

    def get_share_info(self, uid, gid, mi):
        # which = mi.get_param('which')
        mo = MsgPack(Message.MSG_SYS_SHARE_INFO | Message.ID_ACK)

        inviter = Context.Data.get_game_attr_int(uid, gid, 'inviter')
        if not inviter:
            inviter = 0
        else:
            inviter = 1
        now_time = int(time.time())
        create_time = Context.Data.get_attr(uid, 'createTime')
        create_tamp = Time.str_to_timestamp(create_time[:19])
        day_second = now_time - create_tamp
        days = self.day_Time(day_second)
        if not days:
            days = 0
        mo.set_param('invitee', len(self.get_invitee(uid, gid)))
        mo.set_param('h_reward', self.can_get_share_reward(uid, gid))
        mo.set_param('invite_code', self.get_invite_code(uid, gid))
        mo.set_param('inviter', inviter)
        mo.set_param('day', days)
        return mo

    def can_get_share_reward(self, uid, gid):
        last_ts = Context.Data.get_game_attr_int(uid, gid, 'last_share_reward_ts', 0)
        week_start_ts = Time.current_week_start_ts()
        if last_ts > week_start_ts:
            return 0
        return 1

    def get_invite_code(self, uid, gid):
        invite_code = Context.Data.get_game_attr(uid, gid, 'invite_code')
        if not invite_code:
            # invite_code = str(uid) + str(gid) + str(int(random.randint(11, 99)))
            invite_code = str(uid)
            Context.Data.set_game_attr(uid, gid, 'invite_code', invite_code)
        return invite_code


BirdShare = BirdShare()
