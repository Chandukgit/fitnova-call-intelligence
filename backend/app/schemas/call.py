from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.enums import (
    CallStatus,
    ProcessingStatus,
)


class CallBase(BaseModel):
    advisor_id: int
    customer_id: int

    original_filename: str
    audio_path: str
    mime_type: str
    file_size: int

    duration_seconds: int | None = None
    language: str | None = None


class CallCreate(CallBase):
    pass


class CallUpdate(BaseModel):
    duration_seconds: int | None = None
    language: str | None = None

    call_status: CallStatus | None = None

    transcription_status: ProcessingStatus | None = None

    analysis_status: ProcessingStatus | None = None


class CallResponse(CallBase):
    id: int

    call_status: CallStatus

    transcription_status: ProcessingStatus

    analysis_status: ProcessingStatus

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )