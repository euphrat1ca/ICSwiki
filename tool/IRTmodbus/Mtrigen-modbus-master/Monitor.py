import sys
import time
import ReadAndWriteRegisters as IO

RPMPageNumber = 4
RPMRegisterOffset = 6
DCCurrentPageNumber = 4
DCCurrentRegisterOffset = 201

print("Starting the RPM and current monitor")
time.sleep(2)
while 1==1:
	RPM = IO.read_register(RPMPageNumber, RPMRegisterOffset, 1)
	print("Engine RPM ", RPM, " RPM")
	DC = IO.read_register(DCCurrentPageNumber, DCCurrentRegisterOffset, 0.1)
	print("Alternator DC current ", DC, " A")
	time.sleep(2)

