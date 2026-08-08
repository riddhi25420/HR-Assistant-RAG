import re
from backend.database.oracle import get_connection
from backend.services.embedding_service import generate_embedding

STOP_WORDS={"what","is","are","the","how","should","do","i","my","if","after","for","a","an","to","of","and","can","company","does","employee","get","happens","when"}

def normalize(text):
    text = text.lower().replace("_", " ")
    return re.findall(r"[a-z0-9]+", text)

def meaningful_words(text):
    return {word for word in normalize(text) if word not in STOP_WORDS and len(word)>2}

def keyword_score(question,title,chunk_text):
    question_lower=question.lower()
    title_clean=title.lower().replace("_"," ")
    chunk_lower=chunk_text.lower()
    q_words=meaningful_words(question)
    if not q_words:
        return 0.0
    score=0.0
    important_phrases=["data privacy","employee data","security incident","password policy","work from home","travel expenses","medical insurance","payroll process","salary paid","leave policy","attendance rules","employee responsibilities","annual leaves","sick leaves","company laptop"]
    for phrase in important_phrases:
        if phrase in question_lower:
            if phrase in title_clean:
                score+=1.0
            if phrase in chunk_lower:
                score+=0.7
    title_words=set(normalize(title))
    title_matches=q_words & title_words
    if title_matches:
        score+=(len(title_matches)/len(q_words))*0.8
    chunk_words=set(normalize(chunk_text))
    chunk_matches=q_words & chunk_words
    if chunk_matches:
        score+=(len(chunk_matches)/len(q_words))*0.4
    return min(score,2.0)

def search_documents(question,top_k=5):

    connection = get_connection()
    cur = connection.cursor()

    query_embedding = generate_embedding(question)

    print("QUESTION:", question)
    print("EMBEDDING GENERATED:",query_embedding is not None)
    candidate_k=10

    #vector search
    cur.execute("""SELECT c.chunk_id,c.document_id,d.title,d.file_name,d.file_path,c.page_number,c.section_title,c.chunk_text,VECTOR_DISTANCE(c.embedding,:embedding,COSINE) AS distance FROM document_chunks c JOIN hr_documents d ON c.document_id = d.document_id WHERE c.embedding IS NOT NULL ORDER BY distance FETCH FIRST :candidate_k ROWS ONLY""",{"embedding":query_embedding,"candidate_k":candidate_k})
    vector_rows=cur.fetchall()
    print("VECTOR CANDIDATES:",len(vector_rows))

    #lexial search
    q_words=list(meaningful_words(question))
    lexical_rows=[]
    if q_words:
        conditions=[]
        binds={"embedding":query_embedding,"candidate_k":candidate_k}
        for i,word in enumerate(q_words):
            bind_name=f"word{i}"
            conditions.append(
                f"""(LOWER(d.title) LIKE '%' || :{bind_name} || '%' OR LOWER(c.chunk_text) LIKE '%' || :{bind_name} || '%')""")
            binds[bind_name]=word
        lexical_sql=f"""SELECT c.chunk_id,c.document_id,d.title,d.file_name,d.file_path,c.page_number,c.section_title,c.chunk_text,VECTOR_DISTANCE(c.embedding,:embedding,COSINE) AS distance FROM document_chunks c JOIN hr_documents d ON c.document_id=d.document_id WHERE c.embedding IS NOT NULL AND ({" OR ".join(conditions)}) ORDER BY distance FETCH FIRST :candidate_k ROWS ONLY"""
        cur.execute(lexical_sql,binds)
        lexical_rows=cur.fetchall()
    print("LEXICAL CANDIDATES:",len(lexical_rows))

    #merge candidates
    combined={}
    for row in vector_rows+lexical_rows:
        (chunk_id,document_id,title,file_name,file_path,page_number,section_title,chunk_text,distance)=row
        if hasattr(chunk_text,"read"):
            chunk_text=chunk_text.read()
        if chunk_id not in combined:
            combined[chunk_id]={"chunk_id":chunk_id,"document_id":document_id,"title":title,"file_name":file_name,"file_path":file_path,"page_number":page_number,"section_title":section_title,"chunk_text":chunk_text,"distance":float(distance)}

    #hybrid ranking
    results=[]
    for result in combined.values():
        distance=result["distance"]
        vector_score=1.0-distance
        lexical=keyword_score(question,result["title"],result["chunk_text"])

        # Normalize lexical score.
        lexical_score=min(lexical/2.0,1.0)
        final_score=(vector_score*0.65+lexical_score*0.35)
        result["vector_score"]=vector_score
        result["keyword_score"]=lexical_score
        result["final_score"]=final_score
        results.append(result)

    #sort
    results.sort(key=lambda x:x["final_score"],reverse=True)
    print("\nHYBRID SEARCH RESULTS:")
    for result in results[:top_k]:
        print(result["title"],"| distance:",round(result["distance"], 4),"| vector:",round(result["vector_score"], 4),"| keyword:",round(result["keyword_score"], 4),"| final:",round(result["final_score"], 4))
    cur.close()
    connection.close()
    return results[:top_k]