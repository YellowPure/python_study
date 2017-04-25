#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

import struct
def check_bmp(file_url):
    try:
        f = open(file_url, 'rb')
        s = f.read(30)
        unpack_s = struct.unpack('<ccIIIIIIHH', s);
        if unpack_s[0] == 'B' and unpack_s[1] == 'M':

            print 'bmp:Size(%s * %s) ColorNumber(%s)' % (unpack_s[6], unpack_s[7], unpack_s[8])
        else:
            print 'not bmp format'
    except IOError:
        print 'Error! Please input right filename'

if __name__ == '__main__':
    check_bmp('loading_01.png')
