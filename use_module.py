#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

'a test module'
__author__ = 'h.love.pure'

import sys

def test():
    args = sys.argv
    if  len(args) == 1:
        print 'hello world'
    elif len(args) == 2:
        print 'hello, %s' % args[1]
    else:
        print 'too many arguments!'
print __name__
if __name__ == '__main__':
    test()

try:
    import cStringIO as StringIO
except ImportError :
    import StringIO

try:
    import json #python >=2.6
except ImportError:
    import simplejson as json # python <=2.5