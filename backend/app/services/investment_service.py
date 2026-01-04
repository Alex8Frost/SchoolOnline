from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.models.investment import Investment
from app.schemas.investment import InvestmentCreate, InvestmentUpdate


class InvestmentService:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_user_investments(self, user_id: str):
        investments = self.db.query(Investment).filter(
            Investment.user_id == UUID(user_id)
        ).all()
        return investments
    
    async def create_investment(self, investment_data: InvestmentCreate, user_id: str):
        new_investment = Investment(
            user_id=UUID(user_id),
            **investment_data.model_dump()
        )
        
        self.db.add(new_investment)
        self.db.commit()
        self.db.refresh(new_investment)
        
        return new_investment
    
    async def get_investment(self, investment_id: UUID, user_id: str):
        investment = self.db.query(Investment).filter(
            Investment.id == investment_id,
            Investment.user_id == UUID(user_id)
        ).first()
        
        if not investment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Investment not found"
            )
        
        return investment
    
    async def update_investment(self, investment_id: UUID, investment_data: InvestmentUpdate, user_id: str):
        investment = await self.get_investment(investment_id, user_id)
        
        update_data = investment_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(investment, field, value)
        
        self.db.commit()
        self.db.refresh(investment)
        
        return investment
    
    async def delete_investment(self, investment_id: UUID, user_id: str):
        investment = await self.get_investment(investment_id, user_id)
        
        self.db.delete(investment)
        self.db.commit()
        
        return None
