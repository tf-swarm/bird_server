#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-09-29

from framework.context import Context
from framework.entity.manager import TaskManager
from framework.util.tool import Tool
from lemon.games.bird.rank import BirdRank
from lemon.games.bird.props import BirdProps
from lemon.games.bird.account import BirdAccount


def get_user_info(uid, gid):
    chip = Context.UserAttr.get_chip(uid, gid)
    if chip is None:
        return

    chip = int(chip)
    avatar, sex, nick = Context.Data.get_attrs(uid, ['avatar', 'sex', 'nick'])
    sex = Tool.to_int(sex, 0)
    pay_total, exp, vip_exp = Context.Data.get_game_attrs(uid, gid, ['pay_total', 'exp', 'vip_exp'])
    pay_total = Tool.to_int(pay_total, 0) + Tool.to_int(vip_exp, 0)
    exp = Tool.to_int(exp, 0)
    return {
        'uid': uid,
        'avatar': avatar,
        'sex': sex,
        'nick': nick,
        'vip': BirdAccount.get_vip_level(uid, gid, pay_total=pay_total),
        'chip': chip,
        'exp': exp,
    }


def main(gid=2):
    redis_key = '10.44.169.141:16379:0'
    Context.init_with_redis_key(redis_key)
    Context.Log.open_std_log()
    max_uid = Context.RedisMix.hash_get_int('global.info.hash', 'max.user.id', 0)
    Context.RedisMix.delete('rank:2:chip.tmp')
    Context.RedisMix.delete('rank:2:chip.tmp:cache')
    Context.RedisMix.delete('rank:2:egg.tmp')
    Context.RedisMix.delete('rank:2:egg.tmp:cache')
    uid = 1000001
    while uid <= max_uid:
        try:
            attrs = get_user_info(uid, gid)
            if attrs:
                data = Context.json_dumps(attrs)
                BirdRank.add(uid, gid, 'chip.tmp', attrs['chip'], data)
                egg = BirdProps.get_egg_count(uid, gid)
                if egg:
                    attrs['egg'] = egg
                    BirdRank.add(uid, gid, 'egg.tmp', egg, Context.json_dumps(attrs))
        except Exception, e:
            Context.Log.exception(uid)
        uid += 1

    Context.RedisMix.rename('rank:2:chip.tmp', 'rank:2:chip')
    Context.RedisMix.rename('rank:2:chip.tmp:cache', 'rank:2:chip:cache')
    Context.RedisMix.rename('rank:2:egg.tmp', 'rank:2:egg')
    Context.RedisMix.rename('rank:2:egg.tmp:cache', 'rank:2:egg:cache')

    TaskManager.end_loop()


if __name__ == '__main__':
    TaskManager.add_simple_task(main)
    TaskManager.start_loop()
