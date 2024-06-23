#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-07-28

import re


class NumberFilter(object):
    TYPE_UNKNOWN = 0
    TYPE_AAAAA = 1
    TYPE_ABCDE = 2
    TYPE_EDCBA = 3
    TYPE_ABABAB = 4
    TYPE_ABCABC = 5
    TYPE_ABCDABCD = 6
    TYPE_AABBCC = 7
    TYPE_AAABBB = 8
    TYPE_ABBBBB = 9

    def __init__(self):
        self.min_aaaaa = 4
        self.min_abcde = 5
        self.min_edcba = 5
        self.min_ababab = 3
        self.min_abcabc = 2
        self.min_abcdabcd = 2
        self.min_aabbcc = 3
        self.min_aaabbb = 2
        self.min_abbbb = 4

        # AAAAA
        pattern = r'^(\d)\1{%d,}$' % (self.min_aaaaa - 1)
        self.re_aaaaa = re.compile(pattern)
        # ABCDE
        pattern = r'^(?:0(?=1)|1(?=2)|2(?=3)|3(?=4)|4(?=5)|5(?=6)|6(?=7)|7(?=8)|8(?=9)){%d,}\d$' % (self.min_abcde - 1)
        self.re_abcde = re.compile(pattern)
        # EDCBA
        pattern = r'^(?:9(?=8)|8(?=7)|7(?=6)|6(?=5)|5(?=4)|4(?=3)|3(?=2)|2(?=1)|1(?=0)){%d,}\d$' % (self.min_edcba - 1)
        self.re_edcba = re.compile(pattern)
        # ABABAB
        pattern = r'^((\d)[^\2])\1{%d,}$' % (self.min_ababab - 1)
        self.re_ababab = re.compile(pattern)
        self.min_ababab *= 2
        # ABCABC
        pattern = r'^((\d)([^\2])[^\2\3])\1{%d,}$' % (self.min_abcabc - 1)
        self.re_abcabc = re.compile(pattern)
        self.min_abcabc *= 3
        # ABCDABCD
        pattern = r'^((\d)([^\2])([^\2\3])[^\2\3\4])\1{%d,}$' % (self.min_abcdabcd - 1)
        self.re_abcdabcd = re.compile(pattern)
        self.min_abcdabcd *= 4
        # AABBCC
        pattern = r'^((\d)\2){%d,}$' % self.min_aabbcc  # 会匹配AAAAAA, 由于上面已经过滤, 这里不再考虑
        self.re_aabbcc = re.compile(pattern)
        self.min_aabbcc *= 2
        # AAABBB
        pattern = r'^((\d)\2\2){%d,}$' % self.min_aaabbb  # 会匹配AAAAAA, 由于上面已经过滤, 这里不再考虑
        self.re_aaabbb = re.compile(pattern)
        self.min_aaabbb *= 3
        # ABBBB
        pattern = r'^(\d)([^\1])\2{%d,}$' % (self.min_abbbb - 1)
        self.re_abbbb = re.compile(pattern)
        self.min_abbbb += 1

    def check_number(self, number):
        if isinstance(number, (unicode, str)):
            number = int(number)

        if isinstance(number, (int, long)):
            number = str(number)

        if not isinstance(number, str):
            return self.TYPE_UNKNOWN

        if self.__is_aaaaa(number):
            return self.TYPE_AAAAA
        if self.__is_abcde(number):
            return self.TYPE_ABCDE
        if self.__is_edcba(number):
            return self.TYPE_EDCBA
        if self.__is_ababab(number):
            return self.TYPE_ABABAB
        if self.__is_abcabc(number):
            return self.TYPE_ABCABC
        if self.__is_abcdabcd(number):
            return self.TYPE_ABCDABCD
        if self.__is_aabbcc(number):
            return self.TYPE_AABBCC
        if self.__is_aaabbb(number):
            return self.TYPE_AAABBB
        if self.__is_abbbb(number):
            return self.TYPE_ABBBBB
        return self.TYPE_UNKNOWN

    def __is_aaaaa(self, number):
        if self.min_aaaaa > len(number):
            return False
        return self.re_aaaaa.search(number)

    def __is_abcde(self, number):
        if self.min_abcde > len(number):
            return False
        return self.re_abcde.search(number)

    def __is_edcba(self, number):
        if self.min_edcba > len(number):
            return False
        return self.re_edcba.search(number)

    def __is_ababab(self, number):
        if self.min_ababab > len(number):
            return False
        return self.re_ababab.search(number)

    def __is_abcabc(self, number):
        if self.min_abcabc > len(number):
            return False
        return self.re_abcabc.search(number)

    def __is_abcdabcd(self, number):
        if self.min_abcdabcd > len(number):
            return False
        return self.re_abcdabcd.search(number)

    def __is_aabbcc(self, number):
        if self.min_aabbcc > len(number):
            return False
        return self.re_aabbcc.search(number)

    def __is_aaabbb(self, number):
        if self.min_aaabbb > len(number):
            return False
        return self.re_aaabbb.search(number)

    def __is_abbbb(self, number):
        if self.min_abbbb > len(number):
            return False
        return self.re_abbbb.search(number)


NumberFilter = NumberFilter()

if __name__ == '__main__':
    # print NumberFilter.check_number(1111111111)
    # print NumberFilter.check_number(123456)
    # print NumberFilter.check_number(654321)
    # print NumberFilter.check_number(121212)
    # print NumberFilter.check_number(123123123)
    # print NumberFilter.check_number(12341234)
    # print NumberFilter.check_number(112233)
    # print NumberFilter.check_number(111222)

    start = 1000000
    while start < 9999999:
        if NumberFilter.check_number(start):
            print start
        start += 1
