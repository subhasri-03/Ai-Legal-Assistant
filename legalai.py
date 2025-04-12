import streamlit as st
import requests

# Configure page
st.set_page_config(page_title="AI Legal Assistant", layout="centered")
st.title("⚖️ AI Legal Assistant")
st.caption("An AI-powered assistant to simplify legal tasks")

# Create tabs
tab1, tab2, tab3 = st.tabs(["💬 Chatbot", "📄 Generate Document", "📁 Ask from Document"])

# Chatbot Tab
with tab1:
    st.header("Chat with AI Legal Assistant")
    message = st.text_area("Ask a legal question", key="chat_input")
    
    if st.button("Get Answer", key="chat"):
        if message.strip():
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(
                        "http://localhost:8000/chat",
                        json={"message": message},
                        timeout=30
                    )
                    if response.status_code == 200:
                        st.success(response.json().get("response", "No response received"))
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")
        else:
            st.warning("Please enter a question")

# Document Generation Tab
with tab2:
    st.header("Generate Legal Document")
    partyA = st.text_input("Party A")
    partyB = st.text_input("Party B")
    doc_type = st.selectbox("Document Type", ["NDA", "Rental Agreement"])
    
    if st.button("Generate Document", key="docgen"):
        if partyA and partyB:
            with st.spinner("Generating..."):
                try:
                    response = requests.post(
                        "http://localhost:8000/generate-doc",
                        data={
                            "partyA": partyA,
                            "partyB": partyB,
                            "doc_type": doc_type
                        },
                        timeout=30
                    )
                    if response.status_code == 200:
                        doc_content = response.json().get("document")
                        st.code(doc_content, language="markdown")
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")
        else:
            st.warning("Please enter both party names")

# Document Query Tab
with tab3:
    st.header("Ask a Question from Uploaded Document")
    uploaded_file = st.file_uploader("Upload a legal PDF document", type="pdf")
    doc_question = st.text_area("What would you like to ask from the document?")
    
    if st.button("Ask", key="ragquery"):
        if uploaded_file and doc_question.strip():
            with st.spinner("Processing document..."):
                try:
                    files = {"file": uploaded_file}
                    response = requests.post(
                        "http://localhost:8000/rag-query",
                        files=files,
                        data={"question": doc_question},
                        timeout=60
                    )
                    if response.status_code == 200:
                        st.success(response.json().get("answer", "No answer received"))
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")
        else:
            st.warning("Upload a PDF and type a question")

# Simple Footer
st.markdown("---")
st.caption("Note: This is an AI assistant and does not constitute legal advice")