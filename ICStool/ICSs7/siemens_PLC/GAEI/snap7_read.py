# -*- coding: utf-8 -*-

"""
Author: YJ
Email: yj1516268@outlook.com
Created Date: 2018-07-16 15:46:24

"""

import snap7
from snap7 import util


class PLC:
    def __init__(self):
        """Connect to snap7-server"""
        # connect param
        ip = "192.168.41.101"
        port = 102
        rack = 0
        slot = 0

        # db num
        self.db = 0

        # start & end num
        self.bool_start = bool_start = 10
        self.bool_end = bool_end = 20

        # data size
        self.bool_size = bool_end - bool_start + 1

        # create client
        self.client = snap7.client.Client()
        self.client.connect(ip, rack, slot, port)

    def read_Bool(self):
        """
        Read Bool type Data from snap7-server
        """
        # read
        area = snap7.snap7types.areas.MK        # {PE:input, PA:output, MK:bit memory, DB:DB, CT:counters, TM:Timers}
        data = self.client.read_area(area, self.db, self.bool_start,
                self.bool_size)
        print(data)

        # analysis
        bool_list = []
        for be in range(0, self.bool_size):
            for bl in range(0, 8):
                bool_data = util.get_bool(data, byte_index=be, bool_index=bl)
                bool_list.append(bool_data)

        print("bool_list<{}> = {}".format(len(bool_list), bool_list))


if __name__ == "__main__":
    plc = PLC()
    print("<原始值> -------------->")
    plc.read_Bool()
