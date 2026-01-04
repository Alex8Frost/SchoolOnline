from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.models.budget import Budget
from app.schemas.budget import BudgetCreate, BudgetUpdate


class BudgetService:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_user_budgets(self, user_id: str):
        budgets = self.db.query(Budget).filter(
            Budget.user_id == UUID(user_id)
        ).all()
        return budgets
    
    async def create_budget(self, budget_data: BudgetCreate, user_id: str):
        new_budget = Budget(
            user_id=UUID(user_id),
            **budget_data.model_dump()
        )
        
        self.db.add(new_budget)
        self.db.commit()
        self.db.refresh(new_budget)
        
        return new_budget
    
    async def get_budget(self, budget_id: UUID, user_id: str):
        budget = self.db.query(Budget).filter(
            Budget.id == budget_id,
            Budget.user_id == UUID(user_id)
        ).first()
        
        if not budget:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Budget not found"
            )
        
        return budget
    
    async def update_budget(self, budget_id: UUID, budget_data: BudgetUpdate, user_id: str):
        budget = await self.get_budget(budget_id, user_id)
        
        update_data = budget_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(budget, field, value)
        
        self.db.commit()
        self.db.refresh(budget)
        
        return budget
    
    async def delete_budget(self, budget_id: UUID, user_id: str):
        budget = await self.get_budget(budget_id, user_id)
        
        self.db.delete(budget)
        self.db.commit()
        
        return None
