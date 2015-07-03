#!/usr/bin/python

import time
from RobotStatus import *
from Socket import *
from struct import *

json = TCPJSONClient('127.0.0.1', 5700)

gui_socket = Socket()
gui_socket.bind('0.0.0.0', 30001) #socket for computer?

start_time = time.clock()
last_request_time = start_time

robot = RobotStatus()
while True:
    gui_packet = gui_socket.receive()
    if gui_packet is not None:
        # Extract packet ID from packet
        id = gui_packet[0]
        gui_packet = gui_packet[1:]
        
        if id == 'A':
            print("Got left rpm:"+gui_packet)
            json.send({'command': 'put', 'key': 'SET_L_RPM', 'value': gui_packet})
        elif id == 'B':
            print("Got right rpm:"+gui_packet)
            json.send({'command': 'put', 'key': 'SET_R_RPM', 'value': gui_packet})
        elif id == 'C':
            print("Got forward pan:"+gui_packet)
            json.send({'command': 'put', 'key': 'F_PAN', 'value': gui_packet})
        elif id == 'D':
            print("Got forward tilt:"+gui_packet)
            json.send({'command': 'put', 'key': 'F_TILT', 'value': gui_packet})
        elif id == 'E':
            print("Got blade move:"+gui_packet)
            json.send({'command': 'put', 'key': 'BLADE', 'value': gui_packet})
    
    if time.clock() - last_request_time >= 0.1:
        robot.request('RPM_STATUS')
        robot.request('12V_VOLTAGE')
        last_request_time = time.clock()
    
    robot.update_status(gui_socket)
    #end = time.clock()
    #print "Elapsed time:"
    #print end - start_time

gui_socket.close()

