from sqlalchemy.orm import Session

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from app.api.dependencies import get_db
from app.schemas.feedback import (
    FeedbackCreate,
    FeedbackUpdate,
    FeedbackResponse,
)
from app.services.feedback import feedback_service


router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"],
)


@router.post(
    "",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db),
):
    return feedback_service.create_feedback(
        db=db,
        feedback_in=feedback,
    )


@router.get(
    "",
    response_model=list[FeedbackResponse],
)
def get_feedbacks(
    db: Session = Depends(get_db),
):
    return feedback_service.get_all(db)


@router.get(
    "/{feedback_id}",
    response_model=FeedbackResponse,
)
def get_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
):
    return feedback_service.get(
        db,
        feedback_id,
    )


@router.put(
    "/{feedback_id}",
    response_model=FeedbackResponse,
)
def update_feedback(
    feedback_id: int,
    feedback: FeedbackUpdate,
    db: Session = Depends(get_db),
):
    return feedback_service.update(
        db,
        feedback_id,
        feedback,
    )


@router.delete(
    "/{feedback_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
):
    feedback_service.delete(
        db,
        feedback_id,
    )
