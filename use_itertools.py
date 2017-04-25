#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

import itertools
# 无限序列
# itertools.count

ns = itertools.repeat('A', 10)
for i in ns:
    print i

natuals = itertools.count()
ns = itertools.takewhile(lambda x: x <= 10, natuals)
for n in ns:
    print n

# chain 把一组迭代对象串联起来，形成一个更大的迭代器
for c in itertools.chain('ABC', 'DEF'):
    print c

r = map(lambda x: x * x, [1, 2, 3])
print r
r = itertools.imap(lambda x: x * x, [1, 2, 3])
print r
for i in r:
    print i