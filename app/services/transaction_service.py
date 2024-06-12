import uuid
from typing import List, Optional, Union

from app.models.transaction import Transaction
from app.utils.time_utils import parse_timestamp

class TransactionService:
    async def create_transaction(self, data: dict) -> Transaction:
        amount = data["amount"]
        user_id = data["user_id"]
        transaction_type = data["type"]
        timestamp = data.get("timestamp")
        uid = data.get("uid")

        timestamp = parse_timestamp(timestamp)
        uid = uid or uuid.uuid4()

        transaction = await Transaction.create(type=transaction_type, amount=amount, timestamp=timestamp, user_id=user_id, uid=uid)
        return transaction

    @staticmethod
    async def get_transaction(transaction_uid: str) -> Optional[Transaction]:
        return await Transaction.query.where(Transaction.uid == transaction_uid).gino.first()

    async def get_user_transactions(self, user_id: int, timestamp: Optional[str] = None) -> List[Transaction]:
        timestamp = parse_timestamp(timestamp)
        return await Transaction.query.where(Transaction.user_id == user_id).where(Transaction.timestamp < timestamp).gino.all()
