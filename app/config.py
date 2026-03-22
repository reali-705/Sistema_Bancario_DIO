"""Módulo de Configuração das Variáveis de Ambiente."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Gerencia as variáveis de ambiente e configurações globais.

    Utiliza o pydantic-settings para validar os tipos de dados em tempo
    de inicialização, garantindo falha rápida caso o .env esteja ausente ou mal
    configurado.
    """

    DATABASE_URL: str = Field(default="sqlite+aiosqlite:///./database.db")
    ALGORITHM: str = Field(default="HS256")
    TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    SECRET_KEY: str = Field(default=...)

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )


settings = Settings()
