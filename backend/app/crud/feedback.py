from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.feedback import Feedback


class CRUDFeedback(CRUDBase[Feedback]):

    def get_by_analysis(
        self,
        db: Session,
        analysis_id: int,
    ) -> list[Feedback]:

        statement = select(Feedback).where(
            Feedback.analysis_id == analysis_id
        )

        result = db.execute(statement)

        return result.scalars().all()


feedback = CRUDFeedback(Feedback)