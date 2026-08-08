from pathlib import Path
import shutil

DOCUMENTS_DIR=Path("documents")
DOCUMENTS_DIR.mkdir(exist_ok=True)
def save_document(upload_file):
    destination = DOCUMENTS_DIR/upload_file.filename
    with open(destination,"wb") as buffer:
        shutil.copyfileobj(upload_file.file,buffer)
    return str(destination)