from sqlalchemy.orm import Session

from app.crud.advisor import advisor
from app.models.advisor import Advisor
from app.schemas.advisor import AdvisorCreate
from app.services.base import ServiceBase


class AdvisorService(ServiceBase[Advisor]):

    def __init__(self):
        super().__init__(advisor)

    def create_advisor(
        self,
        db: Session,
        advisor_in: AdvisorCreate,
    ):
        return self.crud.create(
            db=db,
            obj_in=advisor_in.model_dump(),
        )


advisor_service = AdvisorService()