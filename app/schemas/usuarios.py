"""Módulo de Esquemas de Dados para Validação e Serialização."""

from pydantic import BaseModel, ConfigDict, Field

# Validação de email usando expressão regular (regex).
REGEX_EMAIL = r"^[\w\.-]+@[\w\.-]+\.\w+$"
REGEX_SENHA = r"^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*()\-_=+\[\]{}|;:,.<>?]).{6,}$"


class UsuarioBase(BaseModel):
    """Esquema base para operações de usuário, compartilhando campos comuns."""

    nome: str = Field(min_length=3, examples=["Nome do Usuario"])
    email: str = Field(pattern=REGEX_EMAIL, examples=["usuario@exemplo.com"])


class UsuarioCreate(UsuarioBase):
    """Esquema para criação de usuário, incluindo campos obrigatórios."""

    senha: str = Field(pattern=REGEX_SENHA, examples=["senha_123"])


class UsuarioResponse(UsuarioBase):
    """Esquema para resposta de usuário, excluindo campos sensíveis."""

    id: int
    ativo: bool

    # Atributo de configuração para permitir a criação do modelo a partir de objetos ORM
    model_config = ConfigDict(from_attributes=True)
