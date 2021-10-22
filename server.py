#!/usr/bin/python3

import socket
import re
import threading
import asyncio

BUF_SIZE = 1024
MAX_SIZE = 160
HOST = ''
PORT = 12345

savedData = {} # Creating a to store PUTs in 

while True:

    async def calledByThread(reader, writer):
        data = await reader.readline(BUF_SIZE) 
        data = data.strip()

        # If message is PUT
        if (data.startswith(b'PUT')):
            data = data[3:] # Remove PUT from the string
            key = data[0:8] # Move first 8 characters into key
            value = data[8:] # Move rest of the data into value
            
            # If no value entered
            if (value == ""):
                writer.write(b"NO\n")
                await writer.drain()
            # If key is not 8 bytes 
            elif not (re.match(b'^[a-zA-Z0-9]{8}$', key)):
                writer.write(b"NO\n")
                await writer.drain()
            # If value is over 160 characters
            elif (len(value) > MAX_SIZE):
                writer.write(b"NO\n")
                await writer.drain()
            # If all conditions are met
            else:
                savedData[key] = value
                writer.write(b"OK\n")
                await writer.drain()
        # If message is GET
        elif (data.startswith(b'GET')):
            if not savedData: # If PUT was not run before and the list is empty
                writer.write(b"\n")
                await writer.drain()
            else: 
                received = data[3:] # Remove GET from the string
                received = received.strip() # Purge spaces

                for key, value in savedData.items():
                    if key == received:
                        writer.write(value)
                        await writer.drain()
                        
                writer.write(b"\n")
                await writer.drain()
        else:
            writer.write(b"NO\n")
            await writer.drain()

        writer.close()
        await writer.wait_closed()
        
    async def main():
        server = await asyncio.start_server(calledByThread, HOST, PORT)
        await server.serve_forever()

    # i = 0
    # while True:
    #     sc, sockname = sock.accept() # Wait until a connection is established
    #     threading.Thread(target = calledByThread, args = (i, sc)).start()
    #     i = i + 1