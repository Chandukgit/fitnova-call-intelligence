from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.advisor import Advisor


class CRUDAdvisor(CRUDBase[Advisor]):

    def get_by_employee_id(
        self,
        db: Session,
        employee_id: str,
    ) -> Advisor | None:

        statement = select(Advisor).where(
            Advisor.employee_id == employee_id
        )

        result = db.execute(statement)

        return result.scalar_one_or_none()

    def get_by_email(
        self,
        db: Session,
        email: str,
    ) -> Advisor | None:

        statement = select(Advisor).where(
            Advisor.email == email
        )

        result = db.execute(statement)

        return result.scalar_one_or_none()

    def get_by_team(
        self,
        db: Session,
        team_id: int,
    ) -> list[Advisor]:

        statement = select(Advisor).where(
            Advisor.team_id == team_id
        )

        result = db.execute(statement)

        return result.scalars().all()


advisor = CRUDAdvisor(Advisor)