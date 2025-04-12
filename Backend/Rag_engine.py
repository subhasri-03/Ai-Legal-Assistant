from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from openai import OpenAI
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def rag_query(file_path: str, question: str):
    try:
        # Load document
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        
        # Create embeddings
        embeddings = OpenAIEmbeddings()
        
        # Create vector store
        db = FAISS.from_documents(pages, embeddings)
        
        # Create QA chain
        qa = RetrievalQA.from_chain_type(
            llm=client,
            chain_type="stuff",
            retriever=db.as_retriever()
        )
        
        return qa.invoke(question)['result']
    except Exception as e:
        return f"⚠️ Document Analysis Error: {str(e)}"
