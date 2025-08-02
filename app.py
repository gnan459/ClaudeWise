import streamlit as st
from utils.file_loader import load_file
from utils.clause_extractor import extract_clauses
from utils.clause_simplifier import simplify_clause
from utils.document_classifier import classify_document
from utils.ner_extractor import extract_entities

st.set_page_config(page_title="ClauseWise - Legal Document Analyzer", layout="wide")

st.title("📄 ClauseWise: AI-Powered Legal Document Analyzer")

# --- Upload Section ---
st.sidebar.header("Upload Legal Document")
uploaded_file = st.sidebar.file_uploader("Choose a file (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"])

# --- Feature Selection ---
st.sidebar.header("Select Features")
do_classify = st.sidebar.checkbox("Document Classification", value=True)
do_extract = st.sidebar.checkbox("Clause Extraction", value=True)
do_simplify = st.sidebar.checkbox("Clause Simplification", value=True)
do_ner = st.sidebar.checkbox("Entity Extraction", value=True)

if uploaded_file:
    with st.spinner("Reading document..."):
        text = load_file(uploaded_file)
    
    if not text:
        st.error("⚠️ Could not extract text from file.")
    else:
        st.success("✅ Document Loaded Successfully")

        # --- Classification ---
        if do_classify:
            st.subheader("📂 Document Type Classification")
            doc_type = classify_document(text)
            st.info(f"**Predicted Document Type:** {doc_type}")

        # --- Clause Extraction ---
        if do_extract:
            st.subheader("📌 Extracted Clauses")
            clauses = extract_clauses(text)
            for i, clause in enumerate(clauses):
                st.markdown(f"-->{clause}")
        clauses = extract_clauses(text)
        # --- RAG Chatbot ---
        st.header("💬 RAG Chatbot (Gemini-powered)")
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        user_query = st.text_input("Ask a question about your document:", key="rag_input")
        if user_query and clauses:
            # Simple retrieval: use all clauses as context (or select top-N relevant ones)
            # For a real RAG, you would embed and select most relevant clauses
            context = "\n".join(clauses)
            import google.generativeai as genai
            model = genai.GenerativeModel(model_name="gemini-2.5-flash")
            prompt = f"Context:\n{context}\n\nQuestion: {user_query}\nAnswer:"
            response = model.generate_content(prompt)
            answer = response.text.strip() if hasattr(response, 'text') else str(response)
            st.session_state.chat_history.append(("user", user_query))
            st.session_state.chat_history.append(("bot", answer))

        for speaker, msg in st.session_state.chat_history:
            st.markdown(f"{speaker.capitalize()}:** {msg}")

        # --- Clause Simplification ---
        if do_extract and do_simplify:
            st.subheader("✏️ Simplified Clauses")
            for i, clause in enumerate(clauses):
                with st.expander(f"Original Clause {i+1}"):
                    st.markdown(clause)
                    simplified = simplify_clause(clause)
                    st.success(f"**Simplified:** {simplified}")

        # --- Entity Extraction ---
        if do_ner:
            st.subheader("🧠 Extracted Legal Entities")
            entities = extract_entities(text)
            for entity_type, values in entities.items():
                st.markdown(f"**{entity_type.capitalize()}:** {', '.join(values)}")
else:
    st.info("📥 Upload a file from the sidebar to begin analysis.")
