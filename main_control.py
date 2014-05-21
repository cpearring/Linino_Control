#!/usr/bin/python

import socket
import time
import select
import sys 
from struct import *

sys.path.insert(0, '/usr/lib/python2.7/bridge/') 
from bridgeclient import BridgeClient as bridgeclient
from tcp import TCPJSONClient
json = TCPJSONClient('', 5700)

class mysocket:
    '''
      - coded for clarity, not efficiency
    '''

    def connect(self, host, port):
        self.UDP_IP = host
        self.UDP_PORT = port  
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("192.168.240.1", port))
        self.sock.setblocking(0)
    def mysend(self, msg):
        #self.sock.sendto(bytes(msg), (self.UDP_IP, self.UDP_PORT)) Probably th right line
        self.sock.sendto(msg, (self.UDP_IP, self.UDP_PORT))

    def myreceive(self):
        result = select.select([self.sock],[],[],0)
        if(result[0] != []):
            return result[0][0].recv(4) 
        return None
    def end(self):
        self.sock.close()

class RobotStatus:
    LeftRPM = 0
    RightRPM = 0
    BrakeStatus = 0
    Value = 0
    def updateStatus(self):
        L = self.Value.get('RPM_STATUS')
        if L is not None:
            self.LeftRPM = (ord(L[0])-1) + ((ord(L[1])-1)<<8)
            self.RightRPM = (ord(L[2])-1) + ((ord(L[3])-1)<<8)
            if self.LeftRPM >= 32511:
                self.LeftRPM = -(self.LeftRPM%32511)
            if self.RightRPM >= 32511:
                self.RightRPM = -(self.RightRPM%32511)
            print self.LeftRPM
            print self.RightRPM
	'''
        #print "Entering updateStatus()"
        L = self.Value.get('LEFT_RPM')
        #print "Got value from Value.get()"
	#Left side--------------------------------------------------------
        if L is not None:
            if ( len(L) == 0 ):
                self.LeftRPM = 0
            elif ( len(L) == 1 ):
                self.LeftRPM = (ord(L[0]))#+ ((ord(L[1])-1)<<8)
            else:
                self.LeftRPM = (ord(L[0])) + ((ord(L[1]))<<8)
            print self.LeftRPM
        #Right Side-------------------------------------------------------
        L = self.Value.get('RIGHT_RPM')
        if L is not None:
            if ( len(L) == 0 ):
                self.LeftRPM = 0
            elif ( len(L) == 1 ):
                self.LeftRPM = (ord(L[0]))
            else:
                self.LeftRPM = (ord(L[0])) + ((ord(L[1]))<<8)
            print self.LeftRPM 
        #self.RightRPM = ord(L[2])+ (ord(L[3])<<8)
        #print "Exiting updateStatus()"'''
    def generatePacket(self):
        '''s = []
        s.append(self.RightRPM%256)
        s.append(self.RightRPM/256)

        s.append(self.LeftRPM%256)
        s.append(self.LeftRPM/256)

        s.append(self.BrakeStatus)'''
        #print "Packing values..."
        return pack('<hhb', self.RightRPM, self.LeftRPM, self.BrakeStatus)
        #print "Finished packing"
        #return ''.join([bin(item) for item in s])

s_test = mysocket()
s_test.connect('192.168.240.155', 30001)
#s_test.mysend("Hello World")


#robot.LeftRPM = 123
robot = RobotStatus()
robot.Value = bridgeclient()
while(1):
    start = time.time() 
    
    s_test.mysend(robot.generatePacket())
    i = s_test.myreceive()
    if( i != None):
        #command recived. Process it----------------------------
        b = unpack('<bbb', i)
        if( b[0] == 1):
            #r = [str(unichr(b[1])),str(unichr(b[2]))]
            if b[1] < 0:
                sg_1 = -b[1] + 128
            else:
                sg_1 = b[1]
            if b[2] < 0:
                sg_2 = -b[2] + 128
            else:
                sg_2 = b[2]
            print sg_1
            print sg_2
            r = [chr(sg_1),chr(sg_2)]
            print r
            json.send({'command':'put', 'key':'SET_L_RPM', 'value':r })
    #print "Hanging in json.send?"
    #if CAN message recieved, update our model and then send out new info to control station   
    robot.updateStatus()
    end = time.time()
    print "Elapsed time:"
    print end - start

s_test.end()
