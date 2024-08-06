from functools import lru_cache

from pydantic import AnyHttpUrl, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки проекта."""

    model_config = SettingsConfigDict(env_prefix="ED_", case_sensitive=True)

    # Project
    API_V1_STR: str = "/api/v1"
    SERVER_NAME: str
    SERVER_HOSTS: str | list[AnyHttpUrl]
    PROJECT_NAME: str
    DEBUG: bool = Field(False)
    PROJECT_BASE_URL: str

    @field_validator("SERVER_HOSTS")
    def _assemble_server_hosts(cls, server_hosts: str | list[str]) -> list[str]:
        if isinstance(server_hosts, str):
            return [item.strip() for item in server_hosts.split(",")]
        return server_hosts


@lru_cache
def get_settings() -> "Settings":
    return Settings()
