#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

# 定制类
class Student(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'Student object (name:%s)' % self.name
    __repr__ = __str__

class Fib(object):
    def __init__(self):
        self.a, self.b = 0, 1
    # 添加遍历
    def __iter__(self):
        return self
    
    def next(self):
        self.a, self.b = self.b, self.a + self.b
        if self.a > 10000:
            raise StopIteration()
        return self.a
    # 添加下标取元素
    def __getitem__(self, n):
        if isinstance(n, int):
            a, b = 1, 1
            for x in range(n):
                a, b = b, a + b
            return a
        # 添加切片
        if isinstance(n, slice):
            start = n.start
            stop = n.stop
            a, b = 1, 1
            L = []
            for x in range(stop):
                if x >= start:
                    L.append(a)
                a, b = b, a + b
        return L
    
    def __getattr__(self, attr):
        if attr=='score':
            return 
    def __call__(self):
        print ('my name is %s' % self.name)

for n in Fib():
    print n

f = Fib()
f()
print f.score
print f[10]

print f[1:10]
# print Student('Micheal')
