"""Módulo Orquestrador de Rotas da API."""

from fastapi import APIRouter

from app.routers import usuarios
from app.schemas.docs import RESPOSTA_404, RESPOSTA_500

api_router = APIRouter(prefix="/api", responses={**RESPOSTA_404, **RESPOSTA_500})


v1_router = APIRouter(prefix="/v1")

v1_router.include_router(usuarios.router, prefix="/usuarios", tags=["Usuários"])


api_router.include_router(v1_router)
