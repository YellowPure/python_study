#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

import base64, sys
print base64.b64encode('binary\x00string')
t = base64.urlsafe_b64encode('i\xb7\x1d\xfb\xef\xff')
print t
print base64.urlsafe_b64decode(t)


def safe_b64decode(str):
    length = len(str) % 4
    if length == 0:
        return base64.b64decode(str)
    else:
        for i in range(4 - int(length)):
            str = str + '='
        return base64.b64decode(str)


if __name__ == '__main__':
    print safe_b64decode(sys.argv[1])
