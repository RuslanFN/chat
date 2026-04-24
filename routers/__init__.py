from .auth import router as auth_router
from .register import router as register_router
from .message import router as message_router
from .ws import router as ws_wouter
from .chat import router as chat_router
__all__ = [
    'auth_router',
    'register_router',
    'message_router',
    'ws_wouter',
    'chat_router',
]