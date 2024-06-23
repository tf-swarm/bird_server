#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-09-23

import os
from cffi import FFI

path = os.path.split(os.path.realpath(__file__))[0]
ffi = FFI()
# 引入动态库
lib = ffi.dlopen(path + "/libframework.so")
print('Loaded lib {0}'.format(lib))
# 函数声明，类似于C的.h文件
ffi.cdef(
    '''
    void rsa_decrypt(char* pristr, char* pubkey, int padding, char* pubstr);
    int printf(const char* format, ...);
    '''
)
# 公钥
pkey_str = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC2kcrRvxURhFijDoPpqZ/IgPlA
gppkKrek6wSrua1zBiGTwHI2f+YCa5vC1JEiIi9uw4srS0OSCB6kY3bP2DGJagBo
Egj/rYAGjtYJxJrEiTxVs5/GfPuQBYmU0XAtPXFzciZy446VPJLHMPnmTALmIOR5
Dddd1Zklod9IQBMjjwIDAQAB
-----END PUBLIC KEY-----'''
# 用私钥加密过的字符串
pri_str = "klzAd6Qu87M/0GdkmmeJbyk/NKuIIRS/M/4GpckMNfe4jwjBc9w38LExpYVvJZ5RKkr2y9Wuj6cZsThqAM0ZDcFZ2Ew2csRZlMnc9kD/yqHHMb0fb6KL3g7DZ3sRAhAIT2MkTDHOVKctxrc5Qcn8Ie2IX1Xgz7G+yvn0j1VYc3xGUbbCxxPjb3MTuDUDFbElPNq98dQufrcFUBsXwVdQJv6+GwE+7N/IJffPA6TNv3aB+AUe7sc/lbKOywxCSb0+rxPkb0mcT6q5O0S1bRIvZqtxQJn0HydqmFYPBYr9X2lzkgGIwZL8oX6vb2YVNHRPoCxKh+10TewAOOlUggbTfA=="
# 申请C风格的数组
pub_str = ffi.new("char[]", 256)
lib.rsa_decrypt(pri_str, pkey_str, 1, pub_str)
print pub_str
lib.printf("%s\n", pub_str)
# 转换成Python可用的字符串
pystr = ffi.string(pub_str)
print pystr, len(pystr)
pystr = ffi.buffer(pub_str)[:]
print pystr, len(pystr)
