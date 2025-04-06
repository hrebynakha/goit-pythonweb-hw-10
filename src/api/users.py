from fastapi import APIRouter, Depends

from src.models.users import User as UserModel
from src.schemas.users import User
from src.dependencies.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=User)
async def me(user: UserModel = Depends(get_current_user)):
    return user
