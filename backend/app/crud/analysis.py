from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.analysis import Analysis


class CRUDAnalysis(CRUDBase[Analysis]):

    def get_by_call(
        self,
        db: Session,
        call_id: int,
    ) -> Analysis | None:

        statement = select(Analysis).where(
            Analysis.call_id == call_id
        )

        result = db.execute(statement)

        return result.scalar_one_or_none()


analysis = CRUDAnalysis(Analysis)