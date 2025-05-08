from pydantic_settings import BaseSettings

from pathlib import Path

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:password@db:5432/dbname"
    CLICKUP_API_URL: str = "https://api.clickup.com/api/v2"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    class Config:
        env_file = ".env"

settings = Settings()