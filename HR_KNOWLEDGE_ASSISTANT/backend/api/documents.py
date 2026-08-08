from fastapi import APIRouter,HTTPException
from backend.models.api_response import APIResponse
from backend.services.document_service import get_all_documents
from backend.database.oracle import get_connection

router=APIRouter()
@router.get("/documents",response_model=APIResponse)
def list_documents():
    documents=get_all_documents()
    return APIResponse(success=True,message="Documents retrieved successfully",data=documents)

@router.delete("/documents/{document_id}")
def delete_document(document_id:int):
    conn=get_connection()
    cur=conn.cursor()
    try:
        cur.execute("""DELETE FROM document_chunks WHERE document_id=:1""",(document_id,))
        cur.execute("""DELETE FROM hr_documents WHERE document_id=:1""",(document_id,))
        if cur.rowcount==0:
            raise HTTPException(status_code=404,detail="Document not found")
        conn.commit()
        return {"status":"ok","message":"Document deleted successfully","document_id":document_id}
    except HTTPException:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        cur.close()
        conn.close()