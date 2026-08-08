from typing import List, Optional
from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.rag_service import answer_question

router=APIRouter()
class ChatRequest(BaseModel):
    session_id:str
    question:str
class Source(BaseModel):
    document:str
    file_name:str
    page:int
    section:Optional[str]=None
    distance:Optional[float]=None
class HistoryItem(BaseModel):
    role:str
    content:str
class ChatResponse(BaseModel):
    answer:str
    sources:List[Source]
    history:List[HistoryItem]
@router.post("/chat",response_model=ChatResponse)
def chat(request: ChatRequest):
    return answer_question(request.session_id,request.question)