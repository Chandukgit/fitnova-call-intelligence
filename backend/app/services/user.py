from sqlalchemy.orm import Session

from app.crud.user import user
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.base import ServiceBase

from app.core.exceptions import DuplicateResourceException
from app.core.security import get_password_hash


class UserService(ServiceBase[User]):

    def __init__(self):
        super().__init__(user)

    def create_user(
        self,
        db: Session,
        user_in: UserCreate,
    ):

        if self.crud.get_by_email(
            db,
            user_in.email,
        ):
            raise DuplicateResourceException(
                "Email already exists."
            )

        if self.crud.get_by_username(
            db,
            user_in.username,
        ):
            raise DuplicateResourceException(
                "Username already exists."
            )

        data = user_in.model_dump()

        data["password_hash"] = get_password_hash(
            data.pop("password")
        )

        return self.crud.create(
            db=db,
            obj_in=data,
        )

    def update(
        self,
        db: Session,
        id: int,
        obj_in: UserUpdate,
    ) -> User:
        data = obj_in.model_dump(exclude_unset=True)

        if "password" in data:
            data["password_hash"] = get_password_hash(data.pop("password"))

        return super().update(db, id, data)


user_service = UserService()
