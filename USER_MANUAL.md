# Unified Asset & Operations Brain - User Manual & Project Guide
### ET - AI Hackathon (Problem Statement 8) — Official User Guide

Welcome to the **Unified Asset & Operations Brain**, an AI-powered Industrial Knowledge Intelligence and Maintenance Root Cause Analysis (RCA) platform designed for heavy industrial facilities (Northgate Energy / Northgate Refinery).

---

## 1. Quick Start: How to Run the App

Both servers run locally on your computer:

```bash
# Option A: Start Backend API (Python FastAPI)
cd c:\Users\dubey\Desktop\ET_AI\backend
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload

# Option B: Start Frontend Web UI (React + Vite)
cd c:\Users\dubey\Desktop\ET_AI\frontend
npm.cmd run dev -- --port 5173
```

- **Web Dashboard URL**: **http://localhost:5173**
- **FastAPI API URL**: **http://localhost:8000** (Interactive Docs: **http://localhost:8000/docs**)

---

## 2. Navigating the 5 Web UI Tabs

### Tab 1: 📊 Control Overview
- **What you see**: System health badges, document ingestion counters, Knowledge Graph triple counts, and high-risk equipment heat cards (e.g. Compressor `C-102`, Boiler `B-201`).
- **Quick Action**: Click any equipment card to jump directly to its Root Cause Analysis report.

### Tab 2: 🤖 Expert RAG Copilot (Chatbot)
- **What you see**: A dark-mode conversational interface powered by Retrieval-Augmented Generation (RAG) over all 10 master refinery documents.
- **Features**:
  - **Auto-Scroll to Answer**: Automatically aligns the view to the top of the AI's latest response so you can read immediately.
  - **Quick Showcase Questions Toolbar**: Click the `Quick Showcase Questions` button at the top right to select pre-configured questions!
  - **Verified Source Citations**: Every technical answer displays clickable citation pills (e.g. `📄 01_refinery_working_and_parts_guide.txt`). Click any pill to inspect the exact retrieved text snippet in the right drawer.
  - **Domain Guardrails**: If asked out-of-scope questions (e.g. *"Who won the IPL?"*), the AI politely refuses and redirects to company topics.

### Tab 3: 🔧 Maintenance & RCA Agent
- **What you see**: Autonomous reliability pattern analysis for plant equipment.
- **How to use**: Select any equipment tag (`C-102`, `PRV-88`, `P-401B`, `T-101`) to view its **Chronological Operational Timeline** and an **Agentic Root Cause Analysis (RCA) Report** detailing failure modes, root causes, violated SOPs, and preventative recommendations.

### Tab 4: 🗺️ Plant Map & Piping Network
- **What you see**: An interactive SVG industrial blueprint map of Northgate Refinery (450-acre facility).
- **How to use**: Click on any of the 6 plant zones (**Zone A: Crude Processing**, **Zone B: Hydrocracker**, **Zone C: Boiler House**, **Zone D: Tank Farm**, **Zone E: Pipe Racks**, **Zone F: Safety CCR**) to inspect equipment coordinates, grid sectors, connected pipe lines, and emergency assembly points.

### Tab 5: 📁 Knowledge Base & Graph Explorer
- **What you see**: Ingested document catalog and SQLite Knowledge Graph entity triples explorer.
- **How to use**: Upload new PDFs or text files via drag-and-drop, or click entity buttons (e.g. `C-102`, `B-201`, `OISD-116`) to inspect relationship triples.

---

## 3. How to Demonstrate the App to Friends & Judges

For maximum impact during a presentation:

1. **Start on the Plant Map Tab**: Show the 6 plant zones and explain that the refinery processes 15.2 MMTPA of crude oil.
2. **Open the RAG Copilot Tab**:
   - Click `Quick Showcase Questions` and ask *"can u give me a map"*.
   - Ask *"What is the required Octane rating for BS-VI petrol?"* and click the source citation pill to show the raw document snippet in the drawer!
   - Ask *"Who won the IPL?"* to demonstrate AI domain guardrails!
3. **Open the RCA Agent Tab**: Select `C-102` and show how the AI extracted a 2018–2024 failure timeline and identified monsoon moisture ingress as the root cause.
4. **Share the PDF Guides**: Show the PDF guides in the `PDF_GUIDES/` folder!

---

## 4. PDF Guides Index in `PDF_GUIDES/` Folder

All PDF guides are neatly organized in `c:\Users\dubey\Desktop\ET_AI\PDF_GUIDES\`:

1. `01_Oil_Refinery_Construction_and_Working_Guide.pdf`: Beginner-friendly guide explaining how an oil refinery works, all 7 sections, and construction phases.
2. `02_30_Meaningful_Showcase_Questions_and_Answers.pdf`: 30 curated questions with expected answer previews across 6 categories.
3. `03_Project_Implementation_Plan.pdf`: Technical architecture, tech stack, and database schema documentation.
4. `04_User_Manual_and_Project_Guide.pdf`: This official User Manual & Demonstration Guide.
