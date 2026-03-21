"""Módulo da estrutura do banco de Dados."""

from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Classe base para as entidades do banco de dados."""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class Usuario(Base):
    """Entidade que representa um usuário do sistema bancário."""

    __tablename__ = "usuarios"

    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)
    ativo: Mapped[bool] = mapped_column(nullable=False, default=True)

    contas: Mapped[list["Conta"]] = relationship(
        back_populates="usuario", cascade="all, delete-orphan"
    )


class Conta(Base):
    """Entidade que representa uma conta bancária."""

    __tablename__ = "contas"

    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    saldo: Mapped[float] = mapped_column(nullable=False, default=0.0)

    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)

    usuario: Mapped["Usuario"] = relationship(back_populates="contas")
    transacoes: Mapped[list["Transacao"]] = relationship(
        back_populates="conta", cascade="all, delete-orphan"
    )


class Transacao(Base):
    """Entidade que representa uma transação bancária."""

    __tablename__ = "transacoes"

    valor: Mapped[float] = mapped_column(nullable=False)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    data_hora: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)

    conta_id: Mapped[int] = mapped_column(ForeignKey("contas.id"), nullable=False)

    conta: Mapped["Conta"] = relationship(back_populates="transacoes")
