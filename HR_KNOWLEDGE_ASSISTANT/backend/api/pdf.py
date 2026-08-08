from fastapi import APIRouter
from backend.services.pdf_service import extract_pdf_text

router=APIRouter()
@router.get("/extract")
def extract():
    pages=extract_pdf_text("documents/POSTER.pdf")
    return {"pages":len(pages),"preview":pages[:2]}