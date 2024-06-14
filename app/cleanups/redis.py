from aiohttp import web
from loguru import logger

async def close_redis(app: web.Application) -> None:
    await app['redis'].close()
    await app['redis'].connection_pool.disconnect()
    logger.info("Redis connection closed")
