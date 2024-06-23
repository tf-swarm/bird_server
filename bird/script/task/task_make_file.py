#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-05-11

# import os
import commands
from framework.helper import Log
from framework.helper import File


def game_make_file(params):
    """编译文件"""
    # if params['server']['corporation'] != 'langang':
    #     cmd = 'sh %s' % os.path.join(params['src_dir'], 'make.sh')
    #     Log.log(cmd)
    #     status, output = commands.getstatusoutput(cmd)
    #     if status:  # 编译失败
    #         Log.log('编译失败!!')
    #         Log.log(output)
    #         return status
    #
    # bin_so = []
    # for _, item in params['server']['exe'].iteritems():
    #     if 'bin' in item:
    #         bin_so.append(item['bin'])
    #     if 'so' in item:
    #         for _, sos in item['so'].iteritems():
    #             for _, so in sos.iteritems():
    #                 bin_so.append(so)
    #
    # for target in bin_so:
    #     cmd = 'cp -f %s %s' % (os.path.join(params['src_dir'], target), params['bin_dir'])
    #     Log.log(cmd)
    #     status, output = commands.getstatusoutput(cmd)
    #     if status:
    #         Log.log(output)
    #         return status

    # 编译so
    compile_path = params['src_dir']
    make_file_list = File.find_py_files(compile_path, 'make.sh')
    for msh in make_file_list:
        cmd = 'sh %s/%s' % (compile_path, msh)
        Log.log('编译SO文件:', msh)
        status, output = commands.getstatusoutput(cmd)
        if status != 0:
            Log.log('ERROR !!', '工程so文件编译失败:', compile_path)
            Log.log(output)
            return status


sdk_make_file = game_make_file
shell_make_file = game_make_file
cdkey_make_file = game_make_file
yyb_make_file = game_make_file
