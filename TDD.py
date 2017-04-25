#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

import unittest

class Dict(dict):
    def __init__(self, **kw):
        super(Dict, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' Object has no attribute '%s' " % key)
    def __setattr__(self, key, value):
        self[key] = value   

class TestDict(unittest.TestCase):
    def test_init(self):
        d = Dict(a = 1, b = 'test')
        self.assertEquals(d.a, 1)
        self.assertEquals(d.b, 'test')
        self.assertTrue(isinstance(d, Dict))
    def test_key(self):
        d = Dict()
        d['key'] = 'value'
        self.assertEquals(d.key, 'value')
    def test_attr(self):
        d = Dict()
        d.key = 'value'
        self.assertTrue('key' in d)
        self.assertEquals(d['key'], 'value')
    def test_keyerror(self):
        d = Dict()
        with self.assertRaises(KeyError):
            value = d['empty']
    def test_attrerror(self):
        d = Dict()
        with self.assertRaises(AttributeError):
            value = d.empty
    def setUp(self):
        print 'setUp...'
    def tearDown(self):
        print 'tearDown...'
    
if __name__ == '__main__':
    unittest.main()