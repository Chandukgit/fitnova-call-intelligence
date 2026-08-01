from datetime import datetime

from sqlalchemy import (
    Integer,
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

from sqlalchemy import Enum as SqlEnum
from app.core.enums import (
    ProcessingStatus,
    CustomerSentiment
)


from app.database.base import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(primary_key=True)

    call_id: Mapped[int] = mapped_column(
        ForeignKey("calls.id"),
        nullable=False,
        unique=True
    )

    overall_score: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )

    needs_discovery_score: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )

    product_knowledge_score: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )

    objection_handling_score: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )

    compliance_score: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )

    next_step_booking_score: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )

    customer_sentiment: Mapped[CustomerSentiment] = mapped_column(
    SqlEnum(CustomerSentiment),
    nullable=True
    )

    summary: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    recommendation: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    processing_status: Mapped[ProcessingStatus] = mapped_column(
    SqlEnum(ProcessingStatus),
    default=ProcessingStatus.PENDING,
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

    call = relationship(
        "Call",
        back_populates="analysis"
    )
    issue_tags = relationship(
    "IssueTag",
    back_populates="analysis",
    cascade="all, delete-orphan"
    )   
    feedbacks = relationship(
    "Feedback",
    back_populates="analysis",
    cascade="all, delete-orphan"
    )