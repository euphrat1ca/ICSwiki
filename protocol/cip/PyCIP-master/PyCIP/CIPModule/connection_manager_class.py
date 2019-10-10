from collections import OrderedDict
import random
from DataTypesModule.DataParsers import *
from DataTypesModule.DataTypes import *

class ConnectionManager():

    def __init__(self, transport, **kwargs):
        self.trans = transport

        #vol 1 3.18 3-5.4
        self.unconnected_send_struct_header = CIPDataStructure(
                                                                ('Time_tick', 'BYTE'),
                                                                ('Time_out_ticks', 'USINT'),
                                                                ('Embedded_Message_Request_Size', 'UINT'),
                                                               )
        self.unconnected_send_struct_footer = CIPDataStructure(
                                                                ('Route_Path_Size', 'USINT'),
                                                                ('Reserved', 'USINT'),
                                                               )

        self.struct_fwd_open_rsp = CIPDataStructure(
                                                        ('OT_connection_ID', 'UDINT'),
                                                        ('TO_connection_ID', 'UDINT'),
                                                        ('connection_serial', 'UINT'),
                                                        ('O_vendor_ID', 'UINT'),
                                                        ('O_serial', 'UDINT'),
                                                        ('OT_API', 'UDINT'),
                                                        ('TO_API', 'UDINT'),
                                                        ('Application_Size', 'USINT'),
                                                        ('Reserved', 'USINT'),
                                                        ('Data', ['Application_Size', 'BYTE']),
                                                    )

        self.struct_fwd_open_send = CIPDataStructure(
                                                        ('tick','BYTE'),
                                                        ('time_out','USINT'),
                                                        ('OT_connection_ID','UDINT'),
                                                        ('TO_connection_ID','UDINT'),
                                                        ('connection_serial','UINT'),
                                                        ('O_vendor_ID','UINT'),
                                                        ('O_serial','UDINT'),
                                                        ('time_out_multiplier','USINT'),
                                                        ('reserved_1','octet'),
                                                        ('reserved_2','octet'),
                                                        ('reserved_3','octet'),
                                                        ('OT_RPI','UDINT'),
                                                        ('OT_connection_params','WORD'),
                                                        ('TO_RPI','UDINT'),
                                                        ('TO_connection_params','WORD'),
                                                        ('trigger','BYTE'),
                                                        ('path_len','USINT')
                                                    )
        self.struct_fwd_close_send = CIPDataStructure(
                                                        ('tick','BYTE'),
                                                        ('time_out','USINT'),
                                                        ('connection_serial','UINT'),
                                                        ('O_vendor_ID','UINT'),
                                                        ('O_serial','UDINT'),
                                                        ('Reserved', 'USINT'),
                                                        ('path_len','USINT')
                                                    )
    def unconnected_send(self, data, route):

        packet = bytearray()
        e_path = EPATH()
        e_path.append(LogicalSegment(LogicalType.ClassID, LogicalFormat.bit_8, 6))
        e_path.append(LogicalSegment( LogicalType.InstanceID, LogicalFormat.bit_8, 1))

        header = self.unconnected_send_struct_header
        header.Time_tick = 100
        header.Time_out_ticks = 100
        header.Embedded_Message_Request_Size = len(data)

        packet += header.export_data()
        packet += data
        if len(data) % 2:
            packet += bytes([0])

        footer = self.unconnected_send_struct_footer
        if hasattr(route, 'export_data'):
            port_path = route.export_data()
            footer.Route_Path_Size = route.byte_size // 2
            footer.Reserved = 0
        else:
            port_path = bytes()
            for item in route:
                port_path += item
            footer.Route_Path_Size = len(port_path)//2
            footer.Reserved = 0

        packet += footer.export_data()
        packet += port_path

        receipt = self.trans.explicit_message(CIPServiceCode.unconnected_Send, e_path, data=packet)
        return receipt


    def forward_open(self, EPath, tick=10, time_out=1, OT_connection_ID=None, TO_connection_ID=None, connection_serial=None,
                     O_vendor_ID=88, O_serial=12345678, time_out_multiplier=0, reserved_1=0, reserved_2=0, reserved_3=0, OT_RPI=0x03E7FC18,
                     OT_connection_params=0x43FF, TO_RPI=0x03E7FC18, TO_connection_params=0x43FF, trigger=0xa3):

        message_router_path = EPATH()
        message_router_path.append(LogicalSegment(LogicalType.ClassID, LogicalFormat.bit_8, 6))
        message_router_path.append(LogicalSegment(LogicalType.InstanceID, LogicalFormat.bit_8, 1))

        connection_path_bytes = EPath.export_data()

        self.struct_fwd_open_send.tick = tick
        self.struct_fwd_open_send.time_out = time_out
        self.struct_fwd_open_send.OT_connection_ID = OT_connection_ID if OT_connection_ID != None else random.randrange(1, 99999)
        self.struct_fwd_open_send.TO_connection_ID = TO_connection_ID if TO_connection_ID != None else self.trans.get_next_sender_context()
        self.struct_fwd_open_send.connection_serial = connection_serial if connection_serial != None else random.randrange(0, 2^16)
        self.struct_fwd_open_send.O_vendor_ID = O_vendor_ID
        self.struct_fwd_open_send.O_serial = O_serial
        self.struct_fwd_open_send.time_out_multiplier = time_out_multiplier
        self.struct_fwd_open_send.reserved_1 = reserved_1
        self.struct_fwd_open_send.reserved_2 = reserved_2
        self.struct_fwd_open_send.reserved_3 = reserved_3
        self.struct_fwd_open_send.OT_RPI = OT_RPI
        self.struct_fwd_open_send.OT_connection_params = OT_connection_params
        self.struct_fwd_open_send.TO_RPI = TO_RPI
        self.struct_fwd_open_send.TO_connection_params = TO_connection_params
        self.struct_fwd_open_send.trigger = trigger
        self.struct_fwd_open_send.path_len = len(connection_path_bytes)//2

        command_specific = self.struct_fwd_open_send.export_data()

        receipt = self.trans.explicit_message(CIPServiceCode.forward_open, message_router_path, data=(command_specific + connection_path_bytes))
        response = self.trans.receive(receipt)
        if response and response.CIP.General_Status == 0:
            self.struct_fwd_open_rsp.import_data(response.data)
            return self.struct_fwd_open_rsp
        return False


    def forward_close(self, EPath, tick=6, time_out=0x28, connection_serial=None, O_vendor_ID=88, O_serial=12345678):

        message_router_path = EPATH()
        message_router_path.append(LogicalSegment(LogicalType.ClassID, LogicalFormat.bit_8, 6))
        message_router_path.append(LogicalSegment(LogicalType.InstanceID, LogicalFormat.bit_8, 1))

        connection_path_bytes = EPath.export_data()

        self.struct_fwd_close_send.tick = tick
        self.struct_fwd_close_send.time_out = time_out
        self.struct_fwd_close_send.connection_serial = connection_serial if connection_serial != None else self.struct_fwd_open_send.connection_serial
        self.struct_fwd_close_send.O_vendor_ID = O_vendor_ID
        self.struct_fwd_close_send.O_serial = O_serial
        self.struct_fwd_close_send.Reserved = 0
        self.struct_fwd_close_send.path_len = len(connection_path_bytes)//2

        command_specific = self.struct_fwd_close_send.export_data()

        receipt = self.trans.explicit_message(CIPServiceCode.forward_close, message_router_path, data=(command_specific + connection_path_bytes))
        response = self.trans.receive(receipt)
        if response and response.CIP.General_Status == 0:
            self.struct_fwd_open_rsp.import_data(response.data)
            return self.struct_fwd_open_rsp
        return None
