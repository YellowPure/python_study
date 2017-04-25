#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# list
classmates = ['Michael', 'Bob', 'Lucy']
classmates.append('Lily')
print classmates
classmates.insert(2, 'bily')
print classmates
classmates.pop(1)
print classmates, 'len is %d' % len(classmates)

# tuple 不可变数组 

classmates1 = ('bob', 'fani', 'lur')
print classmates1
# 每个元素指向不变 其中的list本身可改变
classmates2 = ('bb', 'tt', ['a', 'b'])
classmates2[2][1] = 'x'
classmates2[2][0] = 'y'
print classmates2

sum = ''
for item in classmates:
    sum += item
print sum
sum1 = 0
for i in range(100):
    sum1+=i
print sum1

birth = input(raw_input('birth:'))
if birth > 2000:
    print True
else:
    print False

