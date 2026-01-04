from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.models.goal import Goal
from app.schemas.goal import GoalCreate, GoalUpdate


class GoalService:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_user_goals(self, user_id: str):
        goals = self.db.query(Goal).filter(
            Goal.user_id == UUID(user_id)
        ).all()
        return goals
    
    async def create_goal(self, goal_data: GoalCreate, user_id: str):
        new_goal = Goal(
            user_id=UUID(user_id),
            **goal_data.model_dump()
        )
        
        self.db.add(new_goal)
        self.db.commit()
        self.db.refresh(new_goal)
        
        return new_goal
    
    async def get_goal(self, goal_id: UUID, user_id: str):
        goal = self.db.query(Goal).filter(
            Goal.id == goal_id,
            Goal.user_id == UUID(user_id)
        ).first()
        
        if not goal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Goal not found"
            )
        
        return goal
    
    async def update_goal(self, goal_id: UUID, goal_data: GoalUpdate, user_id: str):
        goal = await self.get_goal(goal_id, user_id)
        
        update_data = goal_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(goal, field, value)
        
        self.db.commit()
        self.db.refresh(goal)
        
        return goal
    
    async def delete_goal(self, goal_id: UUID, user_id: str):
        goal = await self.get_goal(goal_id, user_id)
        
        self.db.delete(goal)
        self.db.commit()
        
        return None
