from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.team import Team


class CRUDTeam(CRUDBase[Team]):

    def get_by_organization(
        self,
        db: Session,
        organization_id: int,
    ) -> list[Team]:

        statement = select(Team).where(
            Team.organization_id == organization_id
        )

        result = db.execute(statement)

        return result.scalars().all()


team = CRUDTeam(Team)