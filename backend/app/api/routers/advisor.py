from sqlalchemy.orm import Session

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from app.api.dependencies import get_db
from app.schemas.advisor import (
    AdvisorCreate,
    AdvisorUpdate,
    AdvisorResponse,
)
from app.services.advisor import advisor_service


router = APIRouter(
    prefix="/advisors",
    tags=["Advisors"],
)


@router.post(
    "",
    response_model=AdvisorResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_advisor(
    advisor: AdvisorCreate,
    db: Session = Depends(get_db),
):
    return advisor_service.create_advisor(
        db=db,
        advisor_in=advisor,
    )


@router.get(
    "",
    response_model=list[AdvisorResponse],
)
def get_advisors(
    db: Session = Depends(get_db),
):
    return advisor_service.get_all(db)


@router.get(
    "/{advisor_id}",
    response_model=AdvisorResponse,
)
def get_advisor(
    advisor_id: int,
    db: Session = Depends(get_db),
):
    return advisor_service.get(
        db,
        advisor_id,
    )


@router.put(
    "/{advisor_id}",
    response_model=AdvisorResponse,
)
def update_advisor(
    advisor_id: int,
    advisor: AdvisorUpdate,
    db: Session = Depends(get_db),
):
    return advisor_service.update(
        db,
        advisor_id,
        advisor,
    )


@router.delete(
    "/{advisor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_advisor(
    advisor_id: int,
    db: Session = Depends(get_db),
):
    advisor_service.delete(
        db,
        advisor_id,
    )