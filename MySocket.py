import socket
import select

class MySocket:
    def connect(self, host, port):
        self.UDP_IP = host
        self.UDP_PORT = port  
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("192.168.240.1", port))
        self.sock.setblocking(0)

    def mysend(self, msg):
        self.sock.sendto(msg, (self.UDP_IP, self.UDP_PORT))

    def myreceive(self):
        result = select.select([self.sock],[],[],0)
        if result[0] != []:
            return result[0][0].recv(64) 
        return None

    def end(self):
        self.sock.close()

