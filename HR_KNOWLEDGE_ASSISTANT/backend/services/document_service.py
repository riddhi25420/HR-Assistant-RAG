from backend.database.oracle import get_connection
from backend.utils.logger import logger
from backend.services.embedding_service import generate_embedding

def get_all_documents():
    connection=None
    cur=None
    try:
        logger.info("Fetching HR documents")
        connection=get_connection()
        cur=connection.cursor()
        cur.execute("""SELECT document_id,title,category,file_name,upload_date,total_pages,status FROM hr_documents ORDER BY document_id""")
        rows=cur.fetchall()
        logger.info(f"{len(rows)} documents retrieved")
        documents = []
        for row in rows:
            documents.append({"document_id":row[0],"title":row[1],"category":row[2],"file_name":row[3],"upload_date":str(row[4]),"total_pages":row[5],"status":row[6]})
        return documents
    except Exception as e:
        logger.error(str(e))
        return []
    finally:
        if cur:
            cur.close()
        if connection:
            connection.close()

def document_exists(file_hash):
    connection=get_connection()
    cur=connection.cursor()
    cur.execute("""SELECT COUNT(*) FROM hr_documents WHERE file_hash=:1""",[file_hash])
    count=cur.fetchone()[0]
    cur.close()
    connection.close()
    return count>0

def insert_document(title,category,file_name,file_path,file_hash,total_pages,uploaded_by="ADMIN"):
    connection=get_connection()
    cur=connection.cursor()
    document_id=cur.var(int)
    cur.execute("""INSERT INTO hr_documents(title,category,file_name,upload_date,total_pages,status,file_path,file_hash,uploaded_by) VALUES(:1,:2,:3,CURRENT_TIMESTAMP,:4,'ACTIVE',:5,:6,:7) RETURNING document_id INTO :8""",[title,category,file_name,total_pages,file_path,file_hash,uploaded_by,document_id])
    connection.commit()
    new_document_id=document_id.getvalue()[0]
    cur.close()
    connection.close()
    return new_document_id

def insert_chunk(document_id,page_number,chunk_number,chunk_text,section_title=None):
    connection=get_connection()
    cur=connection.cursor()
    try:
        embedding=generate_embedding(chunk_text)
        cur.execute("""INSERT INTO document_chunks(document_id,chunk_number,page_number,section_title,chunk_text,embedding) VALUES(:1,:2,:3,:4,:5,:6)""",[document_id,chunk_number,page_number,section_title,chunk_text,embedding])
        connection.commit()
    finally:
        cur.close()
        connection.close()

def update_chunk_embedding(chunk_id, embedding):
    connection=get_connection()
    cur=connection.cursor()
    print("Updating:",chunk_id)
    cur.execute("""UPDATE document_chunks SET embedding=:1 WHERE chunk_id=:2""",[embedding, chunk_id])
    print("Rows updated:",cur.rowcount)
    connection.commit()
    cur.close()
    connection.close()
 
def get_all_chunks():
    connection=get_connection()
    cur=connection.cursor()
    cur.execute("""SELECT chunk_id, chunk_text FROM document_chunks WHERE embedding IS NULL ORDER BY chunk_id""")
    rows=[]
    for chunk_id,chunk_text in cur.fetchall():
        if hasattr(chunk_text,"read"):
            chunk_text=chunk_text.read()
        rows.append((chunk_id,chunk_text))
    cur.close()
    connection.close()
    return rows