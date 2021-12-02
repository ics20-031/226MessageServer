#!/usr/bin/python3 
import asyncio 
import random 
import sys 
import traceback 

BUF_SIZE = 160 
KEY_SIZE = 8 
GET_KEY = b'GET' 
PUT_KEY = b'PUT' 
EXCLAMATION = 33 
TILDE = 126 
NUM_ARGS = 4

# 
# PURPOSE: 
# Given a host, port, and key, contacts the host at the given port, 
# issues a 'GETkey\n' command, parses the reply, and returns the result 
# in the form (nextKey, message) 
# 
# PARAMETERS: 
# 'host' contains the host IP or name 
# 'port' contains the IP at which the host is listening 
# 'key' contains the KEY_SIZE-byte alphanumeric key to be used to retrieve a message 
# 
# RETURN/SIDE EFFECTS: 
# Assuming the host replies with an KEY_SIZE-byte key followed by a message, returns 
# the tuple (key, message) 
# 
# NOTES: 
# If the server has no message associated with the key, or an invalid result 
# is returned, this function returns (key, b''). 
# No exceptions are handled 
#

async def get_message(host, port, key): 
    reader, writer = await asyncio.open_connection(host, port) 
    writer.write(GET_KEY + key + b'\n') 
    data = await reader.read(BUF_SIZE) 
    writer.close() 
    await writer.wait_closed() 
    if data == b'\n': 
        return (key, b'') 
    if len(data) < 8: 
        return (key, b'') 
    nextKey = data[: KEY_SIZE] 
    message = data[KEY_SIZE:] 
    return (nextKey, message)

# 
# PURPOSE: 
# Given a host, port, and key, prompts the user for a message to be transmitted, 
# generates a new KEY_SIZE -byte key, contacts the host at the given port, and 
# issues a 'PUTkeynewKeymessage\n' command 
# 
# PARAMETERS: 
# 'host' contains the host IP or name 
# 'port' contains the IP at which the host is listening 
# 'key' contains the KEY_SIZE-byte alphanumeric key to be used to store a PUT message 
# 
# RETURN/SIDE EFFECTS: 
# N/A 
# 
# NOTES: 
# No exceptions are handled 
#

async def put_message(host, port, key): 
    while True:
        #print("put_message started")
        loop = asyncio.get_running_loop()
        nextMessage = await loop.run_in_executor(None, input, "> ")
        nextKey = '' 
        while len(nextKey) < KEY_SIZE: 
            nextKey = nextKey + chr(random.randint(EXCLAMATION, TILDE)) 
        reader, writer = await asyncio.open_connection(host, port) 
        writer.write(PUT_KEY + key + nextKey.encode('utf-8') + nextMessage.encode('utf-8') + b'\n') 
        await writer.drain() 
        writer.close() 
        await writer.wait_closed()
        (nextKey, message) = await(get_message(host, port, nextKey))
        #print(message)

#
# PURPOSE:
# Polls the server every 5 seconds to see if the newest key already exists
# in the server with an attached message.
#
# PARAMETERS:
# 'host' host IP or name
# 'port' IP at which the host is listening
# 'nextKey' the key entered

async def poll_server(host, port, nextKey):
    while True:
        #print("poll_server started")
        #print(b"poll_server's nextKey is " + nextKey)
        await asyncio.sleep(5)
        (nextKey, message) = await get_message(host, port, nextKey)
        if message != b'':
            print(message) 

# 
# PURPOSE: 
# Given a host, port, and key, retrieves the message associated with the key from the 
# host listening at the given port.  Should this message exist, extracts the next key 
# from this message, then uses that key to get the next message.  This process is 
# continued until no more messages are found.  At that point, the user is prompted for 
# a new message, which is then stored on the server with a new key 
# 
# PARAMETERS: 
# 'host' contains the host IP or name 
# 'port' contains the IP at which the host is listening 
# 'key' contains the KEY_SIZE-byte alphanumeric key to be used to retrieve the first message 
# 
# RETURN/SIDE EFFECTS: 
# N/A 
# 
# NOTES: 
# All exceptions are handled 
#

async def main(host, port, key):
    while True: 
        try:
            print("main started") 
            nextKey = key.encode('utf-8') 
            while True: 
                (nextKey, message) = await get_message(host, port, nextKey) 
                print(message) 
                if message == b'': 
                    await asyncio.gather(put_message(host, port, nextKey), poll_server(host, port, nextKey)) 
                    break 
        except Exception as e: 
            print(e) 

if len(sys.argv) != NUM_ARGS: 
    print(sys.argv[0], 'IP', 'Port', 'Key') 
    sys.exit(-1) 

host = sys.argv[1] 
port = sys.argv[2] 
key = sys.argv[3] 

asyncio.run(main(host, port, key))
