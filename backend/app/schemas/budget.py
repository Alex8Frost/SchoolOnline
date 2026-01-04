from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal


class BudgetBase(BaseModel):
    category_id: UUID
    amount: Decimal
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=2000, le=2100)


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    category_id: Optional[UUID] = None
    amount: Optional[Decimal] = None
    month: Optional[int] = Field(None, ge=1, le=12)
    year: Optional[int] = Field(None, ge=2000, le=2100)


class Budget(BudgetBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
