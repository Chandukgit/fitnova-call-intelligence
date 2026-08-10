from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.exceptions import UnauthorizedException
from app.core.security import decode_access_token
from app.crud.user import user


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):

    try:

        payload = decode_access_token(token)

        user_id = int(payload["sub"])

    except Exception:

        raise UnauthorizedException(
            "Invalid authentication credentials."
        )

    db_user = user.get(
        db,
        user_id,
    )

    if db_user is None:

        raise UnauthorizedException(
            "User not found."
        )

    if not db_user.is_active:
        raise UnauthorizedException(
            "Inactive user."
        )

    return db_user
