from sqlalchemy import Column, String

from app.app import db

class ProcessedMessage(db.Model):
    __tablename__ = 'processed_messages'

    message_id = Column(String(), primary_key=True)
