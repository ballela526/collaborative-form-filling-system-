import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

_mongo_client: AsyncIOMotorClient = None
_db: AsyncIOMotorDatabase = None

async def get_db() -> AsyncIOMotorDatabase:
    global _mongo_client, _db
    if _db is None:
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        db_name = os.getenv("MONGO_DB_NAME", "proactive_db")
        _mongo_client = AsyncIOMotorClient(mongo_uri)
        _db = _mongo_client[db_name]  # ✅ Use named DB directly
    return _db
