import asyncio
import time
import websockets
from fastapi.security import OAuth2PasswordRequestForm
import requests
from api.models import base
from settings import get_settings

api_link = "127.0.0.1:8000"
com_port = get_settings().COM


async def connect_to_server():
    async with websockets.connect(f"ws://{api_link}/ws?token=3ae349508ec46e9ae8d7d31c90ea6546e714ba2b1e4b4637c844fecbd5b058c5") as websocket:
        await websocket.send("test")
        response = await websocket.recv()
        if response == "test":
            print("Connected to server")

        while True:
            response = await websocket.recv()
            print(response)

asyncio.get_event_loop().run_until_complete(connect_to_server())
