import os
import shutil
import hashlib
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ingestion.parse_documents import DocumentParser
from ingestion.chunk_text import TextChunker
from ingestion.extract_entities import EntityExtractor
from storage.vector_store import vector_store
from storage.knowledge_graph import kg_store
from rag.query_engine import RAGQueryEngine
from agents.rca_agent import RcaAgent

app = FastAPI(
    title="Unified Asset & Operations Brain API",
    description="Industrial Knowledge Intelligence & RCA Engine for ET-AI Hackathon",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class AskRequest(BaseModel):
    question: str

class RcaRequest(BaseModel):
    equipment_id: str

@app.get("/")
def read_root():
    return {
        "status": "online",
        "system": "Unified Asset & Operations Brain",
        "version": "1.0.0"
    }

@app.get("/api/stats")
def get_stats():
    stats = kg_store.get_stats()
    return {
        "status": "success",
        "data": stats
    }

@app.get("/api/documents")
def list_documents():
    docs = kg_store.get_all_documents()
    return {
        "status": "success",
        "data": docs
    }

@app.get("/api/entities")
def list_entities():
    entities = kg_store.get_all_entities()
    return {
        "status": "success",
        "data": entities
    }

@app.get("/api/entities/{entity_id}")
def get_entity_details(entity_id: str):
    triples = kg_store.get_entity_triples(entity_id)
    return {
        "status": "success",
        "entity_id": entity_id,
        "triples": triples
    }

@app.post("/api/ingest/initialize")
def initialize_sample_docs():
    """
    Ingests all synthetic/sample documents from the sample_documents folder
    """
    sample_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "sample_documents")
    if not os.path.exists(sample_dir):
        # Fallback to root directory if sample_documents doesn't exist
        sample_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    ingested_files = []
    for filename in os.listdir(sample_dir):
        if filename.endswith(".txt") and not filename.startswith("project_brief"):
            file_path = os.path.join(sample_dir, filename)
            
            # Parse document
            parsed = DocumentParser.parse_file(file_path)
            doc_id = hashlib.md5(filename.encode()).hexdigest()[:12]

            # Chunk document
            chunks = TextChunker.chunk_document(
                doc_id=doc_id,
                filename=filename,
                text=parsed['text']
            )

            # Store in Vector Database
            vector_store.add_chunks(chunks)

            # Extract Entities & Triples into Knowledge Graph
            EntityExtractor.process_and_store(
                doc_id=doc_id,
                filename=filename,
                text=parsed['text']
            )

            # Store document record
            kg_store.add_document(
                doc_id=doc_id,
                filename=filename,
                doc_type=parsed['doc_type'],
                chunk_count=len(chunks)
            )

            ingested_files.append({
                "doc_id": doc_id,
                "filename": filename,
                "type": parsed['doc_type'],
                "chunks": len(chunks)
            })

    return {
        "status": "success",
        "message": f"Successfully ingested {len(ingested_files)} sample documents",
        "ingested": ingested_files,
        "stats": kg_store.get_stats()
    }

@app.post("/api/ingest/file")
async def upload_file(file: UploadFile = File(...)):
    temp_dir = os.path.join(os.path.dirname(__file__), "temp")
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, file.filename)

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        parsed = DocumentParser.parse_file(temp_path)
        doc_id = hashlib.md5(file.filename.encode()).hexdigest()[:12]

        chunks = TextChunker.chunk_document(
            doc_id=doc_id,
            filename=file.filename,
            text=parsed['text']
        )

        vector_store.add_chunks(chunks)
        EntityExtractor.process_and_store(doc_id=doc_id, filename=file.filename, text=parsed['text'])
        kg_store.add_document(doc_id=doc_id, filename=file.filename, doc_type=parsed['doc_type'], chunk_count=len(chunks))

        os.remove(temp_path)
        return {
            "status": "success",
            "filename": file.filename,
            "doc_id": doc_id,
            "chunks_created": len(chunks)
        }
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ask")
def ask_question(req: AskRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    res = RAGQueryEngine.answer_question(req.question)
    return {
        "status": "success",
        "data": res
    }

@app.post("/api/rca")
def perform_rca(req: RcaRequest):
    if not req.equipment_id.strip():
        raise HTTPException(status_code=400, detail="Equipment ID cannot be empty")
    res = RcaAgent.analyze_equipment(req.equipment_id)
    return {
        "status": "success",
        "data": res
    }
