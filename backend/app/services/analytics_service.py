from typing import Dict, List, Any
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import date, datetime, timedelta
from decimal import Decimal
from app.models.transaction import Transaction, TransactionType
from app.models.investment import Investment, InvestmentType
from app.models.category import Category
from app.models.budget import Budget
from app.models.goal import Goal
from sqlalchemy import func


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    async def get_dashboard_summary(self, user_id: str) -> Dict:
        u_id = UUID(user_id)
        
        # Current balance
        income = self.db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == u_id,
            Transaction.type == TransactionType.income
        ).scalar() or Decimal(0)
        
        expense = self.db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == u_id,
            Transaction.type == TransactionType.expense
        ).scalar() or Decimal(0)
        
        balance = income - expense
        
        # Portfolio value
        portfolio_value = self.db.query(func.sum(Investment.amount * Investment.purchase_price)).filter(
            Investment.user_id == u_id
        ).scalar() or Decimal(0)
        
        # Passive income estimation
        investments = self.db.query(Investment).filter(Investment.user_id == u_id).all()
        annual_passive_income = Decimal(0)
        for inv in investments:
            if inv.expected_yield:
                annual_passive_income += (inv.amount * inv.purchase_price) * (inv.expected_yield / 100)
        
        return {
            "current_balance": balance,
            "portfolio_value": portfolio_value,
            "annual_passive_income": annual_passive_income,
            "monthly_passive_income": annual_passive_income / 12,
            "daily_passive_income": annual_passive_income / 365,
            "hourly_passive_income": annual_passive_income / (365 * 24),
            "total_income": income,
            "total_expense": expense
        }

    async def get_category_stats(self, user_id: str, period: str = "month") -> List[Dict]:
        u_id = UUID(user_id)
        # Group by category and sum amounts
        stats = self.db.query(
            Category.name,
            Category.color,
            Category.type,
            func.sum(Transaction.amount).label("total_amount")
        ).join(Transaction).filter(
            Transaction.user_id == u_id
        ).group_by(Category.id).all()
        
        return [
            {
                "category_name": name,
                "color": color,
                "type": t,
                "amount": amount
            } for name, color, t, amount in stats
        ]

    async def get_goal_progress(self, user_id: str) -> List[Dict]:
        u_id = UUID(user_id)
        goals = self.db.query(Goal).filter(Goal.user_id == u_id).all()
        
        results = []
        for goal in goals:
            progress = (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0
            
            # Simple projection: how much is needed per month
            remaining = goal.target_amount - goal.current_amount
            months_left = 12 
            if goal.target_date:
                today = date.today()
                months_left = (goal.target_date.year - today.year) * 12 + goal.target_date.month - today.month
                if months_left <= 0: months_left = 1
            
            monthly_needed = remaining / months_left if remaining > 0 else 0
            
            results.append({
                "goal_id": goal.id,
                "name": goal.name,
                "type": goal.type,
                "target_amount": goal.target_amount,
                "current_amount": goal.current_amount,
                "progress_percentage": progress,
                "monthly_investment_needed": monthly_needed,
                "target_date": goal.target_date
            })
        return results

    async def get_category_dynamics(self, user_id: str) -> List[Dict]:
        u_id = UUID(user_id)
        # Compare this month vs last month
        today = date.today()
        this_month_start = date(today.year, today.month, 1)
        
        last_month_year = today.year
        last_month = today.month - 1
        if last_month == 0:
            last_month = 12
            last_month_year -= 1
        last_month_start = date(last_month_year, last_month, 1)
        
        # This month stats
        this_month_stats = self.db.query(
            Category.id,
            Category.name,
            func.sum(Transaction.amount).label("total")
        ).join(Transaction).filter(
            Transaction.user_id == u_id,
            Transaction.transaction_date >= this_month_start
        ).group_by(Category.id).all()
        
        # Last month stats
        last_month_stats = self.db.query(
            Category.id,
            func.sum(Transaction.amount).label("total")
        ).join(Transaction).filter(
            Transaction.user_id == u_id,
            Transaction.transaction_date >= last_month_start,
            Transaction.transaction_date < this_month_start
        ).group_by(Category.id).all()
        
        last_month_map = {cid: total for cid, total in last_month_stats}
        
        results = []
        for cid, name, total in this_month_stats:
            prev_total = last_month_map.get(cid, Decimal(0))
            change = total - prev_total
            change_pct = (change / prev_total * 100) if prev_total > 0 else 100 if total > 0 else 0
            
            results.append({
                "category_id": cid,
                "category_name": name,
                "this_month": total,
                "last_month": prev_total,
                "change": change,
                "change_percentage": change_pct
            })
        return results

    async def get_income_expense_comparison(self, user_id: str) -> List[Dict]:
        u_id = UUID(user_id)
        # Last 6 months comparison
        today = date.today()
        results = []
        
        for i in range(5, -1, -1):
            # Calculate month and year
            month = today.month - i
            year = today.year
            if month <= 0:
                month += 12
                year -= 1
            
            # Start and end of month
            start_of_month = date(year, month, 1)
            if month == 12:
                next_month = date(year + 1, 1, 1)
            else:
                next_month = date(year, month + 1, 1)
            end_of_month = next_month - timedelta(days=1)
                
            inc = self.db.query(func.sum(Transaction.amount)).filter(
                Transaction.user_id == u_id,
                Transaction.type == TransactionType.income,
                Transaction.transaction_date >= start_of_month,
                Transaction.transaction_date <= end_of_month
            ).scalar() or Decimal(0)
            
            exp = self.db.query(func.sum(Transaction.amount)).filter(
                Transaction.user_id == u_id,
                Transaction.type == TransactionType.expense,
                Transaction.transaction_date >= start_of_month,
                Transaction.transaction_date <= end_of_month
            ).scalar() or Decimal(0)
            
            results.append({
                "month": start_of_month.strftime("%Y-%m"),
                "income": inc,
                "expense": exp
            })
            
        return results
