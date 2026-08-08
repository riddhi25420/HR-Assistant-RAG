from backend.database.oracle import get_connection

def create_chat_session(session_id,title="New Chat"):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("""INSERT INTO chat_sessions(session_id,title) VALUES (:1,:2)""",[session_id,title])
    conn.commit()
    cur.close()
    conn.close()

def add_message(session_id,role,message):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("""INSERT INTO chat_messages(session_id,role,content) VALUES (:1,:2,:3)""",[session_id, role,message])
    conn.commit()
    cur.close()
    conn.close()

def get_history(session_id):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("""SELECT role,content FROM chat_messages WHERE session_id=:1 ORDER BY created_at""",[session_id])
    rows=cur.fetchall()
    history=[]
    for role,content in rows:
        if hasattr(content,"read"):
            content=content.read()
        history.append({"role":role,"content":str(content)})
    cur.close()
    conn.close()
    return history

def clear_history(session_id):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("""DELETE FROM chat_messages WHERE session_id=:1""",[session_id])
    conn.commit()
    cur.close()
    conn.close()