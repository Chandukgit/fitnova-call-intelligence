from sqlalchemy.orm import Session

from app.core.exceptions import ValidationException
from app.core.security import (
    verify_password,
    create_access_token,
)
from app.crud.user import user


class AuthService:

    def login(
        self,
        db: Session,
        email: str,
        password: str,
    ):

        db_user = user.get_by_email(
            db,
            email,
        )

        if not db_user:
            raise ValidationException(
                "Invalid email or password."
            )

        if not db_user.is_active:
            raise ValidationException(
                "Invalid email or password."
            )

        if not verify_password(
            password,
            db_user.password_hash,
        ):
            raise ValidationException(
                "Invalid email or password."
            )

        access_token = create_access_token(
            subject=db_user.id,
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }


auth_service = AuthService()
