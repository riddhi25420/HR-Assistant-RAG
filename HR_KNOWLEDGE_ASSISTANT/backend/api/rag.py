from fastapi import APIRouter
from backend.models.chat_models import ChatRequest
from backend.services.rag_service import answer_question

router=APIRouter()
@router.post("/chat")
def ask(request:ChatRequest):
    return answer_question(request.session_id,request.question)