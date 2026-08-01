from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OrganizationBase(BaseModel):
    name: str
    email: str
    phone: str | None = None


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None


class OrganizationResponse(OrganizationBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )