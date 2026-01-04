from sqlalchemy import Column, DateTime, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.db import Base


class Budget(Base):
    __tablename__ = "budgets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    amount = Column(Numeric(precision=10, scale=2), nullable=False)
    month = Column(Numeric(precision=2, scale=0), nullable=False)  # 1-12
    year = Column(Numeric(precision=4, scale=0), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", backref="budgets")
    category = relationship("Category", backref="budgets")
