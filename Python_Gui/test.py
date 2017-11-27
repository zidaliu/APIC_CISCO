#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from Tkinter import *

root = Tk()


# 按扭调用的函数，
def reg():
    User = e_user.get()
    Pwd = e_pwd.get()
    len_user = len(User)
    len_pwd = len(Pwd)
    if User == '111' and Pwd == '222':
        l_msg['text'] = '登陆成功'
    else:
        l_msg['text'] = '用户名或密码错误'
        e_user.delete(0, len_user)
        e_pwd.delete(0, len_pwd)


# 第一行，用户名标签及输入框
l_user = Label(root, text='用户名：')
l_user.grid(row=0, sticky=W)
e_user = Entry(root)
e_user.grid(row=0, column=1, sticky=E)

# 第二行，密码标签及输入框
l_pwd = Label(root, text='密码：')
l_pwd.grid(row=1, sticky=W)
e_pwd = Entry(root)
e_pwd['show'] = '*'
e_pwd.grid(row=1, column=1, sticky=E)

# 第三行登陆按扭，command绑定事件
b_login = Button(root, text='登陆', command=reg)
b_login.grid(row=2, column=1, sticky=E)

# 登陆是否成功提示
l_msg = Label(root, text='')
l_msg.grid(row=3)

root.mainloop()