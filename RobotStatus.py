import sys
from struct import *

sys.path.insert(0, '/usr/lib/python2.7/bridge/')
#from bridgeclient import BridgeClient
from tcp import TCPJSONClient

class RobotStatus:
    def __init__(self):
        self.left_rpm = 0
        self.right_rpm = 0
        self.brake = 0
        self.json = TCPJSONClient('127.0.0.1', 5700)
    
    def send(self, key, value):
        self.json.send({'command': 'put', 'key': key, 'value': value})
    
    def request(self, key):
        self.json.send({'command': 'get', 'key': key})
    
    def update_status(self, gui_socket):
        r = self.json.recv()
        if r is not None:
            if r['key'] == 'RPM_STATUS':
                rpm_status = r['value']
                rpm_status = rpm_status.split(':')
                self.left_rpm = int(rpm_status[0])
                self.right_rpm = int(rpm_status[1])
            # Send latest info to the GUI
            gui_socket.send(self.generate_packet())

    def generate_packet(self):
        return str(self.left_rpm)+':'+str(self.right_rpm)
        #return pack('<hhb', self.left_rpm, self.right_rpm, self.brake)
