#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

import sqlite3

conn = sqlite3.connect('test.db')

cursor = conn.cursor()

cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')

cursor.execute('insert into user(id, name) values(\'1\', \'Michael\')')

print cursor.rowcount

cursor.close()
conn.commit()
conn.close()