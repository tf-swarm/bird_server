#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-07-06

import os
import sys


def write_file(fname, data):
    with open(fname, 'w') as f:
        f.write(data)

def main():
    """
    Usage: pypy {script_name} (master|slave) redis_ip redis_port [master_redis_ip] [master_redis_port]
    """
    try:
        redis_type = sys.argv[1]
        file_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(file_path)
        script_dir = os.path.dirname(script_dir)
        template_file = os.path.join(script_dir, 'template/redis-%s.conf' % redis_type)
        with open(template_file) as f:
            template_data = f.read()
        if redis_type == 'master':
            kvs = {
                'redis_ip': sys.argv[2],
                'redis_port': int(sys.argv[3]),
            }
            data = template_data.format(**kvs)
            fname = os.path.join(os.getcwd(), '%s-%s.conf' % (redis_type, sys.argv[3]))
            write_file(fname, data)
            print 'make conf success:', fname
        elif redis_type == 'slave':
            kvs = {
                'redis_ip': sys.argv[2],
                'redis_port': int(sys.argv[3]),
                'master_redis_ip': sys.argv[4],
                'master_redis_port': int(sys.argv[5]),
            }
            data = template_data.format(**kvs)
            fname = os.path.join(os.getcwd(), '%s-%s.conf' % (redis_type, sys.argv[3]))
            write_file(fname, data)
            print 'make conf success:', fname
        else:
            print main.__doc__.format(script_name=sys.argv[0])
    except IOError, e:
        raise
    except Exception, e:
        print main.__doc__.format(script_name=sys.argv[0])

if __name__ == '__main__':
    main()
