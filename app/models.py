from sqlalchemy import Column, Integer, String, Date, Text, Float, Boolean, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date
import enum
from .database import Base
from sqlalchemy import DateTime
from datetime import datetime

# Tabela de associação Desbravador<->Especialidade (N:N)
desbravador_especialidade = Table(
    "desbravador_especialidade",
    Base.metadata,
    Column("desbravador_id", ForeignKey("desbravadores.id"), primary_key=True),
    Column("especialidade_id", ForeignKey("especialidades.id"), primary_key=True),
)

class Unidade(Base):
    __tablename__ = "unidades"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    descricao: Mapped[str] = mapped_column(String(255), default="")
    desbravadores = relationship("Desbravador", back_populates="unidade")

class Classe(Base):
    __tablename__ = "classes"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    nivel: Mapped[int] = mapped_column(Integer, default=1)
    desbravadores = relationship("Desbravador", back_populates="classe")

class Especialidade(Base):
    __tablename__ = "especialidades"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    area: Mapped[str] = mapped_column(String(120), default="Geral")
    desbravadores = relationship("Desbravador", secondary=desbravador_especialidade, back_populates="especialidades")

class Desbravador(Base):
    __tablename__ = "desbravadores"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    data_nascimento: Mapped[date | None]
    unidade_id: Mapped[int | None] = mapped_column(ForeignKey("unidades.id"))
    classe_id: Mapped[int | None] = mapped_column(ForeignKey("classes.id"))
    responsavel: Mapped[str] = mapped_column(String(120), default="")
    telefone_responsavel: Mapped[str] = mapped_column(String(40), default="")
    documento: Mapped[str] = mapped_column(String(50), default="")

    unidade = relationship("Unidade", back_populates="desbravadores")
    classe = relationship("Classe", back_populates="desbravadores")
    especialidades = relationship("Especialidade", secondary=desbravador_especialidade, back_populates="desbravadores")
    mensalidades = relationship("Mensalidade", back_populates="desbravador", cascade="all, delete-orphan")

class TipoLancamento(str, enum.Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"

class Caixa(Base):
    __tablename__ = "caixa"
    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[date]
    tipo: Mapped[TipoLancamento]
    categoria: Mapped[str] = mapped_column(String(120), default="Geral")
    descricao: Mapped[str] = mapped_column(String(255), default="")
    valor: Mapped[float]

class Mensalidade(Base):
    __tablename__ = "mensalidades"
    id: Mapped[int] = mapped_column(primary_key=True)
    desbravador_id: Mapped[int] = mapped_column(ForeignKey("desbravadores.id"))
    competencia: Mapped[str] = mapped_column(String(7))  # AAAA-MM
    valor: Mapped[float]
    pago: Mapped[bool] = mapped_column(Boolean, default=False)
    data_pagamento: Mapped[date | None]

    desbravador = relationship("Desbravador", back_populates="mensalidades")

class Patrimonio(Base):
    __tablename__ = "patrimonios"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    descricao: Mapped[str] = mapped_column(String(255), default="")
    data_aquisicao: Mapped[date | None]
    valor: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(50), default="Em uso")

class Ata(Base):
    __tablename__ = "atas"
    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[date]
    titulo: Mapped[str] = mapped_column(String(200))
    conteudo: Mapped[str] = mapped_column(Text)

class Ato(Base):
    __tablename__ = "atos"
    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[date]
    titulo: Mapped[str] = mapped_column(String(200))
    conteudo: Mapped[str] = mapped_column(Text)

class Role(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.USER)

class Visitante(Base):
    __tablename__ = "visitantes"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(200), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

