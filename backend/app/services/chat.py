from fastapi import WebSocket, WebSocketDisconnect, Depends
from typing import Dict, List
from app.core.security import get_current_user

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: int):
        self.active_connections[user_id].remove(websocket)

manager = ConnectionManager()

async def handle_chat_connection(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle message
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id) 