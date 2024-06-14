import aio_pika
from aiohttp import web
from loguru import logger
from app.crud import ProcessedMessageCrud

class MessagingService:
    @staticmethod
    async def process_message(app: web.Application, message: dict):
        message_id = message.get("uid")

        if await ProcessedMessageCrud.is_message_processed(message_id):
            logger.info(f"Message with ID: {message_id} has already been processed.")
            return

        # Simulate message processing
        # Add actual processing logic here
        logger.info(f"Processing message with ID: {message_id}")
        
        # Mark the message as processed
        await ProcessedMessageCrud.add_processed_message(message_id)

    @staticmethod
    async def publish_message(app: web.Application, message: dict):
        try:
            channel = app['rabbitmq_channel']
            queue_name = app['config'].RABBITMQ_QUEUE
            message_body = aio_pika.Message(body=str(message).encode())
            await channel.default_exchange.publish(message_body, routing_key=queue_name)
            logger.info(f"Message published to queue {queue_name}: {message}")
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            raise
