#!/usr/bin/env python
# -*- coding=utf-8 -*-

#时间戳（id）：{
#    [
#       类型
#       邮件信息，{'chip':10000, 'coupon':1000, 'props':[{'id':201, 'count': 10},{'id':201, 'count': 10}]},
#       发件人，
#       描述，
#    ]
# }

import time
import sys
import datetime
from const import Message
from framework.entity.msgpack import MsgPack
from framework.context import Context
import props # BirdProps

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf8')

#获取奖励描述
def get_reward_str(reward):
    desc = []
    keys = ['chip', 'diamond', 'coupon']
    names = [u'鸟蛋', u'钻石', u'鸟券']
    for key, name in zip(keys, names):
        if key in reward:
            desc.append(u'%d%s' % (reward[key], name))

    prop = reward.get('props')
    if prop:
        for one in prop:
            _ = props.BirdProps.get_props_desc(one['id']) + u'%d个' % one['count']
            desc.append(_)
    return u', '.join(desc)

#获取邮件的desc #可根据类型来判断desc
def get_desc(nType, reward, sender, title=""):
    desc = u''
    if int(nType) == 1:#赠送
        try:
            nick = Context.Data.get_attr(int(sender), 'nick', str(sender))
        except:
            nick = ''
        desc = u'{0}赠送给您'.format(nick)
        reward_str = get_reward_str(reward)
        desc += reward_str
    elif int(nType) == 2:#世界boss排行榜
        desc = u'世界boss排行榜第%d名奖励'%(-sender)
    elif int(nType) == 3:#充值榜
        desc = u'充值排行榜第%d名奖励'%(-sender)
    elif int(nType) == 4:#初级场排行榜
        desc = u'新手海岛排行榜第%d名奖励'%(-sender)
    elif int(nType) == 5:#中级场排行榜
        desc = u'林海雪原排行榜第%d名奖励'%(-sender)
    elif int(nType) == 6:#高级场排行榜
        desc = u'猎龙峡谷排行榜第%d名奖励'%(-sender)
    elif int(nType) == 7:#活动排行榜
        desc = u'炮王之王活动排行榜第%d名奖励'%(-sender)
    elif int(nType) == 8:  # 输入邀请码领取福利
        try:
            nick = Context.Data.get_attr(int(sender), 'nick', str(sender))
        except:
            nick = ''
        desc = u'{0}赠送给您的福利'.format(nick)
    elif int(nType) == 9:   #GM赠送
        desc = title
    elif int(nType) == 10:
        desc = u'竞技场快速场排行榜第%d名奖励'%(-sender)
    elif int(nType) == 11:
        desc = u'竞技场快速场退还金币'
    elif int(nType) == 12:
        desc = u'微信公众号福利多多'
    elif int(nType) == 13:
        desc = u'微信公众号新手大礼包'
    elif int(nType) == 14:
        desc = u'风云争霸排行榜第%d名奖励'%(-sender)
    elif int(nType) == 15:
        desc = u'五一劳模光荣榜第%d名奖励'%(-sender)
    return desc

class Mail(object):
    #获取邮件列表
    def get_mail_list(self, uid, gid):
        info = Context.Data.get_game_attr_json(uid, gid, 'present_list')
        if info == None or len(info) <= 0:
            info = {}
        # 只保留30天的邮件信息
        nLen = len(info)
        mail_keys = info.keys()
        for i in mail_keys:
            if not self.check_mail(i):
                del info[i]
        if len(info) != nLen:
            Context.Data.set_game_attr(uid, gid, 'present_list', Context.json_dumps(info))
        return info

    #核对邮件是否超过30天
    def check_mail(self, keys):
        hTime = datetime.datetime.now() - datetime.timedelta(days=30)
        hTime = int(time.mktime(hTime.timetuple()))
        if hTime > float(keys):
            return False
        return True

    #添加邮件
    def add_mail(self, uid, gid, times, nType, reward, sender, title = ""):
        mail_info = self.get_mail_list(uid, gid)
        if mail_info == None or len(mail_info) <= 0:
            mail_info = {}
        if not self.check_mail(times):
            return False
        mail_info[times] = [nType, reward, sender, title]
        Context.Data.set_game_attr(uid, gid, 'present_list', Context.json_dumps(mail_info))
        return True

    #领取邮件的内容
    def ling_qu_mail(self, uid, gid, keys):
        mail_list = self.get_mail_list(uid, gid)
        if not mail_list.has_key(keys):
            return
        mail_info = mail_list[keys]
        nType = mail_info[0]
        reward = mail_info[1]
        sender = mail_info[2]
        if len(mail_info) >= 4:
            title = mail_info[3]
        else:
            title = u''
        event = self.get_event(nType)
        if not reward.has_key('tips'):      #判断是不是没有奖励的邮件（显示的标题）
            if len(reward) > 0:
                props.BirdProps.issue_rewards(uid, gid, reward, event, True)
        final_info = reward
        MailRecord.add_record(uid, gid, nType, reward, sender, title)
        del mail_list[str(keys)]
        Context.Data.set_game_attr(uid, gid, 'present_list', Context.json_dumps(mail_list))
        if len(final_info) <= 0:
            return
        return final_info


    def get_event(self, nType):
        event = 'no.record'
        if nType == 1:
            event = 'present.get'
        elif nType == 2:
            event = 'boss.rank.get'
        elif nType == 3:
            event = 'pay.rank.get'
        elif nType == 4:
            event = 'primary.rank.get'
        elif nType == 5:
            event = 'middle.rank.get'
        elif nType == 6:
            event = 'high.rank.get'
        elif nType == 7:
            event = 'activity.rank.get'
        elif nType == 8:
            event = 'welfare.get'
        elif nType == 9:
            event = 'gm.mail.get'
        elif nType == 10:
            event = 'match_table.mail.get'
        elif nType == 11:
            event = 'match_table.return'
        elif nType == 12:
            event = 'wx.info'
        elif nType == 13:
            event = 'wx.new.play.gift'
        elif nType == 14:
            event = 'activity.pay.rank.reward'
        elif nType == 15:
            event = 'activity.point.shop.reward'
        return event

    #获取邮件的发送json
    def get_mail_json(self, uid, gid):
        mail_info = self.get_mail_list(uid, gid)
        info = []
        if mail_info == None or len(mail_info) <= 0:
            return info
        for k,v in mail_info.items():
            try:
                nick = Context.Data.get_attr(int(v[2]), 'nick', str(v[2]))
            except:
                nick = ''
            rw = v[1]
            if not isinstance(v[1], dict):
                rw = Context.json_loads(v[1])
            if not rw.has_key('tips'):          #判断是不是没有奖励的邮件（显示的标题）
                reward = props.BirdProps.convert_reward(rw)
            else:
                reward = rw
            if len(v) >=4:
                title = v[3]
            else:
                title = u''
            desc = get_desc(int(v[0]), v[1], int(v[2]), title)
            times = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(float(k))))
            mail = {
                'id': str(k),
                'nType': int(v[0]),
                'reward': reward,
                'sender': int(v[2]),
                'nick': u'{0}'.format(nick),
                'desc': desc,
                'times': str(times),
                }
            info.append(mail)
        return info

    # 领取邮件
    def receive_present(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_MAIL_RECEIVE | Message.ID_ACK)
        _id = mi.get_param('id')
        ret = self.ling_qu_mail(uid,gid,_id)
        final = 0
        if ret:
            final = 1
        mo.set_param('final', final)
        return mo

    def del_mail(self, uid, gid, mi):
        mo = MsgPack(Message.MSG_SYS_MAIL_DELETE_RECORD | Message.ID_ACK)
        mail_list = Context.copy_obj(Context.Data.get_game_attr_json(uid, gid, 'present_list', {}))
        mail_record_list = Context.copy_obj(Context.Data.get_game_attr_json(uid, gid, 'present_record', {}))
        keys = mi.get_param('keys')
        for k in keys:
            if mail_record_list.has_key(k):
                del mail_record_list[str(k)]
            if mail_list.has_key(k):
                del mail_list[str(k)]
        Context.Data.set_game_attr(uid, gid, 'present_record', Context.json_dumps(mail_record_list))
        Context.Data.set_game_attr(uid, gid, 'present_list', Context.json_dumps(mail_list))
        mo.set_param('keys', keys)
        return mo

    #发送邮件list：open表示是否打开界面
    def send_mail_list(self, uid, gid, open = 0):
        mo = MsgPack(Message.MSG_SYS_MAIL_LIST | Message.ID_ACK)
        mail_record = MailRecord.get_record_json(uid, gid)
        info = self.get_mail_json(uid, gid)
        if len(info) > 0:
            mo.set_param('open', open)  # open 表示打开界面
            mo.set_param('present_list', info)
        else:
            mo.set_param('open', -1)    # 没有邮件数据
        if len(mail_record) > 0:
            mo.set_param('present_record', mail_record)
        Context.GData.send_to_connect(uid, mo)
        return

class MailRecord(object):
    #添加邮件记录
    def add_record(self, uid, gid, nType, reward, sender, title):
        mail_record = Context.Data.get_game_attr_json(uid, gid, 'present_record', {})
        recv_time = time.time()
        mail_record[recv_time] = [nType, reward, sender, title]
        Context.Data.set_game_attr(uid, gid, 'present_record', Context.json_dumps(mail_record))
        return

    #获取邮件记录的list（超过30条时则删除）
    def get_record_list(self, uid, gid, mail_record = None):
        if not mail_record:
            mail_record = Context.Data.get_game_attr_json(uid, gid, 'present_record')
        if not mail_record:
            mail_record = {}
        rank_ret = sorted(mail_record.items(), key=lambda x: float(x[0]), reverse=True)
        if len(mail_record) > 30:
            rank_ret = rank_ret[:30]
            mail_record_key = mail_record.keys()
            for i in mail_record_key:
                if i == rank_ret[0]:
                    del mail_record[i]
            Context.Data.set_game_attr(uid, gid, 'present_record', Context.json_dumps(mail_record))
        return rank_ret

    #获取邮件记录的json
    def get_record_json(self, uid, gid):
        record_info = self.get_record_list(uid, gid)
        info = []
        if record_info == None or len(record_info) <= 0:
            return info
        for i in record_info:
            k = i[0]
            v = i[1]
            try:
                nick = Context.Data.get_attr(int(v[2]), 'nick', str(v[2]))
            except:
                nick = ''
            rw = v[1]
            if not isinstance(v[1], dict):
                rw = Context.json_loads(v[1])
            if not rw.has_key('tips'):      #判断是不是没有奖励的邮件（显示的标题）
                reward = props.BirdProps.convert_reward(rw)
            else:
                reward = rw
            if len(v) >=4:
                title = v[3]
            else:
                title = u''
            desc = get_desc(int(v[0]), v[1], int(v[2]), title)

            times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(k)))
            record = {
                'id': str(k),
                'nType': int(v[0]),
                'reward': reward,
                'sender': int(v[2]),
                'nick': u'{0}'.format(nick),
                'desc': desc,
                'times': str(times),
                'lingqu': 1,
                }
            info.append(record)
        return info

    #发送邮件信息的记录
    def send_mail_record(self, uid, gid):
        mail_record = MailRecord.get_record_json(uid, gid)
        mo = MsgPack(Message.MSG_SYS_MAIL_RECORD_LIST | Message.ID_ACK)
        if len(mail_record) > 0:
            mo.set_param('present_record', mail_record)
        return mo

Mail = Mail()
MailRecord = MailRecord()