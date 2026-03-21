"""Módulo de Configuração das Variáveis de Ambiente."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Abstrai as configurações do .env para a aplicação."""

    DATABASE_URL: str = Field(default="sqlite+aiosqlite:///./database.db")

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )


settings = Settings()
