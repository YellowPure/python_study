#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

def calc_sum(*args):
    ax = 0
    def sum():
        ax = 0
        for a in args:
            ax += a
        return ax
    return sum
f = calc_sum(1,3,5,7,9)
print f
print f()