from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.db import get_db
from app.dependencies import get_current_user
from app.schemas.goal import Goal, GoalCreate, GoalUpdate
from app.services.goal_service import GoalService

router = APIRouter(prefix="/goals", tags=["Goals"])


@router.get("", response_model=List[Goal])
async def get_goals(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    goal_service = GoalService(db)
    return await goal_service.get_user_goals(current_user["user_id"])


@router.post("", response_model=Goal, status_code=status.HTTP_201_CREATED)
async def create_goal(
    goal_data: GoalCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    goal_service = GoalService(db)
    return await goal_service.create_goal(goal_data, current_user["user_id"])


@router.put("/{goal_id}", response_model=Goal)
async def update_goal(
    goal_id: UUID,
    goal_data: GoalUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    goal_service = GoalService(db)
    return await goal_service.update_goal(goal_id, goal_data, current_user["user_id"])


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(
    goal_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    goal_service = GoalService(db)
    await goal_service.delete_goal(goal_id, current_user["user_id"])
    return None
