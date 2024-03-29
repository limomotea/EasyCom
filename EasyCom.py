import tkinter as tk  # 使用Tkinter前需要先导入
import serial
import serial.tools.list_ports
from tkinter import filedialog
from tkinter import *
from tkinter import scrolledtext
from tkinter import ttk
from typing import Any

global serialPortOpenHl, serialSendDataNumberOfByte, serialgetDataNumberOfByte
global debug, windowFormWidth, windowFormHeight, serial_OpenOrClose, serial_AutoSendState, auto_SendAfterHL


def sysInit():
    global serialPortOpenHl, serialSendDataNumberOfByte, serialgetDataNumberOfByte
    global debug, windowFormWidth, windowFormHeight, serial_OpenOrClose, serial_AutoSendState, auto_SendAfterHL
    serial_OpenOrClose = ''
    serial_AutoSendState = ''
    auto_SendAfterHL = ''
    serialPortOpenHl = ''
    serialSendDataButton.config(state=DISABLED)
    serialSendFileButton.config(state=DISABLED)
    autoSendButtonForm.config(state=DISABLED)
    serialSendDataNumberOfByte = 0
    serialgetDataNumberOfByte = 0



def saveReceiveDataToFileFun():
    save_file_path = tk.filedialog.asksaveasfilename(defaultextension=".txt")
    with open(save_file_path, 'w', encoding='utf-8') as afile:
        afile.write(serialReceiveDataTextForm.get(1.0, END))
        afile.close()
    return


def serialSelectStopBitFormFun(self):
    print(selectSerialStopBitForm.get())
    if serialPortOpenHl != '':
        if serialPortOpenHl.isOpen():
            OpenOrCloseSerialFun()
            OpenOrCloseSerialFun()
    return


def serialSelectBaudRateFormFun(self):
    print(selectSerialBaudRateForm.get())
    if serialPortOpenHl != '':
        if serialPortOpenHl.isOpen():
            OpenOrCloseSerialFun()
            OpenOrCloseSerialFun()
    return


def serialSelectParityCheckFormFun(self):
    print(selectSerialParityCheckForm.get())
    if serialPortOpenHl != '':
        if serialPortOpenHl.isOpen():
            OpenOrCloseSerialFun()
            OpenOrCloseSerialFun()
    return


def saveSendDataToFileFun():
    save_file_path = tk.filedialog.asksaveasfilename(defaultextension=".txt")
    with open(save_file_path, 'w', encoding='utf-8') as afile:
        afile.write(serialSendDataTextForm.get(1.0, END))
        afile.close()
    return

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
    texttemp = '选中串口：' + serialSelectPortForm.get()
    print(texttemp)
    logTextForm.config(text=texttemp)
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


def SerialSendGetDateNumberOfByte():
    global serialSendDataNumberOfByte, serialgetDataNumberOfByte
    serialSendDataNumberOfByte = 0
    serialgetDataNumberOfByte = 0
    logTextForm.config(text='发送字节:{0} 接收字节:{1}'.format(serialSendDataNumberOfByte, serialgetDataNumberOfByte))
    getSerialList()
    return

# 第5步，定义两个触发事件时的函数insert_point和insert_end（注意：因为Python的执行顺序是从上往下，所以函数一定要放在按钮的上面）
def getSerialList():  # 在鼠标焦点处插入输入内容
    port_list = list(serial.tools.list_ports.comports())
    print(port_list)
    if len(port_list) == 0:
        print('无可用串口')
        logTextForm.config(text='无可用串口')
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
    global serialPortOpenHl
    # current()
    try:
        selected_port = serialSelectPortForm.get()  # type: selected_port
        bps = int(selectSerialBaudRateForm.get())
        stop_bits_val = getStopBits()
        parity_val = getParityVal()
        # 超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
        timex = 5
        serialPortOpenHl = serial.Serial(selected_port, bps, parity=parity_val, stopbits=stop_bits_val, timeout=timex, write_timeout=timex)
        print("串口详情参数：", serialPortOpenHl)
        logTextForm.config(text='串口打开成功')
        return True

    except Exception as e:
        print("串口打开错误", e)
        logTextForm.config(text='串口打开错误')
        OpenOrCloseSerialButton.config(text='打开串口')
        return False


def CloseSerial():
    global serialPortOpenHl
    serialPortOpenHl.close()  # 关闭串口
    print("串口关闭")
    logTextForm.config(text='串口关闭')


def OpenOrCloseSerialFun():
    global serial_OpenOrClose, serial_AutoSendState
    if serial_OpenOrClose != 'close':
        if openSerial():
            serial_OpenOrClose = 'close'
            OpenOrCloseSerialButton.config(text='关闭串口')
            serialSendDataButton.config(state=NORMAL)
            serialSendFileButton.config(state=NORMAL)
            autoSendButtonForm.config(state=NORMAL)
            if serial_AutoSendState == 'NeedToRUN':
                autoSendFUN()
        else:
            serialSendDataButton.config(state=DISABLED)
            serialSendFileButton.config(state=DISABLED)
            autoSendButtonForm.config(state=DISABLED)
    else:
        if serial_AutoSendState == 'RUN':
            autoSendFUN()   # 关闭串口前，检查是否在自动发送状态，如果是则先关闭。
            serial_AutoSendState = 'NeedToRUN'
        CloseSerial()
        serial_OpenOrClose = 'open'
        OpenOrCloseSerialButton.config(text='打开串口')
        serialSendDataButton.config(state=DISABLED)
        serialSendFileButton.config(state=DISABLED)
        autoSendButtonForm.config(state=DISABLED)
    return

def str2hex(s):
    odata = 0;
    su =s.upper()
    for c in su:
        tmp=ord(c)
        if ord('0') <= tmp <= ord('9') :
            odata = odata << 4
            odata += tmp - ord('0')
        elif ord('A') <= tmp <= ord('F'):
            odata = odata << 4
            odata += tmp - ord('A') + 10
    return odata

def ConvertToHex(text_send):
    # text_send = text_send + 'HEX'
    a = ''
    i = 0
    b = []
    for eachtext in text_send:
        if i == 0:
            i = 1
            a = eachtext
        else:
            i = 0
            a = a + eachtext
            b.append(str2hex(a))
    if i == 1:
        b.append(str2hex(a))

    return bytes(b)


def serialSendDataFUN():
    global serialSendDataNumberOfByte
    try:
        if serialPortOpenHl.isOpen():
            text_send = serialSendDataTextForm.get('1.0', 'end-1c')
            if serialSendHexSelectV.get() == 1:
                text_send = ConvertToHex(text_send)
                result = serialPortOpenHl.write(text_send)
            else:
                result = serialPortOpenHl.write(text_send.encode('utf-8'))
            serialSendDataNumberOfByte = serialSendDataNumberOfByte + result
            logTextForm.config(text='发送字节:{0} 接收字节:{1}'.format(serialSendDataNumberOfByte, serialgetDataNumberOfByte))
        else:
            logTextForm.config(text='请先打开串口')
    except:
        logTextForm.config(text='请先打开串口')
    return


def serialSendFileFun():
    global serialSendDataNumberOfByte
    open_file_path = tk.filedialog.askopenfilename()
    try:
        with open(open_file_path, encoding='utf-8') as afile:
            file_text = afile.read()
            afile.close()
            try:
                if serialPortOpenHl.isOpen():
                    result = serialPortOpenHl.write(file_text.encode('utf-8'))
                    serialSendDataNumberOfByte = serialSendDataNumberOfByte + result
                    logTextForm.config(
                        text='发送字节:{0} 接收字节:{1}'.format(serialSendDataNumberOfByte, serialgetDataNumberOfByte))
                else:
                    logTextForm.config(text='请先打开串口')
            except Exception as e:
                print("发送错误", e)
                logTextForm.config(text='发送错误')
    except Exception as e:
        print("打开文件错误", e)
        logTextForm.config(text='打开文件错误')
    return


def autoSendRunFUN():
    global serial_AutoSendState, auto_SendAfterHL, serialSendDataNumberOfByte
    try:
        autoSendTimedata_ms = int(autoSendTimeForm.get())
        if serialPortOpenHl.isOpen():
            text_send = serialSendDataTextForm.get('1.0', 'end-1c')
            if serialSendHexSelectV.get() == 1:
                text_send = ConvertToHex(text_send)
                result = serialPortOpenHl.write(text_send)
            else:
                result = serialPortOpenHl.write(text_send.encode('utf-8'))
            serialSendDataNumberOfByte = serialSendDataNumberOfByte + result
            logTextForm.config(text='发送字节:{0} 接收字节:{1}'.format(serialSendDataNumberOfByte, serialgetDataNumberOfByte))
            auto_SendAfterHL = window.after(autoSendTimedata_ms, autoSendRunFUN)
            return(True)
        else:
            logTextForm.config(text='请先打开串口')
            return False
    except:
        logTextForm.config(text='请先打开串口或选择正确的重复时间')
        return False


def autoSendFUN():
    global serial_AutoSendState,auto_SendAfterHL
    if serial_AutoSendState != 'RUN':
        if autoSendRunFUN():
            serial_AutoSendState = 'RUN'
            autoSendButtonForm.config(text='停止自动')
            serialSendDataButton.config(state=DISABLED)
            serialSendFileButton.config(state=DISABLED)
        else:
            serial_AutoSendState = 'STOP'
            autoSendButtonForm.config(text='自动发送')
            serialSendDataButton.config(state=NORMAL)
            serialSendFileButton.config(state=NORMAL)
            return
    else:
        window.after_cancel(auto_SendAfterHL)
        serial_AutoSendState = 'STOP'
        autoSendButtonForm.config(text='自动发送')
        serialSendDataButton.config(state=NORMAL)
        serialSendFileButton.config(state=NORMAL)
    return


def insert_end():
    # 十六进制的发送
    for i in range(10):
        if serialPortOpenHl.isOpen():
            print('ser is open', i)
            # result = ser.write("I am LGS.test long string\n".encode('utf-8'))
            # print(result)
            text = 'I am LGS.test long string. num = {0}\n'.format(i)
            result = serialPortOpenHl.write(text.encode('utf-8'))
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
    logTextForm.config(text='aaaa')
    return




# 第1步，实例化object，建立窗口window
window = tk.Tk() ##
# 第2步，给窗口的可视化起名字
window.title('My Window')
# 第3步，设定窗口的大小(长 * 宽)
window.geometry('500x520')  # 这里的乘是小x


var = 1
serialReceiveHexSelectV = IntVar()
Information1 = tk.LabelFrame(window, text="接收缓冲区", width=490, padx=0, pady=0, height=290)  # 创建子容器，水平，垂直方向上的边距均为10
Information1.place(x=5, y=0)
serialReceiveDataTextForm = scrolledtext.ScrolledText(Information1, width=50, height=17, padx=0, wrap=tk.WORD)
serialReceiveDataTextForm.place(x=110, y=0)
serialReceiveDataTextForm.config(highlightbackground = 'gray')
r1 = tk.Radiobutton(Information1, text='文本模式',  variable=serialReceiveHexSelectV, value=0, command=nil)
r1.place(x=5, y=0)
r2 = tk.Radiobutton(Information1, text='HEX模式', variable=serialReceiveHexSelectV, value=1, command=nil)
r2.place(x=5, y=20)
serialReceiveDataTextFormDeleteAllButton = tk.Button(Information1, text='清空接收区', width=8, height=1,
                                                     command=serialReceiveDataTextFormDeleteAllFun)
serialReceiveDataTextFormDeleteAllButton.place(x=5, y=40)
b2 = tk.Button(Information1, text='保存接收数据', width=8, height=1, command=saveReceiveDataToFileFun)
b2.place(x=5, y=65)

serialSendHexSelectV = IntVar()
Information2 = tk.LabelFrame(window, text="发送缓冲区", width=490, padx=0, pady=0, height=140)  # 创建子容器，水平，垂直方向上的边距均为10
Information2.place(x=5, y=295)
serialSendDataTextForm = scrolledtext.ScrolledText(Information2, width=50, height=5, padx=0, wrap=tk.WORD)
serialSendDataTextForm.place(x=110, y=0)
serialSendDataTextForm.config(highlightbackground='gray')
r1 = tk.Radiobutton(Information2, text='文本模式',  variable=serialSendHexSelectV, value=0, command=nil)
r1.place(x=5, y=0)
r2 = tk.Radiobutton(Information2, text='HEX模式', variable=serialSendHexSelectV, value=1, command=nil)
r2.place(x=5, y=20)
b1 = tk.Button(Information2, text='清空发送区', width=8, height=1, command=serialSendDataTextFormDeleteAllFun)
b1.place(x=5, y=40)
b2 = tk.Button(Information2, text='保存发送数据', width=8, height=1, command=saveSendDataToFileFun)
b2.place(x=5, y=65)
serialSendFileButton = tk.Button(Information2, text='发送文件', width=5, height=1, command=serialSendFileFun)
serialSendFileButton.place(x=5, y=90)
serialSendDataButton = tk.Button(Information2, text='发送数据', width=5, height=1, command=serialSendDataFUN)
serialSendDataButton.place(x=85, y=90)
autoSendButtonForm = tk.Button(Information2, text='自动发送', width=5, height=1, command=autoSendFUN)
autoSendButtonForm.place(x=165, y=90)
autoSendLabelForm = tk.Label(Information2, text="周期(ms):")
autoSendLabelForm.place(x=245, y=93)
autoSendTimeForm = tk.Entry(Information2, width=10)
autoSendTimeForm.place(x=315, y=90)

Information3 = tk.LabelFrame(window, text="端口管理", width = 490,padx=0, pady=0,height = 75)  # 创建子容器，水平，垂直方向上的边距均为10
# Information3.pack(expand=NO, side='left', anchor = 'n', padx=5, pady=5, ipadx=5,ipady=5)
Information3.place(x=5, y=440)
l1 = tk.Label(Information3, text='串口:')  # 创建子容器，水平，垂直方向上的边距均为10
l1.place(x=5, y=0)
serialSelectPortForm = ttk.Combobox(Information3, width=12, textvariable=1)
serialSelectPortForm['values'] = (1, 2, 4, 42, 100)  # 设置下拉列表的值
serialSelectPortForm.place(x=40, y=0)
serialSelectPortForm.bind("<<ComboboxSelected>>", serialSelectPortFormFun)

l1 = tk.Label(Information3, text='波特率:')  # 创建子容器，水平，垂直方向上的边距均为10
l1.place(x=175,  y=0)
selectSerialBaudRateForm = ttk.Combobox(Information3, width=4, textvariable=2)
selectSerialBaudRateForm['values'] = (600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600, 115200, 230400,
                                      460800)  # 设置下拉列表的值
selectSerialBaudRateForm.place(x=220, y=0)
selectSerialBaudRateForm.current(10)
selectSerialBaudRateForm.bind("<<ComboboxSelected>>", serialSelectBaudRateFormFun)

l1 = tk.Label(Information3, text='校验位:')  # 创建子容器，水平，垂直方向上的边距均为10
l1.place(x=280, y=0)
selectSerialParityCheckForm = ttk.Combobox(Information3, width=2, textvariable=3)
selectSerialParityCheckForm['values'] = ('无校验', '奇校验', '偶校验')  # 设置下拉列表的值
selectSerialParityCheckForm.place(x=330, y=0)
selectSerialParityCheckForm.current(0)
selectSerialParityCheckForm.bind("<<ComboboxSelected>>", serialSelectParityCheckFormFun)

l1 = tk.Label(Information3, text='停止位:')  # 创建子容器，水平，垂直方向上的边距均为10
l1.place(x=375, y=0)
selectSerialStopBitForm = ttk.Combobox(Information3, width=2, textvariable=4)
selectSerialStopBitForm['values'] = ('1位', '1.5位', '2位')  # 设置下拉列表的值
selectSerialStopBitForm.place(x=420, y=0)
selectSerialStopBitForm.current(0)
selectSerialStopBitForm.bind("<<ComboboxSelected>>", serialSelectStopBitFormFun)

OpenOrCloseSerialButton = tk.Button(Information3, text='打开串口', width=5, height=1, command=OpenOrCloseSerialFun)
OpenOrCloseSerialButton.place(x=5, y=25)
l1 = tk.Label(Information3, text='信息:')  # 创建子容器，水平，垂直方向上的边距均为10
l1.place(x=90, y=30)
logTextForm = tk.Label(Information3, text='打开串口成功')  # 创建子容器，水平，垂直方向上的边距均为10
logTextForm.place(x=130, y=30)
b2 = tk.Button(Information3, text='刷新串口 计数清零', width=12, height=1, command=SerialSendGetDateNumberOfByte)
b2.place(x=350, y=25)
#
# # 第4步，在图形界面上创建一个标签用以显示内容并放置
# l = tk.Label(window, text='      ', bg='green')
# l.pack()
#
# # 第10步，定义一个函数功能，用来代表菜单选项的功能，这里为了操作简单，定义的功能比较简单
# counter = 0
#
#
# def do_job():
#     global counter
#     l.config(text='do ' + str(counter))
#     counter += 1


# 第5步，创建一个菜单栏，这里我们可以把他理解成一个容器，在窗口的上方
menubar = tk.Menu(window)

# 第6步，创建一个File菜单项（默认不下拉，下拉内容包括New，Open，Save，Exit功能项）
filemenu = tk.Menu(menubar, tearoff=0)
# 将上面定义的空菜单命名为File，放在菜单栏中，就是装入那个容器中
menubar.add_cascade(label='File', menu=filemenu)

# # 在File中加入New、Open、Save等小菜单，即我们平时看到的下拉菜单，每一个小菜单对应命令操作。
# filemenu.add_command(label='New', command=do_job)
# filemenu.add_command(label='Open', command=do_job)
# filemenu.add_command(label='Save', command=do_job)
filemenu.add_separator()  # 添加一条分隔线
filemenu.add_command(label='Exit', command=window.quit)  # 用tkinter里面自带的quit()函数

# # 第7步，创建一个Edit菜单项（默认不下拉，下拉内容包括Cut，Copy，Paste功能项）
# editmenu = tk.Menu(menubar, tearoff=0)
# # 将上面定义的空菜单命名为 Edit，放在菜单栏中，就是装入那个容器中
# menubar.add_cascade(label='Edit', menu=editmenu)
#
# # 同样的在 Edit 中加入Cut、Copy、Paste等小命令功能单元，如果点击这些单元, 就会触发do_job的功能
# editmenu.add_command(label='Cut', command=do_job)
# editmenu.add_command(label='Copy', command=do_job)
# editmenu.add_command(label='Paste', command=do_job)
#
# # 第8步，创建第二级菜单，即菜单项里面的菜单
# submenu = tk.Menu(filemenu)  # 和上面定义菜单一样，不过此处实在File上创建一个空的菜单
# filemenu.add_cascade(label='Import', menu=submenu, underline=0)  # 给放入的菜单submenu命名为Import
#
# # 第9步，创建第三级菜单命令，即菜单项里面的菜单项里面的菜单命令（有点拗口，笑~~~）
# submenu.add_command(label='Submenu_1', command=do_job)  # 这里和上面创建原理也一样，在Import菜单项中加入一个小菜单命令Submenu_1

# 第11步，创建菜单栏完成后，配置让菜单栏menubar显示出来
window.config(menu=menubar)

debug = 0
windowFormWidth = 500
windowFormHeight = 520
fw = 490
fh = 290


def checkSerialReceiverData():
    global serialSendDataNumberOfByte, serialgetDataNumberOfByte
    try:
        if serialPortOpenHl.isOpen():
            if serialPortOpenHl.in_waiting > 0:
                number_of_read_byte = serialPortOpenHl.in_waiting
                ser_read_data = serialPortOpenHl.read(number_of_read_byte)
                if serialReceiveHexSelectV.get() == 1:
                    ser_read_data_convert = ''
                    for eachData in ser_read_data:
                        ser_read_data_convert = ser_read_data_convert + ' {0:0>2x}'.format(eachData)
                    # ser_read_data = binascii.b2a_hex(ser_read_data)
                else:
                    ser_read_data_convert = str(ser_read_data, 'utf-8')
                serialReceiveDataTextForm.insert(END, ser_read_data_convert)
                serialReceiveDataTextForm.see(END)

                serialgetDataNumberOfByte = serialgetDataNumberOfByte + number_of_read_byte
                logTextForm.config(
                    text='发送字节:{0} 接收字节:{1}'.format(serialSendDataNumberOfByte, serialgetDataNumberOfByte))

        window.after(100, checkSerialReceiverData)  # add_letter will run as soon as the mainloop starts.
    except:
        window.after(100, checkSerialReceiverData)  # add_letter will run as soon as the mainloop starts.

    # logTextForm.config(text='Time:{0}'.format(debug))


logTextForm.config(text='Welcome EeayCOM By lgs')

FormInit()
sysInit()

getSerialList()

checkSerialReceiverData()

window.bind("<Configure>", windowReSize)
# 第8步，主窗口循环显示#####

window.mainloop()