from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: str | None = None
    age: int | None = None
    gender: str | None = None
    city: str | None = None
    source: str | None = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    email: str | None = None
    age: int | None = None
    gender: str | None = None
    city: str | None = None
    source: str | None = None
    is_active: bool | None = None


class CustomerResponse(CustomerBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)