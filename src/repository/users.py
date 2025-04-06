from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import User
from src.schemas.users import UserCreate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_user_by_id(self, user_id: int) -> User | None:
        query = select(User).filter_by(id=user_id)
        user = await self.db.execute(query)
        return user.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        query = select(User).filter_by(username=username)
        user = await self.db.execute(query)
        return user.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        query = select(User).filter_by(email=email)
        user = await self.db.execute(query)
        return user.scalar_one_or_none()

    async def create_user(self, body: UserCreate, avatar: str = None) -> User:
        user = User(
            **body.model_dump(exclude_unset=True, exclude={"password"}),
            hashed_password=body.password,
            avatar=avatar,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_user_refresh_token(self, username: str, token: str) -> User:
        user = self.get_user_by_username(username)
        user.refresh_token = token
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_user_by_username_and_token(
        self, username: str, token: str
    ) -> User | None:
        query = select(User).filter(
            User.username == username, User.refresh_token == token
        )
        user = await self.db.execute(query)
        return user.scalar_one_or_none()
