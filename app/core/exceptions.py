"""Módulo de tratamento global de exceções da API."""

# pyright: reportUnusedFunction=false, reportArgumentType=false
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DBAPIError, IntegrityError


def carregar_excecoes_personalizadas(app: FastAPI) -> None:
    """Registra os manipuladores de exceção no ciclo de vida do FastAPI."""

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(
        requisicao: Request, excecao: IntegrityError
    ) -> JSONResponse:
        """Intercepta a falha de constraint UNIQUE do SQLAlchemy."""
        erro_bruto = str(excecao.orig).lower()

        if "usuarios.email" in erro_bruto:
            mensagem = "Este email já está cadastrado no sistema."
        else:
            mensagem = "Violação de integridade nos dados enviados."

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": mensagem},
        )

    @app.exception_handler(DBAPIError)
    async def dbapi_error_handler(
        requisicao: Request, excecao: DBAPIError
    ) -> JSONResponse:
        """Intercepta erros do DBAPI."""
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Erro interno do servidor."},
        )
