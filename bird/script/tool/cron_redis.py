#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-08-20

import os
import sys
import redis
# import scp
# import paramiko
import time
import shutil


def log(*args):
    prefix = time.strftime('%Y-%m-%d %H:%M:%S')
    msg = [str(arg) for arg in args]
    print '%s | %s' % (prefix, ' '.join(msg))


try:
    redis_host = sys.argv[1]
    redis_port = sys.argv[2]
    src_dir = sys.argv[3]
    dst_dir = sys.argv[4]

    log(redis_host, redis_port, src_dir, dst_dir)

    r = redis.StrictRedis(host=redis_host, port=int(redis_port))
    # get rdb
    now_ts = int(time.time())
    now_str = time.strftime('%Y%m%d%H%M%S')
    r.bgsave()
    time.sleep(1)

    # check bgsave process
    count = 500
    while count > 0:
        last_ts = r.execute_command('lastsave')
        log('now_ts:', now_ts, 'last_ts:', last_ts)
        if last_ts >= now_ts:
            break
        time.sleep(3)
        count -= 1
    else:
        raise Exception('bgsave timeout, must check now')
    src_file = os.path.join(src_dir, 'dump-%s.rdb' % redis_port)
    dst_file = os.path.join(dst_dir, 'dump-%s-%s.rdb' % (redis_port, now_str))
    shutil.copy(src_file, dst_file)
    log('copy', src_file, dst_file)
    src_file = os.path.join(src_dir, 'dump-%s.aof' % redis_port)
    dst_file = os.path.join(dst_dir, 'dump-%s-%s.aof' % (redis_port, now_str))
    shutil.copy(src_file, dst_file)
    log('copy', src_file, dst_file)
except Exception, e:
    import traceback

    traceback.print_exc()
