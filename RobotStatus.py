import rclock
import sys
import socket
import select
from struct import *

from Socket import TcpClient

class RobotStatus:
    def __init__(self):
        # Connection to YunServer
        self.yun_sock = TcpClient('127.0.0.1', 5555)

        self.last_tele_time = rclock.clock() # Last telemetry bundle packet to GUI
        self.tele_packet = None

        self.command = None
        self.tele_files = {}
    
    def send(self, packet):
        self.yun_sock.send(packet)
    
    def update_telemetry(self, gui_socket):
        packet = self.yun_sock.receive()
        if packet is not None:
            print("got telemetry packet:"+packet)
            if self.tele_packet is None:
                # Starting a new telemetry bundle packet
                self.tele_packet = packet
            else:
                # Adding onto our telemetry bundle packet
                self.tele_packet += '|'+packet

                # Send the packet if it got too big
                if len(self.tele_packet) > 400:
                    self.send_tele_packet(gui_socket)

            # Data logging stuff
            packets = packet.split('|')
            
            for packet in packets:
                packet_split = packet.split(':')
                if len(packet_split) < 2:
                    continue
                key = packet[0]
                value = ':'.join(packet[1:])
                # Create telemetry data file if it doesn't exist yet
                if key not in self.tele_files:
                    pass
                    #self.tele_files[key] = open('/mnt/sda1/mission_data/'+key, 'w')
                
                # Write telemetry data to files
                #print("Writing " + key + " data "+value)
                #self.tele_files[key].write(value+'\n')

        if rclock.clock() - self.last_tele_time > 0.5:
            self.send_tele_packet(gui_socket)

    def send_tele_packet(self, gui_socket):
        if self.tele_packet is not None:
            self.last_tele_time = rclock.clock()
            gui_socket.send(self.tele_packet)
            self.tele_packet = None

    def update_command(self):
        if self.command is not None:
            start_time = self.command[0]
            duration = self.command[1]
            if rclock.clock() - start_time > duration:
                # Command just finished
                print("finished command at "+str(rclock.clock()))
                self.send('A0')
                self.send('B0')
                self.command = None

    def parse_command(self, command):
        parts = command.split(':')

        if len(parts) < 2:
            print("Invalid command: "+command)
            return

        l_power = 0.0
        r_power = 0.0
        if parts[0] == 'FWD':
            l_power = 100.0
            r_power = 100.0
        elif parts[0] == 'REV':
            l_power = -100.0
            r_power = -100.0
        if parts[0] == 'LEFT':
            l_power = -100.0
            r_power = 100.0
        elif parts[0] == 'RIGHT':
            l_power = 100.0
            r_power = -100.0

        duration = float(parts[1])

        print("applying command at "+str(rclock.clock()))

        self.command = (rclock.clock(), duration)
        self.send('A'+str(l_power))
        self.send('B'+str(r_power))
