import tkinter as tk  # 使用Tkinter前需要先导入

import serial
import serial.tools.list_ports
from tkinter import ttk

# 第1步，实例化object，建立窗口window
window = tk.Tk() ##



# 第2步，给窗口的可视化起名字
window.title('My Window')


# 第3步，设定窗口的大小(长 * 宽)
window.geometry('500x500')  # 这里的乘是小x

# 第4步，在图形界面上设定输入框控件entry框并放置
e = tk.Entry(window, show=None)  # 显示成明文形式
e.grid(column=0, row=0)


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


def insert_end():  # 在文本框内容最后接着插入输入内容
    try:
        port_list = list(serial.tools.list_ports.comports())
        portx = port_list[0].device
        bps = 115200
        # 超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
        timex = None
        ser = serial.Serial(portx, bps, timeout=timex)
        print("串口详情参数：", ser)

        # 十六进制的发送
        result = ser.write(chr(0x06).encode("utf-8"))  # 写数据
        print("Test", result)

        # 十六进制的读取
        print(ser.read().hex())  # 读一个字节

        print("---------------")
        ser.close()  # 关闭串口

    except Exception as e:
        print("---异常---：", e)


# 第6步，创建并放置两个按钮分别触发两种情况
b1 = tk.Button(window, text='Get Serial', width=10,
               height=2, command=insert_point)
b1.grid(column=0, row=1)
b2 = tk.Button(window, text='insert end', width=10,
               height=2, command=insert_end)
b2.grid(column=0, row=2)



# 第7步，创建并放置一个多行文本框text用以显示，指定height=3为文本框是三个字符高度
t = tk.Text(window, width=50,height=10)
t.grid(column=0, row=3)



numberChosen = ttk.Combobox(window, width=22, textvariable=5)
numberChosen['values'] = (1, 2, 4, 42, 100)  # 设置下拉列表的值
numberChosen.grid(column=0, row=4)  # 设置其在界面中出现的位置  column代表列   row 代表行



# 第8步，主窗口循环显示
window.mainloop()