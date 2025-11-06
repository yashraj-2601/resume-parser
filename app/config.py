# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = (
        "postgresql://resume_parser_db_z266_user:"
        "bgKHprxxf0inbXiKMyUVBugjniu4Il4f@"
        "dpg-d45tinadbo4c7385g5ng-a.singapore-postgres.render.com/"
        "resume_parser_db_z266?sslmode=require"
    )
    FLASK_ENV: str = "production"
    SECRET_KEY: str = "super_secret_key"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="", extra="ignore")

# export an instance so `from app.config import settings` works
settings = Settings()
