Entries (chronological, short)

- numpy dtype / binary incompatibility warnings
  - Request: Diagnose "numpy.dtype size changed..." and suggest fixes.
  - Action: Provided debugging steps and environment-recreation guidance.

- ModuleNotFoundError: No module named 'numpy'
  - Request: How to fix missing numpy.
  - Action: Advised to install into the active interpreter / venv and verify interpreter selection.

- Unicode / decoding and txt handling
  - Request: Ensure uploaded .txt files are handled robustly.
  - Action: Added robust_decode() with utf-8 / latin-1 / replace fallbacks; recommended chardet/charset-normalizer if needed.

- Chunking + Retrieval + RAG pipeline
  - Request: Chunk large documents, implement retrieval over chunks, generate grounded answers with a language model.
  - Action: Initially proposed a pure-Python embedding + cosine retrieval approach (no numpy) and then accepted user's preference to use LangChain + Chroma.

- LangGraph + Chroma implementation
  - Request: Use the notebook approach (langgraph_chroma_retreiver.ipynb) exactly.
  - Action: Implemented minimal LangChain / LangGraph style RAG flow; later constrained to minimal additions per your request.

- API model errors and auth
  - Request: Error 400 invalid model name and later 401 Authentication Error.
  - Action: Replaced invalid model names, exposed API_KEY -> OPENAI_API_KEY for LangChain, and advised verifying environment variables and restarting Streamlit.

- Support for PDF extraction
  - Request: Accept .pdf uploads and extract text.
  - Action: Added PDF handling using pypdf (fallback to PyPDF2). Added instructions to install pypdf if missing.

- Multiple-file uploads & cross-document retrieval
  - Request: Allow uploading multiple documents and interact with all in the chat.
  - Action: Modified upload UI to accept multiple files, index each into a per-file Chroma collection, aggregate retrieval across collections, deduplicate retrieved chunks.

- Chroma collection name validation
  - Request: Fix InvalidArgumentError due to collection name containing disallowed chars.
  - Action: Added sanitize_collection_name() to produce valid collection names.

- Minimal / non-invasive edits policy
  - Request: Do not modify current file much; add only what is necessary.
  - Action: All code patches were kept minimal and additive where possible; cache vectorstores in st.session_state.

- README and documentation
  - Request: Include run instructions, feature overview, and config changes.
  - Action: Added README.md with quick start, env var notes, and list of code changes.

- Ref-log and GenAI disclosure
  - Request: Record external tools and GenAI usage.
  - Action: Created this ref-log and a short ref-log.md recording libraries used and that GenAI (assistant) produced code patches and docs as part of the workflow.

GenAI usage summary
- Generated code patches, debugging steps, README improvements and the ref-log itself.
- Rationale: accelerate RAG pipeline scaffolding, integrate LangChain/Chroma, and produce concise developer documentation.
