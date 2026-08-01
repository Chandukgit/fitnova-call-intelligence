from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TeamBase(BaseModel):
    name: str
    organization_id: int


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: str | None = None
    organization_id: int | None = None


class TeamResponse(TeamBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )