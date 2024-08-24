import time

import serial
from fastapi import APIRouter

from settings import get_settings

from .websockets import manager

root = APIRouter()


@root.get("/")
def read_root():
    return {"Hello": "World"}


@root.post("/purchase/{sum}")
async def read_item(sum: int):
    ###            Имплементация схемы СЕРВЕР + RASPBERRY              ###
    ###    Для ее работы необходимо запускать client.py на Raspberry   ###
    # await manager.broadcast(str(sum))
    # return sum

    ###            Имплементация схемы НОТУБУК + ARDUINO               ###
    ###           Необходимо прописать команду на ноутбуке:            ###
    ###               fastapi dev .\backend\__main__.py                ###
    com_port = get_settings().COM

    arduino = serial.Serial(port=com_port, baudrate=115200, timeout=0.1)
    arduino.write(bytes(str(sum), "utf-8"))
    time.sleep(1)
    data = arduino.readlines()
    for line in data:
        print(line)

    return data
