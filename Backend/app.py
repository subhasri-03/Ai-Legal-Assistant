from fastapi import FastAPI, UploadFile, File
from chatbot import legal_chat
from document_generator import generate_document
from rag_engine import answer_from_doc

app = FastAPI()

@app.post("/chat")
def chat_with_bot(message: str):
    return {"response": legal_chat(message)}

@app.post("/generate-doc")
def generate_legal_doc(data: dict):
    return {"document": generate_document(data)}

@app.post("/rag-query")
async def query_uploaded_file(file: UploadFile = File(...), question: str = ""):
    content = await file.read()
    return {"answer": answer_from_doc(content, question)}

