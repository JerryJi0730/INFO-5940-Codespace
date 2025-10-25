import streamlit as st
import os
from openai import OpenAI
from os import environ
# --- ADDED: LangChain + Chroma imports for minimal RAG (kept small) ---
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from PyPDF2 import PdfReader
import io

client = OpenAI(
	api_key=os.environ["API_KEY"],
	base_url="https://api.ai.it.cornell.edu",
)

st.title("📝 File Q&A with OpenAI")
# allow multiple uploads
uploaded_files = st.file_uploader("Upload one or more articles", type=("txt", "md", "pdf"), accept_multiple_files=True)

question = st.chat_input(
    "Ask something about the article",
    disabled=not uploaded_files,
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Ask something about the article"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- ADDED: small robust decode + chunking helpers ---
def robust_decode(raw: bytes) -> str:
    try:
        return raw.decode("utf-8")
    except Exception:
        try:
            return raw.decode("latin-1")
        except Exception:
            return raw.decode("utf-8", errors="replace")

def make_langchain_documents(text: str, chunk_size: int = 200, chunk_overlap: int = 0):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    parts = splitter.split_text(text)
    return [Document(page_content=p) for p in parts]

CHAT_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "openai.text-embedding-3-large")

if question and uploaded_files:
    # ensure session dict for vectorstores
    if "vectorstores" not in st.session_state:
        st.session_state["vectorstores"] = {}

    # index each uploaded file (if not already indexed in session)
    for uploaded_file in uploaded_files:
        raw = uploaded_file.read()
        # extract text
        if uploaded_file.name.lower().endswith(".pdf"):
            try:
                reader = PdfReader(io.BytesIO(raw))
                pages = []
                for p in reader.pages:
                    try:
                        pages.append(p.extract_text() or "")
                    except Exception:
                        pages.append("")
                file_content = "\n\n".join(pages)
            except Exception as e:
                file_content = ""
                st.error(f"Failed to extract PDF text from {uploaded_file.name}: {e}")
        else:
            try:
                file_content = robust_decode(raw)
            except NameError:
                file_content = raw.decode("utf-8", errors="replace")

        # prepare collection name and session key
        collection_name = f"doc_{uploaded_file.name.replace(' ', '_')}"
        vs_key = f"vectorstore:{collection_name}"

        # index if missing
        if vs_key not in st.session_state["vectorstores"]:
            docs = make_langchain_documents(file_content, chunk_size=200, chunk_overlap=50)
            with st.spinner(f"Indexing {uploaded_file.name} into Chroma..."):
                emb = OpenAIEmbeddings(model="openai.text-embedding-3-large", openai_api_key=os.environ.get("API_KEY"))
                vectorstore = Chroma.from_documents(documents=docs, embedding=emb, collection_name=collection_name)
                st.session_state["vectorstores"][vs_key] = vectorstore
                st.success(f"Indexed {len(docs)} chunks into Chroma collection '{collection_name}'")

    # aggregate vectorstores to query across all uploaded docs
    vectorstores = list(st.session_state["vectorstores"].values())

    # Append the user's question to the messages and show it
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    # Retrieve top-k relevant chunks across all vectorstores (simple per-store aggregation)
    k = 4
    per_store_k = max(1, k // max(1, len(vectorstores)))
    aggregated = []
    for vs in vectorstores:
        try:
            docs = vs.similarity_search(question, k=per_store_k)
        except Exception:
            retriever = vs.as_retriever(search_type="similarity", search_kwargs={"k": per_store_k})
            docs = retriever.get_relevant_documents(question)
        aggregated.extend(docs)

    # deduplicate preserving order by page_content
    seen = set()
    retrieved_docs = []
    for d in aggregated:
        key = (d.page_content or "").strip()
        if not key:
            continue
        if key in seen:
            continue
        seen.add(key)
        retrieved_docs.append(d)
        if len(retrieved_docs) >= k:
            break

    # Build context for system prompt using retrieved chunks
    context_text = "\n\n---\n\n".join(d.page_content for d in retrieved_docs)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="openai.gpt-4o",  # Change this to a valid model name
            messages=[
                {"role": "system", "content": f"Here's the content of the file:\n\n{file_content}"},
                 {"role": "system", "content": f"Context:\n\n{context_text}"},
                *st.session_state.messages
            ],
            stream=True
        )
        response = st.write_stream(stream)

    # Append the assistant's response to the messages
    st.session_state.messages.append({"role": "assistant", "content": response})