#!/usr/bin/env python3

import asyncio
import random

host = '192.81.216.237'
port = 5027

messageLogin = bytes.fromhex('000F313233343536373839303132333435')
messageLocation = bytes.fromhex('000000000000002b080100000140d4e3ec6e000cc661d01674a5e0fffc00000900000004020100f0000242322318000000000100007a04')

devices = 100000
period = 0.0001


class AsyncClient(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop
        self.buffer = memoryview(messageLogin)

    def connection_made(self, transport):
        self.send_message(transport)

    def send_message(self, transport):
        transport.write(self.buffer.tobytes())
        self.buffer = memoryview(messageLocation)
        delay = period * (0.9 + 0.2 * random.random())
        self.loop.call_later(delay, self.send_message, transport)

    def data_received(self, data):
        pass

    def connection_lost(self, exc):
        self.loop.stop()


async def main():
    loop = asyncio.get_running_loop()

    for _ in range(devices):
        await loop.create_connection(lambda: AsyncClient(loop), host, port)

    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())



# Explanation

# First, we define the AsyncClient class, which is a subclass of asyncio.Protocol. This class will handle the communication with the server.

# In the AsyncClient class, the __init__ method initializes the instance variables. The loop variable represents the asyncio event loop, and the buffer variable is a memoryview object that initially contains the login message (messageLogin).

# The connection_made method is called when a connection is successfully established with the server. In this method, we call the send_message method to send the initial login message.

# The send_message method is responsible for sending the messages to the server. It takes the transport object as an argument, which represents the connection. Initially, it writes the login message (buffer) to the transport using transport.write(). Then, it updates the buffer to contain the location message (messageLocation). It also schedules the next call to send_message after a random delay, calculated using the period variable and random.random().

# The data_received method is called when data is received from the server. In this code, it is left empty because we are not processing any received data.

# The connection_lost method is called when the connection is closed or lost. In this code, it stops the event loop (self.loop.stop()).

# Moving on to the main() function, it is marked as asynchronous with the async keyword. This function will be the entry point for our asyncio program.

# Inside the main() function, we retrieve the running event loop using asyncio.get_running_loop() and assign it to the loop variable.

# Next, we enter a loop to create connections with the server. We iterate devices number of times and call loop.create_connection() to asynchronously create connections using the AsyncClient class as the protocol. The lambda function lambda: AsyncClient(loop) is used to create a new instance of AsyncClient for each connection. This function returns a coroutine, so we use await to wait for the connections to be established.

# After creating all the connections, we enter an infinite loop using while True:. This loop ensures that our program continues running until interrupted.

# Inside the loop, we use await asyncio.sleep(1) to pause the execution for 1 second. This ensures a delay between subsequent messages.

# With each iteration of the infinite loop, the send_message method of each AsyncClient instance is automatically called due to the previously scheduled call_later tasks. The messages are sent to the server, and the process repeats indefinitely.

# The overall flow of the code is as follows:

# The main() function is called.
# Connections are asynchronously created with the server using the AsyncClient class as the protocol.
# An infinite loop is entered.
# Inside the loop, messages are sent to the server at regular intervals.
# The loop continues indefinitely until the program is interrupted.