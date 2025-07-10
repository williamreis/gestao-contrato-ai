from pydantic import BaseModel, ConfigDict
from typing import List


class DocumentBase(BaseModel):
    arquivo: str
    texto: str


class DocumentResponse(DocumentBase):
    score: float = 0.0


class SearchResponse(BaseModel):
    resultados: List[DocumentResponse]
    total: int
