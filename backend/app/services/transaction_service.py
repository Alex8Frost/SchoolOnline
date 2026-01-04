from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate


class TransactionService:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_user_transactions(
        self, 
        user_id: str, 
        transaction_type: str = None, 
        category_id: UUID = None, 
        start_date: str = None, 
        end_date: str = None
    ):
        query = self.db.query(Transaction).filter(
            Transaction.user_id == UUID(user_id)
        )
        
        if transaction_type:
            query = query.filter(Transaction.type == transaction_type)
        
        if category_id:
            query = query.filter(Transaction.category_id == category_id)
            
        if start_date:
            query = query.filter(Transaction.transaction_date >= start_date)
            
        if end_date:
            query = query.filter(Transaction.transaction_date <= end_date)
            
        return query.order_by(Transaction.transaction_date.desc()).all()
    
    async def create_transaction(self, transaction_data: TransactionCreate, user_id: str):
        new_transaction = Transaction(
            user_id=UUID(user_id),
            amount=transaction_data.amount,
            type=transaction_data.type,
            category_id=transaction_data.category_id,
            description=transaction_data.description,
            transaction_date=transaction_data.transaction_date
        )
        
        self.db.add(new_transaction)
        self.db.commit()
        self.db.refresh(new_transaction)
        
        return new_transaction
    
    async def get_transaction(self, transaction_id: UUID, user_id: str):
        transaction = self.db.query(Transaction).filter(
            Transaction.id == transaction_id,
            Transaction.user_id == UUID(user_id)
        ).first()
        
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        
        return transaction
    
    async def update_transaction(self, transaction_id: UUID, transaction_data: TransactionUpdate, user_id: str):
        transaction = await self.get_transaction(transaction_id, user_id)
        
        update_data = transaction_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(transaction, field, value)
        
        self.db.commit()
        self.db.refresh(transaction)
        
        return transaction
    
    async def delete_transaction(self, transaction_id: UUID, user_id: str):
        transaction = await self.get_transaction(transaction_id, user_id)
        
        self.db.delete(transaction)
        self.db.commit()
        
        return None
