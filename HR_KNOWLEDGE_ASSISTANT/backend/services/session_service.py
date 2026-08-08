from backend.database.oracle import get_connection

def update_chat_title(session_id, question):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute("""SELECT session_id,title FROM chat_sessions ORDER BY created_at DESC""")
    print("TABLE CONTENTS:")
    for row in cur.fetchall():
        print(row)
    cur.execute("""UPDATE chat_sessions SET title=:1 WHERE session_id=:2 AND title='New Chat'""",[question[:50],session_id])
    print("ROWS UPDATED =",cur.rowcount)
    conn.commit()
    cur.close()
    conn.close()