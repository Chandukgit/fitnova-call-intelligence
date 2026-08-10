from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.customer import Customer


class CRUDCustomer(CRUDBase[Customer]):

    def get_by_phone(
        self,
        db: Session,
        phone: str,
    ) -> Customer | None:

        statement = select(Customer).where(
            Customer.phone == phone
        )

        result = db.execute(statement)

        return result.scalar_one_or_none()

    def get_by_email(
        self,
        db: Session,
        email: str,
    ) -> Customer | None:

        statement = select(Customer).where(
            Customer.email == email
        )

        result = db.execute(statement)

        return result.scalar_one_or_none()


customer = CRUDCustomer(Customer)