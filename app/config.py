# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # defaults used only if env vars are missing
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/resumes"
    FLASK_ENV: str = "production"
    SECRET_KEY: str = "change-me"

    # load from environment (and .env locally)
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",    # read exact names
        extra="ignore"
    )

def get_settings() -> Settings:
    return Settings()
