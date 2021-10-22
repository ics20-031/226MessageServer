#!/usr/bin/env python3 
import asyncio 
async def echo(reader, writer): 
    data = await reader.readline() 
    message = data.decode('utf-8') 
    addr = writer.get_extra_info('peername') 
    print(f"Received {message} from {addr}") 
    writer.write(data) # starts to write the data to the stream 
    await writer.drain() # waits until the data is written 
    writer.close() 
    await writer.wait_closed() 
async def main(): 
    server = await asyncio.start_server(echo, '127.0.0.1', 12345) 
    await server.serve_forever() # without this, program terminates 
asyncio.run(main())