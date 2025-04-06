from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.auth import Token, TokenRefreshRequest
from src.schemas.users import User, UserCreate
from src.services.auth import AuthService, Hash
from src.services.users import UserService
from src.database.db import get_db
from src.exceptions.auth import AuthError, RegistrationError

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)

    if await user_service.get_user_by_email(user_data.email):
        raise RegistrationError("User with this email alredy exist")

    if await user_service.get_user_by_username(user_data.username):
        raise RegistrationError

    user_data.password = Hash().get_password_hash(user_data.password)
    new_user = await user_service.create_user(user_data)

    return new_user


@router.post("/login", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    user = await user_service.get_user_by_username(form_data.username)
    if not user or not Hash().verify_password(form_data.password, user.hashed_password):
        raise AuthError(detail="User or password is incorrect")

    return AuthService(db).geneate_jwt(user.username)


@router.post("/refresh-token", response_model=Token)
async def new_token(request: TokenRefreshRequest, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    user = auth_service.verify_refresh_token(request.refresh_token)
    if user is None:
        raise AuthError(detail="Invalid or expired refresh token")

    return auth_service.update_jwt(user.username, request.refresh_token)
