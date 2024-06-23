# coding=utf-8
__author__ = 'pan'


class YSBaseEntity(object):
    def __init__(self):
        pass

    def dict_to_object(self, entries):
        self.__dict__.update(entries)

    def convert_to_dict(self):
        # 把Object对象转换成Dict对象
        obj_dict = {}
        obj_dict.update(self.__dict__)
        return obj_dict