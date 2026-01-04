import csv
import io
from datetime import datetime
from decimal import Decimal
from typing import List, Dict
from uuid import UUID
from app.schemas.transaction import TransactionCreate
from app.models.transaction import TransactionType


class CSVService:
    def __init__(self):
        pass

    def detect_format_and_parse(self, content: str) -> List[Dict]:
        # Simple detection based on headers
        lines = content.splitlines()
        if not lines:
            return []
        
        reader = csv.DictReader(io.StringIO(content))
        headers = reader.fieldnames
        
        transactions = []
        
        # Generic format detection
        # Format 1: date, amount, category, description, type
        if all(h in headers for h in ['date', 'amount', 'type']):
            for row in reader:
                transactions.append({
                    'transaction_date': self._parse_date(row['date']),
                    'amount': Decimal(row['amount']),
                    'type': TransactionType.income if row['type'].lower() == 'income' else TransactionType.expense,
                    'description': row.get('description', ''),
                    'category_name': row.get('category', 'Other')
                })
        
        # Format 2: Tinkoff-like (just as an example)
        elif 'Дата операции' in headers and 'Сумма операции' in headers:
            for row in reader:
                amount = Decimal(row['Сумма операции'].replace(',', '.'))
                transactions.append({
                    'transaction_date': datetime.strptime(row['Дата операции'], '%d.%m.%Y %H:%M:%S').date(),
                    'amount': abs(amount),
                    'type': TransactionType.income if amount > 0 else TransactionType.expense,
                    'description': row.get('Описание', ''),
                    'category_name': row.get('Категория', 'Other')
                })
        
        return transactions

    def _parse_date(self, date_str: str):
        formats = ['%Y-%m-%d', '%d.%m.%Y', '%m/%d/%Y']
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        return datetime.now().date()
