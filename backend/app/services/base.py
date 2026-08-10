from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from app.database.base import Base
from app.core.exceptions import NotFoundException

ModelType = TypeVar(
    "ModelType",
    bound=Base,
)


class ServiceBase(Generic[ModelType]):

    def __init__(
        self,
        crud,
    ):
        self.crud = crud

    def get(
        self,
        db: Session,
        id: int,
    ) -> ModelType:

        obj = self.crud.get(
            db,
            id,
        )

        if not obj:
            raise NotFoundException(
                "Object not found."
            )

        return obj

    def get_all(
        self,
        db: Session,
    ):

        return self.crud.get_multi(db)

    def update(
        self,
        db: Session,
        id: int,
        obj_in,
    ):

        db_obj = self.get(
            db,
            id,
        )

        data = (
            obj_in.model_dump(exclude_unset=True)
            if hasattr(obj_in, "model_dump")
            else obj_in
        )

        return self.crud.update(
            db,
            db_obj,
            data,
        )

    def delete(
        self,
        db: Session,
        id: int,
    ):

        db_obj = self.get(
            db,
            id,
        )

        self.crud.remove(
            db,
            db_obj,
        )
