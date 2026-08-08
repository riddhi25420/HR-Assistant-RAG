from fastapi import APIRouter
from backend.services.chat_memory import get_history

router=APIRouter()
@router.get("/history/{session_id}")
def history(session_id:str):
    return{"history":get_history(session_id)}