"""Módulo de Esquemas para Documentação e Respostas de Erro."""

from typing import Any

from fastapi import status
from pydantic import BaseModel, Field


class ExemploErro(BaseModel):
    """Esquema padronizado para devolução de erros (Detail)."""

    detail: str = Field(examples=["Mensagem de erro detalhada e descritiva."])


TipoResposta = dict[int, dict[str, Any]]

RESPOSTA_409: TipoResposta = {
    status.HTTP_409_CONFLICT: {
        "description": "Conflito: Violação de regra de unicidade.",
        "model": ExemploErro,
    }
}

RESPOSTA_500: TipoResposta = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Erro interno do servidor ou falha de infraestrutura.",
        "model": ExemploErro,
    }
}

RESPOSTA_404: TipoResposta = {
    status.HTTP_404_NOT_FOUND: {
        "description": "Recurso solicitado não encontrado no sistema.",
        "model": ExemploErro,
    }
}
