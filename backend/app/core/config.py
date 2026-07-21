from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "KnowledgeHub API"
    app_version: str = "0.1.0"

    debug: bool = False

    database_url: str

    secret_key: str

    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )

settings = Settings()

