#!/usr/bin/python

import time
from RobotStatus import *
from Socket import *
from struct import *

json = TCPJSONClient('127.0.0.1', 5700)

gui_socket = Socket()
gui_socket.connect('10.10.153.120', 30001) #socket for computer?

start_time = time.clock()
last_request_time = start_time

robot = RobotStatus()
while True:
    gui_packet = gui_socket.receive()
    if gui_packet is not None:
        print("GUI:"+gui_packet)
        json.send({'command': 'put', 'key': 'SET_RPM', 'value': gui_packet})
    
    if time.clock() - last_request_time >= 0.1:
        robot.request('RPM_STATUS')
        last_request_time = time.clock()
    
    robot.update_status(gui_socket)
    #end = time.clock()
    #print "Elapsed time:"
    #print end - start_time

gui_socket.close()

