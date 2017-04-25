#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

# 列表生生成式

print [x * x for x in range(1, 11)]

print [ m + n for m in 'ABC' for n in 'XYZ']

print [ str(k) + '=' + v for k,v in enumerate('abc')]


L = ['Hello', 'World', 18, 'Apple', None]
print [  s.lower() for s in L if isinstance(s, str) == True]
