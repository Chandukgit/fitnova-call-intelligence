from app.api.router_factory import create_crud_router

from app.core.auth import get_current_user
from app.core.permissions import require_roles
from app.core.enums import UserRole

from app.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse,
)

from app.services.organization import (
    organization_service,
)

router = create_crud_router(
    service=organization_service,
    create_schema=OrganizationCreate,
    update_schema=OrganizationUpdate,
    response_schema=OrganizationResponse,
    prefix="/organizations",
    tags=["Organizations"],
)