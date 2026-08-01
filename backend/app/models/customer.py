from datetime import datetime

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )

    age: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )

    gender: Mapped[str] = mapped_column(
        String(20),
        nullable=True
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    source: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    calls = relationship(
    "Call",
    back_populates="customer",
    cascade="all, delete-orphan"
)