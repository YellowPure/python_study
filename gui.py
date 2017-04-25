# -*- coding: utf-8 -*- 
# 文件里有非ASCII字符，需要在第一行或第二行指定编码声明
#!/usr/bin/env python

from Tkinter import *
import tkMessageBox

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
    
    def createWidgets(self):
        self.helloLabel = Label(self, text='hello world')
        self.helloLabel.pack()
        self.nameInput = Entry(self)
        self.nameInput.pack()
        self.alertBtn = Button(self, text='hello', command=self.hello)
        self.alertBtn.pack()
        self.quiteButton = Button(self, text='Quit', command=self.quit)
        self.quiteButton.pack()
    
    def hello(self):
        name = self.nameInput.get() or 'world'
        tkMessageBox.showinfo('Message', 'Hello %s' % name)
        
app = Application()
app.master.title('hello world!')
app.mainloop()