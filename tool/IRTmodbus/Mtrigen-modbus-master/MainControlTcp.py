#!/usr/bin/env python3
import sys
import time
from pymodbus3.client.sync import ModbusTcpClient as ModbusClient
import RPi.GPIO as GPIO

RPMPageNumber = 4
RPMRegisterOffset = 6
DCCurrentPageNumber = 4
DCCurrentRegisterOffset = 201
STOP = 35700 #This are control keys
STOPC = 29835 #This are complements of control keys, must be write together with the control key
AUTO = 35701
AUTOC = 29834
MANUAL = 35702
MANUALC = 29833
AUTOM = 35704
AUTOMC = 29831
START = 35705
STARTC = 29830
RESETAL = 35734

print("Waiting for the unit to start")
time.sleep(30)
host = sys.argv[1]
print("Connecting to DSE with IP ", host)
client = ModbusClient(host)
client.connect()
time.sleep(0.1)

def sync_client_read(registerNumber):
	try:
		result = client.read_holding_registers(registerNumber,1)
		return result.registers
	except:
		print("Connection Error Handled")
		output = False
		return output

def read_register(PageNumber, RegisterOffset, Scale):
	register = 256 * PageNumber + RegisterOffset
	read = sync_client_read(register)
	register = float(read[0]) * Scale
	return register

def write_register(SystemControlKeys, ComplimentControlKey):
	wr = client.write_registers(4104, [SystemControlKeys, ComplimentControlKey])
	return True

def main():
	try:
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(11,GPIO.OUT)
		print("Preparing control, 5 seconds to start")
		
		x = 4
		while x>=1:
			time.sleep(1)
			print(str(x))
			x-=1

		time.sleep(1)
		print("Control ON")
		time.sleep(3)
		print("Reading the actual load")
		time.sleep(2)
		print("Governor speed control ON")
		PWM = GPIO.PWM(11, 100)
		Current = read_register(DCCurrentPageNumber, DCCurrentRegisterOffset, 0.1)
		X = ((Current)/120) * 100
		if X>100:
			X=100
		PWM.start(X)
		while 1==1:
			AC = read_register(170,2,1)
			HEAT = read_register(170,0,1)
			if AC==1.0:
				X = 100
				PWM.ChangeDutyCycle(X)
			else:
				if HEAT==1.0:
					X== 100
					PWM.ChangeDutyCycle(X)
				else:
					Current = read_register(DCCurrentPageNumber, DCCurrentRegisterOffset, 0.1)
					X = ((Current)/120) * 100
					if X>100:
						X=100
					PWM.ChangeDutyCycle(X)

	except (KeyboardInterrupt, SystemExit):
		PWM.stop()
		GPIO.cleanup()
		print("Program stopped, cleaning up the GPIO ports")		

if __name__ == "__main__":
	main()	
	
