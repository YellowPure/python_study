#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

import time, threading

def loop():
    print 'thread %s is running...' % threading.current_thread().name
    n = 0
    while n<5:
        n = n+1
        print 'thread %s >>> %s' % (threading.current_thread().name, n)
        time.sleep(1)
    print 'thread %s is ended' % threading.current_thread().name

print 'thread %s is running...' % threading.current_thread().name
t = threading.Thread(target=loop, name='LoopThread')
t.start()
t.join()
print 'thread %s end' % threading.current_thread().name

balance = 0
lock = threading.Lock()

def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n


def run_thread(n):
    for i in range(10000):
        # 先要获取锁:
        lock.acquire()
        try:
            change_it(n)
        finally:
            # 改完了一定要释放锁:
            lock.release()
