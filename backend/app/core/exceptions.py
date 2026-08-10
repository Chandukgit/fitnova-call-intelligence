class AppException(Exception):
    """
    Base application exception.
    """

    pass


class NotFoundException(AppException):
    pass


class DuplicateResourceException(AppException):
    pass


class ValidationException(AppException):
    pass


class UnauthorizedException(AppException):
    pass


class ForbiddenException(AppException):
    pass