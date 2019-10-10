from CIPModule import CIP
from DataTypesModule import *

class Identity_Object(BaseStructureAutoKeys):

    def __init__(self, transport):
        self._transport = transport

        self.Vendor_ID = UINT()
        self.Device_Type = UINT()
        self.Product_Code = UINT()
        self.Revision = Revision()
        self.Status = WORD()
        self.Serial_Number = UDINT()
        self.Product_Name = SHORTSTRING()

        self.update()

    def update(self):
        rsp = self._transport.get_attr_all(1, 1)
        if rsp.CIP.General_Status == 0:
            self.import_data(rsp.data)


class MemberListStruct(BaseStructureAutoKeys):
    def __init__(self):

        self.Member_Data_Description = UINT()
        self.Member_Path_Size = UINT()
        self.Member_Path = EPATH()


class Assembly_Object(BaseStructureAutoKeys):

    def __init__(self, transport):
        self._transport = transport

        self.Number_of_Members_in_List = UINT()
        self.Member_List = ARRAY(MemberListStruct, self.Number_of_Members_in_List)

        self.update()

    def update(self, instance = 1):
        rsp = self._transport.get_attr_all(4, instance)
        if rsp.CIP.General_Status == 0:
            self.import_data(rsp.data)
            return True
        return False

