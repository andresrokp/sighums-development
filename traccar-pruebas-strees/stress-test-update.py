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
