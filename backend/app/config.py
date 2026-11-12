"""Application configuration, loaded from environment variables / `.env`."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Store Inventory API"
    debug: bool = True

    # Default to a local SQLite file so the app runs with zero setup.
    database_url: str = "sqlite:///./inventory.db"

    # Auth / JWT. Override secret_key in .env for anything beyond local dev.
    secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
