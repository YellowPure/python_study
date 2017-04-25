# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明
#!/usr/bin/env python

from email.mime.text import MIMEText
from email import encoders
from email.header import Header
from email.mime.multipart import MIMEMultipart
import email
from email.utils import parseaddr, formataddr
import smtplib


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((\
        Header(name, 'utf-8').encode(),\
        addr.encode('utf-8') if isinstance(addr,unicode) else addr
    ))

from_addr = raw_input('From:')
password = raw_input('password:')
# smtp_server = raw_input('SMTP server:')
# gmail的加密传输
smtp_server = 'smtp.gmail.com'
smtp_port = 587
to_addr = raw_input('To:')

# msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
# send html
# msg = MIMEText('<html><head><title>email</title></head><body><h1>Hello</h1><p><a href="http://python.org">python...</a></p></body></html>', 'html', 'utf-8')
# send file
msg = MIMEMultipart()
msg['From'] = _format_addr(u'Python developer<%s>' % from_addr)
msg['To'] = _format_addr(u'manager <%s>' % to_addr)
msg['Subject'] = Header(u'from SMTP hello...', 'utf-8').encode()
msg.attach(MIMEText('send with file...', 'plain', 'utf-8'))

with open('./code.jpg', 'rb') as f:
    mime = email.mime.base.MIMEBase('image','jpg',filename='code.png')
    mime.add_header('Content-Disposition','attachment',filename='code.png')
    mime.add_header('Content-ID','<0>')
    mime.add_header('X-Attachment-Id','0')
    mime.set_payload(f.read())
    encoders.encode_base64(mime)
    msg.attach(mime)

server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
