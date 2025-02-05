from fastapi import WebSocket, WebSocketDisconnect, Depends
from typing import Dict, List
import json
from . import models
from .auth import get_current_user
from .database import get_db

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: str, user_id: int):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)

manager = ConnectionManager()

async def handle_chat_connection(
    websocket: WebSocket,
    user_id: int,
    db = Depends(get_db)
):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Зберігаємо повідомлення в БД
            db_message = models.Message(
                content=message_data["content"],
                sender_id=user_id,
                receiver_id=message_data["receiver_id"]
            )
            db.add(db_message)
            db.commit()
            
            # Відправляємо повідомлення отримувачу
            await manager.send_personal_message(
                json.dumps({
                    "sender_id": user_id,
                    "content": message_data["content"]
                }),
                message_data["receiver_id"]
            )
    except WebSocketDisconnect:
        manager.disconnect(user_id) 