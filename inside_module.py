#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

import collections
# 定义数据类型 根据属性引用
Point = collections.namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
p.x
p.y
print isinstance(p, Point)
print isinstance(p, tuple)
# 高效实现插入和删除操作的双向列表，适合用于队列和栈
q = collections.deque(['a', 'b', 'c'])
q.append('x')
q.appendleft('y')
print q
# Key不存在时返回默认值
dd = collections.defaultdict(lambda: 'N/A')
dd['key1'] = 'abc'
print dd['key1']
print dd['key2']
# OrderedDict的Key会按照插入的顺序排列
od = collections.OrderedDict([('a', 1), ('b', 2), ('c', 3)])
print od
od['z'] = 1
od['y'] = 2
od['x'] = 3
print od
# Counter
c = collections.Counter()
for ch in 'programming':
    c[ch] = c[ch] + 1
print c