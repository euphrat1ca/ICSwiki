# -*- coding: utf-8 -*-

"""
Author: YJ
Email: yj1516268@outlook.com
Created Date: 2018-07-16 15:46:24

"""

import snap7
from snap7 import util


class PLC:
    """snap7 - write / read"""
    def __init__(self):
        """
        Connect to snap7-server

        """
        self.conf = conf = {
            "host": "192.168.0.21",    # IP地址
            "rack": 0,              # 台架号
            "slot": 2,              # 插槽号
            "port": 1102,           # 端口
        }
        self.client = snap7.client.Client()
        self.client.connect(
            conf['host'],
            conf['rack'],
            conf['slot'],
            conf['port']
        )

    def write(self, data, db_num=1, start=0):
        """
        Writes to a DB object.

        :param start: write offset
        :param data: bytearray
        """
        self.client.db_write(db_num, start, data)

    def read(self, db_num=1, start=0, size=10):
        """
        Read data from snap7-server

        :param start: 开始的下标
        :param size: 读取的原始数据长度
        """
        data = self.client.db_read(db_num, start, size)

        # int_data = util.get_int(data, 0)        # 2 bytearray --> 1 int
        # dword_data = util.get_dword(data, 1)  # 4 bytearray --> 1 int
        # real_data = util.get_real(data, 0)    # 4 bytearray --> 1 int
        bool_data = util.get_bool(data, 1, 2)    # 4 bytearray --> 1 int
        print(data)
        print(data[1])
        # print(int_data)
        # print(dword_data)
        # print(real_data)
        print(bool_data)


if __name__ == "__main__":
    plc = PLC()
    #plc.write(data=int(0).to_bytes(1, "big"), start=0)
    # plc.write(b'222')
    plc.read()
