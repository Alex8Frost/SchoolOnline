from sqlalchemy import Column, String, DateTime, Date, Numeric, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum
from app.db import Base


class GoalType(str, enum.Enum):
    capital = "capital"
    passive_income = "passive_income"


class Goal(Base):
    __tablename__ = "goals"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    target_amount = Column(Numeric(precision=15, scale=2), nullable=False)
    current_amount = Column(Numeric(precision=15, scale=2), default=0)
    type = Column(Enum(GoalType), nullable=False)
    target_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", backref="goals")
