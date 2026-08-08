from fastapi import APIRouter
from backend.services.embedding_service import generate_embedding

router=APIRouter()
@router.get("/embedding-test")
def embedding_test():
    text="Employees are entitled to annual leave."
    vector=generate_embedding(text)
    return{"text":text,"dimensions":len(vector),"preview":vector[:10]}