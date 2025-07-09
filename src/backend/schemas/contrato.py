from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class ContratoBase(BaseModel):
    arquivo: str
    texto: str


class ContratoResponse(ContratoBase):
    score: float = 0.0


class SearchResponse(BaseModel):
    resultados: List[ContratoResponse]
    total: int
