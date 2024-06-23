#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-23

from lemon.games.bird.quick import BirdQuick
from lemon.games.bird.game import BirdGame
from lemon.games.bird.entity import BirdEntity
from lemon.games.bird.account import BirdAccount
from lemon.games.bird.registry import BirdRegistry
from lemon.games.bird.http import BirdHttp
from lemon.games.bird.shell import BirdShell

class_map = {
    'quick': BirdQuick,
    'game': BirdGame,
    'registry': BirdRegistry,
    'entity': BirdEntity,
    'account': BirdAccount,
    'http': BirdHttp,
    'shell': BirdShell,
}
