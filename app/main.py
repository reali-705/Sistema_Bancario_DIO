"""Módulo de Exceções Personalizadas para a API."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.api import api_router
from app.core.database import init_db
from app.core.exceptions import carregar_excecoes_personalizadas


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Gerenciador de contexto para o ciclo de vida da aplicação."""
    print("Inicializando a aplicação...")
    await init_db()
    yield
    print("Finalizando a aplicação...")


app = FastAPI(
    title="Sistema Bancário - API",
    description="Projeto didático de uma API assíncrona",
    version="0.1.0",
    lifespan=lifespan,
)

carregar_excecoes_personalizadas(app)


app.include_router(api_router)
