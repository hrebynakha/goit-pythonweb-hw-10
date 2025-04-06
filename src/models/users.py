from datetime import datetime
from sqlalchemy import Integer, String, func
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql.sqltypes import DateTime

from src.database.basic import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(40), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=func.now()  # pylint: disable=not-callable
    )
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
