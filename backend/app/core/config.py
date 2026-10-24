from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Prism Workbench"
    app_env: str = "development"
    debug: bool = True
    host: str = "127.0.0.1"
    port: int = 8000
    database_url: str = "sqlite:///./prism.db"

    llm_api_key: Optional[str] = None
    llm_provider: str = "openai-compatible"
    llm_model: str = "gpt-4o-mini"
    llm_base_url: Optional[str] = None

    keycloak_url: Optional[str] = None
    keycloak_realm: Optional[str] = None
    keycloak_client_id: Optional[str] = None
    keycloak_client_secret: Optional[str] = None

    demo_mode: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
