#!/usr/bin/python

import socket
import time
import select
import sys 
from struct import *

sys.path.insert(0, '/usr/lib/python2.7/bridge/') 
from bridgeclient import BridgeClient as bridgeclient
from tcp import TCPJSONClient
json = TCPJSONClient('127.0.0.1', 5700)

class mysocket:
    '''
      - coded for clarity, not efficiency
    '''

    def connect(self, host, port):
        self.UDP_IP = host
        self.UDP_PORT = port  
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", port))
        self.sock.setblocking(0)
    def mysend(self, msg):
        #self.sock.sendto(bytes(msg), (self.UDP_IP, self.UDP_PORT)) Probably th right line
        self.sock.sendto(msg, (self.UDP_IP, self.UDP_PORT))

    def myreceive(self):
        result = select.select([self.sock],[],[],0)
        if(result[0] != []):
            return result[0][0].recv(128) 
        return None
    def end(self):
        self.sock.close()

class RobotStatus:
    LeftRPM = 0
    RightRPM = 0
    BrakeStatus = 0
    def updateStatus(self):
        value = bridgeclient()
        try:
            #L = value.get('LEFT_RPM')
            x = json.loads({'command':'get', 'key':'LEFT_RPM' })
            for i in x:
                print i
            if L is not None:
                if ( len(L) == 0 ):
                    self.LeftRPM = 0
                elif ( len(L) == 1 ):
                    self.LeftRPM = (ord(L[0]))#+ ((ord(L[1])-1)<<8)
                else:
                    self.LeftRPM = (ord(L[0])) + ((ord(L[1]))<<8)
                print self.LeftRPM
        except:
            print None
        #self.RightRPM = ord(L[2])+ (ord(L[3])<<8)
    def generatePacket(self):
        '''s = []
        s.append(self.RightRPM%256)
        s.append(self.RightRPM/256)

        s.append(self.LeftRPM%256)
        s.append(self.LeftRPM/256)

        s.append(self.BrakeStatus)'''

        return pack('<hhb', self.RightRPM, self.LeftRPM, self.BrakeStatus)

        #return ''.join([bin(item) for item in s])

s_test = mysocket()
s_test.connect('192.168.240.155', 30001)
#s_test.mysend("Hello World")


#robot.LeftRPM = 123

while(1):
    robot = RobotStatus()
    i = s_test.myreceive()
    robot.updateStatus()
    s_test.mysend(robot.generatePacket())
    if( i != None):
        #command recived. Process it----------------------------
        b = unpack('<bbb', i)
        print b
        if( b[0] == 1):
            t = bridgeclient()
            r = [b[1],b[2]]
            #t.put('SET_L_RPM', r)
            json.send({'command':'put', 'key':'SET_L_RPM', 'value':r })
    #if CAN message recieved, update our model and then send out new info to control station   

s_test.end()