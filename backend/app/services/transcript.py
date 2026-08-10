from sqlalchemy.orm import Session

from app.crud.transcript import transcript
from app.models.transcript import Transcript
from app.schemas.transcript import TranscriptCreate
from app.services.base import ServiceBase


class TranscriptService(ServiceBase[Transcript]):

    def __init__(self):
        super().__init__(transcript)

    def create_transcript(
        self,
        db: Session,
        transcript_in: TranscriptCreate,
    ):
        return self.crud.create(
            db=db,
            obj_in=transcript_in.model_dump(),
        )

    def get_by_call_id(
        self,
        db: Session,
        call_id: int,
    ) -> Transcript | None:

        return (
            db.query(Transcript)
            .filter(
                Transcript.call_id == call_id
            )
            .first()
        )


transcript_service = TranscriptService()