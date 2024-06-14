import asyncio
import redis.asyncio as redis
from loguru import logger

class CacheService:
    @staticmethod
    async def init_redis(app):
        logger.info("Initializing Redis connection")
        try:
            redis_host = app['config'].REDIS_HOST
            redis_port = app['config'].REDIS_PORT
            redis_db = app['config'].REDIS_DB

            if not isinstance(redis_port, int):
                redis_port = int(redis_port)

            app['redis'] = redis.Redis(
                host=redis_host,
                port=redis_port,
                db=redis_db,
            )
            # Проверка соединения
            await app['redis'].ping()
            logger.info(f"Redis connection established at {redis_host}:{redis_port}/{redis_db}")
        except Exception as e:
            logger.error(f"Failed to initialize Redis: {e}")
            raise

    @staticmethod
    async def close_redis(app):
        logger.info("Closing Redis connection")
        try:
            await app['redis'].close()
            logger.info("Redis connection closed")
        except Exception as e:
            logger.error(f"Failed to close Redis: {e}")

    @staticmethod
    async def get_value(app, key):
        redis = app['redis']
        try:
            value = await redis.get(key)
            if value:
                logger.info(f"Cache hit for key: {key}")
            return value
        except Exception as err:
            logger.error(f"Error getting key from Redis: {err}")
            return None

    @staticmethod
    async def set_value(app, key, value, expire=3600):
        redis = app['redis']
        try:
            await redis.set(key, value, ex=expire)
            logger.info(f"Set key: {key} in Redis with expire: {expire}")
        except Exception as err:
            logger.error(f"Error setting key in Redis: {err}")
