from pydantic import BaseModel
from datetime import datetime
import uuid

from ..db.models.transaction import TransactionType


class TransactionRead(BaseModel):
    id: uuid.UUID
    type: TransactionType
    amount: float
    balance_after: float
    note: str | None = None
    created_at: datetime


class TransactionCreate(BaseModel):
    user_id: uuid.UUID
    type: TransactionType
    amount: float
    balance_after: float
    note: str | None = None
