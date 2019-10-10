from CIPModule import CIP
from DataTypesModule.DataTypes import *
from DataTypesModule.DataParsers import *
class DLR_Object():

    def __init__(self, transport, **kwargs):
        active_node_struct = [
            ('Device_IP_Address', IPAddress_CIP),
            ('Device_MAC_Address', MAC_CIP),
        ]
        self.class_struct = CIPDataStructure(
                ('Revision', 'UINT')
        )
        self.master_struct = CIPDataStructure(
            ('Network_Topology', 'USINT'),
            ('Device_Type', 'USINT'),
            ('Ring_Supervisor_Status', 'USINT'),
            ('Ring_Supervisor_Config', [
                ('Ring_Supervisor_Enable', 'BOOL'),
                ('Ring_Supervisor_Precedence', 'USINT'),
                ('Beacon_Interval', 'UDINT'),
                ('Beacon_Timeout', 'UDINT'),
                ('DLR_VLAN_ID', 'UINT'),
            ]),
            ('Ring_Faults_Count', 'UINT'),
            ('Last_Active_Node_on_Port_1', active_node_struct),
            ('Last_Active_Node_on_Port_2', active_node_struct),
            ('Ring_Protocol_Participants_Count', 'UINT'),
            ('Ring_Protocol_Participants_List', ['Ring_Protocol_Participants_Count', [
                ('Device_IP_Address', IPAddress_CIP),
                ('Device_MAC_Address', MAC_CIP)
            ]]),
            ('Ring_Faults_Count', 'UINT'),
            ('Active_Supervisor_Address', [
                ('Device_IP_Address', IPAddress_CIP),
                ('Device_MAC_Address', MAC_CIP)
            ]),
            ('Active_Supervisor_Precedence', 'USINT'),
            ('Capability_Flags', 'DWORD'),
            ('Gateway_Config', [
                    ('Redundant Gateway Enable', 'BOOL'),
                    ('Gateway_Precedence','USINT'),
                    ('Advertise_Interval','UDINT'),
                    ('Advertise_Timeout','UDINT'),
                    ('Learning_Update_Enable','BOOL'),
                ]
             ),
            ('Redundant_Gateway_Status', 'USINT'),
            ('Active_Gateway_Address', [
                    ('Device_IP_Address', 'UDINT'),
                    ('Device_MAC_Address', MAC_CIP)
                ]
             ),
            ('Active_Gateway_Precedence', 'USINT')
        )

        DLR_1     = 2
        DLR_1_sup = 50
        DLR_2     = 16
        DLR_2_3_all = 54
        DLR_3_gat = 77

        self.dict_of_versions = {
            DLR_1:(1,2,3,4,5,6,7,8,10,11),
            DLR_1_sup:(1,2),
            DLR_2:(1,2,10,12),
            DLR_2_3_all:(1,2,3,4,5,6,7,8,10,11,12),
            DLR_3_gat:(1,2,3,4,5,6,7,8,10,11,12,13,14,15,16)
        }

        self.transport = transport
        self.update()

    def update(self):
        rsp = self.transport.get_attr_single(71, 0, 1)
        if rsp and rsp.CIP.General_Status == 0:
            self.class_struct.import_data(rsp.data)

        rsp = self.transport.get_attr_all(71, 1)
        if rsp.CIP.General_Status == 0:
            data_len = len(rsp.data)
            filter = self.dict_of_versions[data_len]
            st = self.master_struct.get_struct()
            self.struct = CIPDataStructure(*[st[i-1] for i in filter])
            self.struct.import_data(rsp.data)

    def __str__(self):
        return self.struct.print()

