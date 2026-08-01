from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.enums import ProcessingStatus


class TranscriptBase(BaseModel):
    call_id: int
    transcript: str
    speaker_transcript: str | None = None
    confidence_score: float | None = None


class TranscriptCreate(TranscriptBase):
    pass


class TranscriptUpdate(BaseModel):
    transcript: str | None = None
    speaker_transcript: str | None = None
    confidence_score: float | None = None
    processing_status: ProcessingStatus | None = None


class TranscriptResponse(TranscriptBase):
    id: int
    processing_status: ProcessingStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)