import datetime
import uuid
from typing import Union, Optional, List
from app.models import Transaction


class TransactionCrud:
    
    @staticmethod
    async def create_transaction(user_id: int, transaction_type: str, amount: float, timestamp: Optional[Union[str, datetime.datetime]] = None, uid: Optional[str] = None) -> Transaction:
        if isinstance(timestamp, str):
            timestamp = datetime.datetime.fromisoformat(timestamp)
        if uid is None:
            uid = uuid.uuid4()

        transaction = await Transaction.create(
            type=transaction_type,
            amount=amount,
            timestamp=timestamp,
            user_id=user_id,
            uid=uid
        )
        return transaction

    @staticmethod
    async def get_transaction(transaction_uid: uuid.UUID) -> Optional[Transaction]:
        return await Transaction.query.where(Transaction.uid == transaction_uid).gino.first()

    @staticmethod
    async def get_user_transactions(user_id: int, timestamp: Optional[datetime.datetime] = None) -> List[Transaction]:
        if not timestamp:
            timestamp = datetime.datetime.now()
        return await Transaction.query.where(Transaction.user_id == user_id, Transaction.timestamp < timestamp).gino.all()