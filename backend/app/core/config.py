from pathlib import Path
import os
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = os.getenv("ENV_FILE", ".env.local")


class Settings(BaseSettings):
    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------

    app_name: str = "KnowledgeHub API"
    app_version: str = "0.1.0"

    debug: bool = False

    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------

    DATABASE_URL: str

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 14

    REFRESH_TOKEN_COOKIE_NAME: str = "refresh_token"
    REFRESH_TOKEN_COOKIE_SECURE: bool = True
    REFRESH_TOKEN_COOKIE_SAMESITE: Literal["lax", "strict", "none"] = "none"

    ALGORITHM: str = "HS256"

    # ------------------------------------------------------------------
    # File Storage
    # ------------------------------------------------------------------

    UPLOAD_DIR: str = Field(
        default="uploads",
        description="Directory for uploaded files.",
    )

    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10 MB

    STORAGE_PROVIDER: str = "local"
    S3_BUCKET_NAME: str = ""
    S3_REGION: str = "ap-southeast-2"
    S3_PREFIX: str = "documents"

    # ------------------------------------------------------------------
    # Chunking
    # ------------------------------------------------------------------

    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP_SENTENCES: int = 1

    # ------------------------------------------------------------------
    # Embedding
    # ------------------------------------------------------------------

    EMBEDDING_PROVIDER: str = "local"
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"

    # ------------------------------------------------------------------
    # Chat
    # ------------------------------------------------------------------

    LLM_PROVIDER: str = "ollama"
    LLM_MODEL: str = "mistral:latest"
    AWS_REGION: str = "ap-southeast-2"

    OLLAMA_HOST: str = "http://localhost:11434"

    RETRIEVAL_LIMIT: int = 5
    RETRIEVAL_THRESHOLD: float = 0.0

    # ------------------------------------------------------------------
    # Settings
    # ------------------------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=Path(ENV_FILE),
        case_sensitive=False,
    )


settings = Settings()