#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

from transwarp.web import get, post, view, ctx, interceptor, HttpError
from models import User, Blog, Comment

import os, re, time, base64, hashlib, logging
from apis import api, APIError, APIPermissionError, APIResourceNotFoundError, APIValueError
from config import configs

_RE_MD5 = re.compile(r'^[0-9a-f]{32}$')
_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')

_COOKIE_KEY = configs.session.secret

_COOKIE_NAME = 'awesession'

@view('blogs.html')
@get('/')
def test_users():
    users = User.find_all()
    blogs = Blog.find_all()
    return dict(blogs=blogs, users=users)
    return dict(users=users)

@view('signin.html')
@get('/signin')
def signin():
    return dict()

@view('signout.html')
@get('/signout')
def signout():
    ctx.response.delete_cookie(_COOKIE_NAME)
    raise HttpError.seeother('/')

# @view('blogs.html')
# @get('/blog')
# def blog():
#     blogs = Blog.find_all()

#     user = User.find_first('where email=?', 'admin@example.com')
#     return dict(blogs=blogs, user=user)

@view('register.html')
@get('/register')
def register():
    return dict()

@api
@get('/api/users')
def api_get_users():
    users = User.find_by('order by created_at desc')
    for u in users:
        u.password = '******'
    return dict(users=users)


@api
@post('/api/users')
def register_user():
    i = ctx.request.input(name='', email='', password='')
    name = i.name.strip()
    email = i.email.strip().lower()
    password = i.password
    logging.info('xxxxxxxxxxxxxxxxxxxxx %s %s %s' % (name, email, password))
    if not name:
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not password or not _RE_MD5.match(password):
        raise APIValueError('password')
    user = User.find_first('where email=?', email)
    if user:
        raise APIError('register:failed', 'email', 'Email is already exist.')
    user = User(name=name, password=password, email=email, image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email).hexdigest())
    user.insert()

    # make session cookie
    cookie = make_signed_cookie(user.id, user.password, None)
    ctx.response.set_cookie(_COOKIE_NAME, cookie)
    return user

@api
@post('/api/authenticate')
def authenticate():
    i = ctx.request.input(remember='')
    email = i.email.strip().lower()
    logging.info('ctx.request.email %s' % email)
    password = i.password
    remember = i.remember
    user = User.find_first('where email=?', email)
    if user is None:
        raise APIError('auth:Failed', 'email', 'Invalid email')
    elif user.password != password:
        raise APIError('auth:failed', 'password', 'Invalid password')
    max_age = 604800 if remember=='true' else None
    cookie = make_signed_cookie(user.id, user.password, max_age)
    ctx.response.set_cookie(_COOKIE_NAME, cookie, max_age=max_age)
    user.password = '******'
    return user

def make_signed_cookie(id, password, max_age):
    '''
    计算加密cookie:
    '''
    expires = str(int(time.time() + (max_age or 86400)))
    L = [id, expires, hashlib.md5('%s-%s-%s-%s' % (id, password, expires, _COOKIE_KEY)).hexdigest()]
    return '-'.join(L)

@interceptor('/')
def user_interceptor(next):
    user = None
    cookie = ctx.request.cookies.get(_COOKIE_NAME)
    if cookie:
        user = parse_signed_cookie(cookie)
    ctx.request.user = user
    return next()

@interceptor('/manage/')
def manage_interceptor(next):
    user = ctx.request.user
    if user and user.admin:
        return next()
    raise HttpError.seeother('/signin')


def parse_signed_cookie(cookie_str):
    '''
    解密cookie:
    '''
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        id, expires, md5 = L
        if (int(expires) < time.time()):
            return None
        user = User.get(id)
        if user is None:
            return None
        if md5 != hashlib.md5('%s-%s-%s-%s' % (id, user.password, expires, _COOKIE_KEY)).hexdigest():
            return None
        return user
    except:
        return None

def check_admin():
    user = ctx.request.user
    if user and user.admin:
        return
    raise APIPermissionError('No permission')
