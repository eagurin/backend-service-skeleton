import uuid

import enum

import sqlalchemy
from sqlalchemy import Enum, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID

from app.app import db


class TransactionType(enum.Enum):
    WITHDRAW = 1
    DEPOSIT = 2


class User(db.Model):
    __tablename__ = "users"
    __table_args__ = (CheckConstraint("balance >= 0.00"),)

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.DECIMAL(10, 2), default=0.00, nullable=False)


class Transaction(db.Model):
    __tablename__ = "transactions"

    uid = db.Column(UUID(), primary_key=True, default=uuid.uuid4)
    type = db.Column(Enum(TransactionType), nullable=False)
    amount = db.Column(db.DECIMAL(10, 2), nullable=False)
    timestamp = db.Column(
        db.DateTime(), nullable=False, server_default=sqlalchemy.func.now()
    )
    user_id = db.Column(db.ForeignKey("users.id"))
