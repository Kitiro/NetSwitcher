# -*- coding: utf-8 -*-

import platform
from switcher import *
from tkinter import *

from tkinter import ttk
from tkinter import messagebox as msg

def checkSystem():
    if platform.system() != 'Windows':
        msg.showwarning("警告", "非Windows系统暂无法使用。")
        return 1
    return 0

if platform.system() != 'Windows':
    print('error')

top = Tk()
screenwidth = top.winfo_screenwidth()
screenheight = top.winfo_screenheight()
width, height = 300, 100
top.geometry('%dx%d+%d+%d'%(width, height, (screenwidth-width)/2, (screenheight-height)/2))

top.title('Network Switcher v2.0')
top.resizable(0, 0)

if checkSystem():
    exit()
    
# 加载网络信息
switcher = Switcher()

if len(switcher.interfaces) > 2:
    check_msg = f'检测到本地存在多个网卡接口：{",".join(list(switcher.interfaces))}。 请选择两个需要进行对换的接口名，一般为WLAN和以太网，且不能选择同一个接口。'
    msg.showinfo(title='Welcome NetSwitcher', message=check_msg)

def freqQuestion():
    question = f'1. 缺少管理员权限。\n2. 没有检测到网卡接口。\n3. 系统卡顿。'
    msg.showinfo(title='导致失败的常见问题', message=question)

def contactMe():
    contact = f'邮箱：kitiro1874@163.com\n使用中有任何问题，请直接邮箱联系我。'
    msg.showinfo(title='如何联系我', message=contact)


def get_pairs():
    return [interface_box1.get(), interface_box2.get()]


def update():
    names = get_pairs()
    switcher.update_pairs(names)
    switcher.get_net()
    interface_status = [switcher.net_info[switcher.pairs[i]]['isEnabled']+', '+switcher.net_info[switcher.pairs[i]]['isConnected'] for i in range(2)]
    interface_status_label1['text'] = interface_status[0]
    interface_status_label2['text'] = interface_status[1]


def switch():
    names = get_pairs()
    if names[0] == names[1]:
        msg.showwarning("警告", "选择的两个接口为同一接口，请调整为不同接口再进行操作。")
        return
    switcher.switch()
    update()

# 菜单栏
main_menu = Menu(top)
main_menu.add_command(label='常见问题', command=freqQuestion)
main_menu.add_command(label='联系我', command=contactMe)


inter1= Label(top, text="接口1")
inter1.grid(row=1, column=1)
inter2= Label(top, text="接口2")
inter2.grid(row=2, column=1)

# 接口复选框
interface_box1 = ttk.Combobox(top, values=switcher.interfaces, width=15)
interface_box1.grid(row=1, column=2)
# interface_box1['value'] = switcher.interfaces
interface_box1.current(0)
interface_box2 = ttk.Combobox(top, values=switcher.interfaces, width=15)
interface_box2.grid(row=2, column=2)
interface_box2.current(1)


# 接口启用状态
interface_status = [switcher.net_info[switcher.pairs[i]]['isEnabled']+', '+switcher.net_info[switcher.pairs[i]]['isConnected'] for i in range(2)]
interface_status_label1 = Label(top, text=interface_status[0])
interface_status_label1.grid(row=1, column=3)
interface_status_label2 = Label(top, text=interface_status[1])
interface_status_label2.grid(row=2, column=3)

refresh_btn = Button(top, text='刷新', command=update)
refresh_btn.grid(row=4, column=2)
refresh_btn.configure(height = 1, width = 10) 

switch_btn = Button(top, text='切换', command=switch)
switch_btn.grid(row=4, column=3)
switch_btn.configure(height = 1, width = 10) 

# 我的名字！
cr= Label(top, text="c.r. Kitiro")
cr.grid(row=5,column=3,sticky=SE)

top.config(menu=main_menu)
top.mainloop()