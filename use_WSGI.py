# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明
#!/usr/bin/env python

def application(environ, start_response):
    start_response('200 ok', [('Content-Type', 'text/html')])
    return '<h1>Hello, web! %s</h1>' % (environ['PATH_INFO'][1:] or 'test')

