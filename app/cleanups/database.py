from aiohttp import web
from loguru import logger

async def close_db(app: web.Application) -> None:
    logger.info("Closing database connection")
    await app["db"].pop_bind().close()
    logger.info("Database connection closed")
