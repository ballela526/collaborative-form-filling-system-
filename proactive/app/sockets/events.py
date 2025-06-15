import logging, asyncio
from uuid import uuid4
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.config.db import get_db
from app.config.redis import get_redis

logger = logging.getLogger(__name__)

ROOM_PREFIX = "form_"

async def register_events(sio):
    db: AsyncIOMotorDatabase = await get_db()
    redis = await get_redis()
    responses = db.form_responses

    @sio.event
    async def connect(sid, environ):
        logger.info(f"🔌  Client {sid} connected")

    @sio.event
    async def join_form(sid, data):
        form_id = data["form_id"]
        room = ROOM_PREFIX + form_id
        sio.enter_room(sid, room)
        logger.info(f"{sid} joined {room}")

        doc = await responses.find_one({"form_id": form_id})
        await sio.emit("initial_data", doc.get("responses", {}), room=sid)

    @sio.event
    async def update_field(sid, data):
        """
        data = {form_id, field_id, value}
        """
        form_id, field_id, value = data["form_id"], data["field_id"], data["value"]
        lock_key = f"lock:{form_id}:{field_id}"
        room = ROOM_PREFIX + form_id

        # 1️⃣ minimal field lock → 5 s TTL
        got_lock = await redis.set(lock_key, sid, nx=True, ex=5)
        if not got_lock:
            return                        # someone else editing that field

        try:
            # 2️⃣ write to Mongo (single shared doc)
            await responses.update_one(
                {"form_id": form_id},
                {
                    "$set": {f"responses.{field_id}": value, "last_updated": datetime.utcnow()}
                },
                upsert=False,
            )
            # 3️⃣ broadcast to everyone in that form
            await sio.emit("field_updated", {"field_id": field_id, "value": value}, room=room)
        finally:
            # 4️⃣ release lock
            await redis.delete(lock_key)

    @sio.event
    async def disconnect(sid):
        logger.info(f"❌  Client {sid} disconnected")
