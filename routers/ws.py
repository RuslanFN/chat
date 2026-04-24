from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from db import get_session
from utils import decode_access_token
import uuid
router = APIRouter()
from typing import Set, Dict
import logging
logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[uuid.UUID:Set[WebSocket]] = {}

    async def connect(self, chat_id: uuid.UUID, websocket: WebSocket):
        self.active_connections[chat_id] = self.active_connections.get(chat_id, set()).union({websocket})
    async def disconnect(self, chat_id: uuid.UUID, websocket: WebSocket):
        self.active_connections[chat_id].remove(websocket)
        if not self.active_connections[chat_id]:
            del self.active_connections[chat_id]
    async def broadcast_by_chat(self, message: Dict, chat_id: uuid.UUID, sender: WebSocket):
        for recipient in self.active_connections[chat_id]:
            if not recipient == sender:
                try:
                    print('12345', recipient, message)
                    await recipient.send_json(message)
                except WebSocketDisconnect as e:
                    self.disconnect(chat_id, recipient)
                    

manager = ConnectionManager()
@router.websocket('/ws')
async def broadcast(websocket: WebSocket, chat_id: uuid.UUID = Query()):
    await websocket.accept()
    print(websocket)
    await manager.connect(chat_id, websocket)
    try:
        while True:
            msg = await websocket.receive_json()
            await manager.broadcast_by_chat(msg, chat_id, websocket)
    except WebSocketDisconnect:
        await manager.disconnect(chat_id, websocket)
    except Exception as e:
        logger.exception(f'Ошибка обработки сообщения {e}')
    

    
    
