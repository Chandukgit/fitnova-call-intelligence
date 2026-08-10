from sqlalchemy.orm import Session

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from app.api.dependencies import get_db
from app.core.auth import get_current_user
from app.core.permissions import require_roles
from app.core.enums import UserRole

from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
)

from app.services.user import user_service


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_current_user_profile(
    current_user=Depends(get_current_user),
):
    return current_user


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    return user_service.create_user(
        db=db,
        user_in=user,
    )


@router.get(
    "",
    response_model=list[UserResponse],
)
def get_users(
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
    db: Session = Depends(get_db),
):
    return user_service.get_all(db)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return user_service.get(
        db,
        user_id,
    )


@router.put(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user(
    user_id: int,
    user: UserUpdate,
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
    db: Session = Depends(get_db),
):
    return user_service.update(
        db,
        user_id,
        user,
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    user_id: int,
    current_user=Depends(
        require_roles(UserRole.ADMIN)
    ),
    db: Session = Depends(get_db),
):
    user_service.delete(
        db,
        user_id,
    )
