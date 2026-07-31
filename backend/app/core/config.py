from pathlib import Path
import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = os.getenv("ENV_FILE", ".env.local")


class Settings(BaseSettings):
    app_name: str = "KnowledgeHub API"
    app_version: str = "0.1.0"

    debug: bool = False

    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    UPLOAD_DIR: str = Field(
        default="uploads",
        description="Directory or storing uploaded files.",
    )

    model_config = SettingsConfigDict(
        env_file=Path(ENV_FILE),
        case_sensitive=False,
    )


settings = Settings()
