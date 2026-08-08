from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.search_service import search_documents

router=APIRouter()
class SearchRequest(BaseModel):
    question: str
@router.post("/search")
def search(request:SearchRequest):
    return search_documents(request.question)