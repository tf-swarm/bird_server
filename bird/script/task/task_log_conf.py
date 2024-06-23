#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-05-06

import os
from framework.helper import File


def action_log_conf(params):
    """生成process对应log配置文件"""
    fpath = os.path.join(params['template_dir'], 'log4cplus.conf')
    data = File.read_file(fpath)
    File.make_dirs(params['log_dir'])
    server = params['server']
    for process in server['process']:
        log_key = process['log_key']
        network_log = os.path.join(params['log_dir'], 'network-%s.log' % log_key)
        bi_log = os.path.join(params['log_dir'], 'bi-%s.log' % log_key)
        common_log = os.path.join(params['log_dir'], '%s.log' % log_key)
        log_conf = log_key + '.conf'
        if process.get('lang') == 'bin':
            kvs = {
                'network_log': network_log,
                'network_format': '%D{%m-%d %H:%M:%S.%q} | %m%n',
                'bi_log': bi_log,
                'bi_format': '%D{%m-%d %H:%M:%S.%q} | %m%n',
                'common_log': common_log,
                'common_format': '%D{%m-%d %H:%M:%S.%q} | %m%n',
            }
            File.write_file(params['bin_dir'], log_conf, data.format(**kvs))
        process['log_conf'] = log_conf
        process['network_log_file'] = network_log
        process['bi_log_file'] = bi_log
        process['log_file'] = common_log

    # params['monitor_key'] = '%s-monitor' % server['name']
    # params['dispatch_key'] = '%s-dispatch' % server['name']


game_log_conf = action_log_conf
sdk_log_conf = action_log_conf
shell_log_conf = action_log_conf
cdkey_log_conf = action_log_conf
yyb_log_conf = action_log_conf
