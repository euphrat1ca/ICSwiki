#python3
from time import sleep
from random import uniform
from pymodbus3 import exceptions
from pymodbus3.client.sync import ModbusTcpClient
import json



def sync_client_read(registerNumber):
     try:
          #client.write_coil(1, False)
          #result = client.read_coils(1,1)
          #print(result.bits[0])
          result = client.read_holding_registers(registerNumber,1)
          return result.registers
          #print(result.bits)
#     except exceptions.ConnectionException:
     except:
          print("Connection Error Handled")
          output=False
     return output



#client = ModbusTcpClient('127.0.0.1')
client = ModbusTcpClient('192.168.1.21')

while 1==1:
    sleep(5)
    registersPerPage = 256
    pagenumber = 3
    startOffset = 0
    endOffset = 6 + 1
    for register in range(registersPerPage * pagenumber + startOffset,registersPerPage * pagenumber + endOffset):
        registers = sync_client_read(register)
        print("register" + str(register))
        print("msg sent: register value " +  str(registers))

