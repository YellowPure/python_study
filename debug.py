#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

import logging
logging.basicConfig(level=logging.INFO)

# 使用print调试
#  python>> >>> n = 0
def foo1(s):
    n = int(s)
    print '>>> n = %d' % n
    return 10 / n

# foo1('0')

# 使用断言assert调试
# python>> ZeroDivisionError: integer division or modulo by zero
def foo2(s):
    n = int(s)
    assert '>>> n = %d' % n
    return 10 / n
# foo2('0')

def foo3(s):
    n = int(s)
    logging.info('n = %d' % n)
    return 10 / n
# foo3('0')

# 使用pdb调试 python -m pdb error.py
# l 查看代码
# n 单步执行代码
# p 变量名 查看变量
# q 结束调试

import pdb

s = '0'
n = int(s)
pdb.set_trace()
print 10/n

# http://www.jetbrains.com/pycharm/ 调试IDE