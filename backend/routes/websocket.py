from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
import asyncio

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}  # Key: user_id, Value: WebSocket
        self.lock = asyncio.Lock()

    async def connect(self, user_id: str, websocket: WebSocket):
        async with self.lock:
            await websocket.accept()
            self.active_connections[user_id] = websocket

    async def disconnect(self, user_id: str):
        async with self.lock:
            if user_id in self.active_connections:
                del self.active_connections[user_id]

    async def send_message(self, user_id: str, message: str):
        async with self.lock:
            if user_id in self.active_connections:
                websocket = self.active_connections[user_id]
                await websocket.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_message(user_id, f"{data}")
    except WebSocketDisconnect:
        await manager.disconnect(user_id)
