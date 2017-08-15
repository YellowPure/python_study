#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

import sqlite3


# # 创建一个Cursor
# conn = sqlite3.connect('test.db')
# cursor = conn.cursor()

# cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')

# cursor.execute('insert into user(id, name) values(\'1\', \'Michael\')')
# # 通过rowcount获得插入的行数:
# print cursor.rowcount

# cursor.close()
# conn.commit()
# conn.close()


try:
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('select * from user where name=?', ('1',))
    values = cursor.fetchall()
    print values
except sqlite3.Error as e:
    print e
finally:
    cursor.close()
    conn.close()
