from aiohttp import web
from loguru import logger
import redis.asyncio as redis

async def init_redis(app: web.Application):
    redis_conn = redis.from_url(f"redis://{app['config'].REDIS_HOST}:{app['config'].REDIS_PORT}/0")
    app['redis'] = redis_conn
    logger.info(f"Redis connection established at {app['config'].REDIS_HOST}:{app['config'].REDIS_PORT}")