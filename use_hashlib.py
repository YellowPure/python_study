#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

import hashlib, time
md5 = hashlib.md5()
md5.update('how to use md5 in python hashlib?')
print md5.hexdigest()

sha1 = hashlib.sha1()
sha1.update('how to use md5 in python hashlib?')
print sha1.hexdigest()

db = {
    'michael': 'e10adc3949ba59abbe56e057f20f883e',
    'bob': '878ef96e86145580c38c87f0410ad153',
    'alice': '99b1c2188db85afee403b1536010c2c9'
}


def get_md5(str):
    md5 = hashlib.md5()
    md5.update(str)
    return md5.hexdigest()


def calc_md5(password):
    return get_md5(password + 'the-salt')


def login(user, password):
    p = get_md5(password)
    for i in db:
        if i == user and p == db[i]:
            return True
    return False


def register(username, password):
    db[username] = calc_md5(password + username + 'the-salt')


# print calc_md5( raw_input())
print login(raw_input(), raw_input())