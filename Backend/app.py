# Backend/main.py (app.py)
from dotenv import load_dotenv
import os

load_dotenv()  # Load the .env file
api_key = os.getenv("OPENAI_API_KEY")  # Access the key

from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tempfile
import time
import os
from typing import Optional

# Import local modules
from chatbot import legal_chat
from document_generator import generate_document
from Rag_engine import rag_query  # Changed to lowercase filename

# Initialize FastAPI

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for chat
class ChatQuery(BaseModel):
    message: str

# Chat endpoint
@app.post("/chat")
async def chat(query: ChatQuery):
    try:
        response = legal_chat(query.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Document generation endpoint
@app.post("/generate-doc")
async def generate_document_endpoint(
    partyA: str = Form(...),
    partyB: str = Form(...),
    doc_type: str = Form(...)
):
    try:
        data = {
            "type": doc_type,
            "partyA": partyA,
            "partyB": partyB
        }
        doc = generate_document(data)
        return {"document": doc}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# RAG query endpoint
@app.post("/rag-query")
async def rag_query_endpoint(
    file: UploadFile,
    question: str = Form(...)
):
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        # Process the document
        answer = rag_query(tmp_path, question)
        
        # Cleanup temporary file
        os.unlink(tmp_path)
        
        return {"answer": answer}
    except Exception as e:
        if tmp_path:
            os.unlink(tmp_path)
        raise HTTPException(status_code=500, detail=str(e))