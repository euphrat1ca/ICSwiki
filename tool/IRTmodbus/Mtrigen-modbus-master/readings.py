import startDSE as DSE
import time

while 1==1:
	time.sleep(2)
	print("Engine speed ", DSE.RPMRegister, " RPM")
	print("DC load current ", DSE.DCRegister, " A")
