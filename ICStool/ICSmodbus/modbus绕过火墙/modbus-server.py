from twisted.internet import protocol, reactor
import struct
import modbus
import fcntl
import os
import subprocess
import threading


TUNSETIFF = 0x400454ca
TUNSETOWNER = TUNSETIFF + 2
IFF_TUN = 0x0001
IFF_TAP = 0x0002
IFF_NO_PI = 0x1000


class ModbusTunneler(protocol.Protocol):


    # this method runs in a thread and handles data from the _tap device
    # it sends data to the tap device and receives data from the tap device
    def handle_tap(self):
        while True:
            self._tapLock.acquire()
            try:
                packet = list(os.read(self._tap.fileno(), 2048))
            except:
                packet = []
            if len(packet) > 0:
                self._mbBuffLock.acquire()
                print("got tap data, sending via modbus")
                for byte in packet:
                    self._mbDataToWrite += byte
                self._mbBuffLock.release()
            self._tapLock.release()
            self._tapBuffLock.acquire()
            if self._tapBuff!= "":
                print("handle_tap: putting data on wire: ", self._tapBuff)
                self._tapLock.acquire()
                # maybe I don't have to callFromThread here?  there shouldn't
                # be any contention over this device...
                os.write(self._tap.fileno(), self._tapBuff) #tapbuff is a string
                self._tapBuff = ""
                self._tapLock.release()
            self._tapBuffLock.release()
                
    def __init__(self, password):
        print("init")
        self._tapBuff = ""
        # tapbufflock is for the tap buffer (data to write to the tap interface)
        self._tapBuffLock = threading.Lock()
        # mbBuffLock is for the modbus buffer (data to write via Modbus)
        self._mbBuffLock = threading.Lock()
        # Trying to find an issue with a new packet coming in before the last packet
        # has finished processing...this may open a new thread?
        self._mbParseLock = threading.Lock()
        # Note that reading data from the tap and reading via modbus
        # do not require locks
        
        # not sure if we really need a taplock since it
        # should all run in one thread anyway
        self._tapLock = threading.Lock()
        self._decoder = modbus.ModbusDecoder()
        self._loggedIn = False
        self._password = password
        self._mbDataToWrite = ""
        self._databuff = ""
        print("opening tap")
        self._tap = open('/dev/net/tun', 'w+b')
        self._ifr = struct.pack('16sH', 'tap0', IFF_TAP | IFF_NO_PI)
        fcntl.ioctl(self._tap, TUNSETIFF, self._ifr)
        # need to make the tap device nonblocking
        tapfd = self._tap.fileno()
        tapfl = fcntl.fcntl(tapfd, fcntl.F_GETFL)
        fcntl.fcntl(tapfd, fcntl.F_SETFL, tapfl | os.O_NONBLOCK)


        # Optionally, we want it be accessed by the normal user.
        fcntl.ioctl(self._tap, TUNSETOWNER, 1000) 
#        subprocess.check_call('ifconfig tun0 192.168.7.1 pointopoint 192.168.7.2 up',
        subprocess.check_call('ifconfig tap0 192.168.7.1 netmask 255.255.255.0',
                              shell=True)
        self._mbDataToWrite = "ip 192.168.7.2 255.255.255.0"
        print("starting tap thread")
        self._tapThread = threading.Thread(target = self.handle_tap, args = [])
        self._tapThread.start()


    def verify_login(self, payload):
        print "Verifying login of ", payload
        print "--> Hex: ",
        for byte in payload:
            print hex(ord(byte))
        if ("login " + self._password) in payload:
            print "...verified!"
            self._mbDataToWrite = "login success"
            return True
        else:
            return False


    # is this thread-safe?? Can it be called from multiple threads??
    def dataReceived(self, data):
        self._mbParseLock.acquire()
        if self._decoder.decodeModbus(data):
            # modbus decoded at least one entire tap frame
            # so we should play with that frame
            #print "request complete"
            # Packet is now complete
            commandData = self._decoder.getReconstructedPacket()
            while commandData != None:
                # the packet will be the most recent one on the stack
                if self._loggedIn == False:
                    if self.verify_login(commandData):
                        self._loggedIn = True
                else:
                    self.dealWithData(commandData)
                commandData = self._decoder.getReconstructedPacket()
        else:
            self._databuff += data
            #print "waiting on more frames"
        # really need to queue up reply packets in a more meaningful way
        # right now we'll just send them all out willy-nilly, would
        # be nice to make them blend in more
        self._mbParseLock.release()
        if self._mbDataToWrite != "":
            print "sending encrapsulated modbus packet back"
                    # send as much of it as we can
            self.writeData()
            
    def dealWithData(self, commandData):
        #packets = self._decoder.decodeAllPackets(rawdata)
        # we may have been dealing with command data
        if commandData != "\x00\x00\x01": # just a probe
            print "got command?: ",
            for byte in commandData:
                print hex(ord(byte)),
            print ""
            tlen = commandData.find('\x00')
            if tlen == -1:
                tlen = len(commandData)
            tcmd = commandData[0:tlen]
            if "help" == tcmd:
                print "sending help"
                self._mbBuffLock.acquire()
                self._mbDataToWrite += "help: not available :)"
                self._mbBuffLock.release()
            else:
                print "bad command, may be data to send"
                #self._mbBuffLock.acquire()
                #self._mbDataToWrite += tcmd + ": invalid command"
                #self._mbBuffLock.release()
                # actual binary data, send to tap
                self._tapBuffLock.acquire()
                self._tapBuff += commandData
                self._tapBuffLock.release()
                print "data added to queue"
                # should also clear buffer, non?


                    
    # Write as many bytes as we can of the data, then move our _dataToWrite
    # Need to fix this up so it looks more like responses to the queries
    # that are coming in (put in proper register ranges, etc, will slow it down)
    def writeData(self):
        self._mbBuffLock.acquire()
        packets = modbus.encodeModbus(tid = 0x0, fc = 0x3, db = self._mbDataToWrite)
        print "replying with", len(packets), "packets"
        for packet in packets:
            self.transport.write(packet)
        print "done sending", len(packets), "replies, zeroing out buffer"
        self._mbDataToWrite = ""
        self._mbBuffLock.release()


class ModbusTunnelerFactory(protocol.Factory):
    def __init__(self, password):
        self._password = password
    def buildProtocol(self, addr):
        print "Got new client"
        return ModbusTunneler(self._password)


reactor.listenTCP(502, ModbusTunnelerFactory("secret"))
reactor.run()