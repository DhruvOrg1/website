"""Application configuration, loaded from environment variables / `.env`."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Store Inventory API"
    debug: bool = True

    # Default to a local SQLite file so the app runs with zero setup.
    database_url: str = "sqlite:///./inventory.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
