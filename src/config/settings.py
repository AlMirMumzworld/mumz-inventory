from typing import Literal
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""

    API_PREFIX: str = "/api/v1/inventory"
    ENV: str = "DEV"
    TITLE: str = "Mumz Inventory"
    DESCRIPTION: str = """
    API documentation for Mumz Inventory system.
    """
    SECRET_KEY: str = "1234567890"
    DB_URL: str = "sqlite:///./dev.db"

    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    def is_env(self, env: Literal["DEV", "STAG", "PROD"]):
        """return whether the app is running on a specific environment"""

        return str(self.ENV).upper().startswith(env)


@lru_cache
def get_settings() -> Settings:
    """Return application settings"""
    return Settings()
