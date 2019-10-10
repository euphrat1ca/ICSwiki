import sys
import time
from pymodbus3.client.sync import ModbusTcpClient as ModbusClient
import os

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


def main():            
	registersPerPage = 256
	RPMPageNumber = 4
	RPMRegisterOffset = 6
	DCCurrentPageNumber = 4
	DCCurrentStartOffset = 204
	DCCurrentEndOffset = 205
	STOP     =  35700;    # 10001011(H8B,D139) 01110100(H74,116)  # -29836 (35700)
	STOPC    =  29835;    # 01110100(H74,D116) 10001011(H8B,D139) #  29835
	AUTO     =  35701;    # 10001011(H8B,D139) 01110101(H75,D117) # -29835 (35701)
	AUTOC    =  29834;    # 01110100(H74,D116) 10001010(H8A,D138) #  29834
	MANUAL   =  35702;    # 10001011(H8B,D139) 01110110(H76,D118) # -29834 (35702)
	MANUALC  =  29833;    # 01110100(H74,D116) 10001001(H89,D137) #  29833
	AUTOM    =  35704;    # 10001011(H8B,D139) 01111000(H78,D120) # -29832 (35704)
	AUTOMC   =  29831;    # 01110100(H74,D116) 10000111(H87,D135) #  29831
	START    =  35705;    # 10001011(H8B,D139) 01111001(H79,D121) # -29831 (35705)
	STARTC   =  29830;    # 01110100(H74,D116) 10000110(H87,D134) #  29830
	RESETAL  =  35734;    # 10001011(H8B,D139) 10010110(H96,D150) # -35734 (35734)
	#RESETALC =  29801;    # 
	#RESETA2  =  35734;    # 10001011(H8B,D139) 10010110(H96,D150) #  (35734)
	#RESETA2C =  29828;
	#RESETAT  = -29801;    # 10001011(H8B,D139) 10010110(H96,D150) # -35734 (35734)
	#RESETATC =  29800;    
	MODE_STOP          = 0; #Stop mode
	MODE_AUTO          = 1; #Auto mode
	MODE_MANUAL        = 2; #Manual mode
	MODE_TEST          = 3; #Test on load mode
	MODE_AUTO_MRESTORE = 4; #Auto with manual restore mode/Prohibit Return
	MODE_USER_CONFIG   = 5; #User configuration mode
	MODE_TEST_OFF_LOAD = 6; #Test off load mode

	host = sys.argv[1]
	print(host)
	client = ModbusClient(str(host), port=502)
	client.connect()
	time.sleep(0.1)

	rm = client.write_registers(4104, [MANUAL,MANUALC])
	print("Change DSE to MANUAL mode, starting engine in 5 seconds...")

	x = 4
	while x>=1:
		time.sleep(1)
		print(str(x))
		x-=1

	rq = client.write_registers(4104, [START,STARTC])
	time.sleep(3)
	print("Starting engine, proceding to read RPM and DC current")
	time.sleep(1)

	x = 1
	while x==1:
		time.sleep(0.01)
		register = registersPerPage * RPMPageNumber + RPMRegisterOffset
		global RPMRegister
		RPMRegister  = sync_client_read(register)
		register = registersPerPage * DCCurrentPageNumber + DCCurrentEndOffset
		global DCRegister
		DCRegister = sync_client_read(register)
		DCRegister = float(DCRegister)
		x = 0
		os.system('sudo python3 readings.py')

	while 1==1:
		time.sleep(0.01)
		register = registersPerPage * RPMPageNumber + RPMRegisterOffset
		RPMRegister  = sync_client_read(register)
		register = registersPerPage * DCCurrentPageNumber + DCCurrentEndOffset
		DCregister  = sync_client_read(register)
		DCRegister  = float(DCRegister)

if __name__ == "__main__":
	main()
