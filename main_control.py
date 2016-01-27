#!/usr/bin/python

import rclock
from RobotStatus import *
from Socket import *
from struct import *

gui_socket = Socket('0.0.0.0', 30001)

robot = RobotStatus()
while True:
    for gui_packet in gui_socket.listen():
        if gui_packet is not None:
            if len(gui_packet) == 0:
                continue

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

