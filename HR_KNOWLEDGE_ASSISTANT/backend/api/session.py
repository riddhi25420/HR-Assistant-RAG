from fastapi import APIRouter
from pydantic import BaseModel
from backend.database.oracle import get_connection
from backend.services.chat_memory import create_chat_session
from backend.services.chat_memory import get_history

router=APIRouter()
class SessionRequest(BaseModel):
    session_id:str

@router.get("/session")
def session():
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("""SELECT session_id,title FROM chat_sessions ORDER BY created_at DESC""")
    rows=cur.fetchall()
    cur.close()
    conn.close()
    return [{"session_id":r[0],"title":r[1]} for r in rows]

@router.post("/session")
def create_session(request:SessionRequest):
    create_chat_session(request.session_id)
    return {"status":"success","session_id":request.session_id}

@router.get("/session/{session_id}")
def get_chat(session_id:str):
    history=get_history(session_id)
    return {"history":history}

@router.delete("/session/{session_id}")
def delete_session(session_id:str):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("DELETE FROM chat_sessions WHERE session_id=:1",[session_id])
    conn.commit()
    cur.close()
    conn.close()
    return {"status":"deleted"}