import rclock
import sys
from struct import *

sys.path.insert(0, '/usr/lib/python2.7/bridge/')
#from bridgeclient import BridgeClient
from tcp import TCPJSONClient

class RobotStatus:
    def __init__(self):
        self.json = TCPJSONClient('127.0.0.1', 5700)

        self.last_tele_time = rclock.clock() # Last telemetry bundle packet to GUI
        self.tele_packet = None

        self.command = None
        self.tele_files = {}
    
    def send(self, key, value):
        self.json.send({'command': 'put', 'key': key, 'value': value})
    
    def request(self, key):
        self.json.send({'command': 'get', 'key': key})
    
    def update_status(self, gui_socket):
        r = self.json.recv()
        if r is not None and r['value'] is not None:
            #print("got message:"+str(r))
            key = r['key']
            value = r['value']
            packet = key+':'+value

            if self.tele_packet is None:
                # Starting a new telemetry bundle packet
                self.tele_packet = packet
            else:
                # Adding onto our telemetry bundle packet
                self.tele_packet += '|'+packet

                # Send the packet if it got too big
                if len(self.tele_packet) > 400:
                    self.send_tele_packet(gui_socket)
            
            # Create telemetry data file if it doesn't exist yet
            if key not in self.tele_files:
                self.tele_files[key] = open('/mnt/sda1/mission_data/'+key, 'w')
            
            # Write telemetry data to files
            self.tele_files[key].write(value+'\n')

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
                self.send('SET_L_RPM', '0')
                self.send('SET_R_RPM', '0')
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
        self.send('SET_L_RPM', str(l_power))
        self.send('SET_R_RPM', str(r_power))
