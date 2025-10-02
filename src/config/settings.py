from functools import lru_cache

from pydantic import computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    This class loads configuration values used throughout the application from
    environment variables. Since Docker Compose automatically loads the .env file
    from the project root, there's no need to explicitly specify the file path.
    """

    USE_SQLITE: bool = True

    # PostgreSQL settings
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = ""

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        if self.USE_SQLITE:
            return "sqlite:///./test_db.sqlite3"
        else:
            return f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
