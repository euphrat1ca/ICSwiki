from threading import Thread
#from multiprocessing import Process as Thread
from enum import IntEnum
from CIPModule.connection_manager_class import ConnectionManager
from DataTypesModule import *
from collections import OrderedDict
from Tools.signaling import Signaler, SignalerM2M
import struct


class Basic_CIP():

    def __init__(self, transportLayer, **kwargs):
        self.trans = transportLayer
        self.sequence_number = 1
        self.connected = False
        self.OT_connection_id = None
        self.TO_connection_id = None
        self.active = True
        self.transport_messenger = Signaler()
        self.cip_messenger = SignalerM2M()
        self._cip_manager_thread = Thread(target=self._CIP_manager, args=[self.trans], name="cip_layer")
        self._cip_manager_thread.start()

    def _CIP_manager(self, trans):
        while self.active and self.trans.connected:
            message_structure = self.transport_messenger.get_message(0.1)
            if message_structure == None:
                continue
            packet = message_structure.message

            signal_id = 0
            # UnConnected Explicit
            if (packet.CPF[0].Type_ID == CPF_Codes.NullAddress
            and packet.CPF[1].Type_ID == CPF_Codes.UnconnectedData):
                message_response = MessageRouterResponseStruct_UCMM()
                message_response.import_data(packet.data)
                packet.CIP = message_response
                packet.data = packet.data[packet.CIP.sizeof():]
                signal_id = packet.encapsulation_header.Sender_Context()
                self.transport_messenger.unregister(message_structure.signal_id)

            # Connected Explicit
            elif(packet.CPF[0].Type_ID == CPF_Codes.ConnectedAddress
            and packet.CPF[1].Type_ID == CPF_Codes.ConnectedData):
                message_response = MessageRouterResponseStruct()
                message_response.import_data(packet.data)
                packet.CIP = message_response
                packet.data = packet.data[packet.CIP.sizeof():]
                signal_id = message_response.Sequence_Count

            # Connected Implicit
            elif(packet.CPF[0].Type_ID == CPF_Codes.SequencedAddress
            and packet.CPF[1].Type_ID == CPF_Codes.ConnectedData):
                print("Connected Implicit Not Supported Yet")
                continue
            self.cip_messenger.send_message(signal_id, packet)

        return None
    def get_next_sender_context(self):
        return self.trans.get_next_sender_context()

    def set_connection(self, OT_connection_id, TO_connection_id):
        self.connected = True
        self.OT_connection_id = OT_connection_id
        self.TO_connection_id = TO_connection_id

    def clear_connection(self):
        self.connected = False
        self.OT_connection_id = None
        self.TO_connection_id = None

    def explicit_message(self, service, EPath, data=None, receive=True):
        packet = bytearray()
        if self.connected:
            self.sequence_number += 1
            sequence_number = self.sequence_number
            packet += struct.pack('H', sequence_number)

        packet += explicit_request(service, EPath, data=data)

        if receive:
            receive_id = self.TO_connection_id if self.TO_connection_id else self.trans.get_next_sender_context()
            # if we want the manager to be notified that this message has been responded too, we must register
            self.transport_messenger.register(receive_id)
            if self.connected:
                receipt = sequence_number
            else:
                receipt = receive_id
            self.cip_messenger.register(receipt)
        else:
            receive_id = None

        # SEND PACKET
        context = self.trans.send_encap(packet, self.OT_connection_id, receive_id)

        return receipt

    def receive(self, receive_id, time_out=5):
        message = self.cip_messenger.get_message(receive_id, time_out)
        if message:
            return message.message
        else:
            return None

class ReplyService(BaseBitFieldStruct):
    def __init__(self):
        self.RequestResponse = BaseBitField(1)
        self.Service = BaseBitField(7)

#vol1 ver 3.18 2-4.2
class MessageRouterResponseStruct(BaseStructureAutoKeys):

    def __init__(self):
        self.Sequence_Count = UINT()
        self.Reply_Service = ReplyService()
        self.Reserved = USINT()
        self.General_Status = USINT()
        self.Size_of_Additional_Status = USINT()
        self.Additional_Status = ARRAY(WORD, self.Size_of_Additional_Status)

#vol1 ver 3.18 2-4.2
class MessageRouterResponseStruct_UCMM(BaseStructureAutoKeys):

    def __init__(self):
        self.Reply_Service = ReplyService()
        self.Reserved = USINT()
        self.General_Status = USINT()
        self.Size_of_Additional_Status = USINT()
        self.Additional_Status = ARRAY(WORD, self.Size_of_Additional_Status)

def explicit_request(service, EPath, data=None):
    request = bytearray()
    request.append(service)
    EPath_bytes = EPath.export_data()
    request.append(len(EPath_bytes)//2)
    request += EPath_bytes
    if data is not None:
        request += data
    return request


class CIP_Manager():

    def __init__(self, transport, *EPath):
        self.trans = transport
        self.path = EPath
        self.primary_connection = Basic_CIP(transport)
        self.current_connection = self.primary_connection
        self.connection_manager = ConnectionManager(self.primary_connection)
        self.e_connected_connection = None

        # if there is a path then we make a connection
        if len(self.path):
            self.forward_open(*EPath)

    def forward_open(self, EPath=None, **kwargs):
        if EPath == None:
            self.path = EPATH()
            self.path.append(LogicalSegment(LogicalType.ClassID, LogicalFormat.bit_8, 2))
            self.path.append(LogicalSegment(LogicalType.InstanceID, LogicalFormat.bit_8, 1))
        else:
            self.path = EPath
        self._fwd_rsp = self.connection_manager.forward_open(self.path, **kwargs)
        if self._fwd_rsp:
            self.e_connected_connection = Basic_CIP(self.trans)
            self.e_connected_connection.set_connection(self._fwd_rsp.OT_connection_ID, self._fwd_rsp.TO_connection_ID)
            self.current_connection = self.e_connected_connection
            return self._fwd_rsp
        return False

    def forward_close(self, EPath=None, **kwargs):
        if EPath == None:
            self.path = EPATH()
            self.path.append(LogicalSegment(LogicalType.ClassID, LogicalFormat.bit_8, 2))
            self.path.append(LogicalSegment(LogicalType.InstanceID, LogicalFormat.bit_8, 1))
        else:
            self.path = EPath
        fwd_rsp = self.connection_manager.forward_close(self.path, **kwargs)
        if fwd_rsp:
            self.current_connection.clear_connection()
            del self.current_connection
            return fwd_rsp
        return False

    def explicit_message(self, service, request_path, data=None, route=None, try_connected=True):

        if try_connected and self.e_connected_connection and self.e_connected_connection.connected:
            connection = self.e_connected_connection
            receipt = connection.explicit_message(service, request_path, data=data)
        elif route:
            message = explicit_request(service, request_path, data=data)
            connection = self.connection_manager
            receipt = connection.unconnected_send(message, route)
        else:
            connection = self.primary_connection
            receipt = connection.explicit_message(service, request_path, data=data)

        return connection.receive(receipt)

    def get_attr_single(self, class_int, instance_int, attribute_int, try_connected=True, route=None):
        path = EPATH()
        path.append(LogicalSegment(LogicalType.ClassID, LogicalFormat.bit_8, class_int))
        path.append(LogicalSegment(LogicalType.InstanceID, LogicalFormat.bit_8, instance_int))
        path.append(LogicalSegment(LogicalType.AttributeID, LogicalFormat.bit_8, attribute_int))

        return self.explicit_message(CIPServiceCode.get_att_single, path, try_connected=try_connected, route=route)


    def get_attr_all(self, class_int, instance_int, try_connected=True, route=None):
        path = EPATH()
        path.append(LogicalSegment(LogicalType.ClassID, LogicalFormat.bit_8, class_int))
        path.append(LogicalSegment(LogicalType.InstanceID, LogicalFormat.bit_8, instance_int))

        return self.explicit_message(CIPServiceCode.get_att_all, path, try_connected=try_connected, route=route)

    def set_attr_single(self, class_int, instance_int, attribute_int, data, try_connected=True, route=None):
        path = EPATH()
        path.append(LogicalSegment(LogicalType.ClassID, LogicalFormat.bit_8, class_int))
        path.append(LogicalSegment(LogicalType.InstanceID, LogicalFormat.bit_8, instance_int))
        path.append(LogicalSegment(LogicalType.AttributeID, LogicalFormat.bit_8, attribute_int))

        return self.explicit_message(CIPServiceCode.set_att_single, path, try_connected=try_connected, route=route)

    def set_attr_all(self, class_int, instance_int, attribute_int, data, try_connected=True, route=None):
        path = EPATH()
        path.append(LogicalSegment(LogicalType.ClassID, LogicalFormat.bit_8, class_int))
        path.append(LogicalSegment(LogicalType.InstanceID, LogicalFormat.bit_8, instance_int))

        return self.explicit_message(CIPServiceCode.set_att_single, path, try_connected=try_connected, route=route)


class RoutingType(IntEnum):

    ExplicitDefault     = 0,
    ExplicitDirect      = 1,
    ExplicitConnected   = 2,
    ExplicitUnConnected = 3,

    ImplicitDefault     = 4,
    ImplicitDirect      = 5,
    ImplicitConnected   = 6,
    ImplicitUnConnected = 7,