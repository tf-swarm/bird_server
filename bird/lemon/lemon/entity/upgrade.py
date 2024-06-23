#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-04-26


class Upgrade(object):
    no_need_upgrade = 0
    prompt_upgrade = 1
    force_upgrade = 2

    def check_version(self, version):
        try:
            self.__split(version)
            return True
        except Exception, e:
            return False

    def __split(self, version):
        #primary, little, release
        strArr = version.split('.')
        primary = int(strArr[0])
        little = int(strArr[1])
        release = int(strArr[2])
        return primary, little, release

    def cmp_version(self, left, right):
        left_info = self.__split(left)
        right_info = self.__split(right)
        for l, r in zip(left_info, right_info):
            if l < r:
                return -1
            elif l > r:
                return 1

        return 0


Upgrade = Upgrade()
