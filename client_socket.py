# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明
#!/usr/bin/env python

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 9999))
print s.recv(1024)
for data in ['Michael', 'Tracy', 'Sarah']:
    s.send(data)
    print s.recv(1024)

s.send('exit')
s.close()