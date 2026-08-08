def build_prompt(question,chunks):
    context="\n\n".join(chunk["chunk_text"] for chunk in chunks)
    prompt=f"""You are an HR Assistant.Answer ONLY from the HR documents below.
    If the answer is not available, say:"I could not find this information in the HR documents."
    HR Documents:{context}
    Employee Question:{question}
    Answer:"""
    return prompt