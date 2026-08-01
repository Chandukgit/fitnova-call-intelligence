from datetime import datetime

from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    Text
)
from sqlalchemy import Enum as SqlEnum
from app.core.enums import FeedbackStatus

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.database.base import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(primary_key=True)

    analysis_id: Mapped[int] = mapped_column(
        ForeignKey("analyses.id"),
        nullable=False
    )

    advisor_comment: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    reviewer_comment: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    status: Mapped[FeedbackStatus] = mapped_column(
    SqlEnum(FeedbackStatus),
    default=FeedbackStatus.PENDING,
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

    analysis = relationship(
        "Analysis",
        back_populates="feedbacks"
    )