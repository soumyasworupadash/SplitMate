from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from datetime import datetime, timezone
from app.database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)

    description = Column(String(255), nullable=False)

    amount = Column(Float, nullable=False)

    paid_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    group_id = Column(
        Integer,
        ForeignKey("groups.id"),
        nullable=False
    )
    created_at = Column(
    DateTime(timezone=True),
    default=lambda: datetime.now(timezone.utc),
    nullable=False
    )