import time
import sys
from struct import *

sys.path.insert(0, '/usr/lib/python2.7/bridge/')
#from bridgeclient import BridgeClient
from tcp import TCPJSONClient

class RobotStatus:
    def __init__(self):
        self.json = TCPJSONClient('127.0.0.1', 5700)
        self.command = None
        self.tele_files = {}
    
    def send(self, key, value):
        self.json.send({'command': 'put', 'key': key, 'value': value})
    
    def request(self, key):
        self.json.send({'command': 'get', 'key': key})
    
    def update_status(self, gui_socket):
        r = self.json.recv()
        if r is not None and r['value'] is not None:
            print("got message:"+str(r))
            key = r['key']
            value = r['value']
            packet = key+':'+value
            gui_socket.send(packet)
            
            # Create telemetry data file if it doesn't exist yet
            if key not in self.tele_files:
                self.tele_files[key] = open('mission_data/'+key, 'w')
            
            # Write telemetry data to files
            self.tele_files[key].write(value+'\n')

    def update_command(self):
        if self.command is not None:
            start_time = self.command[0]
            duration = self.command[1]
            if time.clock() - start_time > duration:
                # Command just finished
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

        self.command = (time.clock(), duration)
        self.send('SET_L_RPM', str(l_power))
        self.send('SET_R_RPM', str(r_power))
