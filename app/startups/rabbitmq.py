from aio_pika import connect_robust
from loguru import logger

async def init_rabbitmq(app):
    try:
        rabbitmq_url = app["config"].RABBITMQ_URL
        connection = await connect_robust(rabbitmq_url)
        app['rabbitmq'] = connection
        logger.info("RabbitMQ connection established")
    except Exception as e:
        logger.error(f"Failed to connect to RabbitMQ: {e}")
        raise e
