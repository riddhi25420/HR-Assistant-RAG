from pathlib import Path
from fastapi import APIRouter, UploadFile, File,Form
from backend.services.upload_service import save_document
from backend.services.document_service import (document_exists,insert_document)
from backend.utils.file_utils import (calculate_file_hash,get_pdf_page_count)
from backend.services.pdf_service import extract_pdf_text
from backend.services.chunk_service import chunk_text
from backend.services.document_service import insert_chunk
import base64
import io
from pydantic import BaseModel

router=APIRouter()
@router.post("/upload")
async def upload_document(file:UploadFile=File(...),category:str=Form("General")):
    file_path=save_document(file)
    file_hash=calculate_file_hash(file_path)
    if document_exists(file_hash):
        return{"success":False,"message":"This document already exists"}
    pages=get_pdf_page_count(file_path)
    document_id=insert_document(title=Path(file.filename).stem,category=category,file_name=file.filename,file_path=file_path,file_hash=file_hash,total_pages=pages)
    pdf_pages=extract_pdf_text(file_path)
    for page in pdf_pages:
        chunks=chunk_text(page["text"])
        for chunk in chunks:
            insert_chunk(document_id=document_id,page_number=page["page"],chunk_number=chunk["chunk_number"],chunk_text=chunk["text"])
    return{"success":True,"message":"Document uploaded successfully"}

class ApexUploadRequest(BaseModel):
    file_name:str
    category:str="General"
    file_base64:str

@router.post("/upload-apex")
async def upload_document_from_apex(req:ApexUploadRequest):
    print("========== APEX UPLOAD CALLED ==========")
    print("FILE:", req.file_name)
    print("CATEGORY:", req.category)
    print("BASE64 LENGTH:", len(req.file_base64))
    try:
        file_bytes=base64.b64decode(req.file_base64)
        upload_dir=Path("hr_documents")
        upload_dir.mkdir(parents=True,exist_ok=True)
        file_path=upload_dir/req.file_name
        with open(file_path, "wb") as f:
            f.write(file_bytes)
        file_hash=calculate_file_hash(file_path)
        if document_exists(file_hash):
            return {"success":False,"message":"This document already exists"}
        pages=get_pdf_page_count(file_path)
        document_id=insert_document(title=Path(req.file_name).stem,category=req.category,file_name=req.file_name,file_path=str(file_path),file_hash=file_hash,total_pages=pages)
        pdf_pages=extract_pdf_text(file_path)
        for page in pdf_pages:
            chunks=chunk_text(page["text"])
            for chunk in chunks:
                insert_chunk(document_id=document_id,page_number=page["page"],chunk_number=chunk["chunk_number"],chunk_text=chunk["text"])
        return {"success":True,"message":"Document uploaded successfully","document_id":document_id}
    except Exception as e:
        return {"success":False,"message":str(e)}