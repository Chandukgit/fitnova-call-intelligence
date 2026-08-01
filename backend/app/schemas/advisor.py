from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AdvisorBase(BaseModel):
    team_id: int
    employee_id: str
    first_name: str
    last_name: str
    email: str
    phone: str | None = None


class AdvisorCreate(AdvisorBase):
    pass


class AdvisorUpdate(BaseModel):
    team_id: int | None = None
    employee_id: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    is_active: bool | None = None


class AdvisorResponse(AdvisorBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)