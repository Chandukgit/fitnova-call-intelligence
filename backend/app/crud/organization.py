from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.organization import Organization


class CRUDOrganization(CRUDBase[Organization]):

    def get_by_email(
        self,
        db: Session,
        email: str,
    ) -> Organization | None:

        statement = select(Organization).where(
            Organization.email == email
        )

        result = db.execute(statement)

        return result.scalar_one_or_none()


organization = CRUDOrganization(Organization)