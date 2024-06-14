from uuid import UUID
from typing import Union, Optional
from loguru import logger
from app.crud import TransactionCrud, UserCrud
from app.schemas.transaction import TransactionCreate
from app.models import Transaction
from app.services.messaging_service import MessagingService
from aiohttp import web

class TransactionService:
    
    @staticmethod
    async def create_transaction(app: web.Application, transaction_create: TransactionCreate) -> Union[Transaction, None]:
        # Process transaction creation message
        await MessagingService.process_message(app, transaction_create.dict())

        async with app['db'].transaction() as tx:
            try:
                async def transaction_logic(tx):
                    # Update user balance
                    await UserCrud().update_user_balance(
                        tx=tx,
                        amount=transaction_create.amount,
                        user_id=transaction_create.user_id,
                        transaction_type=transaction_create.type,
                    )
                    # Create transaction
                    transaction = await TransactionCrud().create_transaction(
                        tx=tx,
                        user_id=transaction_create.user_id,
                        transaction_type=transaction_create.type,
                        amount=transaction_create.amount,
                        timestamp=transaction_create.timestamp,
                        uid=transaction_create.uid
                    )
                    return transaction

                # Execute transaction logic within atomic transaction
                transaction = await transaction_logic(tx)
                return transaction

            except Exception as e:
                logger.error(f"Error creating transaction: {e}")
                return None

    @staticmethod
    async def get_transaction(transaction_uid: UUID) -> Optional[Transaction]:
        return await TransactionCrud().get_transaction(transaction_uid)
