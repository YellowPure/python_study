#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

import multiprocessing
import copy_reg
import types
import os, time, random

# 进程间通信是通过Queue、Pipes等实现的。
# print 'Process (%s) start...' % os.getgid()
# fork调用一次 返回两次 window没有fork调用
# pid = os.fork()
# if pid == 0:
#     print 'i am child'
# else :
#     print 'i am creater'

def run_proc(name):
    print 'run child process %s (%s)...' % (name, os.getpid())

def long_time_task(name):
    print 'Run task %s (%s)...' % (name, os.getpid())
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print 'Task %s runs %.2f seconds.' % (name, (end - start))

# 写数据进程执行的代码
def write(q):
    for value in ['A', 'B', 'C']:
        print 'Put %s to queue' % value
        q.put(value)
        time.sleep(random.random())

# 读数据进程执行的代码
def read(q):
    while True:
        value = q.get(True)
        print 'Get %s from queue.' % value

if __name__ == '__main__':
    # print 'Parent process %s.' % os.getpid()
    # p = multiprocessing.Process(target=run_proc, args=('test',))
    # print 'Process will start'
    # p.start()
    # p.join()
    # print 'Process end.'

    # p = multiprocessing.Pool()
    # for i in range(5):
    #     p.apply_async(long_time_task, args=(1,))
    # print 'Waiting for all subprocesses done...'
    # p.close()
    # p.join()
    # print 'All subprocesses done'

    # 父进程创建Queue，并传给各个子进程:
    q = multiprocessing.Queue()
    pw = multiprocessing.Process(target=write, args=(q,))
    pr = multiprocessing.Process(target=read, args=(q,))
    # 启动子进程pw，写入:
    pw.start()
     # 启动子进程pr，读取:
    pr.start()
    # 等待pw结束:
    pw.join()
     # pr进程里是死循环，无法等待其结束，只能强行终止:
    pr.terminate()