#!/usr/bin/python  
# version 2.7
# Source Code form https://github.com/tecpal/PyModbus
# change Z-0ne
 
import os
import sys
import socket,thread
from array import array
from time import sleep, ctime
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',502))
s.listen(10)
F = open('c:\modbus.log','a',0)
sys.stdout = F
def TCP(conn,addr,F):
  buffer = array('B',[0]*300)
  while 1:
    try:
      conn.recv_into(buffer)
      ID = buffer[6]
      FC = buffer[7]
      mADR = buffer[8]
      lADR = buffer[9]
      ADR = mADR*256+lADR
      LEN = buffer[10]*256+buffer[11]
      BYT = LEN*2
      print "Received = ",buffer[0:13+buffer[12]]
      if (FC < 5 and FC > 0):   #Read Inputs or Registers
        DAT = array('B')
        if FC < 3: 
          BYT = (lambda x: x/8 if (x%8==0) else x/8+1)(LEN)     #Round off the no. of bytes
          v = 85          #send 85,86.. for bytes.
          for i in range(BYT): 
            DAT.append(v)
            v = (lambda x: x+1 if (x<255) else 85)(v)
        else:
          for i in range(LEN):  #Sends back the address as data
            DAT.append(mADR)
            DAT.append(lADR)
            if (lADR == 255):
              lADR = 0
              mADR = mADR + 1
            else: lADR = lADR + 1
        print "ID= %d,  Fun.Code= %d,  Address= %d,  Length= %d" %(ID, FC, ADR, LEN)
        conn.send(array('B', [0,0,0,0,0, BYT+3, ID, FC, BYT]) + DAT )
      elif (FC == 15 or FC == 16 or FC == 6 or FC == 43 or FC == 17):    #Write Registers
        BYT = buffer[12]
        conn.send(array('B', [0,0,0,0,0, 6, ID, FC, mADR, lADR, buffer[10], buffer[11] ] ) )
        buf = buffer[13:(13+BYT)]
        message = ': ADR:'+str(ADR)+' '
        if FC == 15:
          print "ID= %d,  Fun.Code= %d,  Address= %d,  Length= %d,  Bytes= %d" %(ID, FC, ADR, LEN, BYT)
          for j in range(BYT):  message = message+('Byte:'+str(j)+'='+str(buf[j])+', ')
        elif FC == 16:
          print "ID= %d,  Fun.Code= %d,  Address= %d,  Length= %d,  Bytes= %d" %(ID, FC, ADR, LEN, BYT)
          for j in range(BYT/2): message = message+('Reg:'+str(j)+'='+str((buf[j*2]<<8)+(buf[j*2+1]))+', ')
        elif FC == 6:
          print "ID= %d,  Fun.Code= %d,  Address= %d, Bytes= %d" %(ID, FC, ADR, LEN)
          message = message+('Reg:'+str(LEN))
        elif FC == 43:
          print "ID= %d,  Fun.Code= %d,  Address= %d, Bytes= %d" %(ID, FC, ADR, LEN)
          message = message+('Reg:'+str(LEN))
          conn.send(bytes(bytearray([0x00, 0x00, 
                                        0x00, 0x00, 
                                        0x00, 0x32, 
                                        0x00, 
                                        0x2b, #43 FC
                                        0x0e, 0x01, 0x81, 0x00, 0x00, 0x03, 
                                        0x00, 0x14, 0x53, 0x63, 0x68, 0x6e, #Schneider Electric
                                        0x65, 0x69, 0x64, 0x65, 0x72, 0x20, 
                                        0x45, 0x6c, 0x65, 0x63, 0x74, 0x72, 
                                        0x69, 0x63, 0x20, 0x20, 0x01, 0x0c, 
                                        0x42, 0x4d, 0x58, 0x20, 0x50, 0x33, #BMX P34 20 20
                                        0x34, 0x20, 0x32, 0x30, 0x32, 0x30, 
                                        0x02, 0x04, 0x76, 0x32, 0x2e, 0x32    #V2.2
                                        ])))
        elif FC == 17:
          print "ID= %d,  Fun.Code= %d,  Address= %d, Bytes= %d" %(ID, FC, ADR, LEN)
          message = message+('Reg:'+str(LEN))
          conn.send(array('B', [0,0,0,0,0,3,FC,171,1] ) )#Illegal function
        F.write(ctime() + message + "\n")
      else:
        conn.send(array('B', [0,0,0,0,0,3,FC,171,1])) #Illegal function
        print "Funtion Code %d Not Supported" %FC
        F.write(ctime() + message + "\n")
        exit()
      sleep(1)
    except Exception, e:
      print e, "\nConnection with Client terminated"
      F.write(ctime() + "\n")
      exit()
while 1:
  conn, addr = s.accept()
  print "Connected by", addr[0]
  thread.start_new_thread(TCP,(conn,addr,F))