#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明
import functools

def int2(x, base = 2):
    return int(x, base)
print int2('1000000')

# 偏函数   
int2 = functools.partial(int, base=2)

print int2('101110101')
int

max2 = functools.partial(max, 10)
print max2(10, 1, 2, 3)