#!/usr/bin/env python3
import asyncio
import sys

async def client(message):
    reader, writer = await asyncio.open_connection('127.0.0.1', 12345)
    writer.write(message.encode('utf-8') + b'\n')
    data = await reader.readline() # more on this on the next slides
    print(f'Received: {data.decode("utf-8")}')
    writer.close() # reader has no close() function
    await writer.wait_closed() # wait until writer completes close()
    
if len(sys.argv) != 2:
        print(f'{sys.argv[0]} needs 1 argument to transmit')
        sys.exit(-1)

asyncio.run(client(sys.argv[1]))