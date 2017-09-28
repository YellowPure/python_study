#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

from transwarp.web import get, post, view, ctx, interceptor, HttpError
from models import User, Blog, Comment

import os, re, time, base64, hashlib, logging
from apis import api

@view('test_users.html')
@get('/')
def test_users():
    users = User.find_all()
    return dict(users=users)

@view('blogs.html')
@get('/blog')
def blog():
    blogs = Blog.find_all()

    user = User.find_first('where email=?', 'admin@example.com')
    return dict(blogs=blogs, user=user)

@api
@get('/api/users')
def api_get_users():
    users = User.find_by('order by created_at desc')
    for u in users:
        u.password = '******'
    return dict(users = users)