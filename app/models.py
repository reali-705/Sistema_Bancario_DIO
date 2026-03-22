"""Módulo da estrutura do banco de Dados."""

from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Fornece a estrutura fundamental para as tabelas do banco de dados.

    Todas as classes de modelo herdam desta base, garantindo consistência
    e integração perfeita com o SQLAlchemy. O campo 'id' é definido aqui para
    evitar repetição em cada modelo, seguindo a convenção de chave primária.
    """

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class Usuario(Base):
    """Mapeia a tabela física 'usuarios' e suas regras de negócio.

    Implementa Soft Delete através do campo 'ativo', garantindo a preservação
    do histórico de transações para fins de auditoria financeira.
    """

    __tablename__ = "usuarios"

    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)
    ativo: Mapped[bool] = mapped_column(nullable=False, default=True)

    contas: Mapped[list["Conta"]] = relationship(
        back_populates="usuario", cascade="all, delete-orphan"
    )


class Conta(Base):
    """Mapeia as contas bancárias atreladas aos usuários.

    Possui restrição de chave estrangeira com a tabela 'usuarios'. O atributo
    cascade garante que, em caso de hard delete (excepcional), as contas e
    transações dependentes sejam eliminadas para evitar dados órfãos.
    """

    __tablename__ = "contas"

    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    saldo: Mapped[float] = mapped_column(nullable=False, default=0.0)

    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)

    usuario: Mapped["Usuario"] = relationship(back_populates="contas")
    transacoes: Mapped[list["Transacao"]] = relationship(
        back_populates="conta", cascade="all, delete-orphan"
    )


class Transacao(Base):
    """Mapeia as transações bancárias realizadas nas contas.

    Possui restrição de chave estrangeira com a tabela 'contas'. O atributo
    cascade garante que, em caso de hard delete (excepcional), as transações
    dependentes sejam eliminadas para evitar dados órfãos.
    """

    __tablename__ = "transacoes"

    valor: Mapped[float] = mapped_column(nullable=False)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    data_hora: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)

    conta_id: Mapped[int] = mapped_column(ForeignKey("contas.id"), nullable=False)

    conta: Mapped["Conta"] = relationship(back_populates="transacoes")
