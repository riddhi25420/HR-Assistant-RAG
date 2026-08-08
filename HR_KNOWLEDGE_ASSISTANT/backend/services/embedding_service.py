from sentence_transformers import SentenceTransformer
import array

model=SentenceTransformer("all-MiniLM-L6-v2")
def generate_embedding(text:str):
    embedding=model.encode(text,normalize_embeddings=True)
    return array.array("f",embedding)