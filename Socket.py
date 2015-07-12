import socket
import select

class Socket:
    def bind(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.sock.setblocking(0)
        self.clients = []

    def send(self, msg):
        for client_address in self.clients:
            self.sock.sendto(msg, client_address)

    def receive(self):
        result = select.select([self.sock],[],[],0)
        if result[0] != []:
            received = result[0][0].recvfrom(64)
            message = received[0]
            address = received[1]
            if message == "connect me plz":
                print(str(address) + " has connected")
                self.clients.append(address)
            else:
                return message
        return None

    def close(self):
        self.sock.close()

