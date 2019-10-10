
import struct
from DataTypesModule.Constants import *

class TransportPacket():

    def __init__(self, transport_meta_data=None, encapsulation_header=None, command_specific=None, CPF=None, data=None, CIP=None):
        self.response_id = None
        self.transport_meta_data = transport_meta_data
        self.encapsulation_header = encapsulation_header
        self.command_specific = command_specific
        self.CPF = CPF
        self.CIP = CIP
        self.offset = 0
        self.data = data

    def show_data_hex(self):
        return ' '.join(format(x, '02x') for x in self.data)



# depreciated
def EPath_item(*args, **kwargs):
    seg_type = args[0]
    temp_byte = 0
    data_out = bytearray()
    if  seg_type == SegmentType.PortSegment:
        port = args[1]
        link_address = args[2] # can be a list or a int
        if hasattr(link_address, '__len__') and len(link_address) > 1:
            temp_byte |= 1 << 4
            data_out.append(len(link_address))

        if port >= 15:
            temp_byte |= 0x0f
            data_out += struct.pack('H', port)
        temp_byte |= 0x07 & port
        data_out.insert(0, temp_byte)
        if not isinstance(link_address, (list, tuple)):
            link_address = [link_address]
        data_out += bytes(link_address)
        if len(data_out) % 2:
            data_out += bytearray(0)

    elif seg_type == SegmentType.LogicalSegment:
        temp_byte = 0x07 & args[0]
        temp_byte = temp_byte << 3
        temp_byte |= 0x07 & args[1]
        temp_byte = temp_byte << 2
        temp_byte |= 0x03 & args[2]
        data_out = struct.pack('B', temp_byte)
        data_out = data_out + struct.pack('B', args[3])

    elif seg_type == SegmentType.NetworkSegment:
        pass
    elif seg_type == SegmentType.DataSegment:
        pass
    elif seg_type == SegmentType.DataType_c:
        pass
    elif seg_type == SegmentType.DataType_e:
        pass
    elif seg_type == SegmentType.Reserved:
        pass
    return data_out
