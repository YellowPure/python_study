#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

# 迭代
from collections import Iterable

d = {'a': 1, 'b': 2, 'c': 3}
n = 123
print isinstance(n, Iterable)
for i,v in d.iteritems():
    print i,v

for i,v in enumerate([4,5,6]):
    print i,v