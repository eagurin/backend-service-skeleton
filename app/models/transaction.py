import enum
import uuid

import sqlalchemy
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID

from app.models import db


class TransactionType(enum.Enum):
    WITHDRAW = 1
    DEPOSIT = 2


class Transaction(db.Model):
    __tablename__ = "transactions"

    uid = db.Column(UUID(), primary_key=True, default=uuid.uuid4)
    type = db.Column(Enum(TransactionType), nullable=False)
    amount = db.Column(db.DECIMAL(10, 2), nullable=False)
    timestamp = db.Column(
        db.DateTime(), nullable=False, server_default=sqlalchemy.func.now()
    )
    user_id = db.Column(db.ForeignKey("users.id"))
