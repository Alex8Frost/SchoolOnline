from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.db import get_db
from app.dependencies import get_current_user
from app.services.ai_service import AIService
from app.services.transaction_service import TransactionService
from app.services.category_service import CategoryService
from app.services.budget_service import BudgetService

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/analyze-document")
async def analyze_document(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    content = await file.read()
    ai_service = AIService()
    return await ai_service.analyze_document(content, file.filename)


@router.get("/recommendations")
async def get_recommendations(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    ai_service = AIService()
    transaction_service = TransactionService(db)
    category_service = CategoryService(db)
    
    transactions = await transaction_service.get_user_transactions(current_user["user_id"])
    categories = await category_service.get_user_categories(current_user["user_id"])
    
    return await ai_service.get_saving_recommendations(transactions, categories)


@router.get("/planning-tips")
async def get_planning_tips(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    ai_service = AIService()
    budget_service = BudgetService(db)
    transaction_service = TransactionService(db)
    
    budgets = await budget_service.get_user_budgets(current_user["user_id"])
    transactions = await transaction_service.get_user_transactions(current_user["user_id"])
    
    return await ai_service.get_planning_tips(budgets, transactions)
