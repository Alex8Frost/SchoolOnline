from pydantic import BaseModel, condecimal
from uuid import UUID
from datetime import datetime, date
from typing import Optional
from decimal import Decimal


class TransactionBase(BaseModel):
    amount: condecimal(max_digits=10, decimal_places=2)
    type: str
    category_id: UUID
    description: Optional[str] = None
    transaction_date: date


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    amount: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    type: Optional[str] = None
    category_id: Optional[UUID] = None
    description: Optional[str] = None
    transaction_date: Optional[date] = None


class TransactionResponse(TransactionBase):
    id: UUID
    user_id: UUID
    google_calendar_event_id: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
