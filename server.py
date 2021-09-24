#!/usr/bin/python3

import socket

BUF_SIZE = 1024
MAX_SIZE = 160
HOST = ''
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # More on this later
sock.bind((HOST, PORT)) # Claim messages sent to port "PORT"
sock.listen(1) # Enable server to receive 1 connection at a time
print('Server:', sock.getsockname()) # Source IP and port
while True:
    sc, sockname = sock.accept() # Wait until a connection is established
    print('Client:', sc.getpeername()) # Destination IP and port
    data = sc.recv(BUF_SIZE) # recvfrom not needed since address is known
    sc.sendall(b"received " + data) # Destination IP and port implicit due to accept call
    sc.close() # Termination
