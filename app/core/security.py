"""Módulo de Autenticação e Segurança."""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import settings
from app.schemas import DadosToken


def gerar_senha_hash(senha: str) -> str:
    """Gera o hash da senha usando bcrypt."""
    senha_hash_binario = bcrypt.hashpw(
        password=senha.encode("utf-8"), salt=bcrypt.gensalt()
    )
    return senha_hash_binario.decode("utf-8")


def verificar_senha(senha: str, senha_hash: str) -> bool:
    """Verifica se a senha fornecida corresponde ao hash armazenado."""
    return bcrypt.checkpw(
        password=senha.encode("utf-8"), hashed_password=senha_hash.encode("utf-8")
    )


def criar_token_acesso(dados: DadosToken) -> str:
    """Cria um token JWT de acesso com base nos dados fornecidos."""
    dados_dict = dados.model_dump()
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
    dados_dict.update({"exp": exp})

    jwtoken = jwt.encode(  # type: ignore
        payload=dados_dict,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return jwtoken
