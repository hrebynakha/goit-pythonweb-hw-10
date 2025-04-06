"""Configuration app file"""

from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """Class for keeping app settings and environment configuration."""

    DEBUG: bool
    DB_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_JWT_EXPIRATION_SECONDS: int = 900  # 15 min
    REFRESH_JWT_EXPIRATION_SECONDS: int = 604800  # 7 days
    model_config = ConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


settings = Settings()
