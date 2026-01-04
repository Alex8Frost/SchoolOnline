from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import date, datetime
from decimal import Decimal
from enum import Enum


class GoalType(str, Enum):
    capital = "capital"
    passive_income = "passive_income"


class GoalBase(BaseModel):
    name: str
    target_amount: Decimal
    current_amount: Decimal = Decimal(0)
    type: GoalType
    target_date: Optional[date] = None


class GoalCreate(GoalBase):
    pass


class GoalUpdate(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[Decimal] = None
    current_amount: Optional[Decimal] = None
    type: Optional[GoalType] = None
    target_date: Optional[date] = None


class Goal(GoalBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
