from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db

from app.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse,
)

from app.services.organization import (
    organization_service,
)

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post("", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
def create_organization(organization: OrganizationCreate, db: Session = Depends(get_db)):
    return organization_service.create_organization(db, organization)


@router.get("", response_model=list[OrganizationResponse])
def get_organizations(db: Session = Depends(get_db)):
    return organization_service.get_organizations(db)


@router.get("/{organization_id}", response_model=OrganizationResponse)
def get_organization(organization_id: int, db: Session = Depends(get_db)):
    return organization_service.get_organization(db, organization_id)


@router.put("/{organization_id}", response_model=OrganizationResponse)
def update_organization(organization_id: int, organization: OrganizationUpdate, db: Session = Depends(get_db)):
    return organization_service.update_organization(db, organization_id, organization)


@router.delete("/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_organization(organization_id: int, db: Session = Depends(get_db)):
    organization_service.delete_organization(db, organization_id)
