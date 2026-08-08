from backend.services.search_service import search_documents

def hybrid_search(question,top_k=5):
    results=search_documents(question)
    unique={}
    final_results=[]
    for chunk in results:
        key=(chunk["file_name"],chunk["page_number"],chunk["section_title"])
        if key not in unique:
            unique[key]=True
            final_results.append(chunk)
        if len(final_results)==top_k:
            break
    return final_results