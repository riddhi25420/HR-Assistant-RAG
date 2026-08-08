from backend.services.document_service import (get_all_chunks,update_chunk_embedding)
from backend.services.embedding_service import generate_embedding

def index_documents():
    chunks=get_all_chunks()
    print(f"found {len(chunks)} no. of chunks")
    for chunk_id,text in chunks:
        print(f"\nProcessing chunk {chunk_id}")
        if hasattr(text,"read"):
            text=text.read()
        embedding=generate_embedding(text)
        print(type(embedding))
        print(len(embedding))
        update_chunk_embedding(chunk_id,embedding)
        print(f"finished chunk {chunk_id}")
    return len(chunks)