#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

import logging

# 调用堆栈
def foo(s):
    return 10 / int(s)

def bar(s):
    return foo(s) * 2

def main():
    try:
        bar('0')
    except StandardError, e:
        logging.exception(e);

main()
print 'END'

# 定义错误
class FooError(StandardError):
    pass

def _foo(s):
    n = int(a)
    if n==0:
        raise FooError('invalid value: %s' % s)
    return 10 / n