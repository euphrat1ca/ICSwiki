from DataTypesModule.BaseDataParsers import BaseData, BaseStructure, VirtualBaseStructure

class BOOL(BaseData):
    _byte_size = 1
    _signed = 0

class SINT(BaseData):
    _byte_size = 1
    _signed = 1

class INT(BaseData):
    _byte_size = 2
    _signed = 1

class DINT(BaseData):
    _byte_size = 4
    _signed = 1

class LINT(BaseData):
    _byte_size = 8
    _signed = 1

class USINT(BaseData):
    _byte_size = 1
    _signed = 0

class UINT(BaseData):
    _byte_size = 2
    _signed = 0

class UDINT(BaseData):
    _byte_size = 4
    _signed = 0

class ULINT(BaseData):
    _byte_size = 8
    _signed = 0

class BYTE(BaseData):
    _byte_size = 1
    _signed = 0

class WORD(BaseData):
    _byte_size = 2
    _signed = 0

class DWORD(BaseData):
    _byte_size = 4
    _signed = 0

class LWORD(BaseData):
    _byte_size = 8
    _signed = 0


class ARRAY(list, BaseStructure):

    def __init__(self, data_type, size=None):
        self._data_type = data_type
        self._size = size
        if self._size:
            for _ in range(self._size):
                self.append(self._data_type())

    def import_data(self, data, offset=0, size=None):
        length = len(data)
        start_offset = offset

        if size is None:
            size = int(self._size)

        index = 0
        while offset <= length:
            if index >= size:
                break
            parser = self._data_type()
            offset += parser.import_data(data, offset)
            try:
                self[index] = parser
            except:
                self.append(parser)
            index += 1


        return offset - start_offset

    def keys(self):
        return range(0, len(self))


class STRING(BaseData):

    def __init__(self, char_size=1):
        self._char_size = char_size
        self._byte_size = 0
        self._value

    def import_data(self, data, offset=0):
        start_offset = offset
        section = data[offset: offset + 2]
        offset += 2
        string_size =  int.from_bytes(section, 'little', signed=0 )
        section = data[offset: offset + (self._char_size * string_size)]

        self._byte_size = offset + (self._char_size * string_size)

        if(string_size % 2):
            self._byte_size += 1

        if self._char_size == 1:
            self._value = section.decode('iso-8859-1')
        elif self._char_size > 1:
            self._value =  bytes.decode('utf-8')
        self._byte_size = offset - start_offset
        return self._byte_size

    def export_data(self, string=None):
        if string is None:
            string = self._value
        length = len(string)
        out = USINT().export_data(length)

        if self._char_size == 1:
            out += string.encode('iso-8859-1')
        elif self._char_size > 1:
            out += string.encode('utf-8')

        if(length % 2):
            out += bytes(1)
        self._byte_size = len(out)
        return out

    def sizeof(self):
        self.export_data()
        return self._byte_size


class SHORTSTRING(BaseData):

    def __init__(self):
        self._char_size = 1
        self._byte_size = 0
        self._value = None

    def import_data(self, data, offset=0):
        start_offset = offset
        section = data[offset: offset + 1]
        offset += 1
        string_size =  int.from_bytes(section, 'little', signed=0 )
        section = data[offset: offset + (self._char_size * string_size)]
        self.byte_size = offset + (self._char_size * string_size)

        self._value = section.decode('iso-8859-1')
        self._byte_size =  offset - start_offset
        return self._byte_size

    def export_data(self, string=None):
        if string is None:
            string = self._value
        length = len(string)
        out = USINT().export_data(length)
        out += string.encode('iso-8859-1')
        #if(length % 2):
        #    out += bytes(1)
        self._byte_size = len(out)
        return out

    def sizeof(self):
        self.export_data()
        return self._byte_size
