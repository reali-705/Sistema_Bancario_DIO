"""Módulo de Esquemas de Dados para Validação e Serialização."""

from pydantic import BaseModel, ConfigDict, EmailStr


class JWToken(BaseModel):
    """Esquema para o token de acesso JWT."""

    access_token: str
    token_type: str


class DadosToken(BaseModel):
    """Esquema de dados (payload) para criação do token JWT."""

    sub: int
    email: EmailStr
    nome: str


class UsuarioBase(BaseModel):
    """Esquema base para operações de usuário, compartilhando campos comuns."""

    nome: str
    email: EmailStr


class UsuarioCreate(UsuarioBase):
    """Esquema para criação de usuário, incluindo campos obrigatórios."""

    senha: str


class UsuarioResponse(UsuarioBase):
    """Esquema para resposta de usuário, excluindo campos sensíveis."""

    id: int
    ativo: bool

    # Atributo de configuração para permitir a criação do modelo a partir de objetos ORM
    model_config = ConfigDict(from_attributes=True)
