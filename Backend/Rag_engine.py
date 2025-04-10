from langchain_community.document_loaders import PyPDFLoader  # Updated import
from langchain_community.embeddings import OpenAIEmbeddings  # Updated import
from langchain_community.vectorstores import FAISS  # Updated import
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI  # For OpenAI LLM integration
import os

def rag_query(file_path: str, question: str):
    # Load document
    loader = PyPDFLoader(file_path)
    pages = loader.load()

    # Create embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    
    # Create vector store
    db = FAISS.from_documents(pages, embeddings)
    
    # Create QA chain
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY")),  # Updated LLM initialization
        chain_type="stuff",
        retriever=db.as_retriever()
    )
    
    return qa.run(question)
