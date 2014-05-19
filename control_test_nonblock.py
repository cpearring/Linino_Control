#!/usr/bin/python
import select, socket 

port = 30000  # where do you expect to get a msg?
bufferSize = 128 # whatever you need

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('192.168.240.1', port))
s.setblocking(0)

while True:
    result = select.select([s],[],[])
    msg = result[0][0].recv(bufferSize) 
    print msg