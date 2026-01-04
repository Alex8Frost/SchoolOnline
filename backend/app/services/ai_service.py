from typing import Dict, List
import random


class AIService:
    def __init__(self):
        pass

    async def analyze_document(self, content: bytes, file_name: str) -> Dict:
        # Mocking document analysis
        if "whitepaper" in file_name.lower() or "token" in file_name.lower():
            return {
                "name": "Project Token",
                "type": "token",
                "expected_yield": 15.0,
                "ticker": "PTKN",
                "description": "Analyzed from White Paper"
            }
        elif "bond" in file_name.lower() or "prospectus" in file_name.lower():
            return {
                "name": "Corporate Bond",
                "type": "bond",
                "expected_yield": 8.5,
                "ticker": "CBOND",
                "description": "Analyzed from Bond Prospectus"
            }
        elif "deposit" in file_name.lower() or "agreement" in file_name.lower():
            return {
                "name": "Term Deposit",
                "type": "deposit",
                "expected_yield": 6.0,
                "description": "Analyzed from Deposit Agreement"
            }
        
        return {
            "name": "Unknown Investment",
            "type": "stock",
            "expected_yield": 5.0,
            "description": "Generic analysis"
        }

    async def get_saving_recommendations(self, transactions: List, categories: List) -> List[str]:
        # Mocking recommendations
        recommendations = [
            "You spend a lot on 'Entertainment'. Try reducing it by 10% to invest more in stocks.",
            "Your 'Groceries' expenses are 20% higher than last month. Consider meal planning.",
            "Consider increasing your monthly contribution to your 'Retirement' goal."
        ]
        return random.sample(recommendations, k=2)

    async def get_planning_tips(self, budgets: List, transactions: List) -> List[str]:
        # Mocking planning tips
        tips = [
            "You have already spent 80% of your 'Dining Out' budget this month.",
            "You are well within your budget for 'Transportation'. Good job!",
            "Consider adjusting your budget for 'Utilities' as it consistently exceeds your plan."
        ]
        return random.sample(tips, k=2)
