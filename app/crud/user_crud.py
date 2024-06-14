import datetime
from typing import Optional, Tuple, List, Any
from sqlalchemy import or_
from app.models import User, Transaction


class UserCrud:
    
    @staticmethod
    async def get_user(user_id: int):
        return await User.get(user_id)

    @staticmethod
    async def create_user(name: str) -> User:
        return await User.create(name=name)
    
    @staticmethod
    async def update_user_balance(amount: float, user_id: int, transaction_type: str) -> Tuple[str, Any]:
        if transaction_type.upper() == 'DEPOSIT':
            amount = float(amount)
        else:
            amount = -abs(float(amount))
        return await User.update.values(balance=User.balance + amount).where(User.id == user_id).gino.status()

    @staticmethod
    async def get_user_details(user_id: int, timestamp: Optional[datetime.datetime] = None) -> Tuple[Optional[User], List[Transaction]]:
        if not timestamp:
            timestamp = datetime.datetime.now()
        txn_list = await (User.join(Transaction, isouter=True).select()
                          .where(User.id == user_id)
                          .where(or_(Transaction.timestamp < timestamp, Transaction.uid == None))
                          ).gino.all()

        if not txn_list:
            return None, []

        fetched_user = txn_list[0]
        user_info = User(id=fetched_user.id, name=fetched_user.name, balance=fetched_user.balance)
        transactions = [Transaction(amount=txn.amount, uid=txn.uid, type=txn.type, timestamp=txn.timestamp, user_id=txn.user_id) for txn in txn_list if txn.uid]
        return user_info, transactions