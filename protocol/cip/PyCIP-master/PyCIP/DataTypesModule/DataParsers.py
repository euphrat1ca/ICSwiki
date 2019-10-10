from collections import OrderedDict
import struct
import socket
import abc
from DataTypesModule.EPATH import EPATH

class CIPDataStructureVirtual(object):
    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod
    def keys(self):
        pass

    @abc.abstractmethod
    def import_data(self, bytes, offset=0):
        pass
    @abc.abstractmethod
    def export_data(self):
        pass

    def items(self):
        d = self.get_dict()
        return [(key, d[key]) for key in self.keys()]

    def get_dict(self):
        return {k:self.__dict__[k] for k in self.keys()}

    def __len__(self):
        return len(self.export_data())

    def pprint(self):
        string_list = []
        for key, val in self.items():
            try:
                tmp = ['\t' + x for x in val.pprint()]
                string_list.append("%s:-" % key)
                string_list += tmp
            except AttributeError:
                string_list.append("%s: %s" % (key, val))
        return string_list

    def print(self):
        return '\n'.join(self.pprint())

class CIPDataStructure(CIPDataStructureVirtual):
    global_structure = OrderedDict()

    def __init__(self, *data_tuple, **initial_values):
        self.structure = OrderedDict(self.global_structure)
        self.structure.update(data_tuple)
        self._keys = list(self.structure.keys())
        self._struct_list = tuple(self.structure.items())
        self.byte_size = 0
        self.data = {}
        self.set_values(initial_values)

    def __getattr__(self, item):
        if item in self.structure:
            return self.data[item]

    def __setattr__(self, key, value):
        if 'structure' in self.__dict__:
            if key in self.structure:
                self.data[key] = value
                return None
        super().__setattr__(key, value)

    def __getitem__(self, item):
        name = item
        if isinstance(item, int):
            name = self._keys[item]
        return self.data[name]

    def __setitem__(self, key, value):
        name = key
        if isinstance(key, int):
            name = self._keys[key]
        self.data[name] = value

    def __iter__(self):
        for key in self._keys:
            yield self.data[key]

    def set_values(self, dict_vals):
        for k, v in dict_vals.items():
            self.__setattr__(k, v)

    def items(self):
        return [(key, self.data[key]) for key in self._keys]

    def get_struct(self, index=None):
        if index:
            return self._struct_list[index]
        return self._struct_list

    def keys(self):
        return self._keys

    def import_data(self, bytes, offset=0):
        start_offset = offset
        for key, val in self.structure.items():
            try:
                # see if string representation of type is used
                if isinstance(val, str):
                    val = CIPDataTypes[val]
                # check to see if object need instantiating
                if val.__class__ == type:
                    val = val()
                # see if the type can parse
                self.data[key] = val.import_data(bytes, offset)
                offset += val.byte_size
            except (AttributeError, KeyError):
                sub_struct = val
                # otherwise if not a base unit type see if it is an array with length defined by a previous element
                if isinstance(val[0], str):
                    size = self.data[val[0]]
                    sub_struct = [(i, val[1]) for i in range(size)]
                 # otherwise if not a base unit type see if it is an array with length defined as int
                elif isinstance(val[0], int):
                    sub_struct = [(i, val[1]) for i in range(val[0])]
                # send new sub struct down as a new struct
                if isinstance(sub_struct, (list, tuple)):
                    self.data[key] = CIPDataStructure(*sub_struct)
                    offset += self.data[key].import_data(bytes, offset).byte_size
        self.byte_size = offset - start_offset
        return self

    def export_data(self):
        data_out = bytearray()
        for key, val in self.structure.items():
            if isinstance(val, str):
                val = CIPDataTypes[val]
            try:
                data_out += self.data[key].export_data()
                continue
            except AttributeError:
                pass
            try:
                data_out += val.export_data(self.data[key])
                continue
            except AttributeError:
                pass
            raise TypeError("No parser for " + key)
        self.byte_size = len(data_out)
        return data_out

    def get_dict(self):
        return self.data

    def pprint(self):
        string_list = []
        for key, val in self.items():
            try:
                tmp = ['\t' + x for x in val.pprint()]
                string_list.append("%s:-" % key)
                string_list += tmp
            except AttributeError:
                string_list.append("%s: %s" % (key, val))
        return string_list

    def print(self):
        return '\n'.join(self.pprint())



def not_none(primary, secondary):
    return primary if primary != None else secondary


class BaseDataParser():

    def import_data(self, data, offset=0, endian='little'):
        section = data[offset: offset + self.byte_size]
        return int.from_bytes(section, endian, signed=self.signed )

    def export_data(self, value, endian='little'):
        return value.to_bytes(self.byte_size, endian, signed=self.signed)


class Array_CIP(BaseDataParser):

    def __init__(self, data_type, size=None):
        self.data_type = data_type
        self.size = size

    def import_data(self, data, offset=0):
        i=0

class StringDataParser():

    def __init__(self, char_size=1):
        self.char_size = char_size
        self.byte_size = 0

    def import_data(self, data, offset=0):
        section = data[offset: offset + 2]
        offset += 2
        string_size =  int.from_bytes(section, 'little', signed=0 )
        section = data[offset: offset + (self.char_size * string_size)]

        self.byte_size = offset + (self.char_size * string_size)

        if(string_size % 2):
            self.byte_size += 1

        if self.char_size == 1:
            return section.decode('iso-8859-1')
        elif self.char_size > 1:
            return bytes.decode('utf-8')
        else:
            return u'Error: Incorrect character size defined'

    def export_data(self, string):
        length = len(string)
        out = struct.pack('H', length)
        if self.char_size == 1:
            out += string.encode('iso-8859-1')
        elif self.char_size > 1:
            out += string.encode('utf-8')
        else:
            return u'Error: Incorrect character size defined'

        if(length % 2):
            out += bytes(1)
        return out

class ShortStringDataParser():

    def __init__(self):
        self.char_size = 1

    def import_data(self, data, offset=0):
        section = data[offset: offset + 1]
        offset += 1
        string_size =  int.from_bytes(section, 'little', signed=0 )
        section = data[offset: offset + (self.char_size * string_size)]
        self.byte_size = offset + (self.char_size * string_size)

        string_parsed = section.decode('iso-8859-1')
        #utf_encoded = string_parsed.encode('utf-8')
        return string_parsed

class MAC_CIP(BaseDataParser):
    byte_size = 6
    def __init__(self):
        self.val = []
        pass

    def import_data(self, data, offset=0):
        for i in range(0,6):
            self.val.append(data[offset + i])
        return self

    def export_data(self, value=None):
        self.val = not_none(value ,self.val)
        out = bytearray()
        for v in self.val:
            out += v.to_bytes(1, 'little', signed=False)
        return out

    def __str__(self):
        if len(self.val) == 6:
            return "%02x:%02x:%02x:%02x:%02x:%02x" % tuple(self.val)
        else:
            return "%02x:%02x:%02x:%02x:%02x:%02x" % (0,0,0,0,0,0)

class IPAddress_CIP(BaseDataParser):

    def __init__(self):
        self.val = None
        self.parser = UDINT_CIP()
        self.byte_size = None

    def export_data(self, value=None, endian='little'):
        self.val = not_none(value, self.val)
        return self.parser.export_data(self.val, endian)

    def import_data(self, data, offset=0, endian='little'):
        self.val = self.parser.import_data(data, offset, endian)
        self.byte_size = self.parser.byte_size
        return self

    def __str__(self):
        if self.val:
            return socket.inet_ntoa(struct.pack("!I", self.val))
        else:
            return 'No IP'

class SocketAddress(CIPDataStructureVirtual):
    global_structure  = [('sin_family', 'INT'), ('sin_port', 'UINT'),
                          ('sin_addr', IPAddress_CIP), ('sin_zero', [8,'USINT'])]

    def __init__(self):
        self.sin_family = None
        self.sin_port = None
        self.sin_addr = None
        self.sin_zero = None
        self.byte_size = 0

    def import_data(self, data, offset=0):
        self.byte_size = offset

        self.sin_family = INT_CIP().import_data(data, offset, 'big')
        offset += INT_CIP.byte_size
        self.sin_port = UINT_CIP().import_data(data, offset, 'big')
        offset += UINT_CIP.byte_size
        self.sin_addr = IPAddress_CIP().import_data(data, offset, 'big')
        offset += self.sin_addr.byte_size
        self.sin_zero = ULINT_CIP().import_data(data, offset, 'big')
        offset += ULINT_CIP.byte_size

        self.byte_size = offset - self.byte_size
        return self

    def export_data(self):
        output  = INT_CIP().export_data(self.sin_family, 'big')
        output += UINT_CIP().export_data(self.sin_port, 'big')
        output += self.sin_addr.export_data(endian='big')
        output += ULINT_CIP().export_data(self.sin_zero, 'big')
        self.byte_size = len(output)
        return output

    def keys(self):
        return ('sin_family', 'sin_port', 'sin_addr', 'sin_zero')

    def get_dict(self):
        return self.__dict__

    def items(self):
        return [(k, self.__dict__[k]) for k in self.keys()]

class BOOL_CIP(BaseDataParser):
    byte_size = 1
    signed = 0

class SINT_CIP(BaseDataParser):
    byte_size = 1
    signed = 1

class INT_CIP(BaseDataParser):
    byte_size = 2
    signed = 1

class DINT_CIP(BaseDataParser):
    byte_size = 4
    signed = 1

class LINT_CIP(BaseDataParser):
    byte_size = 8
    signed = 1

class USINT_CIP(BaseDataParser):
    byte_size = 1
    signed = 0

class UINT_CIP(BaseDataParser):
    byte_size = 2
    signed = 0

class UDINT_CIP(BaseDataParser):
    byte_size = 4
    signed = 0

class ULINT_CIP(BaseDataParser):
    byte_size = 8
    signed = 0

class BYTE_CIP(BaseDataParser):
    byte_size = 1
    signed = 0

class WORD_CIP(BaseDataParser):
    byte_size = 2
    signed = 0

class DWORD_CIP(BaseDataParser):
    byte_size = 4
    signed = 0

class LWORD_CIP(BaseDataParser):
    byte_size = 8
    signed = 0


CIPDataTypes = {
    "octet": BYTE_CIP(),
    "BOOL" : BOOL_CIP(),
    "SINT" : SINT_CIP(),
    "INT"  : INT_CIP(),
    "DINT" : DINT_CIP(),
    "LINT" : LINT_CIP(),
    "USINT": USINT_CIP(),
    "UINT" : UINT_CIP(),
    "UDINT": UDINT_CIP(),
    "ULINT": ULINT_CIP(),
    "BYTE" : BYTE_CIP(),
    "WORD" : WORD_CIP(),
    "DWORD": DWORD_CIP(),
    "LWORD": LWORD_CIP(),
    "SHORT_STRING" : ShortStringDataParser(),
    "STRING" : StringDataParser(1),
    "STRING2": StringDataParser(2),
    "EPATH": EPATH()
}


class KeySegment_v4(CIPDataStructure):
    version = 4
    global_structure = OrderedDict((
                                    ('Vendor_ID', 'UINT'),
                                    ('Device_Type', 'UINT'),
                                    ('Product_Code', 'UINT'),
                                    ('Major_Revision', 'BYTE'),
                                    ('Minor_Revision', 'USINT'),

                                    ))


