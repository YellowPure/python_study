#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

def my_abs(num):
    if not (isinstance(num, (int, float))):
        raise TypeError('wrong type')
    if  num>=0:
        return num
    else :
        return -num

res = my_abs(123)

def nx(x, n = 2):
    s = 1
    while n > 0:
        n = n - 1
        s = s * x
    return s

res1 = nx(5, 3)

# 默认参数
# 默认参数必须指向不变对象！

def roll(name, gender, age=6, city='Beijing'):
    print 'name:', name
    print 'gender:', gender
    print 'age: ', age
    print 'city:', city

roll('lilei','F')
print("result is %d and %d" % (res, res1))

# 可变参数
def calc(numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    print 'sum: ',  sum

calc((1, 3, 5, 7, 9))

def calc1(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    print 'sum: ', sum

calc1()

# 关键字参数

def person (name, age, **kw):
    print 'name:', name
    print 'age:', age
    print 'other:', kw
person('mark', 35, city='Beig') 

# 递归函数

def fact(n):
    if n == 1:
        return 1
    s =  n * fact(n-1)
    print 's = %d' % s
    return s
fact(5)

# 尾递归优化

def fact1(n):
    return fact_iter(n, 1)

def fact_iter(n, product):
    if n == 1:
        return product
    print n, product
    return fact_iter(n-1, n * product)

fact1(5)
