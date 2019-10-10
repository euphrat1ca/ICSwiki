from DataTypesModule.BaseDataTypes import *
from DataTypesModule.BaseDataParsers import *
import socket
import struct
import math

class IPAddress(UDINT):

    def __init__(self, value=None, endian='little'):
        self._value = value
        self._endian = endian

    def __str__(self):
        if self._value:
            return socket.inet_ntoa(struct.pack("!I", self._value))
        else:
            return 'No IP'

class MACAddress(ARRAY):

    def __init__(self):
        super().__init__(USINT, 6)

    def __str__(self):
        try:
            return "%02x:%02x:%02x:%02x:%02x:%02x" % tuple([int(x) for x in self])
        except:
            return "%02x:%02x:%02x:%02x:%02x:%02x" % (0,0,0,0,0,0)
    def __repr__(self):
        return self.__str__()

class Revision(BaseStructureAutoKeys):

    def __init__(self):
        self.Major = USINT()
        self.Minor = USINT()

class BaseBitFieldStruct(BaseStructureAutoKeys):

    def import_data(self, bytes, offset=0):
        length = len(bytes)
        start_offset = offset
        bit_offset = 0
        for parser in reversed(self):
            bit_offset += parser.import_data(bytes, offset, bit_offset)
            offset += bit_offset // 8
            bit_offset = bit_offset % 8
            if length <= offset:
                break
        return offset + math.ceil(bit_offset/8.0) - start_offset

    def export_data(self):
        output = int()
        for parser in reversed(self):
            val = parser.export_data()
            output <<= parser.bit_size()
            output |= val
        output_stream = output.to_bytes(self.sizeof(), 'little')
        return output_stream

    def sizeof(self):
        size = 0
        for item in self:
            size += item.bit_sizeof()
        return size // 8 + (1 if size % 8 else 0)

    def __setattr__(self, key, value):
        if isinstance(value, BaseBitField):
            self.add_key(key)
        super().__setattr__(key, value)

class BaseBitField(VirtualBaseData):

    def __init__(self, bit_size, endian='little'):
        self._bit_size = bit_size
        self._mask = 0b00000001 << bit_size
        self._mask -= 1
        self._byte_size = math.ceil(bit_size/8.0)
        self._endian = endian


    def import_data(self, bytes, offset=0, bit_offset=0, endian=None):
        section = bytes[offset: offset + self._byte_size]
        if endian is None:
            endian = self._endian
        value = int.from_bytes(section, endian, signed=False)
        value = value >> bit_offset
        self._value = value & self._mask
        return self._bit_size

    def export_data(self):
        return self._value & self._mask

    def sizeof(self):
        return self._bit_size

    def bit_sizeof(self):
        return self._bit_size

    def __call__(self, *args, **kwargs):
        return self._value & self._mask

    @property
    def internal_data(self):
        return self._value & self._mask

    @internal_data.setter
    def internal_data(self, val):
        self._value = val & self._mask

    def __str__(self):
        if self._bit_size == 1:
            return str(bool(self._value))
        return str(self._value)
