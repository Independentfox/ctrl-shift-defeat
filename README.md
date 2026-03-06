# CO-FOUNDER AI

**Multi-Agent Founding Intelligence System**

Team: Ctrl+Shift+Defeat | IIT Roorkee | AI Unlocked Hackathon — Agent Teamwork Track

---

## What It Does

CO-FOUNDER AI stress-tests startup ideas the way they are evaluated in the real world — simultaneously, through the lens of a Shark Tank investor, a venture capitalist, a management consultant, and a worst-case customer — all grounded in real startup datasets.

Every output follows this strict pipeline:

```
User Input → Retrieve Real Evidence from Datasets → LLM Reasons ON TOP of Evidence → Structured Output
```

Not LLM hallucination. Real data grounding, with a `grounding_score` on every agent output.

---

## The Three Phases

| Phase | What Happens | Output |
|-------|-------------|--------|
| **Ideation** | 4 agents analyze the idea in parallel from distinct lenses | Evidence-backed risk & insight map |
| **Execution** | Validated insights converted into strategic artifacts | Pitch deck (PPTX) + Financial model (XLSX) |
| **Operation** | Constraint-driven roadmap from financial outputs | Month-by-month launch plan |

---

## System Architecture

```
React Frontend (Vite + TypeScript)
         |
FastAPI Backend (Python)
         |
   Orchestrator (Planner)
         |
   ┌─────┼─────┬─────┐
   |     |     |     |
Shark   VC  Consult  Customer
Tank  Agent  Agent   Agent
   |     |     |     |
   └─────┴──┬──┴─────┘
            |
     Azure AI Search
     (4 RAG indexes)
            |
    Google Gemini (LLM)
            |
  Azure Cosmos DB + Blob Storage
```

### Ideation Agents (run in parallel)

| Agent | Dataset | Lens |
|-------|---------|------|
| **Shark Tank Agent** | Shark Tank India S1–S3 + US (~700 pitches) | Investor pitch outcomes |
| **VC Agent** | YC Companies 2005–2024 (~5,000 companies) | Fundability & comparable companies |
| **Consultant Agent** | Crunchbase India + DPIIT data (~7,000 companies) | Market sizing & competitive landscape |
| **Worst-Case Customer Agent** | CB Insights + Failory + Autopsy (~500 post-mortems) | Customer objections & failure patterns |

After all 4 complete, a **Synthesizer** computes an overall viability score and determines whether to proceed.

### Execution Agents (sequential)

- **Pitch Deck Agent** — generates a 12-slide PPTX where every slide is mapped to an ideation finding
- **Financial Model Agent** — builds revenue projections and burn rate from comparable company data, outputs XLSX

### Operation Agent

Produces a constraint-driven month-by-month roadmap based on the actual burn rate and runway from Stage 2 — not generic advice.

---

## RAG Architecture

Each agent:
1. Builds a semantic query from the `StartupContextObject`
2. Runs **hybrid search** (vector + keyword + metadata filters) against its Azure AI Search index
3. Re-ranks retrieved documents (threshold: score > 0.5), takes top-5
4. Passes evidence to Gemini with the instruction: *"Reason ONLY from provided context"*
5. Returns structured JSON with a `grounding_score`

**Embedding model:** `text-embedding-ada-002` (Azure AI Search)
**LLM:** Google Gemini (`gemini-2.0-flash` by default)

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19, TypeScript, Vite, Tailwind CSS v4 |
| Backend | FastAPI, Python 3.11+, Uvicorn |
| LLM | Google Gemini API (`google-genai`) |
| RAG / Search | Azure AI Search (hybrid search) |
| State / Sessions | Azure Cosmos DB |
| File Storage | Azure Blob Storage |
| File Generation | `python-pptx`, `openpyxl` |
| Streaming | `sse-starlette` (Server-Sent Events) |

---

## Project Structure

```
control-shift-delete/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # Settings (pydantic-settings)
│   ├── agents/                  # All agent implementations
│   │   ├── base_agent.py        # RAG + Gemini reasoning loop
│   │   ├── shark_tank_agent.py
│   │   ├── vc_agent.py
│   │   ├── consultant_agent.py
│   │   ├── customer_agent.py
│   │   ├── financial_model_agent.py
│   │   ├── pitch_deck_agent.py
│   │   ├── operations_agent.py
│   │   └── synthesizer.py
│   ├── orchestrator/
│   │   ├── planner.py           # Fan-out orchestration logic
│   │   └── rerun.py             # Selective agent re-run + cascade
│   ├── rag/
│   │   ├── search_client.py     # Azure AI Search hybrid search
│   │   ├── embedding.py         # text-embedding-ada-002 wrapper
│   │   └── grounding.py         # Grounding score computation
│   ├── generators/
│   │   ├── pptx_builder.py      # PPTX file generation
│   │   └── xlsx_builder.py      # XLSX financial model generation
│   ├── models/
│   │   ├── context_object.py    # StartupContextObject schema
│   │   └── api_models.py        # Request/response Pydantic models
│   ├── routes/
│   │   ├── session.py           # POST /api/session/create
│   │   ├── stage.py             # POST /api/stage/run
│   │   ├── agent.py             # POST /api/agent/rerun
│   │   └── download.py          # GET /api/output/download
│   ├── prompts/                 # System prompts per agent (.txt)
│   ├── storage/
│   │   ├── cosmos_client.py     # Cosmos DB session state
│   │   └── blob_client.py       # Azure Blob file uploads
│   ├── scripts/                 # Dataset preprocessing + indexing
│   │   ├── download_datasets.py
│   │   ├── preprocess_shark_tank.py
│   │   ├── preprocess_yc.py
│   │   ├── preprocess_failures.py
│   │   ├── preprocess_crunchbase.py
│   │   └── embed_and_index.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/               # LandingPage, IdeaIntakePage, IdeationDashboard,
│   │   │                        # ExecutionDashboard, OperationDashboard
│   │   ├── components/
│   │   │   ├── agents/          # AgentCard, GroundingBar, SynthesisCard
│   │   │   ├── layout/          # StageProgress
│   │   │   └── shared/          # OverrideModal
│   │   └── api/                 # Typed API client (axios)
│   └── package.json
├── infra/
│   ├── provision.sh             # Azure resource provisioning (az CLI)
│   └── search_index_schemas/    # Azure AI Search index definitions
└── .env.example
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- Azure account (AI Search, Cosmos DB, Blob Storage)
- Google Gemini API key (free tier works)
- Azure CLI (`az`) for infrastructure provisioning

### 1. Provision Azure Infrastructure

```bash
bash infra/provision.sh
```

This creates the resource group, Azure AI Search (free tier), Cosmos DB (free tier), and Blob Storage, then prints all keys.

### 2. Configure Environment

```bash
cp .env.example .env
# Fill in the values printed by provision.sh + your Gemini API key
```

### 3. Prepare Datasets & Search Indexes

```bash
cd backend
pip install -r requirements.txt

# Download raw datasets from Kaggle (see scripts for links)
python scripts/download_datasets.py

# Preprocess each dataset
python scripts/preprocess_shark_tank.py
python scripts/preprocess_yc.py
python scripts/preprocess_failures.py
python scripts/preprocess_crunchbase.py

# Embed and push to Azure AI Search
python scripts/embed_and_index.py
```

### 4. Run the Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

API available at `http://localhost:8000`. Docs at `http://localhost:8000/docs`.

### 5. Run the Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend available at `http://localhost:5173`.

---

## API Reference

```
POST   /api/session/create        Create a new session from idea intake form
POST   /api/stage/run             Trigger an ideation / execution / operation run
GET    /api/session/{id}/status   Poll agent completion status
GET    /api/session/{id}/output   Fetch full StartupContextObject
POST   /api/agent/rerun           Re-run a single agent with updated assumptions
GET    /api/output/download       Get SAS URL for PPTX / XLSX / PDF download
```

---

## Iteration Model

After every agent output, the user can:

- **Update Assumptions** — modify any field in the `StartupContextObject`
- **Re-run Agent** — only the affected agent re-runs; downstream outputs are marked stale
- **Cascade** — changing `target_customer` re-runs all 4 ideation agents and marks execution artifacts as stale

Every session is versioned. Override history is preserved in `StartupContextObject.user_overrides`.

---

## Datasets

| Index | Source | Size |
|-------|--------|------|
| `pitch_outcomes` | Shark Tank India S1–S3 + US (Kaggle) | ~700 pitches |
| `yc_companies` | YC Company Dataset 2005–2024 (Kaggle) | ~5,000 companies |
| `failure_postmortems` | CB Insights + Failory + Autopsy.io | ~500 records |
| `funding_patterns` | Crunchbase Startup Dataset (Kaggle) | ~7,000 companies |

---

## Grounding Score

Every agent output carries a `grounding_score` — the fraction of claims backed by retrieved documents vs. LLM inference.

```json
{
  "grounding_score": 0.84,
  "grounding_note": "84% of claims sourced from 6 retrieved documents. 16% inferred."
}
```

This is displayed on every output card in the UI.

---

*CO-FOUNDER AI — Ctrl+Shift+Defeat | IIT Roorkee | AI Unlocked Hackathon*
