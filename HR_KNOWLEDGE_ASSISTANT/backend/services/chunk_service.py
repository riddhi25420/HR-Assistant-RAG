from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=100,separators=["\n\n","\n",". ","! ","? ","; ",", "," ",""])
def chunk_text(text):
    raw_chunks=splitter.split_text(text)
    chunks=[]
    for i,chunk in enumerate(raw_chunks,start=1):
        chunks.append({"chunk_number":i,"text":chunk})
    return chunks