#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

import os
print os.name
print os.path.abspath('.')
print os.path.splitext('path/to/file.txt')

# os.rename('test.txt', 'tet.txt')

print [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1] == '.py']

def search(s, dir = os.path.abspath('.')):
    for x in os.listdir(dir):
        path = os.path.join(dir, x)
        if os.path.isfile(x) and s in x:
            print x
        if os.path.isdir(x):
            search(s, path)

str = raw_input('input search key:')
search(str)