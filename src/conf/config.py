"""Configuration app file"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Class for keeping app settings and environment configuration."""

    def __init__(self):
        self.debug = bool(os.getenv("DEBUG", "True"))
        self.db_driver = os.getenv("DB_DRIVER", "postgresql+asyncpg")
        if "postgresql" in self.db_driver:
            self.db_user = os.getenv("DB_USER", "postgres")
            self._db_password = os.getenv("POSTGRES_PASSWORD", "password")
        self.db_host = os.getenv("DB_HOST", "db")
        self.db_port = int(os.getenv("DB_PORT", "5432"))
        self.db_name = os.getenv("DB_NAME", "contacts_app")

    def get_db_url(self):
        """Returns the full database URL"""
        cred = f"{self.db_user}:{self._db_password}"
        return f"{self.db_driver}://{cred}@{self.db_host}:{self.db_port}/{self.db_name}"


config = Config()
