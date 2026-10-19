from fastapi import APIRouter

from app.models.request_models import ChatRequest, ChatResponse
from app.services.llm_service import answer_question

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    result = answer_question(request.question)
    return ChatResponse(**result)
