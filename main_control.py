#!/usr/bin/python

import rclock
from RobotStatus import *
from Socket import *
from struct import *

gui_socket = Socket()
gui_socket.bind('0.0.0.0', 30001) #socket for computer?

start_time = rclock.clock()
last_500ms_time = start_time
last_1000ms_time = start_time
last_gps_time = start_time

robot = RobotStatus()
while True:
    gui_packet = gui_socket.receive()
    if gui_packet is not None:
        # Extract packet ID from packet
        id = gui_packet[0]

        print("Got packet:"+gui_packet)
        
        if id == 'Z':
            print("Got command packet:"+gui_packet)
            robot.parse_command(gui_packet)
        else:
            robot.send(gui_packet+'|')
    
    if rclock.clock() - last_500ms_time >= 0.5:
        robot.request('VOLT')
        robot.request('AMP')
        robot.request('L_MOTOR_TEMP')
        robot.request('R_MOTOR_TEMP')
        robot.request('IMU')
        robot.request('LWR_A_TEMP')
        robot.request('UPR_A_TEMP')
        last_500ms_time = rclock.clock()
    if rclock.clock() - last_1000ms_time >= 1.0:
        robot.request('W_WND_SPD')
        robot.request('W_TEMP')
        robot.request('W_PR_ALT')
        last_1000ms_time = rclock.clock()
    if rclock.clock() - last_gps_time >= 2.0:
        robot.request('GPS')
        last_gps_time = rclock.clock()
    
    robot.update_command()
    robot.update_status(gui_socket)
    
    #print "Elapsed time:"
    #print end - start_time

gui_socket.close()

