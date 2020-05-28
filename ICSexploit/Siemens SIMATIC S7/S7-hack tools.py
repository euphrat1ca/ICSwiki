#!/bin/python
# encoding=utf8
from tkinter import *
import snap7
from functools import reduce


class WidgetsDemo:

    def __init__(self):
        window = Tk()
        window.title("剑思庭-S7 hack Tools")

    # 添加一个多选按钮和单选按钮到frame1
        '''
        frame1 = Frame(window)
        frame1.pack()  #看下面的解释（包管理器）

        self.v2 = IntVar()
        rbRed = Radiobutton(frame1, text = "红色", bg = "red", variable = self.v2, value = 1, command = self.processRaidobutton)
        rbYellow = Radiobutton(frame1, text="黄色", bg="yellow", variable=self.v2, value=2, command=self.processRaidobutton)
         #将cbtBold排列在frame1的网格第一行第一列（网格管理器也会在下面有解释）
        rbRed.grid(row=1, column=2)
        rbYellow.grid(row=1, column=3)
        '''
    # 添加一个label、entry、button和message到frame2
        frame2 = Frame(window)
        frame2.pack()
        label = Label(frame2, text="请输入IP")
        #label2 = Label(frame2, text="端口")
        label3 = Label(frame2, text="机架号")
        label4 = Label(frame2, text="插槽号")
        lblDBNo = Label(frame2, text="db")
        lblDataSz = Label(frame2, text="数据大小(byte)")
        lblDataAd = Label(frame2, text="数据起始地址")
        btnCls = Button(frame2, text="清屏", command=self.cearMsg, width=8)
        btnTstCnn = Button(frame2, text="连接测试", command=self.testCnn, width=8)
        self.v1 = IntVar()
        btnRead = Button(frame2, text="查询数据", command=self.queryData, width=8)
        self.IP = StringVar()
        self.IP.set('192.168.100.1')
        self.slot = IntVar()
        self.rack = IntVar()
        self.port = IntVar()
        self.port.set(502)
        self.DBNo = IntVar()
        self.dataAd = IntVar()
        self.dataSz = IntVar()
        self.data = StringVar()
        self.msg = StringVar()
        self.sendTl = StringVar()
        self.sendTl.set("发送")

        entryIP = Entry(frame2, textvariable=self.IP)
        entryslot = Entry(frame2, textvariable=self.slot)
        entryrack = Entry(frame2, textvariable=self.rack)
        #entryport = Entry(frame2, textvariable=self.port)
        entryDBNo = Entry(frame2, textvariable=self.DBNo)
        entrydataAd = Entry(frame2, textvariable=self.dataAd)
        entrydataSz = Entry(frame2, textvariable=self.dataSz)

        self.btnSendData = Button(
            frame2, text=self.sendTl.get(), command=self.sendData, width=8)
        label.grid(row=1, column=1)
        entryIP.grid(row=1, column=2)
        #label2.grid(row=1, column=3)
        #entryport.grid(row=1, column=4)
        label3.grid(row=1, column=3)
        entryslot.grid(row=1, column=4)
        label4.grid(row=1, column=5)
        entryrack.grid(row=1, column=6)
        lblDBNo.grid(row=2, column=1)
        entryDBNo.grid(row=2, column=2)
        lblDataAd.grid(row=2, column=3)
        entrydataAd.grid(row=2, column=4)
        lblDataSz.grid(row=2, column=5)
        entrydataSz.grid(row=2, column=6)
        btnRead.grid(row=4, column=6, sticky=W)
        self.btnSendData.grid(row=3, column=6, sticky=W)
        btnCls.grid(row=4, column=2, sticky=W)
        btnTstCnn.grid(row=4, column=5)

        lblData = Label(frame2, text="发送数据")
        lblData.grid(row=3, column=1)
        txtData = Entry(frame2, textvariable=self.data, width=62)
        txtData.grid(row=3, column=2, columnspan=4, sticky=W)

       # message.grid(row = 1, column = 4)
    # 添加一个texttext = Text(window)，显示测试的相关信息
        self.txtMsg = Text(window)
        self.txtMsg.pack()
        self.txtMsg.insert(END, "")  # END表示插入到当前文本最后
        window.mainloop()
    # 数据查询，查出结果为Bytestring

    def queryData(self):
        plc = snap7.client.Client()
        try:
            plc.connect(self.IP.get(), self.rack.get(), self.slot.get())
            data = plc.db_read(self.DBNo.get(), self.dataAd, self.dataSz)
            self.txtMsg.insert(END, data)
        except Exception as e:
            self.txtMsg.insert(END, (e, 'IP:', self.IP.get()))
        finally:
            if plc.get_connected():
                plc.disconnect()

    # 清空文本框中的信息
    def cearMsg(self):
        self.txtMsg.delete(1.0, END)
    # 连接测试

    def testCnn(self):
        plc = snap7.client.Client()
        try:
            plc.connect(self.IP.get(), self.rack.get(), self.slot.get())
            # if plc.get_connected:
            self.txtMsg.insert(END, '连接成功')
            plc.disconnect()
        except Exception as e:
            self.txtMsg.insert(END, (e, 'IP:', self.IP.get(), 'Port:'))
    # 发送数据

    def sendData(self):
        plc = snap7.client.Client()
        """
            Here we replace a piece of data in a db block with new data

            Args:
               db (int): The db to use
               start(int): The start within the db
               size(int): The size of the data in bytes
               _butearray (enumerable): The data to put in the db
            """
        try:
            data = self.StrtoByesarray(self.data.get())
            if not data.strip():
                self.txtMsg.insert(END, '发送数据不能为空')
                return
            plc.connect(self.IP.get(), self.rack.get(), self.slot.get())
            plc.db_write(self.DBNo, self.dataAd, data)
        except Exception as e:
            self.txtMsg.insert(END, (e, 'IP:', self.IP.get(), 'Port:'))
        finally:
            if plc.get_connected():
                plc.disconnect()
    # 将bytes字符串转化为bytes

    def StrtoByesarray(self, strdata):
        strarry = strdata.split()
        list = []
        for itm in strarry:
            list.append(itm)

        return bytearray(list)


WidgetsDemo()
