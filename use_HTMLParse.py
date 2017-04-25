#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明

import HTMLParser
import htmlentitydefs
import urllib

# class MyHTMLParser(HTMLParser.HTMLParser):
#     def handle_starttag(self, tag, attrs):
#         print '<%s>' % tag

#     def hanle_endtag(self, tag):
#         print '</%s>' % tag

#     def handle_startendtag(self, tag, attrs):
#         print '<%s/>' % tag

#     def handle_data(self, data):
#         print 'data'

#     def handle_comment(self, data):
#         print '<!-- -->'

#     def handle_entityref(self, name):
#         print '&%s;' % name

#     def handle_charref(self, name):
#         print '&#%s;' % name

# parser = MyHTMLParser()
# parser.feed('<html><head></head><body><p>Some <a href=\"#\">html</a> tutorial...<br>END</p></body></html>')


class MeetingHTMLParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self._events = dict()
        self._count  = 0
        self._cur_ele = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'h3' and attrs.__contains__(('class', 'event-title')):
            self._count +=1
            self._events[self._count] = dict()
            self._cur_ele = 'event-title'
        if tag == 'time':
            self._cur_ele = 'time'
        if tag == 'span' and attrs.__contains__(('class', 'event-location')):
            self._cur_ele = 'event-location'
        
    def handle_data(self, data):
        if self._cur_ele == 'event-title':
            self._events[self._count][self._cur_ele] = data
        if self._cur_ele == 'time':
            self._events[self._count][self._cur_ele] = data
        if self._cur_ele == 'event-location':
            self._events[self._count][self._cur_ele] = data
        self._cur_ele = ''
    def show_list(self):
        print '关于Python的会议有：%s 个,具体如下： ' % str(self._count)
        for event in self._events.values():
            print event['event-title'],'\t', event['time'], '\t', event['event-location']
try :
    url = 'https://www.python.org/events/python-events/'
    html = urllib.urlopen(url)
    html_str = html.read()
    parser = MeetingHTMLParser()
except IOError:
    print 'IOError'
else :
    parser.feed(html_str)
    parser.show_list()
