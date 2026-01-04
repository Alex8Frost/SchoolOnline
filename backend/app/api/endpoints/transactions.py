from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.db import get_db
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse
from app.services.transaction_service import TransactionService
from app.dependencies import get_current_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("", response_model=List[TransactionResponse])
async def get_transactions(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    transaction_service = TransactionService(db)
    return await transaction_service.get_user_transactions(current_user["user_id"])


@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    transaction_service = TransactionService(db)
    return await transaction_service.create_transaction(transaction_data, current_user["user_id"])


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    transaction_service = TransactionService(db)
    return await transaction_service.get_transaction(transaction_id, current_user["user_id"])


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: UUID,
    transaction_data: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    transaction_service = TransactionService(db)
    return await transaction_service.update_transaction(transaction_id, transaction_data, current_user["user_id"])


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    transaction_service = TransactionService(db)
    await transaction_service.delete_transaction(transaction_id, current_user["user_id"])
    return None
