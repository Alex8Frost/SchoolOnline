from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.db import get_db
from app.dependencies import get_current_user
from app.schemas.investment import Investment, InvestmentCreate, InvestmentUpdate
from app.services.investment_service import InvestmentService

router = APIRouter(prefix="/investments", tags=["Investments"])


@router.get("", response_model=List[Investment])
async def get_investments(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    investment_service = InvestmentService(db)
    return await investment_service.get_user_investments(current_user["user_id"])


@router.post("", response_model=Investment, status_code=status.HTTP_201_CREATED)
async def create_investment(
    investment_data: InvestmentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    investment_service = InvestmentService(db)
    return await investment_service.create_investment(investment_data, current_user["user_id"])


@router.put("/{investment_id}", response_model=Investment)
async def update_investment(
    investment_id: UUID,
    investment_data: InvestmentUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    investment_service = InvestmentService(db)
    return await investment_service.update_investment(investment_id, investment_data, current_user["user_id"])


@router.delete("/{investment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_investment(
    investment_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    investment_service = InvestmentService(db)
    await investment_service.delete_investment(investment_id, current_user["user_id"])
    return None
