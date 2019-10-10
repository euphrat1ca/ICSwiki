from DataTypesModule.DataParsers import *
import DataTypesModule as DT
from enum import IntEnum

class MessageType(IntEnum):

    explicitUCMM      = 0x00
    explicitCM        = 0x01
    implicitIO        = 0x02


class ENIPCommandCode(IntEnum):

    NOP               = 0x00
    ListServices      = 0x04
    ListIdentity      = 0x63
    ListInterfaces    = 0x64
    RegisterSession   = 0x65
    UnRegisterSession = 0x66
    SendRRData        = 0x6f
    SendUnitData      = 0x70

class CPF_Codes(IntEnum):

    NullAddress       = 0x00
    ConnectedAddress  = 0xA1
    ListIdentity      = 0x63
    SequencedAddress  = 0x8002
    UnconnectedData   = 0xB2
    ConnectedData     = 0xB1
    OTSockaddrInfo    = 0x8000
    TOSockaddrInfo    = 0x8001


class CommandSpecific_Rsp(DT.BaseStructureAutoKeys):
    command = None

class NOP_CS(CommandSpecific_Rsp):
    command = ENIPCommandCode.NOP
    pass

class ListIdentity(CommandSpecific_Rsp):
    command = ENIPCommandCode.ListIdentity
    pass

class ListInterfaces(CommandSpecific_Rsp):
    command = ENIPCommandCode.ListInterfaces
    pass

class RegisterSession(CommandSpecific_Rsp):
    command = ENIPCommandCode.RegisterSession
    def __init__(self, Protocol_version=None, Options_flags=None):
        self.Protocol_version = DT.UINT(Protocol_version)
        self.Options_flags    = DT.UINT(Options_flags)

class UnRegisterSession(CommandSpecific_Rsp):
    command = ENIPCommandCode.UnRegisterSession
    pass

class SendRRData(CommandSpecific_Rsp):
    command = ENIPCommandCode.SendRRData
    def __init__(self, Interface_handle=None, Timeout=None):
        self.Interface_handle = DT.UDINT(Interface_handle)
        self.Timeout          = DT.UINT(Timeout)

class SendUnitData(CommandSpecific_Rsp):
    command = ENIPCommandCode.SendUnitData
    def __init__(self, Interface_handle=None, Timeout=None):
        self.Interface_handle = DT.UDINT(Interface_handle)
        self.Timeout          = DT.UINT(Timeout)

class CommandSpecificParser():
    parsers_rsp = {parser.command:parser for parser in CommandSpecific_Rsp.__subclasses__()}

    @classmethod
    def import_data(cls, data, command, response=False, offset=0):
        if response:
            data_parser = cls.parsers_rsp[command]()
        else:
            pass
        data_parser.import_data(data, offset)
        return data_parser

class ENIPEncapsulationHeader(DT.BaseStructureAutoKeys):

    def __init__(self, Command=None, Length=None, Session_Handle=None, Status=None, Sender_Context=None, Options=0) :

        self.Command        = DT.UINT(Command)
        self.Length         = DT.UINT(Length)
        self.Session_Handle = DT.UDINT(Session_Handle)
        self.Status         = DT.UDINT(Status)
        self.Sender_Context = DT.ULINT(Sender_Context)
        self.Options        = DT.UDINT(Options)

class SocketAddress(DT.BaseStructureAutoKeys):

    def __init__(self):
        self.sin_family = DT.INT(endian='big')
        self.sin_port = DT.UINT(endian='big')
        self.sin_addr = DT.IPAddress(endian='big')
        self.sin_zero = DT.ARRAY(DT.USINT, 8)

class TargetItems(DT.BaseStructureAutoKeys):

    def __init__(self):
        self.Item_ID        = DT.UINT()
        self.Item_Length    = DT.UINT()
        self.Version        = DT.UINT()
        self.Socket_Address = SocketAddress()
        self.Vendor_ID      = DT.UINT()
        self.Device_Type    = DT.UINT()
        self.Product_Code   = DT.UINT()
        self.Revision       = DT.Revision()
        self.Status         = DT.WORD()
        self.Serial_Number  = DT.UDINT()
        self.Product_Name   = DT.SHORTSTRING()
        self.State          = DT.USINT()


class ListIdentityRsp(DT.BaseStructureAutoKeys):

    def __init__(self):
        self.Item_Count = DT.UINT()
        self.Target_Items = DT.ARRAY(TargetItems, self.Item_Count)