"""Módulo de Esquemas de Dados para Validação e Serialização."""

import re

from pydantic import BaseModel, ConfigDict, Field, field_validator

# Validação de email usando expressão regular (regex).
REGEX_EMAIL = r"^[\w\.\-]+@[\w\.\-]+\.\w+$"
REGEX_SENHA = r"""^
    (?=.*[A-Z])
    (?=.*[a-z])
    (?=.*\d)
    (?=.*[\W_])
    .{6,}$
"""


class UsuarioBase(BaseModel):
    """Esquema base para operações de usuário, compartilhando campos comuns."""

    nome: str = Field(min_length=3, examples=["Nome do Usuario"])
    email: str = Field(pattern=REGEX_EMAIL, examples=["usuario@exemplo.com"])


class UsuarioCreate(UsuarioBase):
    """Esquema para criação de usuário, incluindo campos obrigatórios."""

    senha: str = Field(examples=["Senha_123"])

    @field_validator("senha", mode="before")
    @classmethod
    def validar_senha(cls, valor: str) -> str:
        """Valida a senha usando regex personalizada."""
        if not re.match(REGEX_SENHA, valor, re.VERBOSE):
            raise ValueError(
                "A senha deve conter pelo menos 6 caracteres, incluindo "
                "letras maiúsculas, minúsculas, números e caracteres especiais."
            )
        return valor


class UsuarioResponse(UsuarioBase):
    """Esquema para resposta de usuário, excluindo campos sensíveis."""

    id: int
    ativo: bool

    # Atributo de configuração para permitir a criação do modelo a partir de objetos ORM
    model_config = ConfigDict(from_attributes=True)
