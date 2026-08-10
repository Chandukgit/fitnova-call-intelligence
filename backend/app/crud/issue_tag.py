from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.issue_tag import IssueTag


class CRUDIssueTag(CRUDBase[IssueTag]):

    def get_by_analysis(
        self,
        db: Session,
        analysis_id: int,
    ) -> list[IssueTag]:

        statement = select(IssueTag).where(
            IssueTag.analysis_id == analysis_id
        )

        result = db.execute(statement)

        return result.scalars().all()


issue_tag = CRUDIssueTag(IssueTag)