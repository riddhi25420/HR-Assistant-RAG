from fastapi import APIRouter
from backend.services.chunk_service import chunk_text

router=APIRouter()
@router.get("/chunk-test")
def test():
    sample=("This is a sample HR policy. "*200)
    chunks=chunk_text(sample)
    return{"total_chunks":len(chunks),"first_chunk":chunks[0]}