from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.transcript import Transcript


class CRUDTranscript(CRUDBase[Transcript]):

    def get_by_call(
        self,
        db: Session,
        call_id: int,
    ) -> Transcript | None:

        statement = select(Transcript).where(
            Transcript.call_id == call_id
        )

        result = db.execute(statement)

        return result.scalar_one_or_none()


transcript = CRUDTranscript(Transcript)