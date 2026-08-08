from fastapi import FastAPI
from backend.api.health import router as health_router
from backend.api.chat import router as chat_router
from backend.api.documents import router as documents_router
from backend.api.upload import router as upload_router
from backend.api.pdf import router as pdf_router
from backend.api.chunk import router as chunk_router
from backend.api.embedding import router as embedding_router
from backend.api.index import router as index_router
from backend.api.search import router as search_router
from backend.api.rag import router as rag_router
from backend.api.history import router as history_router
from backend.api.session import router as session_router
from fastapi.staticfiles import StaticFiles
from backend.api.routes import router as routes_router

app=FastAPI(title="HR Knowledge Assistant",version="1.0.0")
app.include_router(health_router)
app.include_router(chat_router)   
app.include_router(documents_router) 
app.include_router(upload_router) 
app.include_router(pdf_router) 
app.include_router(chunk_router)
app.include_router(embedding_router)
app.include_router(index_router)
app.include_router(search_router)
app.include_router(rag_router)
app.include_router(history_router)
app.include_router(session_router)
app.include_router(routes_router)
app.mount("/documents",StaticFiles(directory=r"D:\\Riddhi Aggarwal\\internship\\HR-Assistance\\hr_documents"),name="documents")