from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime

class TransactionCreate(BaseModel):
    uid: Optional[UUID4] = None
    type: str
    amount: float
    timestamp: Optional[datetime] = None
    user_id: int

class TransactionResponse(BaseModel):
    uid: Optional[UUID4] = None
    type: str
    amount: str
    timestamp: Optional[datetime] = None
    user_id: int
