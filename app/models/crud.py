import datetime
import uuid
from typing import Union, Optional, List, Tuple

from sqlalchemy import or_

from app.models import User, Transaction, TransactionType


class CrudMixin:
    @staticmethod
    def make_float(amount: float, transaction_type: str) -> float:
        return (
            float(amount)
            if transaction_type.upper() == TransactionType.DEPOSIT.name
            else -abs(float(amount))
        )

    @staticmethod
    def get_timestamp(
        timestamp: Optional[datetime.datetime] = None,
    ) -> datetime.datetime:
        if not timestamp:
            timestamp = datetime.datetime.now()
        return timestamp


class UserCrud(CrudMixin):
    @staticmethod
    async def get_user(user_id: int):
        return await User.get(user_id)

    @staticmethod
    async def create_user(name: str) -> User:
        return await User.create(name=name)

    async def update_user_balance(
        self, amount: float, user_id: int, transaction_type: str
    ) -> tuple:
        amount = self.make_float(amount=amount, transaction_type=transaction_type)
        return (
            await User.update.values(balance=User.balance + amount)
            .where(User.id == user_id)
            .gino.status()
        )

    async def get_user_with_transaction(
        self, user_id: int, timestamp: Optional[datetime.datetime] = None
    ) -> Tuple[Optional[User], List[Transaction]]:
        timestamp = self.get_timestamp(timestamp)
        txns = await (
            User.join(Transaction, isouter=True)
            .select()
            .where(User.id == user_id)
            .where(or_(Transaction.timestamp < timestamp, Transaction.uid == None))
        ).gino.all()
        if not txns:
            return None, []
        user = User(
            id=txns[0].id,
            name=txns[0].name,
            balance=txns[0].balance,
        )
        transactions = [
            Transaction(
                amount=t.amount,
                uid=t.uid,
                type=t.type,
                timestamp=t.timestamp,
                user_id=t.user_id,
            )
            for t in txns if t.uid
        ]
        return user, transactions


class TransactionCrud(CrudMixin):
    async def create_transaction(
        self,
        user_id: int,
        transaction_type: str,
        amount: float,
        timestamp: Optional[Union[str, datetime.datetime]] = None,
        uid: Optional[str] = None,
    ) -> Transaction:
        if timestamp:
            timestamp = datetime.datetime.fromisoformat(timestamp)
        else:
            timestamp = self.get_timestamp(timestamp)
        if not uid:
            uid = uuid.uuid4()
        transaction = await Transaction.create(
            type=transaction_type,
            amount=amount,
            timestamp=timestamp,
            user_id=user_id,
            uid=uid,
        )
        return transaction

    @staticmethod
    async def get_transaction(transaction_uid: str) -> Optional[Transaction]:
        return await Transaction.query.where(
            Transaction.uid == transaction_uid
        ).gino.first()

    async def get_user_transactions(
        self, user_id: int, timestamp: Optional[datetime.datetime] = None
    ) -> List[Transaction]:
        timestamp = self.get_timestamp(timestamp)
        return (
            await Transaction.query.where(Transaction.user_id == user_id)
            .where(Transaction.timestamp < timestamp)
            .gino.all()
        )
