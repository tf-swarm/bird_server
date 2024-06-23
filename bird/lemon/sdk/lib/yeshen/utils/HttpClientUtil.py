# coding=utf-8
__author__ = 'pan'

import urllib
import urllib2


class HttpClientUtil(object):
    def __init__(self):
        pass

    @staticmethod
    def post(url, values):
        req = urllib2.Request(url, values)
        response = urllib2.urlopen(req)
        result = response.read()
        return result

    @staticmethod
    def get(url):
        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        return res