# -*- coding=utf-8 -*-

a = """

05-07 00:18:12.646991 | D | 0000000002fb95c8 | ==== SEND TCP TO SERVER[1000]: 12009F14 '\x10\x101001341\x10{"info":{"config":[{"id":1,"name":"\\u666e\\u901a\\u62bd\\u5956","limit":0,"formula":{"201":[10000,10000],"202":[10000,10000],"203":[10000,10000]},"reward":[{"coupon":2},{"diamond":10},{"diamond":5},{"chip":1000},{"chip":500},{"chip":200}]},{"id":2,"name":"\\u9752\\u94dc\\u62bd\\u5956","limit":10000,"formula":{"201":[100000,100000],"202":[100000,100000],"203":[100000,100000]},"reward":[{"coupon":5},{"diamond":25},{"diamond":10},{"chip":100000},{"chip":50000},{"chip":10000}]},{"id":3,"name":"\\u767d\\u94f6\\u62bd\\u5956","limit":100000,"formula":{"201":[1000000,1000000],"202":[1000000,1000000],"203":[1000000,1000000]},"reward":[{"coupon":15},{"diamond":50},{"props":[{"id":211,"count":1}]},{"chip":300000},{"chip":200000},{"chip":100000}]},{"id":4,"name":"\\u9ec4\\u91d1\\u62bd\\u5956","limit":300000,"formula":{"201":[3000000,3000000],"202":[3000000,3000000],"203":[3000000,3000000]},"reward":[{"coupon":25},{"diamond":100},{"props":[{"id":212,"count":1}]},{"chip":500000},{"chip":400000},{"chip":300000}]},{"id":5,"name":"\\u767d\\u91d1\\u62bd\\u5956","limit":500000,"formula":{"201":[5000000,5000000],"202":[5000000,5000000],"203":[5000000,5000000]},"reward":[{"coupon":50},{"diamond":250},{"props":[{"id":213,"count":1}]},{"chip":1000000},{"chip":800000},{"chip":500000}]},{"id":6,"name":"\\u81f3\\u5c0a\\u62bd\\u5956","limit":1000000,"formula":{"201":[10000000,10000000],"202":[10000000,10000000],"203":[10000000,10000000]},"reward":[{"coupon":100},{"diamond":500},{"props":[{"id":214,"count":1}]},{"chip":2000000},{"chip":1500000},{"chip":1000000}]}],"pool":0,"progress":[0,5]}}'

"""


a.replace('\\\\', '\\')
print a.decode('unicode_escape')

