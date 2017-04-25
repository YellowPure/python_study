#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

try:
    import cPickle as pickle
except ImportError:
    import pickle
import json

d = dict(name='bob', age=28, score=88)
json.dumps(d)
json_str = '{"age": 20, "score": 88, "name": "Bob"}'
json.loads(json_str)

class Student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score
def student2dict(self):
    return {
        'name': self.name,
        'age': self.age,
        'score': self.score
    }
s = Student('Bob', 20, 88)

# print json.dumps(s, default=student2dict)

print json.dumps(s, default=lambda obj: obj.__dict__)

