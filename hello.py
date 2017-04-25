#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明
name = raw_input('please input you name:')
print 'hello, i\'m ok ' , name

# 多行字符串前面加r 字符串中符合默认补转义

print '''line1\'
line2
line3'''
# 10/3 =3 
print 10.0/3
print '中文'

print 'hello %s, have %d' % ('world', 100)