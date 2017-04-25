#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

# 切片操作符

list = [1, 2, 3, 4, 5]

print list[0:3]

print list[-1:]

L = range(100)

print L[:10]

print L[10:20]

print L[:10:2]

tu = (1,2,3,4,5)

print tu[:3]

str = 'ABCDEFG'
print str[::3]

