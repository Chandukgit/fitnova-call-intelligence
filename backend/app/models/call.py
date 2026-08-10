from datetime import datetime

from sqlalchemy import (
    String,
    Integer,
    BigInteger,
    DateTime,
    ForeignKey,
    Enum as SqlEnum,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import Base
from app.core.enums import (
    CallStatus,
    ProcessingStatus,
)


class Call(Base):
    __tablename__ = "calls"

    id: Mapped[int] = mapped_column(primary_key=True)

    advisor_id: Mapped[int] = mapped_column(
        ForeignKey("advisors.id"),
        nullable=False,
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    audio_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    duration_seconds: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    language: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    call_status: Mapped[CallStatus] = mapped_column(
        SqlEnum(CallStatus),
        default=CallStatus.UPLOADED,
        nullable=False,
    )

    transcription_status: Mapped[ProcessingStatus] = mapped_column(
        SqlEnum(ProcessingStatus),
        default=ProcessingStatus.PENDING,
        nullable=False,
    )

    analysis_status: Mapped[ProcessingStatus] = mapped_column(
        SqlEnum(ProcessingStatus),
        default=ProcessingStatus.PENDING,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    advisor = relationship(
        "Advisor",
        back_populates="calls",
    )

    customer = relationship(
        "Customer",
        back_populates="calls",
    )

    transcript = relationship(
        "Transcript",
        back_populates="call",
        uselist=False,
        cascade="all, delete-orphan",
    )

    analysis = relationship(
        "Analysis",
        back_populates="call",
        uselist=False,
        cascade="all, delete-orphan",
    )