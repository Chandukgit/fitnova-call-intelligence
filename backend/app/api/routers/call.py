from sqlalchemy.orm import Session

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from app.api.dependencies import get_db
from app.schemas.call import (
    CallCreate,
    CallUpdate,
    CallResponse,
)
from app.services.call import call_service


router = APIRouter(
    prefix="/calls",
    tags=["Calls"],
)


@router.post(
    "",
    response_model=CallResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_call(
    call: CallCreate,
    db: Session = Depends(get_db),
):
    return call_service.create_call(
        db=db,
        call_in=call,
    )


@router.get(
    "",
    response_model=list[CallResponse],
)
def get_calls(
    db: Session = Depends(get_db),
):
    return call_service.get_all(db)


@router.get(
    "/{call_id}",
    response_model=CallResponse,
)
def get_call(
    call_id: int,
    db: Session = Depends(get_db),
):
    return call_service.get(
        db,
        call_id,
    )


@router.put(
    "/{call_id}",
    response_model=CallResponse,
)
def update_call(
    call_id: int,
    call: CallUpdate,
    db: Session = Depends(get_db),
):
    return call_service.update(
        db,
        call_id,
        call,
    )


@router.delete(
    "/{call_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_call(
    call_id: int,
    db: Session = Depends(get_db),
):
    call_service.delete(
        db,
        call_id,
    )