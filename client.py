import asyncio
import time

import serial
import websockets

from settings import get_settings

api_link = get_settings().API_LINK
com_port = get_settings().COM


async def connect_to_server():
    async with websockets.connect(f"ws://{api_link}/ws") as websocket:
        await websocket.send("test")
        response = await websocket.recv()
        if response == "test":
            print("Connected to server")

        arduino = serial.Serial(port=com_port, baudrate=115200, timeout=0.1)
        while True:
            response = await websocket.recv()
            arduino.write(bytes(response, "utf-8"))
            time.sleep(1)
            data = arduino.readlines()
            for line in data:
                print(line)


asyncio.get_event_loop().run_until_complete(connect_to_server())
