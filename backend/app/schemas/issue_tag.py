from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.enums import Severity


class IssueTagBase(BaseModel):
    analysis_id: int
    issue_type: str
    severity: Severity
    timestamp: str
    quoted_text: str
    reason: str


class IssueTagCreate(IssueTagBase):
    pass


class IssueTagUpdate(BaseModel):
    issue_type: str | None = None
    severity: Severity | None = None
    timestamp: str | None = None
    quoted_text: str | None = None
    reason: str | None = None


class IssueTagResponse(IssueTagBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)