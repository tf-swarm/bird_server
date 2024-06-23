#!/usr/bin/env bash
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-08-19

real_file_name=`readlink -f ${0}`
SHELL_DIR=$(cd `dirname ${real_file_name}`; pwd)
DEST_DIR=${SHELL_DIR}
if [ "${1}" != "" ]; then
    DEST_DIR=${1}
fi

ports=(6379 6380 6381 6382 6383 6384 6385 6386 6387 6400 6401 6402 6403)

# make config
for ((i=0; i < ${#ports[@]}; i++))
do
    port=${ports[$i]}
    pypy ${SHELL_DIR}/make-redis.py slave 172.31.95.15 ${port} 172.31.95.14 ${port}
done

# make dir
mkdir -p ${DEST_DIR}/conf
mkdir -p ${DEST_DIR}/log
mkdir -p ${DEST_DIR}/rdb

mv slave-*.conf ${DEST_DIR}/conf

# stop
for ((i=0; i < ${#ports[@]}; i++))
do
    port=${ports[$i]}
    ps -ef | grep redis-server | grep ":${port}" | awk '{print "kill " $2}' | sh
done

# check
while true; do
    declare -i left=0
    for ((i=0; i < ${#ports[@]}; i++))
    do
        port=${ports[$i]}
        left=${left}+`ps -ef | grep redis-server | grep -c ":${port}"`
    done
    if [ ${left} -eq 0 ]; then
        break
    fi
done

# start
cd ${DEST_DIR}/rdb
for ((i=0; i < ${#ports[@]}; i++))
do
    port=${ports[$i]}
    redis-server ${DEST_DIR}/conf/slave-${port}.conf
done
