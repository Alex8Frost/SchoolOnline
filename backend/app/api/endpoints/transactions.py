from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.db import get_db
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse
from app.services.transaction_service import TransactionService
from app.services.csv_service import CSVService
from app.services.category_service import CategoryService
from app.schemas.category import CategoryCreate, CategoryType
from app.models.transaction import TransactionType
from app.dependencies import get_current_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("", response_model=List[TransactionResponse])
async def get_transactions(
    type: str = None,
    category_id: UUID = None,
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    transaction_service = TransactionService(db)
    return await transaction_service.get_user_transactions(
        current_user["user_id"],
        transaction_type=type,
        category_id=category_id,
        start_date=start_date,
        end_date=end_date
    )


@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    transaction_service = TransactionService(db)
    return await transaction_service.create_transaction(transaction_data, current_user["user_id"])


@router.post("/import/csv")
async def import_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    content = await file.read()
    csv_service = CSVService()
    parsed_transactions = csv_service.detect_format_and_parse(content.decode('utf-8'))
    
    transaction_service = TransactionService(db)
    category_service = CategoryService(db)
    
    user_categories = await category_service.get_user_categories(current_user["user_id"])
    category_map = {c.name: c.id for c in user_categories}
    
    imported_count = 0
    for t_data in parsed_transactions:
        # Get or create category
        category_name = t_data.pop('category_name')
        if category_name not in category_map:
            new_cat = await category_service.create_category(
                CategoryCreate(
                    name=category_name, 
                    type=CategoryType.expense if t_data['type'] == TransactionType.expense else CategoryType.income,
                    color="#808080"
                ),
                current_user["user_id"]
            )
            category_map[category_name] = new_cat.id
        
        t_data['category_id'] = category_map[category_name]
        await transaction_service.create_transaction(
            TransactionCreate(**t_data),
            current_user["user_id"]
        )
        imported_count += 1
        
    return {"message": f"Successfully imported {imported_count} transactions"}


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
