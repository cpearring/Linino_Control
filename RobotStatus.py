from struct import *

class RobotStatus:
    def __init__(self, bridge):
        LeftRPM = 0
        RightRPM = 0
        BrakeStatus = 0
        self.bridge = bridge
    
    def updateStatus(self):
        t_string = self.bridge.get('RPM_STATUS')
        if t_string is not None:
            self.LeftRPM = int(t_string[0:t_string.find(":")])
            self.RightRPM = int(t_string[t_string.find(":")+1:])

            print self.LeftRPM
            print self.RightRPM

    def generatePacket(self):
        #print "Packing values..."
        return pack('<hhb', self.RightRPM, self.LeftRPM, self.BrakeStatus)
        #print "Finished packing"
        #return ''.join([bin(item) for item in s])
