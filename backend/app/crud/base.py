from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.base import Base

ModelType = TypeVar(
    "ModelType",
    bound=Base,
)


class CRUDBase(Generic[ModelType]):

    def __init__(
        self,
        model: type[ModelType],
    ):
        self.model = model

    def create(
        self,
        db: Session,
        obj_in: dict,
    ) -> ModelType:

        db_obj = self.model(**obj_in)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def get(
        self,
        db: Session,
        id: int,
    ) -> ModelType | None:

        statement = select(self.model).where(
            self.model.id == id
        )

        result = db.execute(statement)

        return result.scalar_one_or_none()

    def get_multi(
        self,
        db: Session,
    ) -> list[ModelType]:

        statement = select(self.model)

        result = db.execute(statement)

        return result.scalars().all()

    def update(
        self,
        db: Session,
        db_obj: ModelType,
        obj_in: dict,
    ) -> ModelType:

        for field, value in obj_in.items():
            setattr(db_obj, field, value)

        db.commit()
        db.refresh(db_obj)

        return db_obj

    def remove(
        self,
        db: Session,
        db_obj: ModelType,
    ) -> None:

        db.delete(db_obj)
        db.commit()