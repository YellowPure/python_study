#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明


def reversed_cmp(x, y):
    if x > y:
        return -1
    if x < y:
        return 1
    return 0
print sorted([36,17,222,8,100], reversed_cmp)
