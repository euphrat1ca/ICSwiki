# -*- coding: utf-8 -*-

"""
Author: YJ
Email: yj1516268@outlook.com
Created Date: 2018-07-16 15:46:24

1:AC/DC/RLY ; 2:DC ; 3:RLY
b'\x00\x00\x00\x00'
1.DOa.0-7
1.DOb.0-1 + 3.DOa.0-5
3.DOa.6-7 + 3.DOb.0-5
3.DOb.6-7
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
        self.bool_start = bool_start = 100
        self.bool_end = bool_end = 104

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

    def write_Bool(self):
        """
        Write Bool type Data to snap7-server
        """
        area = snap7.snap7types.areas.MK
        self.client.write_area(area, self.db, self.bool_start,
                b'\xff\x00\x00\x00')


if __name__ == "__main__":
    plc = PLC()
    print("<原始值> -------------->")
    plc.read_Bool()
    plc.write_Bool()
    print("<当前值> -------------->")
    plc.read_Bool()
