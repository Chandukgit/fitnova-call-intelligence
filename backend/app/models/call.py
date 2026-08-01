from datetime import datetime

from sqlalchemy import Enum as SqlEnum 
from app.core.enums import CallStatus, ProcessingStatus

from sqlalchemy import (
    String,
    Integer,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.database.base import Base


class Call(Base):
    __tablename__ = "calls"

    id: Mapped[int] = mapped_column(primary_key=True)

    advisor_id: Mapped[int] = mapped_column(
        ForeignKey("advisors.id"),
        nullable=False
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False
    )

    call_sid: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    recording_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    duration_seconds: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    ended_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    call_status: Mapped[CallStatus] = mapped_column(
        SqlEnum(CallStatus),
        default=CallStatus.PENDING,
        nullable=False
    )

    language: Mapped[str] = mapped_column(
        String(30),
        nullable=True
    )

    transcription_status: Mapped[ProcessingStatus] = mapped_column(
    SqlEnum(ProcessingStatus),
    default=ProcessingStatus.PENDING,
    nullable=False
    )

    analysis_status: Mapped[ProcessingStatus] = mapped_column(
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

    advisor = relationship(
        "Advisor",
        back_populates="calls"
    )

    customer = relationship(
        "Customer",
        back_populates="calls"
    )

    transcript = relationship(
    "Transcript",
    back_populates="call",
    uselist=False,
    cascade="all, delete-orphan"
    )
    
    analysis = relationship(
    "Analysis",
    back_populates="call",
    uselist=False,
    cascade="all, delete-orphan"
)