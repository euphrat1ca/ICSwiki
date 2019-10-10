from abc import ABCMeta, abstractmethod
from  DataTypesModule.NumericTypes import *

class VirtualBaseData():
    __metaclass__ = ABCMeta

    @abstractmethod
    def import_data(self, bytes, offset=0):
        '''
            must convert bytes to internal state, return bytes it used
        '''
        pass
    @abstractmethod
    def export_data(self):
        '''
            must return the internal state in bytes
        '''
        pass
    @abstractmethod
    def sizeof(self):
        '''
            must return size in bytes
        '''
        pass
    @abstractmethod
    def __call__(self, *args, **kwargs):
        '''
            must return internal value if parameters are present it must take them for internal value
        '''
        pass

class VirtualBaseStructure():
    __metaclass__ = ABCMeta

    @abstractmethod
    def import_data(self, bytes, offset=0):
        '''
            must convert bytes to internal state, return bytes it used
        '''
        pass
    @abstractmethod
    def export_data(self):
        '''
            must return the internal state in bytes
        '''
        pass
    @abstractmethod
    def sizeof(self):
        '''
            must return size in bytes
        '''
        pass
    @abstractmethod
    def keys(self):
        '''
            must return attribute names of the CIP structure in the order of the CIP structure
        '''
        pass
    @abstractmethod
    def items(self):
        '''
            must return tuple of tuple pair attribute, base data type in the order of the CIP structure
        '''
        pass
    @abstractmethod
    def values(self):
        '''
            must return tuple data types in key order
        '''
        pass
    @abstractmethod
    def __getitem__(self, item):
        '''
            must return attributes base data type shall support indexing by number and name
        '''
        pass
    @abstractmethod
    def __setitem__(self, key, value):
        '''
            must set attributes base data type shall support indexing by number and name
        '''
        pass
    @abstractmethod
    def __len__(self):
        '''
            return number of CIP items in structure
        '''
        pass
    @abstractmethod
    def __iter__(self):
        '''
            must iter though all CIP attributes return the base data type in key order
        '''

    @abstractmethod
    def __next__(self):
        return self



class BaseData(VirtualBaseData, NumberInt, NumberComp, NumberBasic):

    _byte_size = 0
    _signed    = None

    def __init__(self, value=None, endian='little'):
        self._value = value
        self._endian = endian

    @property
    def internal_data(self):
        return self._value

    @internal_data.setter
    def internal_data(self, val):
        self._value = val

    def import_data(self, data, offset=0, endian=None):
        section = data[offset: offset + self._byte_size]
        if endian is None:
            endian = self._endian
        self._value = int.from_bytes(section, endian, signed=self._signed)
        return self._byte_size

    def export_data(self, value=None, endian=None):
        if value is None:
            value = self._value
        if endian is None:
            endian = self._endian
        return int(value).to_bytes(self._byte_size, endian, signed=self._signed)

    def sizeof(self):
        return self._byte_size

    def __call__(self, value=None):
        if value is not None:
            self._value = value
        return self._value

    def __str__(self):
        return str(self._value)

    def __bytes__(self):
        return bytes(self.export_data())

class BaseStructure(VirtualBaseStructure):

    def import_data(self, bytes, offset=0, key_filter=None):
        length = len(bytes)
        start_offset = offset
        for parser, i in zip(self, range(len(self))):
            if key_filter and i not in key_filter:
                continue
            offset += parser.import_data(bytes, offset)
            if length <= offset:
                break
        return offset - start_offset

    def export_data(self, key_filter=None):
        output_stream = bytearray()
        for parser, i in zip(self, range(len(self))):
            if key_filter and i not in key_filter:
                continue
            output_stream += parser.export_data()
        return output_stream

    def sizeof(self):
        size = 0
        for item in self:
            size += item.sizeof()
        return size

    @abstractmethod
    def keys(self):
        '''
            must return attribute names of the CIP structure in the order of the CIP structure
        '''
        pass

    def items(self):
        try:
            return self._items
        except:
            self._items = []
            for k in self.keys():
                try:
                    self._items.append((k, self.__dict__[k]))
                except:
                    # for subclassed container types
                    self._items.append((k, self[k]))
        return self._items

    def values(self):
        try:
            return self._values
        except:
            self._values = tuple([item[1] for item in self.items()])
        return self._values

    def dict(self):
        try:
            return self._dict
        except:
            self._dict = {item[0]:item[1] for item in self.items()}
        return self._dict

    def __getitem__(self, item):
        '''
            getitem returns the a base data type not a value
        '''
        if isinstance(item, str):
            attr = item
        elif isinstance(item, int):
            attr = self.keys()[item]
        return self.__dict__[attr]


    def __setitem__(self, key, value):
        '''
            setitem sets the a base data type not a value
        '''
        if isinstance(key, str):
            attr = key
        elif isinstance(key, int):
            attr = self.keys()[key]
        if not hasattr(value, 'sizeof'):
            raise ValueError("Structure objects must be a data parser")
        self.__dict__[attr] = value

    def __len__(self):
        return len(self.keys())

    def __iter__(self):
        for x in self.values():
            yield x

    def __next__(self):
        return self.values()

    def __bytes__(self):
        return bytes(self.export_data())

    def recalculate(self):
        '''
            for performance items, values are calculated once off the keys.
            if keys are ever modified they must be recalculated
        '''
        for at in ('_items', '_values', '_dict'):
            try:
                delattr(self, at)
            except:
                pass

    def data_dump(self):
        output = []
        for key, val in self.items():
            try:
                output.append((key, val.data_dump()))
            except AttributeError:
                output.append((key, str(val)))
        return output


class BaseStructureAutoKeys(BaseStructure):

    def keys(self):
        try:
            return self._keys
        except:
            self._keys = []
        return self._keys

    def add_key(self, Name):
        try:
            self._keys
        except:
            self._keys = []
        if Name not in self._keys:
            self._keys.append(Name)
            self.recalculate()

    def __setattr__(self, key, value):
        if hasattr(value, 'sizeof'):
            self.add_key(key)
        super().__setattr__(key, value)

def print_structure(structure, output=print, depth=0):
    struct = structure.data_dump()

    def printer(sub, depth, output):
        for key, val in sub:
            if isinstance(val, list):
                output('%s%s:-' % ('\t'*depth, key))
                printer(val, depth+1, output)
            else:
                output('%s%s: %s' % ('\t'*depth, key, val))
    printer(struct, depth, output)
