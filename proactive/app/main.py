import os, logging, asyncio, socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import admin as admin_router, user as user_router
from app.sockets.events import register_events

logging.basicConfig(level=logging.INFO)

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    logger=False,
    engineio_logger=False,
)
fastapi_app = FastAPI(
    title="Collaborative Form Filling System (Python)",
    version="1.0.0",
)
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

fastapi_app.include_router(admin_router.router)
fastapi_app.include_router(user_router.router)

asgi_app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)

# register socket‑io event handlers
async def startup():
    await register_events(sio)

asyncio.run(startup())
