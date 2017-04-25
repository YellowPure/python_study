#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明
import functools

def log(func):
    def wrapper(*args, **kw):
        print 'call %s():' % func.__name__
        return func(*args, **kw)
    return wrapper
# @log
# def now():
#     print '2016-3-12'
# now()

def logg(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print 'begin %s call' % (func.__name__)
            # return func(*args, **kw)
            func(*args, **kw)
            print 'end call'
        return wrapper
    return decorator

@logg('execute')
def noww():
    print '201666'

noww()