from typing import List, Optional, Tuple
from decimal import Decimal
from sqlalchemy import or_

from app.models.user import User
from app.models.transaction import Transaction, TransactionType
from app.utils.time_utils import parse_timestamp

class UserService:
    @staticmethod
    async def get_user(user_id: int) -> Optional[User]:
        return await User.get(user_id)

    @staticmethod
    async def create_user(name: str) -> User:
        return await User.create(name=name)

    async def update_user_balance(self, amount: float, user_id: int, transaction_type: str) -> Decimal:
        amount = Decimal(self._make_float(amount, transaction_type))
        user = await self.get_user(user_id)

        if user is None:
            raise ValueError("User not found")

        new_balance = user.balance + amount
        if new_balance < 0:
            raise ValueError("Insufficient balance")

        await User.update.values(balance=new_balance).where(User.id == user_id).gino.status()
        return new_balance

    async def get_user_with_transaction(self, user_id: int, timestamp: Optional[str] = None) -> Tuple[Optional[User], List[Transaction]]:
        timestamp = parse_timestamp(timestamp)
        if timestamp is None:
            raise ValueError("Invalid timestamp")
        
        txns = await User.join(Transaction, isouter=True).select().where(User.id == user_id).where(or_(Transaction.timestamp < timestamp, Transaction.uid == None)).gino.all()
        
        if not txns:
            return None, []

        user = User(id=txns[0].id, name=txns[0].name, balance=txns[0].balance)
        transactions = [Transaction(amount=t.amount, uid=t.uid, type=t.type, timestamp=t.timestamp, user_id=t.user_id) for t in txns if t.uid]

        return user, transactions

    @staticmethod
    def _make_float(amount: float, transaction_type: str) -> float:
        return float(amount) if transaction_type.upper() == TransactionType.DEPOSIT.name else -abs(float(amount))

    def calculate_balance(self, transactions: List[Transaction]) -> str:
        balance = sum([t.amount if t.type == TransactionType.DEPOSIT else -abs(t.amount) for t in transactions])
        return "%.2f" % balance
