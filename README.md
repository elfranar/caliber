# NEXUS-PLANT: AI-Powered Manufacturing Knowledge Hub
**CALIBER 2026 Business Case Competition — Case 1: Manufacturing Knowledge Hub**
*PT Chandra Asri Pacific Tbk &bull; Cilegon Petrochemical Complex*


## Source Files and Data Layout

| Data | Location | Role |
|---|---|---|
| Engineering PDFs (SOP/OPL, datasheets, drawings, logic diagrams, and supporting documents) | `data/supporting data pdf/` | Official technical source files; parsed to Markdown by LlamaParse. |
| P&ID images | `data/P&ID Data/` | Official drawing sources; parsed to Markdown and also used for upload/OCR comparison. |
| Maintenance history | `data/Maintenance Data/Maintenance History (All Equipment).xlsx` | Read directly from Excel with Pandas; never converted to JSON. |
| Parsed document text | `data/case1_markdown/` | Generated Markdown derived from PDF and P&ID sources; safe to regenerate with the ingestion command below. |
| Case 1 embeddings | `data/case1_chroma_v2/` | Persistent local Chroma index; `/api/query` synchronizes it against current Markdown and approvals on each query. The legacy `data/case1_chroma/` index is preserved and not opened. |
| Existing local Chroma store | `data/.chroma/` | Store used by the optional LlamaIndex helper in `backend/database.py`. |
| Parsed image artifacts | `data/parsed_images/` | Generated image outputs from the optional `backend/database.py` ingestion helper. |
| Asset metadata | `data/asset_registry.json` | Equipment/instrument tags and attributes used by entity resolution and telemetry. |
| Plant topology | `data/topology_graph.json` | Asset relationships for graph traversal, including failure-memory links. |
| HITL decisions | `data/quarantine_store.json` | Persistent quarantine and SME-resolution records; not a document corpus. |
| Source approvals | `data/source_approvals.json` | Persistent SME approval state for individual source documents and maintenance rows. Missing entries are `unverified` and excluded from retrieval. |

The current workspace snapshot has 89 PDFs, 8 P&ID images, and a workbook with 211 maintenance rows plus an Explanation sheet. The deleted `data/documents/` JSON corpus is not used by the current code.

## Main Runtime Paths

| Path | Used by | Retrieval and answer behavior |
|---|---|---|
| `/api/query` | Existing browser console | The existing browser request now uses the approved-source semantic pipeline (local sentence-transformer embeddings + Chroma; native Excel search). Groq generation is optional and requires explicit cloud consent. The response retains the existing UI contract. |
| `/api/case1/query` | API client | Same approved-source semantic retrieval and optional Groq grounded answer path as `/api/query`; accepts an optional dataset scope. |
| `/api/case1/opl` | API client | Formats caller-supplied troubleshooting session text as an Indonesian OPL using Groq only when explicit Groq transfer consent and a key are configured. It does not persist chat history. |
| `/api/agent/process` | Optional legacy agent route | Local deterministic synthesis; may try the LlamaIndex Chroma helper and fall back to the source-derived in-memory index. |

`backend/vector_engine.py` remains the local token-overlap engine used for the legacy attachment/P&ID audit path and catalogs. It excludes all sources that are not explicitly approved. The browser's ordinary Q&A now uses the local sentence-transformer semantic index.
Legacy `/api/query` responses also HTML-escape untrusted string values before the existing browser renderer receives them.

Retrieval drops Markdown matches below similarity `0.30`; low similarity and Excel-only answers carry a `LOW_CONFIDENCE` flag. The API does not present retrieval similarity as calibrated answer confidence: `confidence` is unset, and the UI-compatible trust badge reports that answer confidence is not calibrated. If no approved evidence matches, the answer is `Sorry, the information was not found in the official database.` Source metadata distinguishes Markdown document/version/section from Excel file/sheet/row/date. Every Chroma query reconciles changed, removed, or newly approved Markdown chunks before retrieval.

SME mutations require the `X-SME-Token` header and a configured `SME_API_KEY`. The authenticated principal is recorded from `SME_APPROVER_NAME`; the caller-supplied `sme_name` is not trusted. Use `GET /api/source-approvals` to list approval IDs. `POST /api/sources/approval` accepts an exact ID or a maintenance wildcard ending in `:*`; document and row approvals are persisted in `data/source_approvals.json`. Resolving a linked quarantine record also updates the associated source approval and refreshes active indexes. The browser layout is unchanged; administrative approvals can be performed through the API.

### External services and data transfer

- PDF/P&ID parsing sends source files to Llama Cloud. It is disabled unless `CALIBER_ALLOW_CLOUD_PROCESSING=true` and `LLAMA_CLOUD_API_KEY` (or the parser's supported alias) are present.
- Groq receives the engineer's question, approved retrieval excerpts, or caller-supplied OPL session text. It is disabled unless `CALIBER_ALLOW_GROQ_PROCESSING=true` and `GROQ_API_KEY` are present.
- Semantic embeddings run locally after the sentence-transformer model is available. The first model download may require network access; query text and source excerpts are not sent to the embedding provider.
- Keep consent flags unset until the relevant data owner authorizes the transfer. Without Groq consent/key, query responses use a local evidence-only mode; if an opted-in Groq request fails, the API returns an explicit service error.

The API reference at `/docs` includes these routes:

| Route | Purpose |
|---|---|
| `GET /api/status`, `/api/assets`, `/api/datasets`, `/api/documents`, `/api/source-approvals` | System status, asset/dataset catalogs, and source/approval inventories. |
| `POST /api/query` | Browser RAG query; accepts optional dataset scope, image attachment, and `rag` or `pid_audit` mode. |
| `POST /api/case1/query`, `/api/case1/opl` | Semantic query and OPL generation; Groq is gated by explicit consent. |
| `POST /api/validate-pid` | Uploaded drawing validation. |
| `GET /api/graph` | Full or asset-centered topology. |
| `GET /api/quarantine`, `POST /api/quarantine/resolve`, `POST /api/sources/approval` | HITL review and authenticated SME source/row approval. Mutation endpoints require `X-SME-Token`. |
| `GET /api/telemetry`, `/api/telemetry/sensors` | Simulated telemetry and sensor catalog. |
| `POST /api/telemetry/simulate-anomaly`, `/step`, `/reset` | Operate the telemetry simulator. |
| `POST /api/agent/process`, `/api/deployment/toggle` | Optional local agent and deployment-mode toggle. |

## Project Structure & Tooling

| Path / Tool | Responsibility |
|---|---|
| `__pycache__/` | Auto-generated Python bytecode caches for performance (ignored in git). |
| `.vscode/` | IDE configurations (e.g., `tasks.json` for debugging). |
| `.venv/` / `venv/` | Isolated Python virtual environment containing dependencies. |
| `backend/` | Contains all Python modules (FastAPI server, vector engine, event simulator, case1 agent). |
| `data/` | Stores raw PDFs, P&IDs, Excel maintenance logs, and the local ChromaDB semantic index. |
| `postman/` | Developer API testing collections for verifying backend routes without UI. |
| `static/` | Frontend Dashboard assets (HTML, JS, CSS) providing the Single Pane of Glass interface. |
| `tests/` | Unit and integration testing scripts. |
| `.gitignore` | Defines files to be excluded from GitHub (e.g., `.env`, `venv`). |
| `app.py` | Application entry point handling port and host configuration for deployment. |
| `README.md` | This file; containing architecture, map, and setup instructions. |
| `render.yaml` | Infrastructure-as-Code for simple 1-click cloud deployment via Render.com. |
| `requirements.txt` | Python library dependency list (FastAPI, Langchain, Uvicorn, etc). |
| `run.py` | Local launcher script (calls `app.py`). |
| `test_api.py`, `test_api_simple.py`, `test_pipeline.py` | Scripts to locally test backend functionality, RAG retrieval, and simulated endpoints. |

## Alur Bisnis & Arsitektur Sistem (Workflow & Business Logic)

**1. Tantangan Bisnis (Pain Points)**
Teknisi membuang banyak waktu mencari informasi valid karena data tersebar: SOP di server, P&ID berbentuk gambar, riwayat maintenance di Excel. Fragmentasi ini berisiko menyebabkan keterlambatan penanganan dan kesalahan eksekusi.

**2. Solusi Bisnis: Manufacturing Knowledge Hub (MKH)**
- **Pemusatan Data:** Menyerap berbagai dokumen teknis menjadi satu *Knowledge Base* cerdas.
- **AI Proaktif:** Teknisi bertanya menggunakan *natural language*. Jawaban AI selalu *traceable* (dilengkapi sumber asli dan *confidence score*).
- **Failure Memory & Telemetry Push:** Sistem terhubung dengan sensor mesin secara virtual. Saat ada anomali tekanan, sistem otomatis menampilkan peringatan darurat dan riwayat kegagalan (RCA) di masa lalu.

**3. Alur Kerja Teknis (Technical Workflow)**
- **Data Ingestion:** File dipecah dan dikonversi menjadi vektor, lalu disimpan di **ChromaDB** lokal.
- **Simulator Telemetri:** Skrip `event_simulator.py` memantau 8 sensor dataset. Jika aktif, akan mengirim *payload Failure Memory*.
- **Semantic Search:** Saat teknisi bertanya, `case1_agent.py` merakit *prompt* dari 1) Pertanyaan, 2) Data ChromaDB, 3) Histori Excel, dan 4) Peringatan sensor aktif.
- **Eksekusi LLM:** Groq LLM API membaca rakitan *prompt* dan mengembalikan jawaban faktual ke Dashboard (Vue/JS) secara *real-time*.

# Casebook Mapping

This section exists so a judge can verify, line by line, that every requirement in the
**CALIBER 2026 – Case 1 (Manufacturing Knowledge Hub)** casebook is addressed by a
specific, runnable part of this prototype — not just claimed in the slide deck.

## 1. Key Questions → Where it's answered

| # | Key Question (casebook) | Answered by | Demo path |
|---|---|---|---|
| 1 | How can the Company build a structured Industrial Data Ops foundation to connect scattered plant knowledge sources? | `backend/hitl_quarantine.py` (entity resolution + conflict gate) + `data/asset_registry.json` (structured metadata layer) | Tab 3 — Industrial Data Ops & HITL Quarantine |
| 2 | How can AI help engineers find trusted technical information faster and reduce the risk of improper execution? | `backend/domain_guardrail.py` → `backend/entity_extractor.py` → `backend/knowledge_graph.py` + `backend/vector_engine.py` → `backend/scoring_fusion.py` | Tab 1 — AI Assistant & Query Router |
| 3 | How can the Manufacturing Knowledge Hub be integrated with operational systems to support reliability, troubleshooting, and continuous improvement? | `backend/event_simulator.py` (proactive push) + `:HAS_INCIDENT` edges in `knowledge_graph.py` (failure memory) | Tab 4 — Live Telemetry & Event-Driven Push |

## 2. Expected Solution bullets → Component

| Casebook expected solution | Implemented in | Status |
|---|---|---|
| **Industrial Data Ops** — structured data/metadata foundation connecting SOPs, P&IDs, datasheets, maintenance logs, asset data | `data/asset_registry.json`, `data/topology_graph.json` | Working (simplified store — see §3) |
| **AI Document Ingestion** — scattered documents into a structured, searchable, AI-ready knowledge base | `backend/case1_ingestion.py` (LlamaParse to Markdown) + `backend/vector_engine.py` (source-derived search) | PDF/P&ID parsing requires Llama Cloud credentials; Excel remains native `.xlsx` |
| **Q&A Assistant & Semantic Search** — natural-language, context-based search | `backend/case1_agent.py` + Chroma + `/api/query` | Working; only approved evidence is retrieved |
| **Traceable Answer with Source** — sources, version, approval status, confidence indicator | Semantic retrieval metadata + API/UI-compatible source cards | Working; retrieval match is explicitly not calibrated answer confidence |
| **EDMS / AIMS / Digital Twin Integration** — technical info in asset/operational context | No live EDMS/AIMS/Digital Twin integration; telemetry is simulated by `backend/event_simulator.py` | Not integrated; simulator only |
| **Failure Memory System & Recommendation** — past failures, RCA, lessons learned | Maintenance workbook rows, parsed OPL/SOP sources, `:HAS_INCIDENT` graph edges, and HITL records | Prototype source retrieval; no separate live RCA database |

## 3. Known simplifications (disclosed, not hidden)

A prototype built in a limited timeframe cannot fully replicate a production petrochemical
data stack. The table below is intentionally explicit about where this build simplifies,
so the design intent in the slide deck isn't mistaken for what's literally running.

| Area | Slide deck / target architecture | This prototype | Why it's still a valid demonstration |
|---|---|---|---|
| Data storage | Separate relational DB + graph DB + vector DB | Source files remain PDF/PNG/XLSX; asset registry, topology, and quarantine decisions are JSON metadata; vector indexes are local Chroma or in-memory | This is a local prototype, not a production relational/graph platform. |
| Document ingestion | Governed document ingestion and OCR | `backend/case1_ingestion.py` sends supported PDFs and P&ID images to LlamaParse and saves Markdown under `data/case1_markdown/`; Pandas reads the workbook directly | LlamaParse requires an API key and transfers source files to Llama Cloud. No source content is converted to JSON. |
| Embeddings and search | Production-grade, domain-tuned retrieval | Ordinary browser Q&A and `/api/case1/query` use Chroma cosine search with local `all-MiniLM-L6-v2` embeddings; the legacy attachment path uses normalized token overlap | Search index synchronizes source content and approval changes before semantic queries. |
| Answer generation | Governed LLM assistance | Browser Q&A and `/api/case1/opl` can use Groq `openai/gpt-oss-120b` after explicit opt-in; otherwise Q&A stays local and evidence-only | Groq receives question/session text and retrieved excerpts only after configured consent. Do not send confidential data without authorization. |
| Conflict detection | AI-assisted anomaly/conflict detection | Deterministic checks over parsed Markdown and Pandas workbook rows; SME decisions remain in `data/quarantine_store.json` | Checks are rule-based, not machine learning. |
| EDMS / AIMS / Digital Twin | Live integration with enterprise systems | Simulated fields and mock event stream representing what those systems would provide | These are external enterprise systems outside the scope of a standalone prototype; the integration *contract* (what data flows in, what the hub does with it) is what's being demonstrated |

## 4. What is genuinely "AI" vs. rule-based in this build

To keep the demo intellectually honest under questioning:


- **AI / model-based:** RapidFuzz entity matching; the optional Case 1 agent uses sentence-transformer embeddings and Groq. The main browser query uses deterministic token overlap, not embeddings.
- **Deterministic / rule-based:** domain guardrail, normalized token-overlap search, graph hop decay, score fusion, conflict checks, telemetry simulation, and main-query synthesis.

Both are legitimate engineering choices — the point of disclosing this is to show the
judges we understand *which* parts of a trustworthy industrial AI system should be
deterministic and auditable, and which parts benefit from a model, rather than treating
"AI" as a label to slap on everything.


## Current Application Flow

```text
PDF/P&ID image --authorized LlamaParse--> Markdown --+--> fingerprint sync --> approved Chroma semantic retrieval
Maintenance XLSX --Pandas + row approval------------+--> approved maintenance search
                                                     +--> /api/query (unchanged browser UI contract)
                                                     +--> optional Groq generation after separate consent

asset_registry.json --> asset/tag metadata      topology_graph.json --> graph traversal
quarantine_store.json --> HITL decisions        event_simulator.py --> simulated telemetry
```

The following is the competition's target architecture, not a description of services that are currently deployed by this prototype.

## Target Enterprise Architecture (Conceptual)

```
[ P&ID / SOP / Historian / Logs / Tacit OPL ]
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ 1. INGESTION & DATA OPS PIPELINE                        │
│  - Vision OCR (AutoCAD schematic & low-res P&ID parsing)│
│  - Entity Resolution & Tag Normalization (ISA-5.1)      │
│  - HITL Quarantine Engine (Conflicting/Dirty Data Gate) │
└────────────────────────────┬────────────────────────────┘
                             │ Clean & Verified Data
                             ▼
┌─────────────────────────────────────────────────────────┐
│ 2. TRI-STORAGE FOUNDATION                               │
│  ├─ Relational DB   : Work Orders, Asset Registry       │
│  ├─ Neo4j Graph DB  : Topological & Process Links       │
│  └─ Vector DB       : Normalized Embeddings Chunks      │
└────────────────────────────┬────────────────────────────┘
                             │
 [ Engineer Query / Alert Event ]
               │
               ▼
┌─────────────────────────────────────────────────────────┐
│ 3. INTELLIGENT QUERY ROUTER & GUARDRAILS                │
│  ├─ Guardrail Filter (Blocks "Weather", prompt leaks)   │
│  ├─ Hybrid NER (Regex ISA-5.1 + RapidFuzz Description)  │
│  └─ Routing Decision Engine                             │
│       ├─ Relational Intent  ──> Graph Traversal         │
│       ├─ Conceptual/SOP     ──> Semantic Search         │
│       └─ Telemetry/Limit    ──> Structured SQL Query    │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│ 4. CONTEXT FUSION & TRUST GENERATION                    │
│  - Score Normalization (Decayed Hops + Cosine + Proximity│
│  - Reciprocal Rank Fusion (RRF) & Weighted Sum          │
│  - Confidence Scoring & SME Approval Weighting          │
│  - LLM Context Synthesis (On-Prem / Secured Inference)  │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│ 5. OPERATIONAL DELIVERY & INTEGRATION (EDMS/AIMS/TWIN) │
│  - Split-pane Engineer UI with Source Highlighting (XAI)│
│  - Event-Driven Alert Push (Proactive Troubleshooting)  │
│  - Failure Memory Feedback Loop (Post-Incident RCA Ingestion)
└─────────────────────────────────────────────────────────┘
```


## 🚀 Quickstart Guide

From PowerShell at the workspace root. Skip virtual-environment creation if `.venv` already exists.

### Install

```powershell
python -m venv .venv
$python = ".\.venv\Scripts\python.exe"
& $python -m pip install -r requirements.txt
```

### Parse PDF and P&ID Sources

```powershell
$env:LLAMA_CLOUD_API_KEY = "<your LlamaParse key>"
& $python -m backend.case1_ingestion
```

LlamaParse writes derived Markdown to `data/case1_markdown/`; it does not modify the PDF or image sources. The parser sends input documents to Llama Cloud, so get approval before using confidential plant files.

### Start the App

```powershell
& $python run.py
```

Open `http://127.0.0.1:8000`; interactive API docs are at `http://127.0.0.1:8000/docs`. The VS Code task **Run Knowledge Hub on 8002** starts the app on port 8002.

The current browser console sends its existing request to `/api/query`; ordinary queries use semantic retrieval. Without Groq consent and a key, it runs in local evidence-only mode. To permit Groq, first confirm authorization to transfer queries and retrieved excerpts, then set `CALIBER_ALLOW_GROQ_PROCESSING=true` and `GROQ_API_KEY` in the server environment or a local `.env` file. `GROQ_MODEL` optionally selects an active model enabled for the Groq organization; it defaults to `qwen/qwen3.8-27b`, which has been verified with this project's configured key. If Groq returns a model-not-found or organization-level model permission error, check model access in the Groq console and set `GROQ_MODEL` to an enabled model. The key is read only from the environment; do not store it in source code or commit `.env`. Rotate any key that has been shared or exposed. When consent is enabled but no key is configured, the API reports a configuration error rather than silently using local generation. To permit parsing, set both `CALIBER_ALLOW_CLOUD_PROCESSING=true` and `LLAMA_CLOUD_API_KEY` only after approving document transfer.

The first semantic query loads `sentence-transformers/all-MiniLM-L6-v2` and builds `data/case1_chroma_v2/` from existing Markdown. The legacy `data/case1_chroma/` directory is left untouched because it cannot be safely opened by the current Chroma runtime. Subsequent queries detect edits, removals, and approval-state changes and synchronize the persistent collection. Unverified or rejected content is never returned as evidence.

For authenticated SME mutations, configure `SME_API_KEY` and optionally `SME_APPROVER_NAME`. Then query `GET /api/source-approvals` and send an approval, for example:

```powershell
$headers = @{ "X-SME-Token" = $env:SME_API_KEY }
$body = @{ approval_id = "OPL-GA-1201A-01"; approval_status = "approved" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/sources/approval -Headers $headers -ContentType "application/json" -Body $body
```

The caller-supplied display name is not treated as identity; the configured SME name is recorded instead. This single-key workflow is a prototype control, not a replacement for enterprise SSO/RBAC. The browser interface remains unchanged, so approvals use the authenticated API.

### Run Tests

```powershell
& $python test_pipeline.py
```

The suite runs 10 integration checks. It does not call live LlamaParse or Groq services.


## 🧪 Interactive Walkthrough Scenarios

1. **Test Domain Guardrail (Off-Topic Rejection)**:
   - Click the prompt chip: *"What is the weather in Jakarta today?"*
   - `/api/query` rejects the off-topic question and returns suggested plant topics.

2. **Test Root Cause & Interlock Guidance (XAI Traceability)**:
   - Query: *"Why did GA-1201A trip on PT-1201 low pressure?"*
   - Inspect the execution timeline, trust badge, and retrieved excerpts. Source approval is shown as `unverified` unless approval metadata is present.

3. **Explore Topological Knowledge Graph**:
   - Navigate to the **"Topological Knowledge Graph"** tab.
   - Select an asset such as `GA-1201A` to see its configured graph links and associated source-file references.

4. **Resolve Quarantined Conflict (HITL Data Ops)**:
   - Navigate to the **"Industrial Data Ops & HITL"** tab.
   - Inspect persisted and source-detected conflicts, then resolve a record through the SME workflow.
   - Submit SME approval with justification notes and observe the Data Health Score dynamically update.

5. **Simulate Event-Driven Proactive Alert Push**:
   - Navigate to the **"Live Telemetry & Event Push"** tab.
   - Click **"Simulate Suction Pressure Collapse"**.
   - Observe the sensor value and advisory from the simulator. This is not a live DCS or historian connection.

6. **Try semantic Q&A from the existing browser**:
   - Ask a technical question in the ordinary assistant tab; it now calls the approved-source Chroma semantic pipeline.
   - Approve demo sources through the authenticated API first. Groq generation remains opt-in; without it, the UI shows local evidence-only excerpts and a non-calibrated confidence warning.
   - To generate an OPL from troubleshooting notes, configure Groq transfer consent and call `POST /api/case1/opl`.
