from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.call import Call


class CRUDCall(CRUDBase[Call]):

    def get_by_advisor(
        self,
        db: Session,
        advisor_id: int,
    ) -> list[Call]:

        statement = select(Call).where(
            Call.advisor_id == advisor_id
        )

        result = db.execute(statement)

        return result.scalars().all()

    def get_by_customer(
        self,
        db: Session,
        customer_id: int,
    ) -> list[Call]:

        statement = select(Call).where(
            Call.customer_id == customer_id
        )

        result = db.execute(statement)

        return result.scalars().all()


call = CRUDCall(Call)
