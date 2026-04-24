from fastapi import FastAPI
from routers import auth_router, register_router, message_router, ws_wouter, chat_router
import uvicorn
import logging
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")

app = FastAPI(
    swagger_ui_parameters={
        "requestInterceptor": "(req) => { req.credentials = 'include'; return req; }"
    }
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.0.0.1:5173',
                   'http://localhost:5173',
                   'http://192.16.10.68:5173'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])
app.include_router(auth_router)
app.include_router(register_router)
app.include_router(message_router)
app.include_router(ws_wouter)
app.include_router(chat_router)
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)