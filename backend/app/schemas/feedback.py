from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.enums import FeedbackStatus


class FeedbackBase(BaseModel):
    analysis_id: int
    advisor_comment: str
    reviewer_comment: str | None = None


class FeedbackCreate(FeedbackBase):
    pass


class FeedbackUpdate(BaseModel):
    advisor_comment: str | None = None
    reviewer_comment: str | None = None
    status: FeedbackStatus | None = None


class FeedbackResponse(FeedbackBase):
    id: int
    status: FeedbackStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)