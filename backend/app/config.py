"""Application settings configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Interview Buddy API"
    environment: str = "development"
    debug: bool = True

    database_url: str = (
        "postgresql+asyncpg://postgres:postgres@db:5432/interview_buddy"
    )

    secret_key: str = "change-me-secret"
    access_token_expire_minutes: int = 90
    auth_algorithm: str = "HS256"

    frontend_origin: str = "http://localhost:3000"
    root_path: str = ""

    first_superuser_email: str | None = None
    first_superuser_password: str | None = None


settings = Settings()  # type: ignore[arg-type]
