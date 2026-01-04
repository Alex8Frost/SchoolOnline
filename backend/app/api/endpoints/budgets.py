from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.db import get_db
from app.dependencies import get_current_user
from app.schemas.budget import Budget, BudgetCreate, BudgetUpdate
from app.services.budget_service import BudgetService

router = APIRouter(prefix="/budgets", tags=["Budgets"])


@router.get("", response_model=List[Budget])
async def get_budgets(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    budget_service = BudgetService(db)
    return await budget_service.get_user_budgets(current_user["user_id"])


@router.post("", response_model=Budget, status_code=status.HTTP_201_CREATED)
async def create_budget(
    budget_data: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    budget_service = BudgetService(db)
    return await budget_service.create_budget(budget_data, current_user["user_id"])


@router.put("/{budget_id}", response_model=Budget)
async def update_budget(
    budget_id: UUID,
    budget_data: BudgetUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    budget_service = BudgetService(db)
    return await budget_service.update_budget(budget_id, budget_data, current_user["user_id"])


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_budget(
    budget_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    budget_service = BudgetService(db)
    await budget_service.delete_budget(budget_id, current_user["user_id"])
    return None
