from pathlib import Path
import os

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = os.getenv("ENV_FILE", ".env.local")


class Settings(BaseSettings):
    app_name: str = "KnowledgeHub API"
    app_version: str = "0.1.0"

    debug: bool = False

    database_url: str
    secret_key: str
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=Path(ENV_FILE),
        case_sensitive=False,
    )


settings = Settings()