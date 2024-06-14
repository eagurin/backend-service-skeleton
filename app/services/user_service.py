from app.crud import UserCrud
from app.schemas.user import UserCreate
from app.models import User, Transaction
from uuid import UUID
from typing import Optional, List, Tuple
from datetime import datetime
from loguru import logger
from aiohttp import web

class UserService:

    @staticmethod
    async def create_user(name: str) -> User:
        user = await UserCrud().create_user(name=name)
        return user

    @staticmethod
    async def get_user_with_transactions(app: web.Application, user_id: int, timestamp: Optional[datetime] = None) -> Tuple[Optional[User], List[Transaction]]:
        redis = app.get('redis')
        if redis is None:
            logger.error("Redis connection not found in app")
            return None, []

        key = f"user:{user_id}"
        try:
            cached_user = await redis.get(key)
            if cached_user:
                logger.info(f"Cache hit for user: {user_id}")
                user, transactions = User.from_json(cached_user)
                return user, transactions

            logger.info(f"Cache miss for user: {user_id}")
            user, transactions = await UserCrud().get_user_with_transactions(user_id=user_id, timestamp=timestamp)

            if user:
                await redis.set(key, user.to_json(), ex=3600)  # Cache for 1 hour

            return user, transactions
        except Exception as e:
            logger.error(f"Error accessing Redis: {e}")
            return None, []

    @staticmethod
    async def update_user_balance(user_id: int, amount: float, transaction_type: str) -> None:
        await UserCrud().update_user_balance(amount=amount, user_id=user_id, transaction_type=transaction_type)