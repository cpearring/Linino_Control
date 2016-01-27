import socket
import select

class Socket:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.sock.setblocking(False)
        self.clients = []

    def broadcast(self, msg):
        for client_address in self.clients:
            self.sock.sendto(msg, client_address)

    def listen(self):
        result = select.select([self.sock],[],[],0)
        if result[0] != []:
            received = result[0][0].recvfrom(64)
            message = received[0]
            address = received[1]
            if message == "connect me plz":
                print(str(address) + " has connected")
                if address not in self.clients:
                    self.clients.append(address)
            else:
                yield message

    def close(self):
        self.sock.close()

####################################################################################################

class TcpServer:

    def __init__(self, host, port):
        # List to keep track of socket descriptors
        self.connections = []
        self.port = port 

        # Create server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)

        # Add server socket to the list of readable connections
        self.connections.append(self.server_socket)

    def listen(self):
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(self.connections,[],[], 0)

        for sock in read_sockets:
            # New connection
            if sock == self.server_socket:
                sockfd, addr = self.server_socket.accept()
                self.connections.append(sockfd)
                print("Client "+str(addr)+" connected.")
            else: # Incoming data from client
                received = sock.recvfrom(64)
                message = received[0]
                address = received[1]
                if message == "connect me plz":
                    print(str(address) + " confirmed")
                else:
                    yield message
   
    def broadcast(self, message):
        # Iterate through every socket except server socket, which is the first one
        for sock in self.connections[1:]:
            try:
                sock.send(message)
            except:
                # Broken socket connection
                sock.close()
                self.connections.remove(sock)

class TcpClient:
    def __init__(self, host, port):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((host, port))
        self.conn.setblocking(False)

    def send(self, msg):
        self.conn.sendall(msg)

    def receive(self):
        try:
            return self.conn.recv(512)
        except:
            return None

    def close(self):
        self.conn.close()
