#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-11-20

import os
import time
import json
import copy
from framework.helper import File


def action_build_shell(params, service_type):
    """生成process相关脚本"""
    # 生成启动脚本
    params['shell'] = []
    server = params['server']
    date_time = time.strftime("%Y-%m-%d")
    redis_key = params['redis_key']
    bin_dir = params['bin_dir']

    # 生成启动process脚本
    __make_process_start_script(params, server, date_time, redis_key, bin_dir)

    # if service_type == 'game':
    #     # 生成monitor脚本
    #     __make_monitor_script(params, date_time, redis_key)
    #
    #     # 生成dispatch脚本
    #     __make_dispatch_script(params, date_time, redis_key)

    # 生成启动全部脚本
    __make_start_all(params, date_time, service_type)

    # 生成停止process脚本
    __make_process_stop_script(params, server, date_time)

    # 生成停止全部脚本
    __make_stop_all(params, date_time, redis_key, service_type)

    if service_type == 'game':
        # 生成iptable脚本
        # __make_iptable_script(params, date_time)

        # 生成清理缓存脚本
        __make_redis_clear(params, server, date_time)

    del params['shell']


def __make_process_start_script(params, server, date_time, redis_key, bin_dir):
    # 生成启动脚本
    fpath = os.path.join(params['template_dir'], 'start.sh')
    shell_start_template = File.read_file(fpath)
    fpath_py = os.path.join(params['template_dir'], 'start-py.sh')
    shell_start_template_py = File.read_file(fpath_py)
    for process in server['process']:
        if process.get('local') == 1 and process['type'] in server['startup']:
            log_conf = process['log_conf']
            listen_port = process['port']
            process['proc_key'] = "%s:%s:%s" % (redis_key, listen_port, process['id'])
            if process.get('lang') == 'bin':
                svrd, so = __get_svrd_and_so(params, server, process)
                ext_param = so or {}
                ext_param = json.dumps(ext_param)
                s = shell_start_template % (date_time, params['service_file'], bin_dir, svrd, log_conf,
                                            process['proc_key'], server['id'], process['log_file'], ext_param)
            else:
                svrd = 'lemon/framework/service.py'
                s = shell_start_template_py % (date_time, params['service_file'], bin_dir, svrd, log_conf,
                                               process['proc_key'], process['log_file'])
            fname = "start-" + process['shell_key']
            File.write_file(params['shell_dir'], fname, s)
            params['shell'].append(os.path.join(params['shell_dir'], fname))


def __make_process_stop_script(params, server, date_time):
    # 生成停止脚本
    fpath = os.path.join(params['template_dir'], 'stop.sh')
    shell_stop_template = File.read_file(fpath)
    for process in server['process']:
        if process.get('local') == 1 and process['type'] in server['startup']:
            s = shell_stop_template % (date_time, params['service_file'], process['proc_key'], params['bin_dir'])
            fname = "kill-" + process['shell_key']
            File.write_file(params['shell_dir'], fname, s)
            params['shell'].append(os.path.join(params['shell_dir'], fname))


def __make_monitor_script(params, date_time, redis_key):
    log_path = os.path.join(params['log_dir'], params['monitor_key'] + '.log')
    shell_template = '''
#!/usr/bin/env bash
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: %s

export service_file=%s
export bin_dir=%s
export redis_key=%s
export log_path=%s
export PYTHONPATH=${bin_dir}/script:${bin_dir}/lemon

. ${bin_dir}/script/template/base.sh

log "cd ${bin_dir}/script/python"
cd ${bin_dir}/script/python
log "pypy monitor.py ${redis_key} ${log_path}"
nohup pypy monitor.py ${redis_key} ${log_path} > /dev/null 2>&1 &
    ''' % (date_time, params['service_file'], params['bin_dir'], redis_key, log_path)
    fname = "start-" + params['monitor_key'] + '.sh'
    File.write_file(params['shell_dir'], fname, shell_template)
    params['shell'].append(os.path.join(params['shell_dir'], fname))


def __make_dispatch_script(params, date_time, redis_key):
    log_path = os.path.join(params['log_dir'], params['dispatch_key'] + '.log')
    shell_template = '''
#!/usr/bin/env bash
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: %s

export service_file=%s
export bin_dir=%s
export redis_key=%s
export log_path=%s
export PYTHONPATH=${bin_dir}/script:${bin_dir}/lemon

. ${bin_dir}/script/template/base.sh

log "cd ${bin_dir}/script/python"
cd ${bin_dir}/script/python
log "pypy dispatch.py ${redis_key} ${log_path}"
nohup pypy dispatch.py ${redis_key} ${log_path} > /dev/null 2>&1 &
    ''' % (date_time, params['service_file'], params['bin_dir'], redis_key, log_path)
    fname = "start-" + params['dispatch_key'] + '.sh'
    File.write_file(params['shell_dir'], fname, shell_template)
    params['shell'].append(os.path.join(params['shell_dir'], fname))


def __make_iptable_script(params, date_time):
    shell_template = '''
#!/usr/bin/env bash
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: %s

export service_file=%s

%s
''' % (date_time, params['service_file'], '\n'.join(params['iptable']))
    fname = 'config-iptable.sh'
    File.write_file(params['shell_dir'], fname, shell_template)
    params['shell'].append(os.path.join(params['shell_dir'], fname))


def __make_redis_clear(params, server, date_time):
    fpath = os.path.join(params['template_dir'], 'redis-cache-clear.sh')
    shell_clear_cache = File.read_file(fpath)
    cache_redis = server['redis']['cache']
    s = shell_clear_cache % (date_time, params['service_file'], params['bin_dir'], cache_redis['host'],
                             cache_redis['port'], cache_redis['db'])
    File.write_file(params['shell_dir'], 'redis-cache-clear.sh', s)
    params['clear_script'] = os.path.join(params['shell_dir'], 'redis-cache-clear.sh')


def __make_start_all(params, date_time, service_type):
    if params['shell']:
        shell_template = '''
#!/usr/bin/env bash
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: %s

export service_file=%s

sh %s
    ''' % (date_time, params['service_file'], '\nsh '.join(params['shell']))
        fname = 'start-%s-all.sh' % service_type
        File.write_file(params['shell_dir'], fname, shell_template)
        params['shell'].append(os.path.join(params['shell_dir'], fname))
        params['start_script'] = os.path.join(params['shell_dir'], fname)


def __make_stop_all(params, date_time, redis_key, service_type):
    if params['shell']:
        fpath = os.path.join(params['template_dir'], 'stop.sh')
        shell_stop_template = File.read_file(fpath)

        # 生成停止全部脚本
        s = shell_stop_template % (date_time, params['service_file'], redis_key, params['bin_dir'])
        fname = 'kill-%s-all.sh' % service_type
        File.write_file(params['shell_dir'], fname, s)
        params['shell'].append(os.path.join(params['shell_dir'], fname))
        params['kill_script'] = os.path.join(params['shell_dir'], fname)


def __get_svrd_and_so(params, server, process):
    conf = server['exe'][process['type']]
    exe = os.path.basename(conf['bin'])
    if 'so' in conf:
        so = copy.deepcopy(conf['so'])
        for _, sos in so.iteritems():
            for t, path in sos.iteritems():
                sos[t] = os.path.join(params['bin_dir'], os.path.basename(path))
    else:
        so = {}

    return exe, so


def game_build_shell(params):
    action_build_shell(params, 'game')


def sdk_build_shell(params):
    action_build_shell(params, 'sdk')

def cdkey_build_shell(params):
    action_build_shell(params, 'cdkey')


def shell_build_shell(params):
    action_build_shell(params, 'shell')

def yyb_build_shell(params):
    action_build_shell(params, 'yyb')
