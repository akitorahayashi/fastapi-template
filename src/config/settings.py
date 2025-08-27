from functools import lru_cache

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Manages application settings loaded from environment variables.
    """

    # Database settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB_NAME: str
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    # API server settings
    HOST_BIND_IP: str = "127.0.0.1"
    HOST_PORT: int = 8000

    @property
    def database_url(self) -> str:
        """
        Constructs the database connection URL from individual components.
        """
        return str(
            PostgresDsn.build(
                scheme="postgresql+psycopg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB_NAME,
            )
        )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
