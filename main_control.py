#!/usr/bin/python

import rclock
from RobotStatus import *
from Socket import *
from struct import *

gui_socket = Socket()
gui_socket.bind('0.0.0.0', 30001) #socket for computer?

robot = RobotStatus()
while True:
    gui_packet = gui_socket.receive()
    if gui_packet is not None:
        # Extract packet ID from packet
        id = gui_packet[0]

        print("Got packet:"+gui_packet)
        
        if id == 'Z':
            print("Got command packet:"+gui_packet)
            robot.parse_command(gui_packet[1:])
        else:
            robot.send(gui_packet+'|')
    
    robot.update_command()
    robot.update_telemetry(gui_socket)

gui_socket.close()

