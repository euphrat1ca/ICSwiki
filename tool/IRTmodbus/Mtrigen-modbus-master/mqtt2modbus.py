#!/usr/bin/python

import paho.mqtt.client as paho
import os
import sys
import socket
import ssl
from pymodbus3 import exceptions
from pymodbus3.client.sync import ModbusTcpClient
import json
#import csv
#from time import sleep

def sync_client_write(registerNumber, value):
     try:
          result = client.write_registers(registerNumber, value)
#     except exceptions.ConnectionException:
     except:
          print("Connection Error Handled")
          output=False
          return output


def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc) )
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$aws/things/"+thingName+"/shadow/update" , 1 )

def on_message(client, userdata, msg):
    jsonModbusShadow = json.loads(str(bytes.decode(msg.payload)))
    if "desired" in jsonModbusShadow["state"]:
       listRegisters = jsonModbusShadow["state"]["desired"]["registers"]
       print(str(listRegisters))
       try:
         sync_client_write(int(register['register']), listRegisters.value)
       except:
          print("Register Error Handled")


#def on_log(client, userdata, level, msg):
#    print(msg.topic+" "+str(msg.payload))

#client = ModbusTcpClient('127.0.0.1')
client = ModbusTcpClient('192.168.0.101')
pathname = os.path.abspath(os.path.dirname(sys.argv[0]))

with open(pathname + '/' + 'thingInfo.json') as data_file:    
    configData = json.load(data_file)
thingName=configData['thingName']
print(thingName)
mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
#mqttc.on_log = on_log

awshost = "data.iot.us-east-1.amazonaws.com"
awsport = 8883
clientId = thingName
thingName = thingName
caPath = pathname + "/aws-iot-rootCA.crt"
certPath = pathname + "/certificate.pem"
print(certPath)
keyPath = pathname + "/private-key.pem"

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.connect(awshost, awsport, keepalive=60)

mqttc.loop_forever()
