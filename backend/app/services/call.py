from sqlalchemy.orm import Session

from app.crud.call import call
from app.models.call import Call
from app.schemas.call import (
    CallCreate,
)

from app.services.base import ServiceBase


class CallService(ServiceBase[Call]):

    def __init__(self):
        super().__init__(call)

    def create_call(
        self,
        db: Session,
        call_in: CallCreate,
    ) -> Call:

        return self.crud.create(
            db=db,
            obj_in=call_in.model_dump(),
        )


call_service = CallService()