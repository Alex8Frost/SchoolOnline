from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.db import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("")
async def get_categories(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return {
        "message": "Get categories endpoint - to be implemented",
        "user_id": current_user["user_id"]
    }


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_category(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return {
        "message": "Create category endpoint - to be implemented"
    }


@router.put("/{category_id}")
async def update_category(
    category_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return {
        "message": f"Update category {category_id} endpoint - to be implemented"
    }


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return None
