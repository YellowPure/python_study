# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明
#!/usr/bin/env python

import poplib
import email
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

email = raw_input('Email:')
password = raw_input('Password:')
pop3_server = 'pop.163.com'
port = 995
server = poplib.POP3_SSL(pop3_server, 995)
print server.getwelcome()
server.set_debuglevel(1)
server.user(email)
server.pass_(password)
print 'Message: %s.Size: %s' % server.stat()

resp, mails, octets = server.list()
print mails
index = len(mails)

resp, lines, octets = server.retr(index)
msg_content = '\r\n'.join(lines)
msg = Parser().parsestr(msg_content)

server.quit()
