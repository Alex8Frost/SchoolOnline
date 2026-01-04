from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import date, datetime
from decimal import Decimal
from enum import Enum


class InvestmentType(str, Enum):
    stock = "stock"
    bond = "bond"
    token = "token"
    deposit = "deposit"


class InvestmentBase(BaseModel):
    name: str
    type: InvestmentType
    ticker: Optional[str] = None
    amount: Decimal
    purchase_price: Decimal
    current_price: Optional[Decimal] = None
    purchase_date: date
    expected_yield: Optional[Decimal] = None
    description: Optional[str] = None


class InvestmentCreate(InvestmentBase):
    pass


class InvestmentUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[InvestmentType] = None
    ticker: Optional[str] = None
    amount: Optional[Decimal] = None
    purchase_price: Optional[Decimal] = None
    current_price: Optional[Decimal] = None
    purchase_date: Optional[date] = None
    expected_yield: Optional[Decimal] = None
    description: Optional[str] = None


class Investment(InvestmentBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
