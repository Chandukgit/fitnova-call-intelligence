from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.enums import (
    ProcessingStatus,
    CustomerSentiment,
)


class AnalysisBase(BaseModel):
    call_id: int
    overall_score: int | None = None
    needs_discovery_score: int | None = None
    product_knowledge_score: int | None = None
    objection_handling_score: int | None = None
    compliance_score: int | None = None
    next_step_booking_score: int | None = None
    customer_sentiment: CustomerSentiment | None = None
    summary: str | None = None
    recommendation: str | None = None


class AnalysisCreate(AnalysisBase):
    pass


class AnalysisUpdate(BaseModel):
    overall_score: int | None = None
    needs_discovery_score: int | None = None
    product_knowledge_score: int | None = None
    objection_handling_score: int | None = None
    compliance_score: int | None = None
    next_step_booking_score: int | None = None
    customer_sentiment: CustomerSentiment | None = None
    summary: str | None = None
    recommendation: str | None = None
    processing_status: ProcessingStatus | None = None


class AnalysisResponse(AnalysisBase):
    id: int
    processing_status: ProcessingStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)