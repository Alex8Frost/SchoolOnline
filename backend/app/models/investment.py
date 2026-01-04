from sqlalchemy import Column, String, DateTime, Date, Text, Numeric, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum
from app.db import Base


class InvestmentType(str, enum.Enum):
    stock = "stock"
    bond = "bond"
    token = "token"
    deposit = "deposit"


class Investment(Base):
    __tablename__ = "investments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(Enum(InvestmentType), nullable=False)
    ticker = Column(String, nullable=True)
    amount = Column(Numeric(precision=18, scale=8), nullable=False)  # For tokens we need more precision
    purchase_price = Column(Numeric(precision=18, scale=8), nullable=False)
    current_price = Column(Numeric(precision=18, scale=8), nullable=True)
    purchase_date = Column(Date, nullable=False)
    expected_yield = Column(Numeric(precision=5, scale=2), nullable=True)  # e.g. 10.5 for 10.5%
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", backref="investments")
