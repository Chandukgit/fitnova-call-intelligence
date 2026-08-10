from sqlalchemy.orm import Session

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from app.api.dependencies import get_db
from app.schemas.transcript import (
    TranscriptCreate,
    TranscriptUpdate,
    TranscriptResponse,
)
from app.services.transcript import transcript_service


router = APIRouter(
    prefix="/transcripts",
    tags=["Transcripts"],
)


@router.post(
    "",
    response_model=TranscriptResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transcript(
    transcript: TranscriptCreate,
    db: Session = Depends(get_db),
):
    return transcript_service.create_transcript(
        db=db,
        transcript_in=transcript,
    )


@router.get(
    "",
    response_model=list[TranscriptResponse],
)
def get_transcripts(
    db: Session = Depends(get_db),
):
    return transcript_service.get_all(db)


@router.get(
    "/{transcript_id}",
    response_model=TranscriptResponse,
)
def get_transcript(
    transcript_id: int,
    db: Session = Depends(get_db),
):
    return transcript_service.get(
        db,
        transcript_id,
    )


@router.put(
    "/{transcript_id}",
    response_model=TranscriptResponse,
)
def update_transcript(
    transcript_id: int,
    transcript: TranscriptUpdate,
    db: Session = Depends(get_db),
):
    return transcript_service.update(
        db,
        transcript_id,
        transcript,
    )


@router.delete(
    "/{transcript_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_transcript(
    transcript_id: int,
    db: Session = Depends(get_db),
):
    transcript_service.delete(
        db,
        transcript_id,
    )