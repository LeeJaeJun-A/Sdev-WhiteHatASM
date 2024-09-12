from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
import asyncio

router = APIRouter()

class ConnectionManager:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ConnectionManager, cls).__new__(cls)
            cls._instance.active_connections = {}
            cls._instance.lock = asyncio.Lock()
        return cls._instance

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
                try:
                    await websocket.send_text(message)
                except Exception as e:
                    print(f"Failed to send message to {user_id}: {e}")
            else:
                print(f"User {user_id} is not connected")



manager = ConnectionManager()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "cancel":
                await manager.disconnect(user_id)
                break
    except WebSocketDisconnect:
        print(f"User {user_id} has disconnected.")
        await manager.disconnect(user_id)
    except Exception as e:
        print(f"An error occurred for user {user_id}: {e}")
