from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from enum import Enum


class CategoryType(str, Enum):
    income = "income"
    expense = "expense"


class CategoryBase(BaseModel):
    name: str
    type: CategoryType
    color: str
    icon: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[CategoryType] = None
    color: Optional[str] = None
    icon: Optional[str] = None


class Category(CategoryBase):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True
