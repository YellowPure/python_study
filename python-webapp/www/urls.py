#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

from transwarp.web import get, post, view, ctx, interceptor, HttpError
from models import User, Blog, Comment

import os, re, time, base64, hashlib, logging


@view('test_users.html')
@get('/')
def test_users():
    users = User.find_all()
    return dict(users=users)

