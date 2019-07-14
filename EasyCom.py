import tkinter as tk  # 使用Tkinter前需要先导入

import serial
import serial.tools.list_ports
from tkinter import *
from tkinter import scrolledtext
from tkinter import ttk
global ser
global debug, windowFormWidth, windowFormHeight

def serialSelectFun(self):
    texttemp = '选中串口：' + serialSelect.get()
    print(texttemp)
    logtext.config(text=texttemp)
    return


def windowReSize(self):
    global debug, windowFormHeight, windowFormWidth,fw,fh
    w = window.winfo_width()
    h = window.winfo_height()
    getdata = Information1.config()
    rw = w - windowFormWidth
    rh = h - windowFormHeight
    windowFormWidth = w
    windowFormHeight = h
    fw = getdata['width'][-1] + rw
    fh = getdata['height'][-1] + rh
    Information1.config(width = fw,height = fh)

    fw = getdata['width'][-1] + rw
    Information2.config(width = fw)
    getdata = Information2.place_info()
    newy = int(getdata['y']) + rh
    Information2.place(y = newy)

    Information3.config(width = fw)
    getdata = Information3.place_info()
    newy = int(getdata['y']) + rh
    Information3.place(y = newy)

    # getdata = Information2_text.config()
    newwidth = int((w-120) / 7.3)
    newheight = int((fh-10) / 15.8)

    Information1_text.config(width = newwidth,height = newheight)
    Information2_text.config(width = newwidth)

    # text = 'resize w: {0} H: {1}'.format(w, h)
    # print(text)
    return

# 第5步，定义两个触发事件时的函数insert_point和insert_end（注意：因为Python的执行顺序是从上往下，所以函数一定要放在按钮的上面）
def getSerialList():  # 在鼠标焦点处插入输入内容
    port_list = list(serial.tools.list_ports.comports())
    print(port_list)
    if len(port_list) == 0:
        print('无可用串口')
        logtext.config(text='无可用串口')
    else:
        numberChosen.textvariable = len(port_list)
        list_portname = []
        for eachPort in port_list:
            list_portname.append(eachPort.device)
        serialSelect['values'] = list_portname  # 设置下拉列表的值
        serialSelect.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值

def openSerial():
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


def clearAll():
    logtext.config(text='aaaa')
    return




# 第1步，实例化object，建立窗口window
window = tk.Tk() ##
# 第2步，给窗口的可视化起名字
window.title('My Window')
# 第3步，设定窗口的大小(长 * 宽)
window.geometry('500x520')  # 这里的乘是小x


var = 1
Information1 = tk.LabelFrame(window, text="接收缓冲区", width = 490,padx=0, pady=0,height = 290)  # 创建子容器，水平，垂直方向上的边距均为10
# Information.pack(expand=NO, side='left', anchor = 'n', padx=5, pady=5, ipadx=5,ipady=5)
Information1.place(x=5, y=0)
Information1_text = scrolledtext.ScrolledText(Information1, width=50, height=17, padx=0, wrap=tk.WORD)
Information1_text.place(x=110, y=0)
Information1_text.config(highlightbackground = 'gray')
r1 = tk.Radiobutton(Information1, text='文本模式',  variable=var, value='A', command=nil)
r1.place(x=5, y=0)
r2 = tk.Radiobutton(Information1, text='HEX模式', variable=var, value='B', command=nil )
r2.place(x=5, y=20)
b1 = tk.Button(Information1, text='清空接收区', width=8, height=1, command=nil)
b1.place(x=5, y=40)
b2 = tk.Button(Information1, text='保存接收数据', width=8, height=1, command=nil)
b2.place(x=5, y=65)

Information2 = tk.LabelFrame(window, text="发送缓冲区", width = 490,padx=0, pady=0,height = 140)  # 创建子容器，水平，垂直方向上的边距均为10
# Information2.pack(expand=NO, side='left', anchor = 'n', padx=5, pady=5, ipadx=5,ipady=5)
Information2.place(x=5, y=295)
Information2_text = scrolledtext.ScrolledText(Information2, width=50, height=5, padx=0, wrap=tk.WORD)
Information2_text.place(x=110, y=0)

Information2_text.config(highlightbackground = 'gray')
r1 = tk.Radiobutton(Information2, text='文本模式',  variable=var, value='A', command=nil)
r1.place(x=5, y=0)
r2 = tk.Radiobutton(Information2, text='HEX模式', variable=var, value='B', command=nil )
r2.place(x=5, y=20)
b1 = tk.Button(Information2, text='清空接收区', width=8, height=1, command=nil)
b1.place(x=5, y=40)
b2 = tk.Button(Information2, text='保存接收数据', width=8, height=1, command=nil)
b2.place(x=5, y=65)
b1 = tk.Button(Information2, text='发送文件', width=5, height=1, command=nil)
b1.place(x=5, y=90)
b2 = tk.Button(Information2, text='发送数据', width=5, height=1, command=nil)
b2.place(x=85, y=90)
b2 = tk.Button(Information2, text='自动发送', width=5, height=1, command=nil)
b2.place(x=165, y=90)
l1=tk.Label(Information2, text="周期(ms):")  # 创建子容器，水平，垂直方向上的边距均为10
l1.place(x=245, y=93)
nameEntered = tk.Entry(Information2, width=10)
nameEntered.place(x=315, y=90)

Information3 = tk.LabelFrame(window, text="端口管理", width = 490,padx=0, pady=0,height = 75)  # 创建子容器，水平，垂直方向上的边距均为10
# Information3.pack(expand=NO, side='left', anchor = 'n', padx=5, pady=5, ipadx=5,ipady=5)
Information3.place(x=5, y=440)
l1=tk.Label(Information3, text='串口:')  # 创建子容器，水平，垂直方向上的边距均为10
l1.place(x=5, y=0)
serialSelect = ttk.Combobox(Information3, width=12, textvariable=5)
serialSelect['values'] = (1, 2, 4, 42, 100)  # 设置下拉列表的值
serialSelect.place(x=40, y=0)
serialSelect.bind("<<ComboboxSelected>>", serialSelectFun)

l1=tk.Label(Information3, text='波特率:')  # 创建子容器，水平，垂直方向上的边距均为10
l1.place(x=175,  y=0)
numberChosen = ttk.Combobox(Information3, width=4, textvariable=5)
numberChosen['values'] = (1, 2, 4, 42, 115200)  # 设置下拉列表的值
numberChosen.place(x=220, y=0)

l1=tk.Label(Information3, text='校验位:')  # 创建子容器，水平，垂直方向上的边距均为10
l1.place(x=280, y=0)
numberChosen = ttk.Combobox(Information3, width=2, textvariable=5)
numberChosen['values'] = (1, 2, 4, 4, 5)  # 设置下拉列表的值
numberChosen.place(x=330, y=0)

l1=tk.Label(Information3, text='停止位:')  # 创建子容器，水平，垂直方向上的边距均为10
l1.place(x=375, y=0)
numberChosen = ttk.Combobox(Information3, width=2, textvariable=5)
numberChosen['values'] = (1, 2, 4, 42, 1)  # 设置下拉列表的值
numberChosen.place(x=420, y=0)

b2 = tk.Button(Information3, text='打开串口', width=5, height=1, command=openSerial)
b2.place(x=5, y=25)
l1 = tk.Label(Information3, text='信息:')  # 创建子容器，水平，垂直方向上的边距均为10
l1.place(x=90, y=30)
logtext = tk.Label(Information3, text='打开串口成功')  # 创建子容器，水平，垂直方向上的边距均为10
logtext.place(x=130, y=30)
b2 = tk.Button(Information3, text='清零', width=3, height=1, command=clearAll)
b2.place(x=410, y=25)

debug = 0
windowFormWidth = 500
windowFormHeight = 520
fw = 490
fh = 290



def checkSerialReceiverData():
    global debug
    debug += 1
    # logtext.config(text='Time:{0}'.format(debug))
    window.after(100, checkSerialReceiverData)  # add_letter will run as soon as the mainloop starts.


logtext.config(text='gggg')



getSerialList()
checkSerialReceiverData()

window.bind("<Configure>", windowReSize)
# 第8步，主窗口循环显示
window.mainloop()