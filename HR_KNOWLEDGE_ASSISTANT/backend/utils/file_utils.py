from pathlib import Path
import hashlib
from pypdf import PdfReader

def calculate_file_hash(file_path:str):
    sha256=hashlib.sha256()
    with open(file_path,"rb") as file:
        while chunk:=file.read(4096):
            sha256.update(chunk)
    return sha256.hexdigest()

def get_pdf_page_count(file_path:str):
    reader=PdfReader(file_path)
    return len(reader.pages)