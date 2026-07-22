# Northgate Energy — Industrial Knowledge Intelligence & RCA Engine

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.0-61DAFB.svg)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-5.0-646CFF.svg)](https://vitejs.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An enterprise-grade **Industrial Knowledge Intelligence Platform & Root Cause Analysis (RCA) Engine** built for heavy industrial facilities (Northgate Refinery — 15.2 MMTPA capacity).

This platform ingests heterogeneous engineering documents (P&ID schematics, maintenance work orders, annual quality inspection reports, standard operating procedures, and safety specs) into a hybrid **Vector Database** and **SQLite Knowledge Graph**, making collective industrial intelligence queryable, actionable, and groundable.

---

## 🌟 Key Architectural Features

1. **Multi-Format Ingestion Pipeline**: Parsers for TXT, PDF inspection manuals, and CSV/XLSX spreadsheets.
2. **Dual-Layer Knowledge Storage**:
   - **Vector Store**: Cosine-similarity vector database for semantic chunk retrieval.
   - **SQLite Knowledge Graph**: Relational triples store (`MENTIONS_EQUIPMENT`, `SERVICED_UNDER`, `INSPECTED_IN`, `GOVERNED_BY`) tracking relationships between equipment, work orders, parts, and engineers.
3. **Expert RAG Copilot**: Grounded question-answering engine returning plain-English responses alongside clickable, verified source document citations.
4. **Maintenance & RCA Agent**: Extracts chronological operational failure timelines and synthesizes root cause analysis reports, identifying recurring failure patterns (e.g. monsoon weather moisture ingress), violated SOPs, and preventative recommendations.
5. **Interactive Plant Blueprint & Piping Network**: Dynamic visual layout of plant zones (Zones A through F), grid coordinates, pipe rack bridges, and emergency muster points.
6. **Domain Guardrails**: Built-in intent filtering that restricts answers to plant operations and safety protocols while refusing out-of-scope queries.

---

## 🏗️ System Architecture

```
TIER 1 — Data Sources
  ├── Engineering Drawings & Manuals (P&IDs, PDFs, Spreadsheets)
  └── Maintenance & Inspection Logs (WO logs, OISD quality reports)
        ↓
TIER 2 — Ingestion & Processing
  ├── Document Parsing & Text Cleaning (PDF / CSV / TXT)
  ├── Word-Bounded Text Chunking
  └── Entity & Relational Triples Extraction
        ↓
TIER 3 — Dual Storage Layer
  ├── Vector Database (Semantic Chunk Search)
  └── Knowledge Graph (SQLite Entity Triples Table)
        ↓
TIER 4 — Intelligence & Reasoning Layer
  ├── Hybrid Vector + Knowledge Graph Retriever
  ├── Expert RAG Query Engine (Cited Answers)
  └── Maintenance & RCA Agent (Timeline & Root Cause Synthesis)
        ↓
TIER 5 — Frontend Dashboard
  └── React + Vite Industrial Dark Mode UI
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- Node.js 18+ & npm

### 1. Backend Setup (FastAPI)
```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server (runs on http://127.0.0.1:8000)
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

### 2. Frontend Setup (React + Vite)
```bash
# Navigate to frontend directory
cd frontend

# Install packages
npm install

# Start Vite dev server (runs on http://127.0.0.1:5173)
npm run dev -- --port 5173
```

---

## 📁 Repository Structure

```
industrial-knowledge-ai/
├── backend/
│   ├── agents/
│   │   └── rca_agent.py          # Maintenance & Root Cause Analysis Agent
│   ├── api/
│   │   └── main.py               # FastAPI server REST endpoints
│   ├── ingestion/
│   │   ├── parse_documents.py    # Document parsers (PDF, CSV, XLSX, TXT)
│   │   ├── chunk_text.py         # Text chunking
│   │   └── extract_entities.py   # Entity & triple extractor
│   ├── llm/
│   │   └── llm_provider.py       # LLM provider with domain guardrails
│   ├── rag/
│   │   ├── retriever.py          # Hybrid vector + Knowledge Graph retriever
│   │   └── query_engine.py       # RAG answer generator with citations
│   ├── storage/
│   │   ├── vector_store.py       # Vector database
│   │   └── knowledge_graph.py    # SQLite Knowledge Graph triples store
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.jsx        # Navigation sidebar & facility status
│   │   │   ├── Dashboard.jsx      # High-level overview & risk metrics
│   │   │   ├── ChatCopilot.jsx    # RAG Copilot chat interface
│   │   │   ├── RcaAgent.jsx       # Maintenance & RCA agent module
│   │   │   ├── PlantMap.jsx       # Interactive blueprint map & zones
│   │   │   └── DocumentManager.jsx# Document catalog & Knowledge Graph viewer
│   │   ├── App.jsx
│   │   └── index.css
│   └── package.json
├── PDF_GUIDES/                    # Formatted PDF user manuals & question guides
├── sample_documents/              # 10 master refinery documents
├── USER_MANUAL.md                 # Step-by-step user guide
└── README.md
```

---

## 📄 Documentation & PDF Guides

All official project documentation and user manuals are available in the **`PDF_GUIDES/`** folder:
- **`01_Oil_Refinery_Construction_and_Working_Guide.pdf`**: Beginner-friendly guide explaining refinery operations and plant sections.
- **`02_30_Meaningful_Showcase_Questions_and_Answers.pdf`**: 30 showcase questions with answer previews across 6 categories.
- **`03_Project_Implementation_Plan.pdf`**: Technical implementation plan and database schemas.
- **`04_User_Manual_and_Project_Guide.pdf`**: Comprehensive user manual and demonstration guide.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
