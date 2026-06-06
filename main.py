import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ingest import ingest_document
from retriever import retrieve_and_answer

app = FastAPI(title="DocuMind - RAG Powered Document Q&A")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "DocuMind API is running"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    upload_dir = "./uploaded_files"
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = f"{upload_dir}/{file.filename}"
    
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    ingest_document(file_path)
    
    return {"message": f"{file.filename} uploaded and ingested successfully"}

@app.post("/ask")
async def ask_question(payload: dict):
    question = payload.get("question")
    
    if not question:
        return {"error": "No question provided"}
    
    result = retrieve_and_answer(question)
    
    return {
        "question": question,
        "answer": result["answer"],
        "sources": result["sources"]
    }

@app.get("/sources")
async def get_sources():
    results = collection.get()
    return {"total_chunks": len(results["ids"])}