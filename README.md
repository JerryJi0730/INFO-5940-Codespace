# File Q&A (Streamlit) — README

Overview
- Small Streamlit app that indexes uploaded text and PDF documents, stores chunk embeddings in Chroma, and answers user questions with a retrieval-augmented generation (RAG) workflow.
- Uses OpenAI-compatible API for embeddings and chat completions (via OpenAI SDK + LangChain helpers + Chroma).
- Supports multiple-file upload and interactive chat history in the Streamlit UI.

Features
- Upload one or more .txt / .md / .pdf files.
- Automatic text extraction from PDFs.
- Chunking of documents (configurable chunk size / overlap in the code).
- Indexing into a Chroma vector store (per uploaded document).
- Cross-document retrieval and concise answers from a chat model.
- Session caching of indexed vectorstores to avoid re-indexing during the session.

Quick start (devcontainer / Debian bookworm)
1. Open the devcontainer workspace in VS Code (already set up for this repo).
2. Install Python dependencies:
   - From the workspace root:
     - python3 -m pip install --upgrade pip
     - pip3 install -r requirements.txt
   - If you get missing package errors, install these explicitly:
     - pip3 install chromadb pypdf langchain chroma-langchain
     - (The project uses langchain_openai / langchain_chroma wrappers — ensure matching packages are present.)
3. Ensure API keys and base URL are set in the environment the app runs in:
   - Example (Linux / devcontainer terminal):
     - export API_KEY="sk-...."           # preferred variable used by this app
   - Verify:
     - python3 -c "import os; print('API_KEY=', bool(os.environ.get('API_KEY')), 'OPENAI_API_KEY=', bool(os.environ.get('OPENAI_API_KEY')))"
4. Run the app:
   - streamlit run /workspaces/INFO-5940-Codespace/chat_with_pdf.py
   - The terminal will print the local URL (e.g., http://localhost:8501). In this devcontainer you can open it using:
     - "$BROWSER" http://localhost:8501

Configuration notes / environment
- The app reads API keys from API_KEY (primary) and exposes the same value to OPENAI_API_KEY for LangChain compatibility.
- Model selection:
  - CHAT_MODEL and EMBEDDING_MODEL can be set via environment variables OPENAI_MODEL and EMBEDDING_MODEL.
- Chroma:
  - Collections are created per uploaded file. Names are sanitized to meet Chroma naming rules.
  - The app currently uses in-memory or default Chroma configuration. To persist the DB, modify the Chroma initialization in the code to set persist_directory.

Changes made (code-level)
- chat_with_pdf.py:
  - Added robust file decoding helper (utf-8, latin-1, fallback).
  - Added PDF extraction (pypdf / PyPDF2).
  - Added chunking using RecursiveCharacterTextSplitter -> LangChain documents.
  - Added per-file Chroma indexing with OpenAIEmbeddings (indexing cached in st.session_state["vectorstores"]).
  - Sanitized Chroma collection names to satisfy allowed characters/length.
  - Enabled multiple file uploads and cross-document retrieval aggregation and deduplication.
  - Exposed OPENAI_API_KEY / OPENAI_BASE_URL environment variables for LangChain/OpenAI helper libs.
  - Minimal UI updates: preview (first file), chat history preserved in session_state.
- No other configuration files were overwritten. If you keep requirements in sync you should be able to install needed libs.

Troubleshooting
- Authentication (401):
  - Confirm API_KEY / OPENAI_API_KEY present in the environment used to launch Streamlit.
  - Restart Streamlit after changing env vars.
- Missing libraries:
  - ModuleNotFoundError: install via pip3 install pypdf chromadb langchain langchain_openai langchain_chroma
- Chroma collection name errors:
  - Filenames with special characters may fail — the app sanitizes names but if you still see errors, rename files to simple ASCII alphanumerics or update sanitize function.
- numpy dtype / binary incompatibility:
  - Recreate venv or reinstall numpy and binary dependencies (see earlier notes in repo issues).
- PDF text extraction blank / partial:
  - Some PDFs have images or scanned pages — use OCR prior to upload if needed.

Developer tips
- To re-index a file during the same session, refresh the Streamlit session or remove the session entry st.session_state["vectorstores"][vs_key] manually.
- To persist Chroma across sessions, update the Chroma initialization to set a persist_directory and call persist on the client.

If you want, I can produce a minimal requirements.txt diff or a small helper script to validate environment variables before running.