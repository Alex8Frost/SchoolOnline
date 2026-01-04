from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.db import get_db
from app.dependencies import get_current_user
from app.schemas.category import Category, CategoryCreate, CategoryUpdate
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=List[Category])
async def get_categories(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    category_service = CategoryService(db)
    return await category_service.get_user_categories(current_user["user_id"])


@router.post("", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    category_service = CategoryService(db)
    return await category_service.create_category(category_data, current_user["user_id"])


@router.put("/{category_id}", response_model=Category)
async def update_category(
    category_id: UUID,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    category_service = CategoryService(db)
    return await category_service.update_category(category_id, category_data, current_user["user_id"])


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    category_service = CategoryService(db)
    await category_service.delete_category(category_id, current_user["user_id"])
    return None
