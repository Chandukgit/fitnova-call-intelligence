from sqlalchemy.orm import Session

from app.crud.organization import organization
from app.models.organization import Organization
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate,
)
from app.core.exceptions import (
    NotFoundException,
    DuplicateResourceException,
)

class OrganizationService:

    def create_organization(
        self,
        db: Session,
        organization_in: OrganizationCreate,
    ) -> Organization:

        existing = organization.get_by_email(
            db,
            organization_in.email,
        )

        if existing:
            raise DuplicateResourceException(
                "Organization with this email already exists."
            )

        return organization.create(
            db=db,
            obj_in=organization_in.model_dump(),
        )

    def get_organization(
        self,
        db: Session,
        organization_id: int,
    ) -> Organization:

        db_org = organization.get(
            db,
            organization_id,
        )

        if not db_org:
            raise NotFoundException(
               "Organization not found."
            )

        return db_org

    def get_organizations(
        self,
        db: Session,
    ) -> list[Organization]:

        return organization.get_multi(db)

    def update_organization(
        self,
        db: Session,
        organization_id: int,
        organization_in: OrganizationUpdate,
    ) -> Organization:

        db_org = self.get_organization(
            db,
            organization_id,
        )

        if (
            organization_in.email
            and organization_in.email != db_org.email
        ):
            existing = organization.get_by_email(
                db,
                organization_in.email,
            )

            if existing:
                raise DuplicateResourceException(
                    "Organization with this email already exists."
                )

        return organization.update(
            db=db,
            db_obj=db_org,
            obj_in=organization_in.model_dump(
                exclude_unset=True
            ),
        )

    def delete_organization(
        self,
        db: Session,
        organization_id: int,
    ) -> None:

        db_org = self.get_organization(
            db,
            organization_id,
        )

        organization.remove(
            db,
            db_obj=db_org,
        )


organization_service = OrganizationService()
