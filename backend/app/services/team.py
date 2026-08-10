from app.crud.team import team
from app.models.team import Team
from app.schemas.team import TeamCreate
from app.services.base import ServiceBase


class TeamService(ServiceBase[Team]):

    def __init__(self):
        super().__init__(team)

    def create_team(
        self,
        db,
        team_in: TeamCreate,
    ):
        return self.crud.create(
            db=db,
            obj_in=team_in.model_dump(),
        )


team_service = TeamService()