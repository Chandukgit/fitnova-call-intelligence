from sqlalchemy.orm import Session

from app.crud.issue_tag import issue_tag
from app.models.issue_tag import IssueTag
from app.schemas.issue_tag import IssueTagCreate
from app.services.base import ServiceBase


class IssueTagService(ServiceBase[IssueTag]):

    def __init__(self):
        super().__init__(issue_tag)

    def create_issue_tag(
        self,
        db: Session,
        issue_tag_in: IssueTagCreate,
    ):
        return self.crud.create(
            db=db,
            obj_in=issue_tag_in.model_dump(),
        )


issue_tag_service = IssueTagService()