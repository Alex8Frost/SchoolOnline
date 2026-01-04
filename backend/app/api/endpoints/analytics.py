from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.dependencies import get_current_user
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary")
async def get_summary(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    analytics_service = AnalyticsService(db)
    return await analytics_service.get_dashboard_summary(current_user["user_id"])


@router.get("/category-stats")
async def get_category_stats(
    period: str = "month",
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    analytics_service = AnalyticsService(db)
    return await analytics_service.get_category_stats(current_user["user_id"], period)


@router.get("/category-dynamics")
async def get_category_dynamics(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    analytics_service = AnalyticsService(db)
    return await analytics_service.get_category_dynamics(current_user["user_id"])


@router.get("/goals-progress")
async def get_goals_progress(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    analytics_service = AnalyticsService(db)
    return await analytics_service.get_goal_progress(current_user["user_id"])


@router.get("/income-expense-comparison")
async def get_income_expense_comparison(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    analytics_service = AnalyticsService(db)
    return await analytics_service.get_income_expense_comparison(current_user["user_id"])
