# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明
#!/usr/bin/env python

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/signin', methods=['GET'])
def signin_form():
    return render_template('form.html')

@app.route('/signin', methods=['POST'])
def signin():
    # 从form表单读取内容
    username = request.form['username']
    password = request.form['password']
    if request.form['username']=='admin' and request.form['password']=='password':
        return render_template('signok.html', username = username)
    return render_template('form.html', message='bad username or passowrd', username = username)

if __name__ == '__main__':
    app.run()
