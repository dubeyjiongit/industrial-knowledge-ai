# Project Brief: AI for Industrial Knowledge Intelligence
### Unified Asset & Operations Brain

> **Note on assumptions:** Plant type is set to **Oil Refinery** and the primary agentic module is set to **Maintenance & RCA Agent**. Both are easily swappable — see "Open Decisions" at the bottom if you want to change them.

---

## 1. Problem Statement (verbatim context)

**Theme:** Industrial Intelligence / Document Management / Knowledge Engineering / Quality

**Problem context:**
Large asset-intensive industries (refineries, steel plants, manufacturing) suffer from severe knowledge fragmentation:
- Professionals spend ~35% of working hours searching for information, clarifying instructions, or recreating documents that already exist somewhere in the organization.
- Large plants typically run 7–12 disconnected document systems: P&IDs and engineering drawings in one place, maintenance work orders in another, operating procedures in a third, inspection records in a fourth, regulatory submissions scattered across email.
- This fragmentation contributes to an estimated 18–22% of unplanned downtime in heavy industry, because maintenance teams make decisions without complete equipment history or failure-pattern context.
- A "knowledge cliff" is approaching: ~25% of experienced industrial engineers/operators will retire within the next decade, taking undocumented operational knowledge with them permanently.
- This is not just a file-management problem — it is a safety problem, a quality problem, and an operational efficiency problem that compounds over time.

**Challenge statement:**
Build an AI-powered Industrial Knowledge Intelligence platform that:
1. Ingests heterogeneous documents — engineering drawings, maintenance records, safety procedures, inspection reports, project files — across structured and unstructured formats.
2. Makes their collective intelligence queryable, actionable, and continuously updated.
3. Works at the point of need, across any device or function (including mobile for field technicians).

---

## 2. Scope for This Build (5-day hackathon, decided)

We are **not** building all five illustrative directions from the brief. We are building a focused core + one agentic module, to maximize the "Innovation" (25%) and "Business Impact" (25%) judging weight without overextending in 5 days.

### IN SCOPE (build this)
1. **Document Ingestion Pipeline** — parses PDFs, scanned forms, spreadsheets → clean text
2. **Chunking + Embedding + Vector Store** — semantic search over all ingested content
3. **Lightweight Knowledge Graph** — entity relationship triples (equipment ↔ documents ↔ people ↔ dates), NOT a full Neo4j graph — a simple relational table is enough
4. **Expert Knowledge Copilot (RAG chatbot)** — user asks a question in plain English, gets an answer with source citations and confidence, works on mobile-responsive UI
5. **Maintenance & RCA Agent** — analyzes maintenance history + inspection findings to surface patterns ("Pump 4B has failed 3 times, always during monsoon season — likely seal degradation") and suggest root causes / predictive maintenance flags

### OUT OF SCOPE (mention only as "future scope" in the deck — do NOT build)
- Full Computer Vision P&ID parsing (real diagram digitization is a multi-week problem)
- Compliance & Regulatory Intelligence module
- Lessons Learned & Failure Intelligence Engine (org-wide pattern mining)
- Real-time OEM/sensor integration

---

## 3. System Architecture (5 tiers)

```
TIER 1 — Data Sources
  ├── Drawings & documents (P&IDs, PDFs, spreadsheets, email)
  └── Logs & records (maintenance, inspection, safety data)
        ↓
TIER 2 — Ingestion & Processing
  ├── OCR & parsing         (extract clean text from PDFs / scanned docs)
  ├── Chunk & embed         (split into ~500-word chunks, generate embeddings)
  └── Entity extraction     (LLM-based: pull equipment IDs, dates, people, doc refs as JSON)
        ↓
TIER 3 — Knowledge Storage
  ├── Vector database       (ChromaDB — semantic search over chunks)
  └── Knowledge graph       (SQLite table of entity-relationship triples)
        ↓
TIER 4 — Intelligence Layer
  ├── RAG query engine      (retrieve relevant chunks + rank)
  ├── Agent modules         (Maintenance & RCA agent)
  └── LLM reasoning         (Claude API — generates final answer + citations)
        ↓
TIER 5 — Frontend
  └── Chat interface        (web + mobile-responsive, shows source citations)
```

---

## 4. Tech Stack

| Layer | Tool |
|---|---|
| Frontend | React |
| Backend / API | FastAPI (Python) or Node/Express |
| PDF/text parsing | `pdfplumber`, `PyPDF2` |
| OCR (scanned docs) | `pytesseract` |
| Embeddings | Claude/OpenAI embeddings API, or local `sentence-transformers` |
| Vector database | ChromaDB (local, free, zero setup) |
| Knowledge graph | SQLite (simple entity-relationship triples table — NOT Neo4j, too slow to set up in 5 days) |
| LLM (reasoning/generation/entity extraction) | Claude API |
| Agent logic | Custom Python module calling Claude with specialized prompts over retrieved maintenance data |

---

## 5. Folder Structure

```
industrial-knowledge-ai/
├── backend/
│   ├── ingestion/
│   │   ├── parse_documents.py      # OCR/PDF/spreadsheet parsing
│   │   ├── chunk_text.py           # splitting into chunks
│   │   └── extract_entities.py     # LLM-based entity extraction
│   ├── storage/
│   │   ├── vector_store.py         # ChromaDB wrapper
│   │   └── knowledge_graph.py      # entity relationship storage (SQLite)
│   ├── rag/
│   │   ├── retriever.py            # semantic search logic
│   │   └── query_engine.py         # RAG pipeline (retrieve + generate + cite)
│   ├── agents/
│   │   └── rca_agent.py            # Maintenance & RCA agent
│   ├── api/
│   │   └── main.py                 # FastAPI server, exposes endpoints
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/ChatUI.jsx
│   │   └── App.jsx
│   └── package.json
├── sample_documents/                # synthetic refinery documents (see section 6)
├── architecture_diagram.png
└── README.md
```

---

## 6. Sample Dataset Plan

Real industrial document datasets are not publicly available (proprietary/safety-sensitive). Strategy:

- **Synthetic documents (primary):** ~20–25 realistic refinery documents — maintenance logs, SOPs, safety procedures, inspection reports — with **consistent recurring equipment IDs and names across documents** (e.g. "Pump 4B" appears in a maintenance log, an inspection report, AND a safety procedure) so entity linking and knowledge graph connections are demonstrable.
- **Real numeric dataset (supporting credibility):** AI4I 2020 Predictive Maintenance dataset (UCI) — realistic sensor readings (temperature, torque, tool wear) + failure labels, usable to ground the RCA agent's pattern-finding in real-feeling data.

---

## 7. API Endpoints (minimum viable)

```
POST /ingest          → upload + process a document into the pipeline
POST /ask             → RAG query: { question } → { answer, sources[], confidence }
GET  /entities/:id    → knowledge graph lookup for a given equipment/entity
POST /rca             → Maintenance & RCA agent: { equipment_id } → { pattern_summary, likely_cause, recommendation }
```

---

## 8. Day-by-Day Build Plan

| Day | Focus |
|---|---|
| 1 | Lock scope, generate synthetic dataset (25 docs), set up repo structure |
| 2 | Build ingestion pipeline (parsing, chunking, embeddings → ChromaDB), basic entity extraction |
| 3 | Build RAG query engine + API endpoints, build lightweight knowledge graph (SQLite triples) |
| 4 | Build Maintenance & RCA agent module, build frontend chat UI, connect end-to-end |
| 5 | Testing with sample questions, bug fixes, polish UI, build architecture diagram, presentation deck, record demo video |

---

## 9. Deliverables Required

- Working Prototype (end-to-end: ingest → ask questions → get cited answers → RCA insights)
- Architecture Diagram
- Presentation Deck
- Demo Video

---

## 10. Judging Criteria (weight the build decisions accordingly)

| Criteria | Weight |
|---|---|
| Innovation | 25% |
| Business Impact | 25% |
| Technical Excellence | 20% |
| Scalability | 15% |
| User Experience | 15% |

**Implication for Antigravity:** Innovation + Business Impact = 50% of the score. Prioritize a working, clearly-demoable RAG + RCA loop with a clean UI over adding more modules half-finished. A polished 2-module system beats a broken 5-module system.
---

## 11. Open Decisions (confirm or change before building)

1. **Plant type** — currently set to **Oil Refinery**. Alternatives: steel plant, power plant, manufacturing line.
2. **Primary agentic module** — currently set to **Maintenance & RCA Agent**. Alternatives: Compliance Checker, Lessons Learned Engine.

**Strategic Implications:** Innovation + Business Impact = 50% of the score. Prioritize a working, clearly-demoable RAG + RCA loop with a clean UI over adding more modules half-finished. A polished 2-module system beats a broken 5-module system.

---

## Engineering Guidelines

Build this system in the order laid out in Section 8 (Day-by-Day Build Plan), following the architecture in Section 3 and folder structure in Section 5. Start with the ingestion pipeline and vector store (Tier 2 + 3) since everything else depends on it. Use the API contract in Section 7 as the interface between backend and frontend so both can be built in parallel. Keep the knowledge graph implementation simple (SQLite triples, not a graph database) — this is a prototype, not a production system.
