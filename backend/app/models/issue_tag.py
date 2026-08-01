from datetime import datetime

from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    Text
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.database.base import Base

from sqlalchemy import Enum as SqlEnum
from app.core.enums import Severity


class IssueTag(Base):
    __tablename__ = "issue_tags"

    id: Mapped[int] = mapped_column(primary_key=True)

    analysis_id: Mapped[int] = mapped_column(
        ForeignKey("analyses.id"),
        nullable=False
    )

    issue_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    severity: Mapped[Severity] = mapped_column(
        SqlEnum(Severity),
        nullable=False
    )

    timestamp: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    quoted_text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    reason: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    analysis = relationship(
        "Analysis",
        back_populates="issue_tags"
    )