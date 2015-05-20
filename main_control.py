#!/usr/bin/python

import time
import sys
from RobotStatus import *
from MySocket import *
from struct import *

sys.path.insert(0, '/usr/lib/python2.7/bridge/')
from bridgeclient import BridgeClient
from tcp import TCPJSONClient
#import simplejson as json
json = TCPJSONClient('', 5700)


s_test = MySocket()
s_test.connect('192.168.240.155', 30001) #socket for computer?
#s_test.mysend("Hello World")


#robot.LeftRPM = 123
robot = RobotStatus(BridgeClient())
while True:
    start = time.time() 
    
    s_test.mysend(robot.generatePacket())
    raw_Packet = s_test.myreceive()
    if raw_Packet is not None:
            raw_Packet.strip('\x00')
            #print raw_Packet
            #print raw_Packet
            SetLeftRPM = int(raw_Packet[0:raw_Packet.find(":")])
            #print "Raw packet.find('\x00') " + str(raw_Packet.find("\x00"))
            SetRightRPM = int(raw_Packet[raw_Packet.find(":")+1:raw_Packet.find("\x00")])
            
            print SetRightRPM;
            print SetLeftRPM;
            #json.send({'command':'put', 'key':'SET_R_RPM', 'value':str(SetRightRPM) })
            json.send({'command':'put', 'key':'SET_RPM', 'value':str(SetLeftRPM)+':'+str(SetRightRPM) })
      
            #json.send({'command':'put', 'key':'SET_L_RPM', 'value':str(SetLeftRPM) })
            #print str(SetLeftRPM)+":"+str(SetRightRPM)
            #json.send({'command':'put', 'key':'RPM_STATUS', 'value':str(SetLeftRPM)+":"+str(SetRightRPM) })

            #here I need to put in the CAN data packet to be sent every second?
            #json.send({'data':'put', 'key':'LS_Battery_Voltage', 'value':str(LS_Battery_Voltage) })
            
    #print "Hanging in json.send?"
    #if CAN message recieved, update our model and then send out new info to control station   
    robot.updateStatus()
    end = time.time()
    print "Elapsed time:"
    print end - start

s_test.end()

