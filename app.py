import time
import streamlit as st
import fitz  # PyMuPDF
import ollama
import chromadb
from logger import init_monitor_db, log_telemetry, log_feedback

# Initialize monitoring SQLite database
init_monitor_db()

# Initialize Persistent Vector Database
PERSIST_DIR = "./course_tutor_db"
chroma_client = chromadb.PersistentClient(path=PERSIST_DIR)
collection = chroma_client.get_or_create_collection(name="pdf_course_materials")

st.set_page_config(page_title="Free Local Course Tutor", page_icon="📚")
st.title("📚 Course Tutor (100% Local & Free)")

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    pages = []
    for page_num in range(len(doc)):
        text = doc[page_num].get_text("text")
        if text.strip():
            pages.append({"page": page_num + 1, "content": text})
    return pages

def index_pdf_material(pages, filename):
    for item in pages:
        response = ollama.embeddings(
            model="nomic-embed-text", 
            prompt=item["content"]
        )
        embedding = response["embedding"]
        doc_id = f"{filename}_page_{item['page']}"
        collection.upsert(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[item["content"]],
            metadatas=[{"source": filename, "page": item["page"]}]
        )

# Sidebar Interface
with st.sidebar:
    st.header("Course Material Manager")
    uploaded_file = st.file_uploader("Upload Course PDF or Slides", type=["pdf"])
    
    if uploaded_file and st.button("Index Material"):
        with st.spinner("Indexing into local SQLite database..."):
            pages = extract_text_from_pdf(uploaded_file)
            index_pdf_material(pages, uploaded_file.name)
            st.success(f"Successfully saved '{uploaded_file.name}' to SQLite DB!")

    st.markdown("---")
    st.caption("⚡ Powered by Ollama (llama3.2 + nomic-embed-text) & SQLite")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a question about your course material..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 1. Retrieval Latency Benchmark
    start_retrieval = time.time()
    query_embed = ollama.embeddings(
        model="nomic-embed-text", 
        prompt=prompt
    )["embedding"]

    results = collection.query(query_embeddings=[query_embed], n_results=3)
    retrieval_latency = (time.time() - start_retrieval) * 1000  # ms
    
    context_chunks = []
    if results and results["documents"]:
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            context_chunks.append(f"[Source: {meta['source']}, Page {meta['page']}]:\n{doc}")
    
    context_text = "\n\n".join(context_chunks)

    system_instruction = (
        "You are an expert, encouraging Course Tutor. Answer the student's question "
        "using ONLY the provided course context below. Always mention which slide/page "
        "the information comes from. If the context doesn't contain the answer, say "
        "'This specific topic wasn't covered in the uploaded course material.'\n\n"
        f"--- COURSE CONTEXT ---\n{context_text}"
    )

    # 2. Generation Latency Benchmark
    start_generation = time.time()
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        stream = ollama.chat(
            model="llama3.2",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )

        for chunk in stream:
            full_response += chunk["message"]["content"]
            response_placeholder.markdown(full_response + "▌")
            
        response_placeholder.markdown(full_response)
        
    generation_latency = (time.time() - start_generation) * 1000  # ms
    
    # 3. Log Telemetry Data
    log_id = log_telemetry(retrieval_latency, generation_latency, len(prompt), len(full_response))
    st.session_state.messages.append({"role": "assistant", "content": full_response})