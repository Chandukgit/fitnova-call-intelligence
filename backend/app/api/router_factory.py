from typing import Type

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db


def create_crud_router(
    service,
    create_schema: Type,
    update_schema: Type,
    response_schema: Type,
    prefix: str,
    tags: list[str],
):

    router = APIRouter(
        prefix=prefix,
        tags=tags,
    )

    @router.post(
        "",
        response_model=response_schema,
        status_code=status.HTTP_201_CREATED,
    )
    def create(
        obj: create_schema,
        db: Session = Depends(get_db),
    ):
        return service.create(db, obj)

    @router.get(
        "",
        response_model=list[response_schema],
    )
    def get_all(
        db: Session = Depends(get_db),
    ):
        return service.get_all(db)

    @router.get(
        "/{id}",
        response_model=response_schema,
    )
    def get(
        id: int,
        db: Session = Depends(get_db),
    ):
        return service.get(db, id)

    @router.put(
        "/{id}",
        response_model=response_schema,
    )
    def update(
        id: int,
        obj: update_schema,
        db: Session = Depends(get_db),
    ):
        return service.update(db, id, obj)

    @router.delete(
        "/{id}",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    def delete(
        id: int,
        db: Session = Depends(get_db),
    ):
        service.delete(db, id)

    return router