from sqlalchemy.orm import Session

from app.crud.feedback import feedback
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate
from app.services.base import ServiceBase


class FeedbackService(ServiceBase[Feedback]):

    def __init__(self):
        super().__init__(feedback)

    def create_feedback(
        self,
        db: Session,
        feedback_in: FeedbackCreate,
    ):
        return self.crud.create(
            db=db,
            obj_in=feedback_in.model_dump(),
        )


feedback_service = FeedbackService()
