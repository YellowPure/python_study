# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明
#!/usr/bin/env python

from wsgiref.simple_server import make_server

from use_WSGI import application

httpd = make_server('', 8000, application)

print 'Sering HTTP on port 8000...'

httpd.serve_forever()