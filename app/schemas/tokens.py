"""Módulo de Esquemas para Tokens JWT."""

from pydantic import BaseModel


class JWToken(BaseModel):
    """Esquema para o token de acesso JWT."""

    access_token: str
    token_type: str


class DadosToken(BaseModel):
    """Esquema de dados (payload) para criação do token JWT."""

    sub: int
    email: str
    nome: str
