#python3
#!/usr/bin/python

# this source is part of my Hackster.io project:  https://www.hackster.io/mariocannistra/radio-astronomy-with-rtl-sdr-raspberrypi-and-amazon-aws-iot-45b617

# use this program to test the AWS IoT certificates received by the author
# to participate to the spectrogram sharing initiative on AWS cloud

# this program will publish test mqtt messages using the AWS IoT hub
# to test this program you have to run first its companion awsiotsub.py
# that will subscribe and show all the messages sent by this program

import paho.mqtt.client as paho
import os
import sys
import socket
import ssl
import time
from time import sleep
from random import uniform
from pymodbus3 import exceptions
from pymodbus3.client.sync import ModbusTcpClient
import paho.mqtt.client as mqtt
import json
from urllib.request import urlopen



def sync_client_read(registerNumber, registerCount):
     try:
          result = client.read_holding_registers(registerNumber,registerCount)
          return result.registers
#     except exceptions.ConnectionException:
     except:
          print("Connection Error Handled")
          output=registerCount * [0]
          return output


connflag = False

def on_connect(client, userdata, flags, rc):
    global connflag
    connflag = True
    print("Connection returned result: " + str(rc) )

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

#def on_log(client, userdata, level, buf):
#    print(msg.topic+" "+str(msg.payload))

mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
#mqttc.on_log = on_log

pathname = os.path.abspath(os.path.dirname(sys.argv[0]))
with open(pathname + '/thingInfo.json') as certificate_file:    
    certificateData = json.load(certificate_file)
thingName=str(certificateData['thingName'])

awshost = "data.iot.us-east-1.amazonaws.com"
awsport = 8883
clientId = thingName
thingName = thingName
caPath = pathname + "/aws-iot-rootCA.crt"
certPath = pathname + "/certificate.pem"
print(certPath)
keyPath = pathname + "/private-key.pem"

#client = ModbusTcpClient('127.0.0.1')

client = ModbusTcpClient('192.168.0.101')


mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
try:
    mqttc.connect(awshost, awsport, keepalive=60)

    mqttc.loop_start()
except:
    print("mqtt connection failed")

#while 1==1:
#timeout = time.time() + 55   # until < 1 minute from now
while True:
#    if time.time() > timeout:
#        break
    sleep(5)
    try:
        publicIP = bytes.decode(urlopen('http://ip.42.pl/raw').read())
    except:
        publicIP = "no public internet"
    print(publicIP)
        
    with open(pathname + '/modbusPageRegisterRangeArray.json') as modbusPageRegisterRangeArray_file:    
        modbusPageRegisterRangeArray = json.load(modbusPageRegisterRangeArray_file)
#        print()
    print(str(modbusPageRegisterRangeArray))
    registersPerPage = 256
    jsonModbusShadow=json.loads('{"state": {"reported":{"registers":{}, "publicIP":{}}}}')
    jsonModbusShadow["state"]["reported"]["publicIP"]=publicIP
    registerArray= []
    for modbusPageRegisterRange in modbusPageRegisterRangeArray:
        #Convert requested page-offset addresses to register addresses
        modbusFirstRegister=(modbusPageRegisterRange[0] * registersPerPage-1) + modbusPageRegisterRange[1]
        modbusRegisterCount=modbusPageRegisterRange[2]
        registers = sync_client_read(modbusFirstRegister, modbusRegisterCount)
        #Attach obtained Registers to copy of page-offset request
        modbusPageRegisterRangeRegisters = modbusPageRegisterRange
        modbusPageRegisterRangeRegisters.append(registers)
        registerArray.append(modbusPageRegisterRangeRegisters)
        sleep(0.5)
    jsonModbusShadow["state"]["reported"]["registers"]=registerArray
    print("Published: " + json.dumps(jsonModbusShadow))
    if connflag == True:
        mqttc.publish("$aws/things/"+thingName+"/shadow/update", json.dumps(jsonModbusShadow),qos=1)
        print("$aws/things/"+thingName+"/shadow/update")

    else:
        print("waiting for connection...")
