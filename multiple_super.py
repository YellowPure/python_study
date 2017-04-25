#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

# 多重继承，一个子类就可以同时获得多个父类的所有功能
class Animal(object):
    pass

class Mammal(Animal):
    pass

class Runnable(object):
    pass

class Flyable(object):
    pass

class Bird(Animal):
    pass

class Dog(Mammal, Runnable):
    pass

class Bat(Mammal, Flyable):
    pass

class Parrot(Bird, Flyable):
    pass

class Ostrich(Bird, Runnable):
    pass


