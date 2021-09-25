#!/usr/bin/python3

import socket
import re

BUF_SIZE = 1024
MAX_SIZE = 160
HOST = ''
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # More on this later
sock.bind((HOST, PORT)) # Claim messages sent to port "PORT"
sock.listen(1) # Enable server to receive 1 connection at a time
print('Server:', sock.getsockname()) # Source IP and port
savedData = {} # Creating a to store PUTs in 

while True:
    sc, sockname = sock.accept() # Wait until a connection is established
    print('Client:', sc.getpeername()) # Destination IP and port
    data = sc.recv(BUF_SIZE) # recvfrom not needed since address is kn
    data = data.strip()
    data = data[:MAX_SIZE]
    # If message is PUT
    if (data.startswith(b'PUT')):
        item = data.split(b" ", 2) # Splits the input into 3 parts as a list and stores it into savedData
        # Error checking if item is less than 3 parts
        if (len(item) != 3):
            print("NO, length not correct")
        # If key is not 8 bytes 
        elif not (re.match(b'^[a-zA-Z0-9]{8}$',item[1])):
            print("NO, alphanumeric key is not up to par")
        else:
            savedData[item[1]] = item[2]
            sc.sendall(b"OK\n")
    # If message is GET
    elif (data.startswith(b'GET')):
        if not savedData: # If PUT was not run before and the list is empty
            print("nothing saved")
        else: 
            received = data.split(b" ")
            
            for key, value in savedData.items():
                if key == received[1]:
                    sc.sendall(value)
                    
            sc.sendall(b"\n")
    

    sc.close() # Termination
