import tkinter as tk  # 使用Tkinter前需要先导入

import serial
import serial.tools.list_ports
from tkinter import *
from tkinter import scrolledtext
from tkinter import ttk
from typing import Any

global ser
global debug, windowFormWidth, windowFormHeight,serial_OpenOrClose,serial_AutoSendState,auto_SendAfterHL
serial_OpenOrClose = ' '
serial_AutoSendState = ' '
auto_SendAfterHL = ''


def FormInit():
    autoSendTimeForm.insert(END, '100')
    return


def serialReceiveDataTextFormDeleteAllFun():
    serialReceiveDataTextForm.delete(1.0, END)
    return


def serialSendDataTextFormDeleteAllFun():
    serialSendDataTextForm.delete(1.0, END)
    return


def serialSelectPortFormFun(self):
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

    serialReceiveDataTextForm.config(width = newwidth,height = newheight)
    serialSendDataTextForm.config(width = newwidth)

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
        list_port_name = []  # type: Any
        for eachPort in port_list:
            list_port_name.append(eachPort.device)
        serialSelectPortForm['values'] = list_port_name  # 设置下拉列表的值
        serialSelectPortForm.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值


def getStopBits():
    val = {'1位' : serial.STOPBITS_ONE, '1.5位' : serial.STOPBITS_ONE_POINT_FIVE, '2位' : serial.STOPBITS_TWO,}
    return val.get(selectSerialStopBitForm.get(), serial.STOPBITS_ONE)


def getParityVal():
    val = {'无校验': serial.PARITY_NONE, '奇校验': serial.PARITY_ODD, '偶校验': serial.PARITY_EVEN, '1校验': serial.PARITY_MARK, '0校验': serial.PARITY_SPACE, }
    return val.get(selectSerialParityCheckForm.get(), serial.PARITY_NONE)


def openSerial():
    global ser
    # current()
    try:
        selected_port = serialSelectPortForm.get()  # type: selected_port
        bps = int(selectSerialBaudRateForm.get())
        stop_bits_val = getStopBits()
        parity_val = getParityVal()
        # 超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
        timex = 5
        ser = serial.Serial(selected_port, bps, parity=parity_val, stopbits=stop_bits_val, timeout=timex,write_timeout=timex)
        print("串口详情参数：", ser)
        logtext.config(text='串口打开成功')
    except Exception as e:
        print("串口打开错误", e)
        logtext.config(text='串口打开错误')


def CloseSerial():
    global ser
    ser.close()  # 关闭串口
    print("串口关闭")
    logtext.config(text='串口关闭')


def OpenOrCloseSerialFun():
    global serial_OpenOrClose
    if serial_OpenOrClose != 'close':
        openSerial()
        serial_OpenOrClose = 'close'
        OpenOrCloseSerialButton.config(text='关闭串口')
    else:
        CloseSerial()
        serial_OpenOrClose = 'open'
        OpenOrCloseSerialButton.config(text='打开串口')
    return


def serialSendDataFUN():
    if ser.isOpen():
        text_send = serialSendDataScrolledText.get('1.0', 'end-1c')
        result = ser.write(text_send.encode('utf-8'))
        print(result)
    else:
        logtext.config(text='请先打开串口')
    return


def serialSendFileFun():
    return


def autoSendRunFUN():
    global serial_AutoSendState,auto_SendAfterHL
    try:
        autoSendTimedata_ms = int(autoSendTimeForm.get())
        if ser.isOpen():
            text_send = serialSendDataScrolledText.get('1.0', 'end-1c')
            result = ser.write(text_send.encode('utf-8'))
            print(result)
            auto_SendAfterHL = window.after(autoSendTimedata_ms, autoSendRunFUN)
            return(True)
        else:
            logtext.config(text='请先打开串口')
            serial_AutoSendState = 'STOP'
            autoSendButtonForm.config(text='自动发送')
            serialSendDataButton.config(state=NORMAL)
            serialSendFileButton.config(state=NORMAL)
    except:
        logtext.config(text='请先打开串口或选择正确的重复时间')
        serial_AutoSendState = 'STOP'
        autoSendButtonForm.config(text='自动发送')
        serialSendDataButton.config(state=NORMAL)
        serialSendFileButton.config(state=NORMAL)
        return False


def autoSendFUN():
    global serial_AutoSendState,auto_SendAfterHL
    if serial_AutoSendState != 'RUN':
        isAutoSendOk = autoSendRunFUN()
        if isAutoSendOk:
            serial_AutoSendState = 'RUN'
            autoSendButtonForm.config(text='停止自动')
            serialSendDataButton.config(state=DISABLED)
            serialSendFileButton.config(state=DISABLED)
        else:
            return
    else:
        window.after_cancel(auto_SendAfterHL)
        serial_AutoSendState = 'STOP'
        autoSendButtonForm.config(text='自动发送')
        serialSendDataButton.config(state=NORMAL)
        serialSendFileButton.config(state=NORMAL)
    return


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
serialReceiveDataTextForm = scrolledtext.ScrolledText(Information1, width=50, height=17, padx=0, wrap=tk.WORD)
serialReceiveDataTextForm.place(x=110, y=0)
serialReceiveDataTextForm.config(highlightbackground = 'gray')
r1 = tk.Radiobutton(Information1, text='文本模式',  variable=11, value='A', command=nil)
r1.place(x=5, y=0)
r2 = tk.Radiobutton(Information1, text='HEX模式', variable=11, value='B', command=nil )
r2.place(x=5, y=20)
serialReceiveDataTextFormDeleteAllButton = tk.Button(Information1, text='清空接收区', width=8, height=1, command=serialReceiveDataTextFormDeleteAllFun)
serialReceiveDataTextFormDeleteAllButton.place(x=5, y=40)
b2 = tk.Button(Information1, text='保存接收数据', width=8, height=1, command=nil)
b2.place(x=5, y=65)

Information2 = tk.LabelFrame(window, text="发送缓冲区", width = 490,padx=0, pady=0,height = 140)  # 创建子容器，水平，垂直方向上的边距均为10
# Information2.pack(expand=NO, side='left', anchor = 'n', padx=5, pady=5, ipadx=5,ipady=5)
Information2.place(x=5, y=295)
serialSendDataTextForm = scrolledtext.ScrolledText(Information2, width=50, height=5, padx=0, wrap=tk.WORD)
serialSendDataTextForm.place(x=110, y=0)
serialSendDataTextForm.config(highlightbackground = 'gray')
r1 = tk.Radiobutton(Information2, text='文本模式',  variable=12, value='A', command=nil)
r1.place(x=5, y=0)
r2 = tk.Radiobutton(Information2, text='HEX模式', variable=12, value='B', command=nil )
r2.place(x=5, y=20)
b1 = tk.Button(Information2, text='清空接收区', width=8, height=1, command=serialSendDataTextFormDeleteAllFun)
b1.place(x=5, y=40)
b2 = tk.Button(Information2, text='保存接收数据', width=8, height=1, command=nil)
b2.place(x=5, y=65)
serialSendFileButton = tk.Button(Information2, text='发送文件', width=5, height=1, command=serialSendFileFun)
serialSendFileButton.place(x=5, y=90)
serialSendDataButton = tk.Button(Information2, text='发送数据', width=5, height=1, command=serialSendDataFUN)
serialSendDataButton.place(x=85, y=90)
autoSendButtonForm = tk.Button(Information2, text='自动发送', width=5, height=1, command=autoSendFUN)
autoSendButtonForm.place(x=165, y=90)
autoSendlabelForm=tk.Label(Information2, text="周期(ms):")  # 创建子容器，水平，垂直方向上的边距均为10
autoSendlabelForm.place(x=245, y=93)
autoSendTimeForm = tk.Entry(Information2, width=10)
autoSendTimeForm.place(x=315, y=90)

Information3 = tk.LabelFrame(window, text="端口管理", width = 490,padx=0, pady=0,height = 75)  # 创建子容器，水平，垂直方向上的边距均为10
# Information3.pack(expand=NO, side='left', anchor = 'n', padx=5, pady=5, ipadx=5,ipady=5)
Information3.place(x=5, y=440)
l1=tk.Label(Information3, text='串口:')  # 创建子容器，水平，垂直方向上的边距均为10
l1.place(x=5, y=0)
serialSelectPortForm = ttk.Combobox(Information3, width=12, textvariable=1)
serialSelectPortForm['values'] = (1, 2, 4, 42, 100)  # 设置下拉列表的值
serialSelectPortForm.place(x=40, y=0)
serialSelectPortForm.bind("<<ComboboxSelected>>", serialSelectPortFormFun)

l1=tk.Label(Information3, text='波特率:')  # 创建子容器，水平，垂直方向上的边距均为10
l1.place(x=175,  y=0)
selectSerialBaudRateForm = ttk.Combobox(Information3, width=4, textvariable=2)
selectSerialBaudRateForm['values'] = (600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600, 115200, 230400, 460800)  # 设置下拉列表的值
selectSerialBaudRateForm.place(x=220, y=0)
selectSerialBaudRateForm.current(10)

l1=tk.Label(Information3, text='校验位:')  # 创建子容器，水平，垂直方向上的边距均为10
l1.place(x=280, y=0)
selectSerialParityCheckForm = ttk.Combobox(Information3, width=2, textvariable=3)
selectSerialParityCheckForm['values'] = ('无校验', '奇校验', '偶校验', '1校验', '0校验')  # 设置下拉列表的值
selectSerialParityCheckForm.place(x=330, y=0)
selectSerialParityCheckForm.current(0)

l1=tk.Label(Information3, text='停止位:')  # 创建子容器，水平，垂直方向上的边距均为10
l1.place(x=375, y=0)
selectSerialStopBitForm = ttk.Combobox(Information3, width=2, textvariable=4)
selectSerialStopBitForm['values'] = ('1位', '1.5位', '2位')  # 设置下拉列表的值
selectSerialStopBitForm.place(x=420, y=0)
selectSerialStopBitForm.current(0)

OpenOrCloseSerialButton = tk.Button(Information3, text='打开串口', width=5, height=1, command=OpenOrCloseSerialFun)
OpenOrCloseSerialButton.place(x=5, y=25)
l1 = tk.Label(Information3, text='信息:')  # 创建子容器，水平，垂直方向上的边距均为10
l1.place(x=90, y=30)
logtext = tk.Label(Information3, text='打开串口成功')  # 创建子容器，水平，垂直方向上的边距均为10
logtext.place(x=130, y=30)
b2 = tk.Button(Information3, text='清零', width=3, height=1, command=CloseSerial)
b2.place(x=410, y=25)

debug = 0
windowFormWidth = 500
windowFormHeight = 520
fw = 490
fh = 290


def checkSerialReceiverData():
    try:
        if ser.isOpen():
            print('ready')
            if ser.in_waiting > 0:
                serReadData = ser.read(ser.in_waiting)
                serReadData = str(serReadData, 'utf-8')
                serialReceiveDataTextForm.insert(END, serReadData)
                print('getdata')
        window.after(100, checkSerialReceiverData)  # add_letter will run as soon as the mainloop starts.
    except:
        window.after(100, checkSerialReceiverData)  # add_letter will run as soon as the mainloop starts.

    # logtext.config(text='Time:{0}'.format(debug))


logtext.config(text='gggg')

FormInit()

getSerialList()

checkSerialReceiverData()

window.bind("<Configure>", windowReSize)
# 第8步，主窗口循环显示
window.mainloop()