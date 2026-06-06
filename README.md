# DocuMind - RAG Powered Document Q&A

An end-to-end Retrieval-Augmented Generation (RAG) pipeline built from scratch without high-level frameworks.

## What it does
Upload any PDF and ask questions about it. The system retrieves the most relevant sections and generates grounded answers using LLaMA3.

## Tech Stack
- **FastAPI** - REST API backend
- **ChromaDB** - Vector database for semantic search
- **Sentence Transformers** - Local embeddings (all-MiniLM-L6-v2)
- **Groq + LLaMA3** - LLM for answer generation
- **PyPDF2** - PDF text extraction

## Architecture
PDF Upload → Text Extraction → Chunking → Embeddings → ChromaDB

Question → Embed Question → Semantic Search → Top 3 Chunks → LLaMA3 → Answer

## API Endpoints
- `POST /upload` - Upload and ingest a PDF
- `POST /ask` - Ask a question about the document
- `GET /sources` - View ingested chunks

## Setup
1. Clone the repository
2. Create virtual environment and install dependencies:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
3. Add your Groq API key to `.env`:

GROQ_API_KEY=your_key_here

4. Run the server:
```bash
uvicorn main:app --reload
```
5. Visit `http://127.0.0.1:8000/docs` for Swagger UI