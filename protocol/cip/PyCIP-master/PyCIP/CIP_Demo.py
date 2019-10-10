import ENIPModule
import CIPModule
from DataTypesModule import LogicalSegment, LogicalType, LogicalFormat, DataSegment, EPATH, DataSubType, TransportPacket, CIPServiceCode,\
                            ShortStringDataParser, print_structure, MACAddress
import time

def main():
    # Get a EthNetIP Handler un-initialized
    ENIP_Layer = ENIPModule.ENIP_Originator()

    # broadcast a list identity
    rsp = ENIP_Layer.list_identity()
    devices = ENIPModule.parse_list_identity(rsp)
    print("devices found: " + ', '.join(devices.keys()))

    device_ip = devices['1715-AENTR'][0]
    reply = ENIP_Layer.register_session(str(device_ip))
    if not reply:
        return

    # create a CIP handler with a ENIP layer
    con = CIPModule.CIP_Manager(ENIP_Layer)
    data = con.get_attr_all(1, 1)

    # convenience object can use the CIP handler, they have knowledge of the CIP object structure and services
    ID1 = CIPModule.Identity_Object(con)
    print_structure(ID1)


    DLR = CIPModule.DLR_Object(con)
    print(DLR)
    print()


    # CIP handler can perform common services such as get attr,
    # raw rsp come in the form of a transport packet from DataTypes.TransportPacket
    TransportPacket()
    rsp = con.get_attr_single(1 , 1 , 7)
    # the structure is as follows:
    print("transport header:-")
    print_structure(rsp.encapsulation_header, depth=1)
    print("command specific:-")
    print_structure(rsp.command_specific, depth=1)
    print("common packet format:-")
    print_structure(rsp.CPF, depth=1)
    print("CIP format:-")
    print_structure(rsp.CIP, depth=1)
    print("raw data in CIP packet:-")
    print('\t', rsp.data)


    # a raw encap send can be used instead of the built in methods

    # first building a EPATH object this is a path to the name field in the identity object
    epath = EPATH()
    epath.append(LogicalSegment(LogicalType.ClassID, LogicalFormat.bit_8, 0x04))
    epath.append(LogicalSegment(LogicalType.InstanceID, LogicalFormat.bit_8, 0x67))
    epath.append(LogicalSegment(LogicalType.ConnectionPoint, LogicalFormat.bit_8, 0x68))
    epath.append(LogicalSegment(LogicalType.ConnectionPoint, LogicalFormat.bit_8, 0x6A))
    epath.append(DataSegment(DataSubType.SimpleData, bytearray([0,0,0,0])))

    # raw send is used along with the service code
    rsp = con.forward_open(epath)

    # check to see if successful before parsing
    if rsp:
        parsed_string = ShortStringDataParser().import_data(rsp.data)
        print(parsed_string)

    # close down
    ENIP_Layer.unregister_session()

    return


if __name__ == '__main__':
    main()