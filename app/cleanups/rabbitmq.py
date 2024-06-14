from aiohttp import web
from loguru import logger

async def close_rabbitmq(app: web.Application):
    logger.info("Closing RabbitMQ connection")
    await app['rabbitmq'].close()
    logger.info("RabbitMQ connection closed")
