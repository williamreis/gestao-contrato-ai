from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class DocumentoBase(BaseModel):
    arquivo: str
    texto: str


class DocumentoResponse(DocumentoBase):
    score: float = 0.0


class SearchResponse(BaseModel):
    resultados: List[DocumentoResponse]
    total: int
