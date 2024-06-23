#!/usr/bin/env python
# -*- coding=utf-8 -*-

# author: likebeta <ixxoo.me@gmail.com>
# create: 2016-10-13

from framework.helper import *

add_game_config(2, 'passion.config', {
    'room_type': 221,
    'room_name': u'激情场',
    'room_fee': 0,
    'base_point': 1,
    'chip_min': 50000,
    'chip_max': -1,
    'barrel_min': 3000,
    'barrel_max': 10000,
    'level_min': 40,
    'level_max': 54,
    'barrel_min1': 1000,
    'barrel_max1': 10000,
    'level_min1': 40,
    'level_max1': 54,
    'vip': 5,
    'time': [['08:00:00', '13:00:00'], ['14:00:00', '21:00:00']],
    'gap': 10 * 60
})
