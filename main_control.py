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
        t_string = self.Value.get('RPM_STATUS')
        if t_string is not None:
            self.LeftRPM = int(t_string[0:t_string.find(":")])
            self.RightRPM = int(t_string[t_string.find(":")+1:])
            print t_string
            print self.LeftRPM
            print self.RightRPM
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
	if( b[0] == 2):
            #r = [str(unichr(b[1])),str(unichr(b[2]))]
            if b[1] < 0:
                sg_1 = -b[1] + 128
            else:
                sg_1 = b[1]
            if b[2] < 0:
                sg_2 = -b[2] + 128
            else:
                sg_2 = b[2]
            if sg_1 > 255:
                sg_1 = 255
            if sg_2 > 255:
                sg_2 = 255
            r = [chr(sg_1),chr(sg_2)]
            print "Right Set"
            print r
            json.send({'command':'put', 'key':'SET_R_RPM', 'value':r })
        elif( b[0] == 1):
            #r = [str(unichr(b[1])),str(unichr(b[2]))]
            if b[1] < 0:
                sg_1 = -b[1] + 128
            else:
                sg_1 = b[1]
            if b[2] < 0:
                sg_2 = -b[2] + 128
            else:
                sg_2 = b[2]
            if sg_1 > 255:
                sg_1 = 255
            if sg_2 > 255:
                sg_2 = 255
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
