from sqlalchemy import CheckConstraint

from app.models import db


class User(db.Model):
    __tablename__ = "users"
    __table_args__ = (CheckConstraint("balance >= 0.00"),)

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.DECIMAL(10, 2), default=0.00, nullable=False)
