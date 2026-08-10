from sqlalchemy.orm import Session

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from app.api.dependencies import get_db
from app.schemas.analysis import (
    AnalysisCreate,
    AnalysisUpdate,
    AnalysisResponse,
)
from app.services.analysis import analysis_service


router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)


@router.post(
    "",
    response_model=AnalysisResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_analysis(
    analysis: AnalysisCreate,
    db: Session = Depends(get_db),
):
    return analysis_service.create_analysis(
        db=db,
        analysis_in=analysis,
    )


@router.get(
    "",
    response_model=list[AnalysisResponse],
)
def get_analysis_list(
    db: Session = Depends(get_db),
):
    return analysis_service.get_all(db)


@router.get(
    "/{analysis_id}",
    response_model=AnalysisResponse,
)
def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
):
    return analysis_service.get(
        db,
        analysis_id,
    )


@router.put(
    "/{analysis_id}",
    response_model=AnalysisResponse,
)
def update_analysis(
    analysis_id: int,
    analysis: AnalysisUpdate,
    db: Session = Depends(get_db),
):
    return analysis_service.update(
        db,
        analysis_id,
        analysis,
    )


@router.delete(
    "/{analysis_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
):
    analysis_service.delete(
        db,
        analysis_id,
    )