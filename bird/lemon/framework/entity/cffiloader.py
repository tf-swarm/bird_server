#!/usr/bin/env python
# -*- coding=utf-8 -*-

# Author: likebeta <ixxoo.me@gmail.com>
# Create: 2016-09-26

import os
import cffi
from framework.util.tool import Time
from framework.util.log import Logger


class CFFILoader(object):
    def __init__(self):
        self.fw_lib = None
        self.fw_ffi = None

    def load_lib(self, lib_name, py_file, folder):
        start = Time.current_ms()
        lib_path = os.path.dirname(py_file) + '/' + folder + '/'
        cdef_file = os.path.abspath(lib_path + 'cdef.h')
        ffi = cffi.FFI()
        with open(cdef_file) as f:
            csource = f.read()
            ffi.cdef(csource)

        if not lib_name.endswith('.so'):
            lib_name = 'lib%s.so' % lib_name

        so_file = os.path.abspath(lib_path + lib_name)
        Logger.info('load exits so ->', so_file)
        lib = ffi.dlopen(so_file)
        end = Time.current_ms()
        Logger.info('load so use time %d ms' % (end - start))
        return lib, ffi

    def load_framework_cffi(self):
        if self.fw_lib:
            return self.fw_lib, self.fw_ffi

        lib_c, ffi = self.load_lib('framework', __file__, '/framework_cffi/')
        self.fw_lib = lib_c
        self.fw_ffi = ffi
        return lib_c, ffi


CFFILoader = CFFILoader()
