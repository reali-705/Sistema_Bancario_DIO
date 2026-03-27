"""Módulo de Rotas da API."""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Usuario
from app.schemas import UsuarioCreate, UsuarioResponse
from app.security import gerar_senha_hash

router_v1 = APIRouter(
    tags=["Usuários"],
    prefix="/usuarios",
    responses={status.HTTP_404_NOT_FOUND: {"detalhe": "Nao encontrado"}},
)


@router_v1.post(
    path="",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
)
async def criar_usuario(
    usuario: UsuarioCreate, db: Annotated[AsyncSession, Depends(get_db)]
) -> UsuarioResponse:
    """Rota para criar um novo usuário."""
    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=gerar_senha_hash(usuario.senha),
    )
    db.add(novo_usuario)

    await db.commit()
    await db.refresh(novo_usuario)
    return UsuarioResponse.model_validate(novo_usuario)
