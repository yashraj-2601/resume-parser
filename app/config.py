import os
from pydantic import BaseModel

class Settings(BaseModel):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/resumes")

def get_settings() -> Settings:
    return Settings()
