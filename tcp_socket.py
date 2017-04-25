# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明
#!/usr/bin/env python

import socket
import threading, time


def tcplink(sock, addr):
    print 'new connection from %s:%s' % addr
    sock.send('welcome')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if data == 'exit' or not data:
            break
        sock.send('hello, %s!' % data)
    sock.close()
    print 'Connection from %s:%s closed.' % addr


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 9999))
s.listen(5)
print 'Waiting for connection...'
while True:
    sock, addr = s.accept()
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
