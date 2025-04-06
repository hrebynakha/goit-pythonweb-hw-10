from fastapi import status
from src.exceptions.core import AppHttpError


class AuthError(AppHttpError):
    def __init__(
        self,
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail: str = "Could not validate credentials",
    ):
        super().__init__(status_code, detail, {"WWW-Authenticate": "Bearer"})


class RegistrationError(AppHttpError):
    def __init__(
        self,
        status_code=status.HTTP_409_CONFLICT,
        detail: str = "User with this username alredy exist",
        headers: dict = None,
    ):
        super().__init__(status_code, detail, headers)
