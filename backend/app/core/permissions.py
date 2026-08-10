from fastapi import Depends

from app.core.auth import get_current_user
from app.core.enums import UserRole
from app.core.exceptions import ForbiddenException


def require_roles(*roles: UserRole):

    def checker(
        current_user=Depends(get_current_user),
    ):

        if current_user.role not in roles:

            raise ForbiddenException(
                "You do not have permission to perform this action."
            )

        return current_user

    return checker