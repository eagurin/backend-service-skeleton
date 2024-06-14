from app.models import ProcessedMessage

class ProcessedMessageCrud:
    @staticmethod
    async def is_message_processed(message_id: str) -> bool:
        message = await ProcessedMessage.query.where(ProcessedMessage.message_id == message_id).gino.first()
        return message is not None

    @staticmethod
    async def add_processed_message(message_id: str):
        await ProcessedMessage.create(message_id=message_id)
