#!/usr/bin/env python3
import asyncio
import sys

# host = str(input("Input a server ip: "))
# port = str(input("Input a server port: "))
# key = "GET" + str(input("Input an 8 digit server key: "))
# try:
#     if len(key) != 11:
#         raise TypeError
# except TypeError:
#     print("Key must be 8 characters long.")
#     sys.exit(1)
host = "127.0.0.1"                                            
port = 12345
key = str(input("Input an 8 digit server key: "))
key = "GET" + key

async def client():
    reader, writer = await asyncio.open_connection(host, port)
    writer.write(key.encode('utf-8') + b'\n')
    data = await reader.readline()
    data = data.decode("utf-8")

    # take the key from the first 8 characters and format it into GET command
    nextKey = data[0:8]
    # take the message from the rest
    message = data[8:]
    
    print(f'Received: {message}')
    print(f"Next key is: {nextKey}")

    while len(data) > 1:
        nextKey = "GET" + nextKey
        reader, writer = await asyncio.open_connection(host, port)
        writer.write(nextKey.encode('utf-8') + b'\n')
        data = await reader.readline()
        data = data.decode("utf-8")

        if len(data) > 1:
            nextKey = data[0:8]
            message = data[8:]

            print(f'Received: {message}')
            print(f'Next key is: {nextKey}')

    # prompt for message to send back and format it into PUT command
    reader, writer = await asyncio.open_connection(host, port)
    sendMessage = "PUT" + nextKey[3:] + str(input(f"Please enter a message to send: "))
    writer.write(sendMessage.encode('utf-8') + b'\n')

    writer.close() # reader has no close() function
    await writer.wait_closed() # wait until writer completes close()

asyncio.run(client())