#!/usr/bin/env bash
# -*- coding=utf-8 -*-

#  Author: 易思龙 <ixxoo.me@gmail.com>
#  Create: 2015-05-29

declare -i total=${1}

LEMON_HOME=/home/happybirds/server/bird/bird/lemon
TEST_HOME=/home/happybirds/server/bird/bird/script
export PYTHONPATH=${TEST_HOME}:${LEMON_HOME}

redis-cli -p 6379 hmset game.2.hash.info "official.div.base.202" 20000000
count=0
total=1

while  [ ${count} -lt ${total} ]; do
    ((count++))
    echo -e " ******************************************loop ${count}******************************************"
    #pypy bird_ab.py
    pypy bird_stat.py 20001 20500 > ${count}.log
    sleep 2
done
