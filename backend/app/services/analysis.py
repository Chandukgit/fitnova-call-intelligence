from sqlalchemy.orm import Session

from app.crud.analysis import analysis
from app.models.analysis import Analysis
from app.schemas.analysis import AnalysisCreate
from app.services.base import ServiceBase


class AnalysisService(ServiceBase[Analysis]):

    def __init__(self):
        super().__init__(analysis)

    def create_analysis(
        self,
        db: Session,
        analysis_in: AnalysisCreate,
    ):
        return self.crud.create(
            db=db,
            obj_in=analysis_in.model_dump(),
        )


analysis_service = AnalysisService()