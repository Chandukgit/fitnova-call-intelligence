from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.enums import (
    CallStatus,
    ProcessingStatus,
)


class CallBase(BaseModel):
    advisor_id: int
    customer_id: int
    call_sid: str
    recording_url: str
    duration_seconds: int
    started_at: datetime
    ended_at: datetime
    call_status: CallStatus
    language: str | None = None


class CallCreate(CallBase):
    pass


class CallUpdate(BaseModel):
    recording_url: str | None = None
    duration_seconds: int | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None
    call_status: CallStatus | None = None
    language: str | None = None
    transcription_status: ProcessingStatus | None = None
    analysis_status: ProcessingStatus | None = None


class CallResponse(CallBase):
    id: int
    transcription_status: ProcessingStatus
    analysis_status: ProcessingStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)