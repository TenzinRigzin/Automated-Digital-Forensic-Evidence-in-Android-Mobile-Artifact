import os
import streamlit as st
from io import BytesIO
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

st.set_page_config(page_title="Local Intelligence Hub", layout="wide")
st.title("📂 Local Evidence Chatbot & Reporting Tool")

INPUT_DIR = "./data_input"
DB_DIR = "./chroma_db"
os.makedirs(INPUT_DIR, exist_ok=True)

# Cache resource generation so it doesn't freeze the page on load
@st.cache_resource
def load_heavy_models():
    with st.spinner("Downloading embedding model on first run... Please wait."):
        embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    with st.spinner("Connecting to local Ollama server..."):
        llm_model = ChatOllama(model="llama3", temperature=0.0)
        
    return embeddings_model, llm_model

# Load cached instances
embeddings, local_llm = load_heavy_models()

# Increase 'k' so we have a wider selection to locate the real top rows
if os.path.exists(DB_DIR):
    vector_store = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    base_retriever = vector_store.as_retriever(search_kwargs={"k": 8})
else:
    vector_store = Chroma.from_texts(["Initial setup context"], embeddings, persist_directory=DB_DIR)
    base_retriever = vector_store.as_retriever(search_kwargs={"k": 1})

# Enhanced prompt forcing an absolute halt when newest lines are found
system_prompt = (
    "You are a strict data auditor inspecting real-time messaging logs.\n"
    "CRITICAL CHRONOLOGY RULE:\n"
    "1. The provided context fragments are sorted by row index. Fragments containing low row markers "
    "(e.g., row_id 1, row 2, line 5) represent the LATEST, most recent mobile information.\n"
    "2. If you find the answer regarding the latest logs or recent items within these top-priority fragments, "
    "focus ONLY on that. You are explicitly ordered to IGNORE older trailing database rows (like row 2450+).\n"
    "3. Do not scan, summarize, or look at remaining context once the most recent target event is identified.\n\n"
    "Context Fragments:\n{context}"
)

prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{input}")])
qa_chain = create_stuff_documents_chain(local_llm, prompt)

# --- NEW CHRONOLOGICAL INTERCEPT ENGINE ---
def chronological_rag_invoke(query_text):
    # 1. Pull semantic matches from database
    docs = base_retriever.invoke(query_text)
    
    # Helper to scan text and extract numerical row order
    def extract_row_number(doc):
        content = doc.page_content.lower()
        # Look for patterns like 'row: 1', 'row 1', 'line 1'
        for i in range(1, 100):
            if f"row {i}" in content or f"line {i}" in content or f"row_id {i}" in content:
                return i
        return 9999  # Send old unmatched rows (like 2452) to the absolute bottom

    # 2. Sort documents so Row 1 is forced to the front
    sorted_docs = sorted(docs, key=extract_row_number)
    
    # 3. Early Termination Optimization: Drop older rows if latest rows are matched
    optimized_docs = []
    for doc in sorted_docs:
        optimized_docs.append(doc)
        # If we successfully captured a fresh log (Row 1-50), trigger an early stop.
        # This completely drops rows like 2452 from being processed or scanned by the LLM.
        if extract_row_number(doc) < 50:
            break
            
    # 4. Fire structured parameters directly to LLM chain
    response = qa_chain.invoke({"input": query_text, "context": optimized_docs})
    return response

def generate_pdf(text_content):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    story = [Paragraph("Automated Data Analysis Report", ParagraphStyle('Title', parent=styles['Heading1'], fontSize=24, spaceAfter=20)), Spacer(1, 12)]
    for paragraph in text_content.split('\n\n'):
        if paragraph.strip():
            story.append(Paragraph(paragraph.replace("**", "").replace("*", ""), ParagraphStyle('Body', parent=styles['BodyText'], fontSize=11, leading=16, spaceAfter=10)))
    doc.build(story)
    buffer.seek(0)
    return buffer

def generate_excel(text_content):
    buffer = BytesIO()
    wb = Workbook()
    ws = wb.active
    ws.title = "Analysis Report"
    ws['A1'], ws['B1'] = "Report Section", "Extracted Analysis & Evidence"
    row_num = 2
    for line in [l.strip() for l in text_content.split('\n') if l.strip()]:
        if line.startswith('#') or line.endswith(':'):
            ws.cell(row=row_num, column=1, value=line.replace('#', '').strip())
        else:
            ws.cell(row=row_num, column=2, value=line)
            row_num += 1
    wb.save(buffer)
    buffer.seek(0)
    return buffer

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_query := st.chat_input("Ask a question about your extracted evidence..."):
    with st.chat_message("user"): st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    with st.chat_message("assistant"):
        with st.spinner("Scanning database records using chronological priority..."):
            try:
                # Use our new chronological intercept call here
                answer = chronological_rag_invoke(user_query)
            except Exception as e:
                answer = f"Error communicating with local LLM. Details: {str(e)}"
            st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})

st.sidebar.header("📋 Export Operations")
if st.session_state.messages:
    full_chat_log = "".join([f"### {msg['role'].upper()}:\n{msg['content']}\n\n" for msg in st.session_state.messages])
    st.sidebar.download_button("📥 Download PDF Report", data=generate_pdf(full_chat_log), file_name="evidence_analysis.pdf", mime="application/pdf")
    st.sidebar.download_button("📥 Download Excel Spreadsheet", data=generate_excel(full_chat_log), file_name="evidence_matrix.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
else:
    st.sidebar.info("Ask questions to compile data for export.")
