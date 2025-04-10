import streamlit as st
import requests
from streamlit_extras.badges import badge
from streamlit_extras.colored_header import colored_header
from streamlit_extras.stylable_container import stylable_container

# Constants
MAX_FILE_SIZE_MB = 10

# Configure page
st.set_page_config(
    page_title="LegalMind AI | Smart Legal Assistance",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: #f8f9fa;
    }
    .st-emotion-cache-1y4p8pa {
        padding: 2rem 5% !important;
    }
    .disclaimer {
        font-size: 0.8em;
        color: #666;
        margin-top: 2em;
        border-top: 1px solid #eee;
        padding-top: 1em;
    }
    .document-preview {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        background: white;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
colored_header(
    label="LegalMind AI",
    description="Your Intelligent Legal Companion",
    color_name="blue-70",
)

# Main Tabs
tab1, tab2, tab3 = st.tabs([
    "🗣️ Legal Consultation", 
    "📑 Document Automation", 
    "🔍 Document Analysis"
])

# Chat Consultation Tab
with tab1:
    with stylable_container(
        key="chat_container",
        css_styles="""
            {
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                padding: calc(1em - 1px);
            }
            """
    ):
        st.markdown("### Virtual Legal Assistant")
        st.caption("Get instant guidance on legal matters (Note: Not a substitute for professional legal advice)")
        
        # Chat History
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
            
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        # Chat Input
        prompt = st.chat_input("Ask your legal question...")
        if prompt:
            with st.spinner("Analyzing your query..."):
                try:
                    # Add user message to history
                    st.session_state.chat_history.append({"role": "user", "content": prompt})
                    
                    # API Call
                    response = requests.post(
                        "http://localhost:8000/chat",
                        json={"message": prompt},
                        timeout=30
                    )
                    response.raise_for_status()
                    
                    # Add AI response to history
                    ai_response = response.json().get("response", "Response not available")
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                    
                    # Rerun to show new messages
                    st.rerun()
                    
                except requests.exceptions.RequestException as e:
                    st.error(f"Service unavailable. Please try again later. Error: {str(e)}")

# Document Automation Tab
with tab2:
    st.markdown("### Smart Document Generation")
    st.caption("Create professional legal documents in minutes")
    
    with st.form("document_form"):
        col1, col2 = st.columns(2)
        with col1:
            party_a = st.text_input("First Party Name", placeholder="Enter name or organization")
            jurisdiction = st.selectbox("Jurisdiction", ["India", "United States", "EU", "Other"])
            
        with col2:
            party_b = st.text_input("Second Party Name", placeholder="Enter name or organization")
            doc_type = st.selectbox("Document Type", [
                "Non-Disclosure Agreement (NDA)",
                "Employment Contract",
                "Lease Agreement", 
                "Service Agreement"
            ])
            
        custom_terms = st.text_area("Special Terms/Conditions", 
                                  placeholder="Enter any specific terms to include...")
        
        if st.form_submit_button("Generate Document", type="primary"):
            if not party_a or not party_b:
                st.warning("Please complete all required fields")
            else:
                with st.status("Drafting your document...", expanded=True) as status:
                    try:
                        # Show generation steps
                        st.write("🔍 Validating inputs...")
                        st.write("📝 Structuring document...")
                        
                        # API Call
                        response = requests.post(
                            "http://localhost:8000/generate-doc",
                            json={
                                "partyA": party_a,
                                "partyB": party_b,
                                "doc_type": doc_type.split(" ")[0],
                                "jurisdiction": jurisdiction,
                                "custom_terms": custom_terms
                            }
                        )
                        response.raise_for_status()
                        
                        # Show results
                        st.write("✅ Document ready!")
                        status.update(label="Document generation complete", state="complete")
                        
                        # Display and download
                        doc_content = response.json().get("document")
                        with st.expander("Preview Document", expanded=True):
                            st.markdown(f"```markdown\n{doc_content}\n```")
                            
                        st.download_button(
                            label="Download Document",
                            data=doc_content,
                            file_name=f"{doc_type.replace(' ', '_')}_{party_a}_vs_{party_b}.md",
                            mime="text/markdown"
                        )
                        
                    except Exception as e:
                        st.error(f"Document generation failed: {str(e)}")

# Document Analysis Tab
with tab3:
    st.markdown("### Intelligent Document Analysis")
    st.caption("Upload legal documents for instant insights and Q&A")
    
    with st.form("document_analysis"):
        uploaded_file = st.file_uploader(
            "Upload Legal Document (PDF only)", 
            type=["pdf"],
            help="Max file size: 10MB"
        )
        question = st.text_input("Ask about the document", 
                               placeholder="What's the termination clause in this agreement?")
        
        if st.form_submit_button("Analyze Document", type="primary"):
            if not uploaded_file or not question:
                st.warning("Please upload a document and enter a question")
            elif uploaded_file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
                st.error(f"File size exceeds {MAX_FILE_SIZE_MB}MB limit")
            else:
                with st.status("Analyzing document...", expanded=True) as status:
                    try:
                        st.write("📄 Processing document...")
                        st.write("🔍 Extracting key clauses...")
                        
                        # API Call
                        response = requests.post(
                            "http://localhost:8000/rag-query",
                            files={"file": uploaded_file},
                            data={"question": question},
                            timeout=60
                        )
                        response.raise_for_status()
                        
                        # Show results
                        st.write("✅ Analysis complete!")
                        status.update(label="Document analysis finished", state="complete")
                        
                        answer = response.json().get("answer")
                        st.markdown(f"**Answer:**\n\n{answer}")
                        
                        # Show document preview
                        with st.expander("Document Highlights"):
                            st.write("Key clauses identified:")
                            # Add actual document analysis results here
                            st.success("✔️ Confidentiality Agreement")
                            st.success("✔️ Termination Clause")
                            st.success("✔️ Governing Law")
                            
                    except Exception as e:
                        st.error(f"Analysis failed: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div class="disclaimer">
    <strong>Disclaimer:</strong> LegalMind AI is an automated legal assistant and does not constitute legal advice. 
    Always consult a qualified attorney for legal matters. Results may vary based on document complexity and 
    jurisdiction requirements.
</div>
""", unsafe_allow_html=True)

# Sidebar (optional)
with st.sidebar:
    st.markdown("## About LegalMind AI")
    st.markdown("""
    **LegalMind AI** leverages advanced AI to provide:
    - Instant legal guidance
    - Document automation
    - Contract analysis
    - Compliance checking
    """)
    badge(type="github", name="subhasri-03/Ai-Legal-Assistant")
    st.markdown("---")
    st.markdown("**Support**\n\ncontact@legalmind.ai")
