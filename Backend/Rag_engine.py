from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
import os

def rag_query(file_path: str, question: str):
    try:
        # Load document
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        
        # Create embeddings
        embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        
        # Create vector store
        db = FAISS.from_documents(pages, embeddings)
        
        # Create QA chain
        qa = RetrievalQA.from_chain_type(
            llm=OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY")),
            chain_type="stuff",
            retriever=db.as_retriever()
        )
        
        return qa.invoke(question)['result']
    except Exception as e:
        print(f"RAG Error: {str(e)}")
        return "Could not process document"
