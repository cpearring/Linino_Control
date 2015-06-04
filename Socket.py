import socket
import select

class Socket:
    def connect(self, host, port):
        self.UDP_IP = host
        self.UDP_PORT = port  
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", port))
        self.sock.setblocking(0)

    def send(self, msg):
        self.sock.sendto(msg, (self.UDP_IP, self.UDP_PORT))

    def receive(self):
        result = select.select([self.sock],[],[],0)
        if result[0] != []:
            return result[0][0].recv(64) 
        return None

    def close(self):
        self.sock.close()

