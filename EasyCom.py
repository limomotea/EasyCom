import tkinter as tk  # 使用Tkinter前需要先导入

import serial
import serial.tools.list_ports
from tkinter import *
from tkinter import scrolledtext
global ser

# 第1步，实例化object，建立窗口window
window = tk.Tk() ##



# 第2步，给窗口的可视化起名字
window.title('My Window')


# 第3步，设定窗口的大小(长 * 宽)
window.geometry('600x600')  # 这里的乘是小x




# 第5步，定义两个触发事件时的函数insert_point和insert_end（注意：因为Python的执行顺序是从上往下，所以函数一定要放在按钮的上面）
def insert_point():  # 在鼠标焦点处插入输入内容
    var = e.get()
    t.insert('insert', var)
    port_list = list(serial.tools.list_ports.comports())
    print(port_list)
    if len(port_list) == 0:

        print('无可用串口')
    else: #
        t.delete(1.0,'end')
        for i in range(0, len(port_list)):
            print(port_list[i])
            var = port_list[i]
            t.insert('insert', var)
            t.insert('insert', '\n')
        numberChosen.textvariable = len(port_list)
        list_portname = []
        for eachPort in port_list:
            list_portname.append(eachPort.device)
        numberChosen['values'] = list_portname  # 设置下拉列表的值
        numberChosen.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值

def OpenSerial():
    global ser
    try:
        port_list = list(serial.tools.list_ports.comports())
        portx = port_list[1].device
        print(portx)
        bps = 115200
        # 超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
        timex = 1
        ser = serial.Serial(portx, bps, timeout=timex,write_timeout=timex)
        print("串口详情参数：", ser)

    except Exception as e:
        print("---异常---：", e)

def CloseSerial():
    global ser
    ser.close()  # 关闭串口
    print('ser colsed')


def insert_end():  # 在文本框内容最后接着插入输入内容
    # 十六进制的发送
    for i in range(10):
        if ser.isOpen():
            print('ser is open', i)
            # result = ser.write("I am LGS.test long string\n".encode('utf-8'))
            # print(result)
            text = 'I am LGS.test long string. num = {0}\n'.format(i)
            result = ser.write(text.encode('utf-8'))
            print(result)
    # print("Test", result)
    result = 1
    print("写总字节数:", result)
    # 十六进制的读取
    # print(ser.read().hex())  # 读一个字节
    print('ser write ok')
    # print("---------------")


def nil():
    return()

var = 1
Information = tk.LabelFrame(window, text="接收缓冲区", width = 490,padx=0, pady=0,height = 290)  # 创建子容器，水平，垂直方向上的边距均为10
# Information.pack(expand=NO, side='left', anchor = 'n', padx=5, pady=5, ipadx=5,ipady=5)
Information.place(x=5, y=0)
Information_Window = scrolledtext.ScrolledText(Information, width=50, height=17, padx=0, wrap=tk.WORD)
Information_Window.place(x=110, y=0)
Information_Window.config(highlightbackground = 'gray')
r1 = tk.Radiobutton(Information, text='文本模式',  variable=var, value='A', command=nil)
r1.place(x=5, y=0)
r2 = tk.Radiobutton(Information, text='HEX模式', variable=var, value='B', command=nil )
r2.place(x=5, y=20)
b1 = tk.Button(Information, text='清空接收区', width=8, height=1, command=nil)
b1.place(x=5, y=40)
b2 = tk.Button(Information, text='保存接收数据', width=8, height=1, command=nil)
b2.place(x=5, y=65)

Information = tk.LabelFrame(window, text="接收缓冲区", width = 490,padx=0, pady=0,height = 140)  # 创建子容器，水平，垂直方向上的边距均为10
# Information.pack(expand=NO, side='left', anchor = 'n', padx=5, pady=5, ipadx=5,ipady=5)
Information.place(x=5, y=295)
Information_Window = scrolledtext.ScrolledText(Information, width=50, height=5, padx=0, wrap=tk.WORD)
Information_Window.place(x=110, y=0)
Information_Window.config(highlightbackground = 'gray')
r1 = tk.Radiobutton(Information, text='文本模式',  variable=var, value='A', command=nil)
r1.place(x=5, y=0)
r2 = tk.Radiobutton(Information, text='HEX模式', variable=var, value='B', command=nil )
r2.place(x=5, y=20)
b1 = tk.Button(Information, text='清空接收区', width=8, height=1, command=nil)
b1.place(x=5, y=40)
b2 = tk.Button(Information, text='保存接收数据', width=8, height=1, command=nil)
b2.place(x=5, y=65)
b1 = tk.Button(Information, text='发送文件', width=5, height=1, command=nil)
b1.place(x=5, y=90)
b2 = tk.Button(Information, text='发送数据', width=5, height=1, command=nil)
b2.place(x=85, y=90)
b2 = tk.Button(Information, text='自动发送', width=5, height=1, command=nil)
b2.place(x=165, y=90)
l1=tk.Label(Information, text="周期(ms):")  # 创建子容器，水平，垂直方向上的边距均为10
l1.place(x=245, y=93)
nameEntered = tk.Entry(Information, width=10)
nameEntered.place(x=315, y=90)



# 第8步，主窗口循环显示
window.mainloop()