#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明


# try:
#     f = open('./test.txt', 'r')
#     print f.read()
# finally:
#     if f:
#         f.close()
# 替代方法
with open('./test.txt', 'r') as f:
    # 不能确文件大小时，反复调用read(size)
    # print f.read(4)
    for line in f.readlines():
        print line.strip()
    f.close()
    
with open('./test.txt', 'w') as f:
    f.write('hello world')
    f.close()