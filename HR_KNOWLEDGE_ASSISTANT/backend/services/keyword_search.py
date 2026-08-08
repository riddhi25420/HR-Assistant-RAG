from backend.database.oracle import get_connection

def keyword_search(question, top_k=5):
    connection=get_connection()
    cur=connection.cursor()
    cur.execute("""SELECT c.chunk_id,c.document_id,d.title,d.file_name,c.page_number,c.section_title,c.chunk_text FROM document_chunks c JOIN hr_documents d ON c.document_id=d.document_id WHERE CONTAINS(c.chunk_text,:1)>0 FETCH FIRST :2 ROWS ONLY""",[question,top_k])
    rows=cur.fetchall()
    cur.close()
    connection.close()
    return rows