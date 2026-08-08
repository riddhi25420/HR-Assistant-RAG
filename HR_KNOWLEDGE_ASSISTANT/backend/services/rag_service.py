from backend.services.chat_memory import (get_history,add_message)
from backend.services.hybrid_search import hybrid_search
from backend.services.ollama_service import ask_llm
from backend.services.session_service import update_chat_title

def answer_question(session_id,question):
    print("QUESTION SESSION:",session_id)
    chunks=hybrid_search(question)
    print("====================================")
    print("QUESTION:", question)
    print("NUMBER OF CHUNKS:", len(chunks))
    print("CHUNKS:", chunks)
    print("====================================")
    if not chunks:
        return {"answer":"DEBUG: hybrid_search returned zero chunks","sources":[],"history":get_history(session_id)}
    context=""
    for i,chunk in enumerate(chunks,start=1):
        context+=f"""Document{i}
                Title:{chunk['title']}
                Page:{chunk['page_number']}
                Section:{chunk['section_title']}

                {chunk['chunk_text']}"""
    history=get_history(session_id)
    history_text=""
    for msg in history:
        history_text+=f"{msg['role']}: {msg['content']}\n"
    prompt=f"""You are an HR Assistant.
            Use the conversation history to understand follow-up questions.
            Conversation History:{history_text}
            HR Documents:{context}
            Current User Question:{question}
            Rules:
            - Answer ONLY from the HR documents.
            - Do NOT invent information.
            - Use conversation history only to understand context.
            - If the answer is unavailable reply exactly:
            "I could not find this information in the HR documents."
            """
    answer=ask_llm(prompt)
    add_message(session_id,"User",question)
    print("UPDATING TITLE FOR:", session_id)
    update_chat_title(session_id,question)
    add_message(session_id,"Assistant",answer)
    return {"answer":answer,"sources":[{"document":chunk["title"],"file_name":chunk["file_name"],"file_path":chunk["file_path"],"page":chunk["page_number"],"section":chunk["section_title"],"distance":round(chunk["distance"],4)} for chunk in chunks],"history":get_history(session_id)}