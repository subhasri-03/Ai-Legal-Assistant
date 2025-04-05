import streamlit as st
import requests

st.set_page_config(page_title="AI Legal Assistant", layout="centered")
st.title("⚖️ AI Legal Assistant")
st.caption("An AI-powered assistant to simplify legal tasks.")

tab1, tab2, tab3 = st.tabs(["💬 Chatbot", "📄 Generate Document", "📁 Ask from Document"])

with tab1:
    st.header("Chat with AI Legal Assistant")
    message = st.text_area("Ask a legal question")
    if st.button("Get Answer", key="chat"):
        if message.strip():
            with st.spinner("Thinking..."):
                res = requests.post("http://localhost:8000/chat", data={"message": message})
                st.success(res.json().get("response", "No response received."))
        else:
            st.warning("Please enter a question.")

with tab2:
    st.header("Generate Legal Document")
    partyA = st.text_input("Party A")
    partyB = st.text_input("Party B")
    doc_type = st.selectbox("Document Type", ["NDA", "Rental Agreement"])
    if st.button("Generate Document", key="docgen"):
        if partyA and partyB:
            with st.spinner("Generating..."):
                res = requests.post("http://localhost:8000/generate-doc", data={
                    "partyA": partyA,
                    "partyB": partyB,
                    "doc_type": doc_type
                })
                st.code(res.json().get("document", "Failed to generate."), language="markdown")
        else:
            st.warning("Please enter both party names.")

with tab3:
    st.header("Ask a Question from Uploaded Document")
    uploaded_file = st.file_uploader("Upload a legal PDF document", type="pdf")
    doc_question = st.text_area("What would you like to ask from the document?")
    if st.button("Ask", key="ragquery"):
        if uploaded_file and doc_question.strip():
            with st.spinner("Processing document and retrieving answer..."):
                files = {"file": uploaded_file}
                data = {"question": doc_question}
                res = requests.post("http://localhost:8000/rag-query", files=files, data=data)
                st.success(res.json().get("answer", "No answer received."))
        else:
            st.warning("Upload a PDF and type a question.")
