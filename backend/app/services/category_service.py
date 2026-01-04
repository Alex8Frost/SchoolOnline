from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_user_categories(self, user_id: str):
        categories = self.db.query(Category).filter(
            Category.user_id == UUID(user_id)
        ).all()
        return categories
    
    async def create_category(self, category_data: CategoryCreate, user_id: str):
        new_category = Category(
            user_id=UUID(user_id),
            name=category_data.name,
            type=category_data.type,
            color=category_data.color,
            icon=category_data.icon
        )
        
        self.db.add(new_category)
        self.db.commit()
        self.db.refresh(new_category)
        
        return new_category
    
    async def get_category(self, category_id: UUID, user_id: str):
        category = self.db.query(Category).filter(
            Category.id == category_id,
            Category.user_id == UUID(user_id)
        ).first()
        
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        
        return category
    
    async def update_category(self, category_id: UUID, category_data: CategoryUpdate, user_id: str):
        category = await self.get_category(category_id, user_id)
        
        update_data = category_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category, field, value)
        
        self.db.commit()
        self.db.refresh(category)
        
        return category
    
    async def delete_category(self, category_id: UUID, user_id: str):
        category = await self.get_category(category_id, user_id)
        
        self.db.delete(category)
        self.db.commit()
        
        return None
