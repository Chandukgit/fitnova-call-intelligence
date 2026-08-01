from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Advisor(Base):
    __tablename__ = "advisors"

    id: Mapped[int] = mapped_column(primary_key=True)

    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"),
        nullable=False
    )

    employee_id: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    phone: Mapped[str] = mapped_column(
        String(20),
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

    team: Mapped["Team"] = relationship(
        back_populates="advisors"
    )

    calls = relationship(
    "Call",
    back_populates="advisor",
    cascade="all, delete-orphan"
)