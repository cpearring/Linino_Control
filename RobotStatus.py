import sys
from struct import *

sys.path.insert(0, '/usr/lib/python2.7/bridge/')
#from bridgeclient import BridgeClient
from tcp import TCPJSONClient

class RobotStatus:
    def __init__(self):
        self.json = TCPJSONClient('127.0.0.1', 5700)
    
    def send(self, key, value):
        self.json.send({'command': 'put', 'key': key, 'value': value})
    
    def request(self, key):
        self.json.send({'command': 'get', 'key': key})
    
    def update_status(self, gui_socket):
        r = self.json.recv()
        if r is not None and r['value'] is not None:
            print("got message:"+str(r))
            packet = r['key']+':'+r['value']
            gui_socket.send(packet)
