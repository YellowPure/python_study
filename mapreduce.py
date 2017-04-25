# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明
# pylint: disable=C0103

# map/reduce

def func(x):
    return x * x


print map(func, range(10))
print map(str, range(10))

def func1(x, y):
    return x*y
print reduce(func1, range(1,6,2))

def char2num(s):
        return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]
print map(char2num, '123')

def fn(x, y):
    print x, y
    return x * 10 + y
print reduce(fn, [1,2,3])

# practice

def Letter(string):
    return string.capitalize()

print map(Letter, ['adam', 'LISA', 'barT'])

def prod(x, y):
    return x * y
print reduce(prod, [1,2,3,4,5])