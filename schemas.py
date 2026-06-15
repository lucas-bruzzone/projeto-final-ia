"""Schemas Pydantic da API de extração de vagas.

Esta é a fonte da verdade do formato. Tanto a API quanto o cliente Ollama
referenciam estas classes para garantir que estamos todos falando do mesmo
JSON.
"""
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class Modalidade(str, Enum):
    """Modalidade de trabalho declarada na vaga."""
    REMOTO = "remoto"
    HIBRIDO = "hibrido"
    PRESENCIAL = "presencial"


class Nivel(str, Enum):
    """Nível de senioridade declarado na vaga."""
    ESTAGIO = "estagio"
    JUNIOR = "junior"
    PLENO = "pleno"
    SENIOR = "senior"


class Salario(BaseModel):
    """Faixa salarial. Ambos os campos são opcionais para acomodar vagas
    com apenas o mínimo, apenas o máximo, ou nenhum dos dois (caso de
    salário "a combinar" — neste caso, o objeto Salario inteiro deve ser
    None na Vaga)."""
    min: Optional[float] = None
    max: Optional[float] = None


class Vaga(BaseModel):
    """Estrutura final extraída de um anúncio de vaga.

    Campos opcionais devem vir como None quando não declarados no texto.
    Inferir o que não está escrito é considerado erro de extração.
    """
    cargo: str = Field(..., description="Cargo/título da vaga")
    empresa: Optional[str] = None
    localidade: Optional[str] = None
    modalidade: Modalidade
    nivel: Optional[Nivel] = None
    salario: Optional[Salario] = None
    requisitos: List[str] = Field(default_factory=list)
    beneficios: List[str] = Field(default_factory=list)


class RequestExtracao(BaseModel):
    """Corpo do POST /extrair."""
    texto: str = Field(..., min_length=1, description="Texto bruto do anúncio")
