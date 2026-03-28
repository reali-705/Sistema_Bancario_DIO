"""Módulo de Esquemas de Dados para Validação e Serialização."""

from pydantic import BaseModel, ConfigDict, Field, field_validator

# Validação de email usando expressão regular (regex).
REGEX_EMAIL = r"^[\w\.-]+@[\w\.-]+\.\w+$"


class UsuarioBase(BaseModel):
    """Esquema base para operações de usuário, compartilhando campos comuns."""

    nome: str = Field(min_length=3, examples=["Nome do Usuario"])
    email: str = Field(pattern=REGEX_EMAIL, examples=["usuario@exemplo.com"])


class UsuarioCreate(UsuarioBase):
    """Esquema para criação de usuário, incluindo campos obrigatórios."""

    senha: str = Field(examples=["senha_123"])

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, senha: str) -> str:
        """Valida a senha para garantir que atenda aos critérios de segurança."""
        if len(senha) < 6:
            raise ValueError("A senha deve conter pelo menos 6 caracteres.")
        elif not any(char.isdigit() for char in senha):
            raise ValueError("A senha deve conter pelo menos um número.")
        elif not any(char.isalpha() for char in senha):
            raise ValueError("A senha deve conter pelo menos uma letra.")
        elif not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for char in senha):
            raise ValueError("A senha deve conter pelo menos um caractere especial.")
        return senha


class UsuarioResponse(UsuarioBase):
    """Esquema para resposta de usuário, excluindo campos sensíveis."""

    id: int
    ativo: bool

    # Atributo de configuração para permitir a criação do modelo a partir de objetos ORM
    model_config = ConfigDict(from_attributes=True)
