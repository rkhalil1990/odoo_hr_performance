# -*- coding: utf-8 -*-

y = u'录入'
s = [u'\u5f55\u5165', u'\u884c\u53f7\u5f55\u5165', u'\u884c\u53f7\u9009\u62e9']
x = u'\u5f55\u5165'
print x.encode("utf8").decode('utf-8')
print y.encode('utf8')
print u'\u98de\u8f6c\u9080\u8bf7\u6392\u884c\u699c'.encode('utf-8')
print unicode('呵呵','utf-8')