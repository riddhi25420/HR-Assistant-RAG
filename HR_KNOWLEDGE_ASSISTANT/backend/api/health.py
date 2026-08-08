from fastapi import APIRouter
router = APIRouter()
@router.get("/health")
def health():
    return {"status":"healthy","message":"Backend is running successfully."}