from twisted.internet import reactor

from twisted.internet.protocol import Factory, Protocol, ClientFactory
#from twisted.internet.endpoints import TCP4ClientEndpoint
from sys import stdout
import modbus
import sys
import struct
import threading
from threading import Thread
import time
import os
import fcntl
import subprocess


TUNSETIFF = 0x400454ca
TUNSETOWNER = TUNSETIFF + 2
IFF_TUN = 0x0001
IFF_TAP = 0x0002
IFF_NO_PI = 0x1000


class modbusClient(Protocol):




    def connectionMade(self):
        self._tapBuff = ""
        self._mbDataToWrite = ""
        self._mbBuffLock = threading.Lock()
        self._tapBuffLock = threading.Lock()
        self._tapLock = threading.Lock()
        self._mbParseLock = threading.Lock()
        self._decoder = modbus.ModbusDecoder()
        print "sending login"
        self.sendMessage("login secret")
        #print "starting command thread"
        #self._commandThread = Thread(target = self.commandLoop, args = [])
        #self._commandThread.start()
        print "starting query thread"
        self._queryThread = Thread(target = self.pollLoop) # adjust accordingly
        self._queryThread.start()
        print "opening tap"
        self._tap = open('/dev/net/tun', 'w+b')
        self._ifr = struct.pack('16sH', 'tap1', IFF_TAP | IFF_NO_PI)
        fcntl.ioctl(self._tap, TUNSETIFF, self._ifr)
        # need to make the tap device nonblocking
        tapfd = self._tap.fileno()
        tapfl = fcntl.fcntl(tapfd, fcntl.F_GETFL)
        fcntl.fcntl(tapfd, fcntl.F_SETFL, tapfl | os.O_NONBLOCK)
        
        # Optionally, we want it be accessed by the normal user.
        fcntl.ioctl(self._tap, TUNSETOWNER, 1000) 
#        subprocess.check_call('ifconfig tun0 192.168.7.1 pointopoint 192.168.7.2 up',
        subprocess.check_call('ifconfig tap1 192.168.7.2 netmask 255.255.255.0',
                              shell=True)
        print "starting tap thread"
        self._tapThread = Thread(target = self.handle_tap, args = [])
        self._tapThread.start()
        


    def commandLoop(self):
        while True:
            try:
                mycommand = raw_input("cl> ")
                reactor.callFromThread(self.sendMessage, mycommand)
            except:
                print "Exiting command loop"
                exit(1)


    def handle_tap(self):
        while True:
            self._tapLock.acquire()
            try: # because it's nonblock, this will throw exception when no data is available
                packet = list(os.read(self._tap.fileno(), 2048))
            except:
                # todo: only catch the exceptions we want!
                packet = []
            if len(packet) > 0:
                self._mbBuffLock.acquire()
                for byte in packet:
                    self._mbDataToWrite += byte
                self._mbBuffLock.release()
            self._tapLock.release()
            if self._tapBuff != "":
                print "tap out: ", self._tapBuff
                self._tapBuffLock.acquire()
                self._tapLock.acquire()
                os.write(self._tap.fileno(), self._tapBuff)
                self._tapBuff = ""
                self._tapLock.release()
                self._tapBuffLock.release()
                
    def tapLoop(self):
        # keep reading from the tap device
        packet = list(os.read(self._tap.fileno(), 2048))
        # put any packet data onto our _dataToWrite queue
        # need to keep a semaphore so that the poll loop is assured
        # to delete data from the dataToWrite
        this._tapBuffLock.acquire()
        this._mbDataToWrite.append(packet)
        this._tapBuffLock.release()


        
    def pollLoop(self, delay=0.1):
        print "poll loop starting up"
        while True:
            if self._mbDataToWrite != "":
                # send the data
                # Couldn't I just use the 
                print "had modbus data to write, calling from main thread"
                self._mbBuffLock.acquire()
                reactor.callFromThread(self.sendMessage, self._mbDataToWrite)
                self._mbDataToWrite = ""
                self._mbBuffLock.release()
            else:
                # send a probe
            #print "sending poll"
                reactor.callFromThread(self.sendProbe)
            time.sleep(delay)


    def sendProbe(self):
        # generate a Modbus frame that means "probe!"
        packets = modbus.encodeModbus(tid = 0x00, fc = 0x3, db = "", probe = True)
        for packet in packets:
            self.transport.write(packet)


    def dataReceived(self, data):
        self._mbParseLock.acquire()
        if self._decoder.decodeModbus(data):
            #print "request complete"
            # Packet is now complete
            commandData = self._decoder.getReconstructedPacket()
            while commandData != None:
                self.dealWithData(commandData)#, data)
                commandData = self._decoder.getReconstructedPacket()
        else:
            # our _decoder's state will be updated with partial packet
            self._mbParseLock.release()
            return
            #self._mbDatabuff += data
            #print "waiting on more frames"
        self._mbParseLock.release()
        
    def dealWithData(self, commandData):#, rawdata):
        #packets = self._decoder.decodeAllPackets(rawdata)
        # we may have been dealing with command data
        if commandData != "\x00\x00\x01": # just a probe
            #print "got command?: ",
            #for byte in commandData:
            #    print hex(ord(byte)),
            #print ""
            tlen = commandData.find('\x00')
            if tlen == -1:
                tlen = len(commandData)
            tcmd = commandData[0:tlen]
            if "help" == tcmd:
                print "sending help"
                self._mbBuffLock.acquire()
                self._mbDataToWrite += "help: not available :)"
                self._buffLock.release()
            elif "login success" in tcmd:
                print "succeeded login, continuing"
            else:
                print "bad command, may be data to send"
                #self._mbBuffLock.acquire()
                #self._mbDataToWrite += tcmd + ": invalid command"
                #self._mbBuffLock.release()
                # actual binary data, send to tap
                self._tapBuffLock.acquire()
                self._tapBuff += commandData
                self._tapBuffLock.release()
                #print "data added to queue"
                # should also clear buffer, non?
        else:
            # actual binary data, send to tap
            self._tapBuffLock.acquire()
            self._tapBuff += commandData
            self._tapBuffLock.release()




    
    def sendMessage(self, msg):
        #print "encrapsulating ", msg
        packets = modbus.encodeModbus(tid = 0x00, fc = 0x3, db = msg)
  
        for packet in packets:
            #print "sending: " + packet
            self.transport.write(packet)


class modbusClientFactory(ClientFactory):
    protocol = modbusClient
    def sendMessage(self, data):
        self.protocol.sendMessage(data)
            
def notThreadSafe(x):
     """do something that isn't thread-safe"""
     # ...
     print "I am in a thread"


def threadSafeScheduler():
    """Run in thread-safe manner."""
    reactor.callFromThread(notThreadSafe, 3) # will run 'notThreadSafe(3)'
                                             # in the event loop


def commandLoop():
    while True:
        command = input("> ")
        reactor.callInThread(f.sendMessage, command)
        
# TODO make this connect to acttual hosts
f = modbusClientFactory()
reactor.connectTCP("66.228.57.244", 502, f)
#reactor.callInThread(commandLoop)
try:
    reactor.run()
except:
    print "exception caught, exiting"
    exit(1)