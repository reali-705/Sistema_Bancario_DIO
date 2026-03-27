"""Módulo de Configuração do Banco de Dados."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models import Base

async_engine = create_async_engine(
    url=settings.DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Injeta a sessão do banco de dados nas rotas do FastAPI.

    Atua como um gerenciador de contexto assíncrono (Generator).
    A sessão é entregue à rota via `yield` e fechada automaticamente
    após o término da requisição, prevenindo vazamento de conexões.

    Yields:
        AsyncSession: Sessão ativa com o banco de dados (aiosqlite).
    """
    async with AsyncSessionLocal() as db:
        yield db


async def init_db() -> None:
    """Executa os comandos DDL para criação das tabelas.

    Deve ser chamada na inicialização da aplicação para garantir que o
    esquema (schema) físico do SQLite esteja sincronizado com os metadados do SQLModel.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
