from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    db_name: str = Field(..., alias="POSTGRES_DB")
    db_user: str = Field(..., alias="POSTGRES_USER")
    db_password: str = Field(..., alias="POSTGRES_PASSWORD")
    db_host: str = Field(default="postgres", alias="POSTGRES_HOST")
    db_port: int = Field(default=5432, alias="POSTGRES_PORT")

    api_key: str = Field(..., alias="API_KEY")
    rabbit_url: str = Field(..., alias="RABBIT_URL")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )

    @property
    def database_url(self) -> str:

        return (
            f"postgresql+asyncpg://"
            f"{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def sync_database_url(self) -> str:

        return (
            f"postgresql://"
            f"{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()
