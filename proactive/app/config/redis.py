import os, asyncio, logging, redis.asyncio as redis

logger = logging.getLogger(__name__)
_redis = None

async def get_redis():
    global _redis
    if _redis is None:
        _redis = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            decode_responses=True,
        )
        #await _redis.ping()
        logger.info("✅ Connected to Redis")
    return _redis
