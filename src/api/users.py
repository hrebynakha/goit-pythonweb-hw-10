from fastapi import APIRouter, Depends, Request

from slowapi import Limiter
from slowapi.util import get_remote_address

from src.models.users import User as UserModel
from src.schemas.users import User
from src.schemas.auth import UnauthorizedResponse
from src.dependencies.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


limiter = Limiter(key_func=get_remote_address)


@router.get(
    "/me",
    response_model=User,
    description="No more than 5 requests per minute",
    responses={
        401: {"model": UnauthorizedResponse, "description": "Unauthorized"},
    },
)
@limiter.limit("5/minute")
async def me(
    request: Request, user: UserModel = Depends(get_current_user)
):  # pylint: disable=unused-argument
    return user
