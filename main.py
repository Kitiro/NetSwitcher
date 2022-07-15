# coding=utf-8

from __future__ import print_function
import ctypes, sys
import platform
from switcher import *
from tkinter import *

from tkinter import ttk
from tkinter import messagebox as msg

def checkSystem():
    if platform.system() != 'Windows':
        msg.showerror("错误", "非Windows系统暂无法使用。")
        return 1
    return 0

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
if not is_admin():
    if sys.version_info[0] == 3:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

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
    check_msg = f'检测到本地存在多个网卡接口：{", ".join(list(switcher.interfaces))}。 请选择两个需要进行对换的接口名，一般为WLAN和以太网，且不能选择同一个接口。'
    msg.showwarning(title='提醒', message=check_msg)

def freqQuestion():
    question = f'1. 缺少管理员权限。\n    将程序以管理员权限打开，或右键程序->属性->兼容性->以管理员身份运行此程序。\n2. 没有检测到需要的网卡接口。\n    可能由于适配器命名问题，建议在控制面板->网络和Internet->网络连接 中将需要的网卡命名到规范格式，如WLAN，以太网，以太网1等 \n3. 系统卡顿。\n4. 未知BUG。'
    msg.showinfo(title='导致失败的常见问题', message=question, icon="question")  # icon=question不会引发提示音！

def contactMe():
    contact = f'本程序仅供交流学习使用，无任何商业目的。\n已开源在：https://github.com/Kitiro/NetSwitcher，可自行clone后按需修改使用。\n本人邮箱：kitiro1874@163.com\n使用中有任何问题，请直接邮箱联系我。'
    msg.showinfo(title='如何联系我', message=contact, icon="question")


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
        msg.showerror("错误", "选择的两个接口为同一接口，请调整为不同接口再进行操作。")
        return
    switcher.switch()
    update()

# 菜单栏
main_menu = Menu(top)
main_menu.add_command(label='常见问题', command=freqQuestion)
main_menu.add_command(label='需知', command=contactMe)


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