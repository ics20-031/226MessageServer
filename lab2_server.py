#!/usr/bin/python3

import socket
import threading
import asyncio 

KEY_SIZE = 8
MAX_MSG_SIZE = 160
BUF_SIZE = 1024

ERROR_RESPONSE = b"NO"
GET_CMD = "GET".encode('utf-8')
HOST = ''
NUM_CONNECTIONS = 1
OK_RESPONSE = b'OK'
PORT = 12345
PUT_CMD = "PUT".encode('utf-8')

messages = {}

#
# PURPOSE:
# Given a valid socket connection, reads in bytes from the connection until
# either a newline is encountered or BUF_SIZE charcters have been read,
# whichever occurs first
#
# PARAMETERS:
# 'current_socket' contains a valid server socket
#
# RETURN/SIDE EFFECTS:
# Returns the bytes that have been read in
#
# NOTES:
# No connection errors are handled
#
async def get_line(reader, writer):
        buffer = b''
        size = 0
        while True:
                data = await reader.read(1)
                size += 1
                if data == b'\n' or size >= BUF_SIZE:
                        return buffer
                buffer = buffer + data

#
# PURPOSE:
# Given a string, extracts the key and message from it
#
# PARAMETERS:
# 's' is the string that will be used for the key and message extraction
#
# RETURN/SIDE EFFECTS:
# Returns (key, message, flag), where flag is True if the extraction
# succeeded, False otherwise
#
# NOTES:
# To succeed, the string must be of format "KEYMSG" where KEY is of length KEY_SIZE
#
def get_key(s):
    if len(s) < KEY_SIZE:
        return ("", "", False)
    else:
        return (s[:KEY_SIZE], s[KEY_SIZE:], True)

#
# PURPOSE:
# Given a string, extracts the key and message, and stores the message in messages[key]
#
# PARAMETERS:
# 's' is the string that will be used for the key and message extraction
#
# RETURN/SIDE EFFECTS:
# Returns OK_RESPONSE on success, ERROR_RESPONSE otherwise
#
# NOTES:
# To succeed, the string must be of format "KEYMSG" where KEY is of length KEY_SIZE
# and MSG does not exceed MAX_MSG_SIZE
#
def process_put(s):
    (key, msg, ok) = get_key(s)
    if (not ok) or (len(msg) > MAX_MSG_SIZE):
        return ERROR_RESPONSE

    #print("Saving", msg, "with key", key)
    messages[key] = msg

    return OK_RESPONSE

#
# PURPOSE:
# Given a string, extracts the key and message from it, and returns message[key]
#
# PARAMETERS:
# 's' is the string that will be used for the key and message extraction
#
# RETURN/SIDE EFFECTS:
# Returns the message if the extraction succeeded, and b'' otherwise
#
# NOTES:
# To succeed, the string must be of format "KEY" where KEY is of length KEY_SIZE
#
def process_get(s):
    (key, msg, ok) = get_key(s)
    if not ok or len(msg) != 0 or not key in messages:
        return b''

    #print("Found", messages[key], "with key", key)
    return messages[key]

#
# PURPOSE:
# Given a string, parses the string and implements the contained PUT or GET command
#
# PARAMETERS:
# 's' is the string that will be used for parsing
#
# RETURN/SIDE EFFECTS:
# Returns the result of the command if the extraction succeeded, ERROR_RESPONSE otherwise
#
# NOTES:
# The string is assumed to be of format "CMDKEYMSG" where CMD is either PUT_CMD or GET_CMD,
# KEY is of length KEY_SIZE, and MSG varies depending on the command. See process_put(s)
# and process_get(s) for details regarding what the commands do and their return values
#
def process_line(s):
    if s.startswith(PUT_CMD):
        return process_put(s[(len(PUT_CMD)):])
    elif s.startswith(GET_CMD):
        return process_get(s[(len(GET_CMD)):])
    else:
        return ERROR_RESPONSE

# 
# PURPOSE:
# receives data via get_line function, processes using proccess_line , then replies
#
# PARAMETERS:
# id: current thread id
# sc: current socket
#
async def calledByThread(reader, writer):
    data = await get_line(reader, writer)
    response = process_line(data)
    writer.write(response + b'\n')
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def main(): 
    server = await asyncio.start_server(calledByThread, '127.0.0.1', 12345) 
    await server.serve_forever() # without this, program terminates

asyncio.run(main())