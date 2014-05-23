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
        self.sock.sendto(msg, (self.UDP_IP, self.UDP_PORT))

    def myreceive(self):
        result = select.select([self.sock],[],[],0)
        if(result[0] != []):
            return result[0][0].recv(64) 
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

            print self.LeftRPM
            print self.RightRPM
    def generatePacket(self):
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
    raw_Packet = s_test.myreceive()
    if raw_Packet is not None:
            #print raw_Packet
            SetLeftRPM = int(raw_Packet[0:raw_Packet.find(":")])
            SetRightRPM = int(raw_Packet[raw_Packet.find(":")+1:raw_Packet.find("n")])
            print SetRightRPM;
            print SetLeftRPM;
            #json.send({'command':'put', 'key':'SET_R_RPM', 'value':SetRightRPM })
        
            json.send({'command':'put', 'key':'SET_L_RPM', 'value':SetLeftRPM })
    #print "Hanging in json.send?"
    #if CAN message recieved, update our model and then send out new info to control station   
    robot.updateStatus()
    end = time.time()
    print "Elapsed time:"
    print end - start

s_test.end()
