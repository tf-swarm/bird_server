#!/usr/bin/env bash
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2015-05-28

real_file_name=`readlink -f ${0}`
SHELL_DIR=$(cd `dirname ${real_file_name}`; pwd)
ulimit -c unlimited
LEMON_DIR=$(cd `dirname ${SHELL_DIR}`; pwd)/lemon
export PYTHONPATH=${LEMON_DIR}:${SHELL_DIR}
pypy ${SHELL_DIR}/main.py "cdkey" "$@"
_RET_=$?
exit ${_RET_}
