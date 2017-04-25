#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

import types
from types import MethodType 

class Student(object):
    # 限制该class能添加的属性__slots__
    # __slots__ = ('name', 'score', '__age')
    def __init__(self, name, score, age):
        
        self.name = name
        self._score = score
        # 内部属性 __age
        # __xxx__ 特殊变量 可以直接访问
        self.__age = age
        
    @property
    def score(self):
        return self._score
    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100')
        self._score = value
    def print_score(self):
        print '%s''s score is %s' % (self.name, self.score)

s = Student('bart', 59, 8)
s.print_score()
s.score = 60
print s.score
def set_age(self, age):
    self.age = age
    return self.age
s.set_age = MethodType(set_age, s, Student)
print s.set_age(10)
# s.age = 8
# print s.__age

# 继承and多态
class Animal(object):
    def run(self):
        print 'Animal is running'

class Dog(Animal):
    def run(self):
        print 'dog is running'
class Cat(Animal):
    def run(self):
        print 'dog is running'
dog = Dog()
dog.run()
cat = Cat()
cat.run()
# 判断一个变量是否是某个类型可以用isinstance()判断
print isinstance(dog, Animal),isinstance(dog, Cat)

def tun_twice(animal):
    animal.run()
    animal.run()

tun_twice(dog)

# 获取对象信息
# 有一种类型就叫TypeType，所有类型本身的类型就是TypeType
type('123') == types.StringType
type(int) == type(str) == types.TypeType 

isinstance('a', str) # True
isinstance('a', (str, unicode))
# 获得一个对象的所有属性和方法
# print dir('ABC')
