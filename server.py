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

    # If message is PUT
    if (data.startswith(b'PUT')):
        data = data[3:] # Remove PUT from the string
        key = data[0:8] # Move first 8 characters into key
        value = data[8:] # Move rest of the data into value
        
        # If no value entered
        if (value == ""):
            sc.sendall(b"NO\n")
        # If key is not 8 bytes 
        elif not (re.match(b'^[a-zA-Z0-9]{8}$', key)):
            sc.sendall(b"NO\n")
        # If value is over 160 characters
        elif (len(value) > MAX_SIZE):
            sc.sendall(b"NO\n")
        # If all conditions are met
        else:
            savedData[key] = value
            sc.sendall(b"OK\n")
    # If message is GET
    elif (data.startswith(b'GET')):
        if not savedData: # If PUT was not run before and the list is empty
            sc.sendall(b"\n")
        else: 
            received = data[3:] # Remove GET from the string
            received = received.strip() # Purge spaces

            for key, value in savedData.items():
                if key == received:
                    sc.sendall(value)
                    
            sc.sendall(b"\n")
    else:
        sc.sendall(b"NO\n")
    

    sc.close() # Termination
