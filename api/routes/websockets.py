from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Cookie, Query, status, WebSocketException
from typing import Annotated
from .auth import oauth2_scheme
ws = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, token: str):
        await websocket.accept()
        self.active_connections[token] = websocket

    def disconnect(self, token: str):
        self.active_connections.pop(token, None)

    async def send_personal_message(self, message: str, token: str):
        try:
            await self.active_connections[token].send_text(message)
        except KeyError:
            print(f"User {token} is not connected")

    async def broadcast(self, message: str):
        for connection in list(self.active_connections.values()):
            await connection.send_text(message)


manager = ConnectionManager()

async def get_cookie_or_token(
    websocket: WebSocket,
    session: Annotated[str | None, Cookie()] = None,
    token: Annotated[str | None, Query()] = None,
):
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token

@ws.websocket("")
async def websocket_endpoint(websocket: WebSocket, cookie_or_token: Annotated[str, Depends(get_cookie_or_token)]):
    print(cookie_or_token)
    await manager.connect(websocket, "string")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(data, "string")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
