from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=1)


class ChatResponse(BaseModel):
    question: str
    question_type: str
    countries: list[str]
    years: list[int]
    evidence: list[str]
    answer: str
    model: str
    llm_used: bool
    error: str | None = None
