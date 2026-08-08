from pydantic import BaseModel
from fastapi import APIRouter
from backend.database.oracle import get_connection

router=APIRouter()
class RenameRequest(BaseModel):
    session_id:str
    title:str
@router.post("/rename")
def rename_chat(req:RenameRequest):
    print("Session:",repr(req.session_id))
    print("Title:",repr(req.title))
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("""UPDATE chat_sessions SET title=:1 WHERE session_id=:2""",(req.title,req.session_id))
    print("Rows updated:",cur.rowcount)
    conn.commit()
    cur.close()
    conn.close()
    return {"status":"ok"}