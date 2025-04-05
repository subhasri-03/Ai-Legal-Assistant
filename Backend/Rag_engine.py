from langchain.document_loaders import PyPDFLoader
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI

def answer_from_doc(file_bytes, question):
    # Save temp PDF
    with open("temp.pdf", "wb") as f:
        f.write(file_bytes)
    
    loader = PyPDFLoader("temp.pdf")
    documents = loader.load()

    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(documents, embeddings)
    chain = load_qa_chain(OpenAI(), chain_type="stuff")
    docs = db.similarity_search(question)
    result = chain.run(input_documents=docs, question=question)
    return result
