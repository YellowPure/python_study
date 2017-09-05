#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明
"""
这是一个简单的， 轻量级的， WSGI兼容(Web Server Gateway Interface)的web 框架
WSGI概要：
    工作方式： WSGI server -----> WSGI 处理函数
    作用：将HTTP原始的请求、解析、响应 这些交给WSGI server 完成，
          让我们专心用Python编写Web业务，也就是 WSGI 处理函数
          所以WSGI 是HTTP的一种高级封装。
    例子：
        wsgi 处理函数
            def application(environ, start_response):
                method = environ['REQUEST_METHOD']
                path = environ['PATH_INFO']
                if method=='GET' and path=='/':
                return handle_home(environ, start_response)
                if method=='POST' and path='/signin':
                return handle_signin(environ, start_response)
        wsgi server
            def run(self, port=9000, host='127.0.0.1'):
                from wsgiref.simple_server import make_server
                server = make_server(host, port, application)
                server.serve_forever()
设计web框架的原因：
    1. WSGI提供的接口虽然比HTTP接口高级了不少，但和Web App的处理逻辑比，还是比较低级，
       我们需要在WSGI接口之上能进一步抽象，让我们专注于用一个函数处理一个URL，
       至于URL到函数的映射，就交给Web框架来做。
设计web框架接口：
    1. URL路由： 用于URL 到 处理函数的映射
    2. URL拦截： 用于根据URL做权限检测
    3. 视图： 用于HTML页面生成
    4. 数据模型： 用于抽取数据（见models模块）
    5. 事物数据：request数据和response数据的封装（thread local）
"""

import types, os, re, cgi, sys, time, datetime, functools, mimetypes, threading, logging, traceback, urllib

from db import Dict
import utils

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


#################################################################
# 实现事物数据接口, 实现request 数据和response数据的存储,
# 是一个全局ThreadLocal对象
#################################################################
ctx = threading.local()


_RE_RESPONSE_STATUS = re.compile(r'^\d\d\d(\ [\w\ ]+)?$')
_HEADER_X_POWERED_BY = ('X-Powered-By', 'transwarp/1.0')

# 用于时区转换
_TIMEDELTA_ZERO = datetime.timedelta(0)
_RE_TZ = re.compile('^([\+\-])([0-9]{1,2})\:([0-9]{1,2})$')

# response status
_RESPONSE_STATUSES = {
    # Informational
    100: 'Continue',
    101: 'Switching Protocols',
    102: 'Processing',

    # Successful
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    203: 'Non-Authoritative Information',
    204: 'No Content',
    205: 'Reset Content',
    206: 'Partial Content',
    207: 'Multi Status',
    226: 'IM used',

    # Redirection
    300: 'Multiple Choices',
    301: 'Moved Permanently',
    302: 'Found',
    303: 'See Other',
    304: 'Not Modified',
    305: 'Use Proxy',
    307: 'Temporary Redirect',

    # Client Error
    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    406: 'Not Acceptable',
    407: 'Proxy Authentication Required',
    408: 'Request Timeout',
    409: 'Conflict',
    410: 'Gone',
    411: 'Length Required',
    412: 'Precondition Failed',
    413: 'Request Entity Too Large',
    414: 'Request URI Too Long',
    415: 'Unsupported Media Type',
    416: 'Requested Range Not Satisfiable',
    417: 'Expectation Failed',
    418: "I'm a teapot",
    422: 'Unprocessable Entity',
    423: 'Locked',
    424: 'Failed Dependency',
    426: 'Upgrade Required',

    # Server Error
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout',
    505: 'HTTP Version Not Supported',
    507: 'Insufficient Storage',
    510: 'Not Extended'
}

_RESPONSE_HEADERS = {
    'Accept-Ranges',
    'Age',
    'Allow',
    'Cache-Control',
    'Connection',
    'Content-Encoding',
    'Content-Language',
    'Content-Length',
    'Content-Location',
    'Content-MD5',
    'Content-Disposition',
    'Content-Range',
    'Content-Type',
    'Date',
    'ETag',
    'Expires',
    'Last-Modified',
    'Link',
    'Location',
    'P3P',
    'Pragma',
    'Proxy-Authenticate',
    'Refresh',
    'Retry-After',
    'Server',
    'Set-Cookie',
    'Strict-Transport-Security',
    'Trailer',
    'Transfer-Encoding',
    'Vary',
    'Via',
    'Warning',
    'WWW-Authenticate',
    'X-Frame-Options',
    'X-XSS-Protection',
    'X-Content-Tytpe-Options',
    'X-Forwarded-Proto',
    'X-Powered-By',
    'X-UA-Compatible'
}

class UTC(datetime.tzinfo):
    """
    tzinfo 是一个基类，用于给datetime对象分配一个时区
    使用方式是 把这个子类对象传递给datetime.tzinfo属性
    传递方法有2种：
        １.　初始化的时候传入
            datetime(2009,2,17,19,10,2,tzinfo=tz0)
        ２.　使用datetime对象的 replace方法传入，从新生成一个datetime对象
            datetime.replace(tzinfo= tz0）
    >>> tz0 = UTC('+00:00')
    >>> tz0.tzname(None)
    'UTC+00:00'
    >>> tz8 = UTC('+8:00')
    >>> tz8.tzname(None)
    'UTC+8:00'
    >>> tz7 = UTC('+7:30')
    >>> tz7.tzname(None)
    'UTC+7:30'
    >>> tz5 = UTC('-05:30')
    >>> tz5.tzname(None)
    'UTC-05:30'
    >>> from datetime import datetime
    >>> u = datetime.utcnow().replace(tzinfo=tz0)
    >>> l1 = u.astimezone(tz8)
    >>> l2 = u.replace(tzinfo=tz8)
    >>> d1 = u - l1
    >>> d2 = u - l2
    >>> d1.seconds
    0
    >>> d2.seconds
    28800
    """

    def __init__(self, utc):
        utc = str(utc.strip().upper())
        mt = _RE_TZ.match(utc)
        if mt:
            minus = mt.group(1) == '-'
            h = int(mt.group(2))
            m = int(mt.group(3))
            if minus:
                h, m = (-h), (-m)
            self._utcoffset = datetime.timedelta(hours=h, minutes=m)
            self._tzname = 'UTC%s' % utc
        else:
            raise ValueError('bad utc time zone')
    
    def utcoffset(self, dt):
        """
        表示与标准时区的 偏移量
        """
        return self._utcoffset

    def dst(self, dt):
        """
        Daylight Saving Time 夏令时
        """
        return _TIMEDELTA_ZERO

    def tzname(self, dt):
        """
        所在时区的名字
        """
        return self._tzname

    def __str__(self):
        return 'UTC timezone info object (%s)' % self._tzname

    __repr__ = __str__

UTC_0 = UTC('+00:00')

# 用于异常处理
class _HttpError(Exception):
    """
    HttpError that defines http error code.
    >>> e = _HttpError(404)
    >>> e.status
    '404 Not Found'
    """
    def __init__(self, code):
        """
        Init an HttpError with response code.
        """
        super(_HttpError, self).__init__()
        self.status = '%d %s' % (code, _RE_RESPONSE_STATUSES[code])
        self._headers = None
    
    def header(self, name, value):
        """
        添加header， 如果header为空则 添加powered by header
        """
        if not self._headers:
            self._headers = [_HEADER_X_POWERED_BY]
        self._headers.append((name, value))
    
    @property
    def headers(self):
        """
        使用setter方法实现的 header属性
        """
        if hasattr(self, '_headers'):
            return self._headers
        return []

    def __str__(self):
        return self.status

    __repr__ = __str__

class _RedirectError(_HttpError):
    """
    RedirectError that defines http redirect code.
    >>> e = _RedirectError(302, 'http://www.apple.com/')
    >>> e.status
    '302 Found'
    >>> e.location
    'http://www.apple.com/'
    """
    def __init__(self, code, location):
        """
        Init an HttpError with response code.
        """
        super(_RedirectError, self).__init__(code)
        self.location = self.location
    
    def __str__(self):
        return '%s, %s' % (self.status, self.location)

    __repr__ = __str__

class HttpError(object):
    """
    HTTP Exceptions
    """
    @staticmethod
    def badrequest():
        """
        Send a bad request response.
        >>> raise HttpError.badrequest()
        Traceback (most recent call last):
          ...
        _HttpError: 400 Bad Request
        """
        return _HttpError(400)

    @staticmethod
    def unauthorized():
        """
        Send an unauthorized response.
        >>> raise HttpError.unauthorized()
        Traceback (most recent call last):
          ...
        _HttpError: 401 Unauthorized
        """
        return _HttpError(401)

    @staticmethod
    def forbidden():
        """
        Send a forbidden response.
        >>> raise HttpError.forbidden()
        Traceback (most recent call last):
          ...
        _HttpError: 403 Forbidden
        """
        return _HttpError(403)

    @staticmethod
    def notfound():
        """
        Send a not found response.
        >>> raise HttpError.notfound()
        Traceback (most recent call last):
          ...
        _HttpError: 404 Not Found
        """
        return _HttpError(404)

    @staticmethod
    def internalerror():
        """
        Send an internal error response.
        >>> raise HttpError.internalerror()
        Traceback (most recent call last):
          ...
        _HttpError: 500 Internal Server Error
        """
        return _HttpError(500)
    
    @staticmethod
    def redirect(location):
        """
        Do permanent redirect.
        >>> raise HttpError.redirect('http://www.itranswarp.com/')
        Traceback (most recent call last):
          ...
        _RedirectError: 301 Moved Permanently, http://www.itranswarp.com/
        """
        return _RedirectError(301, location)

    @staticmethod
    def found(location):
        """
        Do temporary redirect.
        >>> raise HttpError.found('http://www.itranswarp.com/')
        Traceback (most recent call last):
          ...
        _RedirectError: 302 Found, http://www.itranswarp.com/
        """
        return _RedirectError(302, location)

    @staticmethod
    def seeother(location):
        """
        Do temporary redirect.
        >>> raise HttpError.seeother('http://www.itranswarp.com/')
        Traceback (most recent call last):
          ...
        _RedirectError: 303 See Other, http://www.itranswarp.com/
        >>> e = HttpError.seeother('http://www.itranswarp.com/seeother?r=123')
        >>> e.location
        'http://www.itranswarp.com/seeother?r=123'
        """
        return _RedirectError(303, location)

_RESPONSE_HEADER_DICT = dict(zip(map(lambda x: x.upper(), _RESPONSE_HEADERS), _RESPONSE_HEADERS))

class Request(object):
    """
    请求对象， 用于获取所有http请求信息。
    """
    def __init__(self, environ):
        """
        environ  wsgi处理函数里面的那个 environ
        wsgi server调用 wsgi 处理函数时传入的
        包含了用户请求的所有数据
        """
        self._environ = environ

    def _parse_input(self):
        """
        将通过wsgi 传入过来的参数，解析成一个字典对象 返回
        比如： Request({'REQUEST_METHOD':'POST', 'wsgi.input':StringIO('a=1&b=M%20M&c=ABC&c=XYZ&e=')})
            这里解析的就是 wsgi.input 对象里面的字节流
        """
        def _convert(item):
            if isinstance(item, list):
                return [utils.to_unicode(i.value) for i in item]
            if item.filename:
                return MultipartFile(item)
            return utils.to_unicode(item.value)
        fs = cgi.FieldStorage(fp=self._environ['wsgi.input'], environ=self._environ, keep_blank_values=True)
        inputs = dict()
        for key in fs:
            inputs[key] = _convert(fs[key])
        return inputs

    def _get_raw_input(self):
        """
        将从wsgi解析出来的 数据字典，添加为Request对象的属性
        然后 返回该字典
        """
        if not hasattr(self, '_raw_input'):
            self._raw_input = self._parse_input()
        return self._raw_input

    def __getitem__(self, key):
        """
        实现通过键值访问Request对象里面的数据，如果该键有多个值，则返回第一个值
        如果键不存在，这会 raise KeyError
        >>> from StringIO import StringIO
        >>> r = Request({'REQUEST_METHOD':'POST', 'wsgi.input':StringIO('a=1&b=M%20M&c=ABC&c=XYZ&e=')})
        >>> r['a']
        u'1'
        >>> r['c']
        u'ABC'
        >>> r['empty']
        Traceback (most recent call last):
            ...
        KeyError: 'empty'
        >>> b = '----WebKitFormBoundaryQQ3J8kPsjFpTmqNz'
        >>> pl = ['--%s' % b, 'Content-Disposition: form-data; name=\\"name\\"\\n', 'Scofield', '--%s' % b, 'Content-Disposition: form-data; name=\\"name\\"\\n', 'Lincoln', '--%s' % b, 'Content-Disposition: form-data; name=\\"file\\"; filename=\\"test.txt\\"', 'Content-Type: text/plain\\n', 'just a test', '--%s' % b, 'Content-Disposition: form-data; name=\\"id\\"\\n', '4008009001', '--%s--' % b, '']
        >>> payload = '\\n'.join(pl)
        >>> r = Request({'REQUEST_METHOD':'POST', 'CONTENT_LENGTH':str(len(payload)), 'CONTENT_TYPE':'multipart/form-data; boundary=%s' % b, 'wsgi.input':StringIO(payload)})
        >>> r.get('name')
        u'Scofield'
        >>> r.gets('name')
        [u'Scofield', u'Lincoln']
        >>> f = r.get('file')
        >>> f.filename
        u'test.txt'
        >>> f.file.read()
        'just a test'
        """
        r = self._get_raw_input()[key]
        if isinstance(r, list):
            return r[0]
        return r

    
    def get(self, key, default=None):
        """
         实现了字典里面的get功能
        和上面的__getitem__一样(request[key]),但如果没有找到key,则返回默认值。
        >>> from StringIO import StringIO
        >>> r = Request({'REQUEST_METHOD':'POST', 'wsgi.input':StringIO('a=1&b=M%20M&c=ABC&c=XYZ&e=')})
        >>> r.get('a')
        u'1'
        >>> r.get('empty')
        >>> r.get('empty', 'DEFAULT')
        'DEFAULT'
        """
        r = self._get_raw_input().get(key, default)
        if isinstance(r, list):
            return r[0]
        return r

    def gets(self, key):
        '''
        Get multiple values for specified key.
        >>> from StringIO import StringIO
        >>> r = Request({'REQUEST_METHOD':'POST', 'wsgi.input':StringIO('a=1&b=M%20M&c=ABC&c=XYZ&e=')})
        >>> r.gets('a')
        [u'1']
        >>> r.gets('c')
        [u'ABC', u'XYZ']
        >>> r.gets('empty')
        Traceback (most recent call last):
            ...
        KeyError: 'empty'
        '''
        r = self._get_raw_input()[key]
        if isinstance(r, list):
            return r[:]
        return [r]

    def input(self):
        """
        返回一个由传入的数据和从environ里取出的数据 组成的Dict对象，Dict对象的定义 见db模块
        Get input as dict from request, fill dict using provided default value if key not exist.
        i = ctx.request.input(role='guest')
        i.role ==> 'guest'
        >>> from StringIO import StringIO
        >>> r = Request({'REQUEST_METHOD':'POST', 'wsgi.input':StringIO('a=1&b=M%20M&c=ABC&c=XYZ&e=')})
        >>> i = r.input(x=2008)
        >>> i.a
        u'1'
        >>> i.b
        u'M M'
        >>> i.c
        u'ABC'
        >>> i.x
        2008
        >>> i.get('d', u'100')
        u'100'
        >>> i.x
        2008
        """
        copy = Dict(**kw)
        raw = self._get_raw_input()
        for k,v in raw.iteritems():
            copy[k] = v[0] if isinstance(v, list) else v
        return copy

    def get_body(self):
         """
        从HTTP POST 请求中取得 body里面的数据，返回为一个str对象
        >>> from StringIO import StringIO
        >>> r = Request({'REQUEST_METHOD':'POST', 'wsgi.input':StringIO('<xml><raw/>')})
        >>> r.get_body()
        '<xml><raw/>'
        """
        fp = self._environ['wsgi.input']
        return fp.read()

    @property
    def remote_addr(self):
        """
        Get remote addr. Return '0.0.0.0' if cannot get remote_addr.
        >>> r = Request({'REMOTE_ADDR': '192.168.0.100'})
        >>> r.remote_addr
        '192.168.0.100'
        """
        return self._environ.get('REMOTE_ADDR', '0.0.0.0')

    @property
    def document_root(self):
        """
        Get raw document_root as str. Return '' if no document_root.
        >>> r = Request({'DOCUMENT_ROOT': '/srv/path/to/doc'})
        >>> r.document_root
        '/srv/path/to/doc'
        """
        return self._environ.get('DOCUMENT_ROOT', '')

    @property
    def query_string(self):
        """
        Get raw query string as str. Return '' if no query string.
        >>> r = Request({'QUERY_STRING': 'a=1&c=2'})
        >>> r.query_string
        'a=1&c=2'
        >>> r = Request({})
        >>> r.query_string
        ''
        """
        return self._environ.get('QUERY_STRING', '')

    @property
    def environ(self):
        """
        Get raw environ as dict, both key, value are str.
        >>> r = Request({'REQUEST_METHOD': 'GET', 'wsgi.url_scheme':'http'})
        >>> r.environ.get('REQUEST_METHOD')
        'GET'
        >>> r.environ.get('wsgi.url_scheme')
        'http'
        >>> r.environ.get('SERVER_NAME')
        >>> r.environ.get('SERVER_NAME', 'unamed')
        'unamed'
        """
        return self._environ

    @property
    def request_method(self):
        """
        Get request method. The valid returned values are 'GET', 'POST', 'HEAD'.
        >>> r = Request({'REQUEST_METHOD': 'GET'})
        >>> r.request_method
        'GET'
        >>> r = Request({'REQUEST_METHOD': 'POST'})
        >>> r.request_method
        'POST'
        """
        return self._environ['REQUEST_METHOD']

    def path_info(self):
        pass

    @property
    def headers(self):
        pass

    def cookie(self, name, default=None):
        pass


class Response(self):
    def set_header(self, key, value):
        pass

    def set_cookie(self, name, value, max_age=None, expires=None, path='/'):
        pass

    @property
    def status(self):
        pass

    @status.setter
    def status(self, value):
        pass


def get(path):
    pass


def post(path):
    pass


def view(path):
    pass


def interceptor(pattern):
    pass


class TemplateEngine(object):
    def __call__(self, path, model):
        pass


class Jinja2TemplateEngine(TemplateEngine):
    def __init__(self, templ_dir, **kw):
        from jinja2 import Environment, FileSystemLoader
        self._env = Environment(loader=FileSystemLoader(templ_dir), **kw)

    def __call__(self, path, model):
        return self._env.get_template(path).render(**model).encode('utf-8')


wsgi = WSGIApplication()

if __name__ == '__main__':
    wsgi.run()
else:
    application = wsgi.get_wsgi_application()


class WSGIApplication(object):
    def __init__(self, document_root=None, **kw):
        pass

    def add_url(self, func):
        pass

    def add_interceptor(self, func):
        pass

    @property
    def template_engine(self):
        pass

    @template_engine.setter
    def template_engine(self, engine):
        pass

    def get_wsgi_application(self):
        def wsgi(env, start_response):
            pass

    return wsgi

    def run(self, port=9000, host='127.0.0.1'):
        from wsgiref.simple_server import make_server
        server = make_server(host, port, self.get_wsgi_application())
        server.serve_forever()
