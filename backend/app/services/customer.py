from sqlalchemy.orm import Session

from app.crud.customer import customer
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate
from app.services.base import ServiceBase


class CustomerService(ServiceBase[Customer]):

    def __init__(self):
        super().__init__(customer)

    def create_customer(
        self,
        db: Session,
        customer_in: CustomerCreate,
    ):
        return self.crud.create(
            db=db,
            obj_in=customer_in.model_dump(),
        )


customer_service = CustomerService()