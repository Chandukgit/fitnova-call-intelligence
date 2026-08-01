from datetime import datetime
from sqlalchemy import Enum as SqlEnum
from app.core.enums import ProcessingStatus

from sqlalchemy import (
    String,
    DateTime,
    Float,
    ForeignKey,
    Text
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.database.base import Base


class Transcript(Base):
    __tablename__ = "transcripts"

    id: Mapped[int] = mapped_column(primary_key=True)

    call_id: Mapped[int] = mapped_column(
        ForeignKey("calls.id"),
        nullable=False,
        unique=True
    )

    transcript: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    speaker_transcript: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    confidence_score: Mapped[float] = mapped_column(
        Float,
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
        back_populates="transcript"
    )