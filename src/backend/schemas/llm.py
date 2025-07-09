from pydantic import BaseModel
from typing import List


class QuestionRequest(BaseModel):
    question: str
    max_results: int = 50


class QuestionResponse(BaseModel):
    answer: str
    sources: List[dict]
