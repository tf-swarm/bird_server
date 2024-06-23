#!/usr/bin/env bash
# -*- coding=utf-8 -*-

# Author: 易思龙 <ixxoo.me@gmail.com>
# Create: 2015-05-29

SHELL_FOLDER=$(cd `dirname ${0}`; pwd)
cd ${SHELL_FOLDER}
make

# export LD_LIBRARY_PATH=`pwd`
# gcc main.c -o main -L./ -lframework -lcrypto
