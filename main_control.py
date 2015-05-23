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
json = TCPJSONClient('127.0.0.1', 5700)


gui_socket = MySocket()
gui_socket.connect('192.168.240.189', 30001) #socket for computer?
#gui_socket.mysend("Hello World")


#robot.LeftRPM = 123
robot = RobotStatus(BridgeClient())
while True:
    start = time.time() 
    
    gui_socket.mysend(robot.generatePacket())
    raw_Packet = gui_socket.myreceive()
    if raw_Packet is not None:
            #raw_Packet.strip('\x00')
            #print raw_Packet
            #print raw_Packet
            split_colon = raw_Packet.split(':')
            SetLeftRPM = int(split_colon[0])
            #print "Raw packet.find('\x00') " + str(raw_Packet.find("\x00"))
            SetRightRPM = int(split_colon[1])
            
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
    #robot.updateStatus()
    end = time.time()
    print "Elapsed time:"
    print end - start

gui_socket.end()

