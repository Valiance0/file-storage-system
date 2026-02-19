from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    FILE_STORAGE_PATH: str
    HOST: str
    PORT: int

    APP_NAME: str
    FILE_READING_CHUNK_SIZE: int

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings() # pyright: ignore[reportCallIssue]