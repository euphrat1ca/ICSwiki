from DataTypesModule.Constants import *

import struct
import DataTypesModule.BaseDataParsers
from DataTypesModule.BaseDataTypes import *
from DataTypesModule.SpecialDataTypes import *

class SegType():
    type_code = None
    pass

class PortSegment(SegType):
    type_code = SegmentType.PortSegment

    def __init__(self, port=None, link_address=None, bytes_object=None):
        self.port = port
        self.link_address = link_address
        self.link_address_size = 1
        self.extended_port = False
        self.bytes_object = bytes_object

        if port != None and link_address != None:
            self.bytes_object = self.export_data(port, link_address)

    def build(self, port, link_address):
        temp_byte = 0
        data_out = bytearray()
        if hasattr(link_address, '__len__') and len(link_address) > 1:
            temp_byte |= 1 << 4
            data_out.append(len(link_address))
            self.link_address_size = len(link_address)
        if port >= 15:
            temp_byte |= 0x0f
            data_out += struct.pack('H', port)
            self.extended_port = True
        temp_byte |= 0x07 & port
        data_out.insert(0, temp_byte)
        if not isinstance(link_address, (list, tuple)):
            link_address = [link_address]
        data_out += bytes(link_address)
        if len(data_out) % 2:
            data_out += bytearray(0)
        self.bytes_object = data_out
        return data_out

    def export_data(self, port=None, link_address=None):
        self.port         =         port if port != None         else self.port
        self.link_address = link_address if link_address != None else self.link_address

        return self.build(self.port, self.link_address)

    def import_data(self, data, offset=0):
        self.bytes_object = data

    def __str__(self):
        if self.port != None and self.link_address != None:
            return "PortSegment: Port %s, Link %s, Extended %s, Address size %s" % (self.port, self.link_address,
                                                                                    self.extended_port, self.link_address_size)
        return "PortSegment NULL"

class LogicalSegment(SegType):
    type_code = SegmentType.LogicalSegment

    def __init__(self, logical_type=None, format=None, value=None, extended=None, bytes_object=None):
        self.logical_type = logical_type
        self.format = format
        self.value = value
        self.extended = extended
        self.bytes_object = bytes_object

        if self.logical_type != None and self.format != None and self.value != None:
            self.bytes_object = self.export_data(self.logical_type, self.format, self.value, extended=self.extended)

    def build(self, logical_type, format, value, extended=None):
        data_out = bytearray()
        temp_byte = 0x07 & SegmentType.LogicalSegment
        temp_byte = temp_byte << 3
        temp_byte |= 0x07 & logical_type
        temp_byte = temp_byte << 2
        temp_byte |= 0x03 & format
        data_out = struct.pack('B', temp_byte)
        if logical_type == LogicalType.Special:
            data_out += struct.pack('B', value.version)
            data_out += value.export_data()
            self.bytes_object = data_out
            return data_out

        if logical_type == LogicalType.ExtendedLogical:
            if extended == None : raise ValueError("No extended value provided")
            data_out.append(extended)
        if format == LogicalFormat.bit_8:
            data_out += struct.pack('B', value)
        elif format == LogicalFormat.bit_16:
            data_out += struct.pack('H', value)
        elif format == LogicalFormat.bit_32:
            if (logical_type in (LogicalType.InstanceID, LogicalType.ConnectionPoint)
            or extended in (1, 3, 5, 6)):
                data_out += struct.pack('I', value)
            else:
                raise ValueError("Invalid logical extended type for 32 bit format")
        else:
            raise ValueError("Invalid format parameter")
        self.bytes_object = data_out
        return data_out

    def export_data(self, logical_type=None, format=None, value=None, extended=None):
        self.logical_type   = not_none(logical_type, self.logical_type)
        self.format         = not_none(format, self.format)
        self.value          = not_none(value, self.value)
        self.extended       = not_none(extended, self.extended)
        return self.build(self.logical_type, self.format, self.value, extended=self.extended)

    def import_data(self, data, offset=0):
        self.bytes_object = data

    def __str__(self):
        if self.logical_type != None and self.format != None and self.value != None:
            return "Logical: Type %s, format %s, value %s" % (str(LogicalType(self.logical_type)).split('.')[1],
                                                              str(LogicalFormat(self.format)).split('.')[1],
                                                              self.value)
        return "LogicalSegment NULL"

class DataSegment(SegType):
    type_code = SegmentType.DataSegment

    def __init__(self, type=None,  value=None, bytes_object=None):
        self.type = type
        self.value = value
        self.bytes_object = bytes_object

        if self.type != None and self.value != None:
            self.bytes_object = self.export_data(self.type, self.value)

    def build(self, type, value):
        data_out = bytearray()
        temp_byte = 0x07 & SegmentType.DataSegment
        temp_byte = temp_byte << 5
        temp_byte |= 0x17 & type
        data_out.append(temp_byte)
        length = len(value)//2
        if length <= 255:
            data_out.append(length)
            data_out += value
        else:
            raise IndexError("data too large")
        self.length = length
        return data_out

    def export_data(self, type=None, value=None):
        self.type   = not_none(type, self.type)
        self.value  = not_none(value, self.value)
        return self.build(self.type, self.value)

    def import_data(self, data, offset=0):
        self.bytes_object = data

    def __str__(self):
        if self.type != None and self.value != None:
            return "Data: Type %s, size %s" % (str(DataSubType(self.ype)).split('.')[1],
                                               self.length)
        return "DataSegment NULL"


class KeySegment_v4(DataTypesModule.BaseDataParsers.BaseStructureAutoKeys):
    version = 4
    def __init__(self):
        self.Vendor_ID      = UINT()
        self.Device_Type    = UINT()
        self.Product_Code   = UINT()
        self.Minor_Revision = Revision()

class EPATH(list):

    def add(self, *args, **kwargs):
        seg_type, *args = args
        if seg_type == SegmentType.PortSegment:
            item = PortSegment(*args, **kwargs)
        elif seg_type == SegmentType.LogicalSegment:
            item = LogicalSegment(*args, **kwargs)
        else:
            raise TypeError("segment type not supported")
        self.append(item)

    def export_data(self):
        data_out = bytearray()
        for e_item in self:
            data_out += e_item.export_data()
        return data_out

    def import_data(self, data, length, offset=0):
        index = offset
        while index < length + offset:
            seg_type = data[index]
            for sub in SegType.__subclasses__():
                if sub.type_code == seg_type:
                    segment = sub()
                    index += segment.import_data(data,
                                                 )
                    self.append(segment).byte_size
                    break
            else:
                raise ValueError("Value not a acceptable segment: " + str(seg_type))
        return index - offset

def not_none(primary, secondary):
    return primary if primary != None else secondary