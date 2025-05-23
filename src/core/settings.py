from pydantic_settings import BaseSettings, SettingsConfigDict
import sys


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env.test" if "pytest" in sys.argv else ".env",
        env_file_encoding="utf-8",
    )

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/postgres"
    MB_URL: str = "http://localhost:8001"


settings = Settings()
