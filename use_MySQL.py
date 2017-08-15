#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

import mysql.connector

conn = mysql.connector.connect(user='root', password='admin', database='test',use_unicode=True)
cursor = conn.cursor()

# cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
cursor.execute('insert into user (id,name) values (%s, %s)', ['1', 'Michael'])

print cursor.rowcount

conn.commit()
cursor.close()

cursor = conn.cursor()

cursor.execute('select * from user where id = %s', ('1',))
values = cursor.fetchall()
values

cursor.close()

conn.close()