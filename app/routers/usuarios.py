"""Módulo de Rotas da API."""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import gerar_senha_hash
from app.models import Usuario
from app.schemas.docs import RESPOSTA_409
from app.schemas.usuarios import UsuarioCreate, UsuarioResponse

router = APIRouter()


@router.post(
    path="",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    responses={**RESPOSTA_409},
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


@router.get(
    path="",
    response_model=list[UsuarioResponse],
    status_code=status.HTTP_200_OK,
)
async def listar_usuarios(
    db: Annotated[AsyncSession, Depends(get_db)],
    nome: str | None = None,
    email: str | None = None,
    ativo: bool | None = None,
) -> list[UsuarioResponse]:
    """Rota para listar todos os usuários.

    Possui filtro dinamicos/opicionais para nome, email e ativo.
    """
    query = select(Usuario)

    # Contrutor de filtros
    if nome:
        query = query.where(Usuario.nome.ilike(f"%{nome}%"))
    if email:
        query = query.where(Usuario.email.ilike(f"%{email}%"))
    if ativo is not None:
        query = query.where(Usuario.ativo == ativo)

    result = await db.execute(query)
    usuarios = result.scalars().all()
    return list(map(UsuarioResponse.model_validate, usuarios))
