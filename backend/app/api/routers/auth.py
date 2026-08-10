from sqlalchemy.orm import Session

from fastapi import (
    APIRouter,
    Depends,
)

from app.api.dependencies import get_db
from app.schemas.auth import (
    LoginRequest,
    Token,
)
from app.services.auth import auth_service


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=Token,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    return auth_service.login(
        db=db,
        email=request.email,
        password=request.password,
    )