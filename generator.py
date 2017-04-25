#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明
# pylint: disable=C0103
# 生成器
g = (x*x for x in range(11))

for n in g:
    pass

def fib(max):
    n, a, b = 0, 0, 1
    while n<max:
        yield b
        a, b = b, a + b
        n = n + 1

for n in fib(6):
    print n

def odd():
    print 'step 1'
    yield 1
    print 'step 2'
    yield 3
    print 'step 3'
    yield 5

o = odd()
o.next()
o.next()
o.next()
o.next()
