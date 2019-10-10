from enum import IntEnum

class CIPServiceCode(IntEnum):

    get_att_single = 0x0e
    set_att_single = 0x10
    get_att_all    = 0x01
    set_att_all    = 0x02
    unconnected_Send = 0x52
    forward_open   = 0x54
    forward_close  = 0x4E

class SegmentType(IntEnum):

    PortSegment     = 0
    LogicalSegment  = 1
    NetworkSegment  = 2
    SymbolicSegment = 3
    DataSegment     = 4
    DataType_c      = 5
    DataType_e      = 6
    Reserved        = 7

class LogicalType(IntEnum):

    ClassID         = 0
    InstanceID      = 1
    MemberID        = 2
    ConnectionPoint = 3
    AttributeID     = 4
    Special         = 5
    ServiceID       = 6
    ExtendedLogical = 7

class LogicalFormat(IntEnum):

    bit_8    = 0
    bit_16   = 1
    bit_32   = 2
    Reserved = 3

class DataSubType(IntEnum):

    SimpleData = 0
    ANSI       = 9