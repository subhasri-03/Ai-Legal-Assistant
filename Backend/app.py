# Backend/main.py

from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time

app = FastAPI()

# Allow frontend to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatQuery(BaseModel):
    message: str

@app.post("/chat")
def chat(query: ChatQuery):
    return {"response": f"🔍 Here's a simple legal explanation for: {query.message}"}

@app.post("/generate-doc")
def generate_document(partyA: str = Form(...), partyB: str = Form(...), doc_type: str = Form(...)):
    doc = f"📝 This is a {doc_type} between {partyA} and {partyB}.\nTerms and conditions apply."
    return {"document": doc}

@app.post("/rag-query")
async def rag_query(file: UploadFile, question: str = Form(...)):
    # Simulate answer from document
    content = await file.read()
    time.sleep(1)  # simulate processing
    return {"answer": f"📄 Based on your document and question: '{question}', here is the answer."}

