from fastapi import APIRouter
from backend.services.index_service import index_documents

router=APIRouter()
@router.post("/index")
def build_index():
    print(">>> ENTERED /index <<<")
    total=index_documents()
    print(">>> INDEXING FINISHED <<<")
    return {"message":"Index created successfully","chunks_processed":total}
