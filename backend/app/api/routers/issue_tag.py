from sqlalchemy.orm import Session

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from app.api.dependencies import get_db
from app.schemas.issue_tag import (
    IssueTagCreate,
    IssueTagUpdate,
    IssueTagResponse,
)
from app.services.issue_tag import issue_tag_service


router = APIRouter(
    prefix="/issue-tags",
    tags=["Issue Tags"],
)


@router.post(
    "",
    response_model=IssueTagResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_issue_tag(
    issue_tag: IssueTagCreate,
    db: Session = Depends(get_db),
):
    return issue_tag_service.create_issue_tag(
        db=db,
        issue_tag_in=issue_tag,
    )


@router.get(
    "",
    response_model=list[IssueTagResponse],
)
def get_issue_tags(
    db: Session = Depends(get_db),
):
    return issue_tag_service.get_all(db)


@router.get(
    "/{issue_tag_id}",
    response_model=IssueTagResponse,
)
def get_issue_tag(
    issue_tag_id: int,
    db: Session = Depends(get_db),
):
    return issue_tag_service.get(
        db,
        issue_tag_id,
    )


@router.put(
    "/{issue_tag_id}",
    response_model=IssueTagResponse,
)
def update_issue_tag(
    issue_tag_id: int,
    issue_tag: IssueTagUpdate,
    db: Session = Depends(get_db),
):
    return issue_tag_service.update(
        db,
        issue_tag_id,
        issue_tag,
    )


@router.delete(
    "/{issue_tag_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_issue_tag(
    issue_tag_id: int,
    db: Session = Depends(get_db),
):
    issue_tag_service.delete(
        db,
        issue_tag_id,
    )