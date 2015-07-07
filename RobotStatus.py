import sys
from struct import *

sys.path.insert(0, '/usr/lib/python2.7/bridge/')
#from bridgeclient import BridgeClient
from tcp import TCPJSONClient

class RobotStatus:
    def __init__(self):
        self.left_rpm = "NONE"
        self.right_rpm = "NONE"
        self.brake = 0
        self.json = TCPJSONClient('127.0.0.1', 5700)
    
    def send(self, key, value):
        self.json.send({'command': 'put', 'key': key, 'value': value})
    
    def request(self, key):
        self.json.send({'command': 'get', 'key': key})
    
    def update_status(self, gui_socket):
        r = self.json.recv()
        if r is not None and r['value'] is not None:
            print("got message:"+str(r))
            packet = None
            if r['key'] == 'RPM_STATUS':
                rpm_status = r['value']
                rpm_status = rpm_status.split(':')
                self.left_rpm = rpm_status[0]
                self.right_rpm = rpm_status[1]
                packet = str(self.left_rpm)+':'+str(self.right_rpm)
            if r['key'] == 'GPS':
                gps_data = r['value']
                packet = gps_data
            elif r['key'] == '12V_VOLTAGE':
                packet = r['value']
            # Send latest info to the GUI
            if packet is not None:
                gui_socket.send(r['key']+':'+packet)
