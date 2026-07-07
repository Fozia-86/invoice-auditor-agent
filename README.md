# Smart Invoice Auditor & Autonomous Settlement Agent

A production-grade, cloud-deployed **Multi-Agent AI system** built with the Google Agent Development Kit (ADK) and deployed via the Agents CLI to the Agent Runtime environment.

## What It Does

This system serves **small-to-medium businesses (SMBs)** and corporate finance departments by:

1. **Ingesting** raw invoices (images/PDFs) from Google Cloud Storage (GCS)
2. **Extracting** structured transaction data using multimodal Gemini models
3. **Auditing** compliance against enterprise policies via Model Context Protocol (MCP)
4. **Verifying** vendor checkout state via Universal Commerce Protocol (UCP)
5. **Executing** secure payments via Agent Payments Protocol (AP2) with cryptographically signed mandates
6. **Logging** all operations to Google Cloud Firestore and streaming final ledger to BigQuery

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Agent Runtime (Cloud)                  │
│                                                         │
│  ┌──────────────┐   A2A Protocol   ┌─────────────────┐  │
│  │  Extractor    │ ──────────────► │  Compliance      │  │
│  │  Agent        │  Structured     │  Auditor Agent   │  │
│  │  (Gemini      │  JSON Handoff   │                  │  │
│  │   Multimodal) │                 │  ┌─────────────┐ │  │
│  └──────┬───────┘                 │  │ MCP Server  │ │  │
│         │                          │  │ (Policy)    │ │  │
│         │                          │  ├─────────────┤ │  │
│    GCS Bucket                      │  │ UCP Tool    │ │  │
│    (Invoices)                      │  │ (Vendor)    │ │  │
│                                    │  ├─────────────┤ │  │
│                                    │  │ AP2 Tool    │ │  │
│                                    │  │ (Payments)  │ │  │
│                                    │  └─────────────┘ │  │
│                                    └────────┬────────┘  │
│                                             │           │
│                    ┌────────────────────────┼──────┐    │
│                    │         Cloud Sync      │      │    │
│                    │                         ▼      │    │
│                    │  Firestore ◄──── Audit Log     │    │
│                    │  BigQuery  ◄──── Ledger Stream  │    │
│                    └────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

## Technology Stack

| Technology | Purpose |
|------------|---------|
| **Agent Development Kit (ADK)** | Framework for building agent personas and defining skills |
| **Gemini (Multimodal)** | AI model for extracting data from invoice images/PDFs |
| **Agent-to-Agent (A2A) Protocol** | Secure communication between Extractor and Auditor agents |
| **Model Context Protocol (MCP)** | Grounding the Auditor with live enterprise rules from `config/company_policy.json` |
| **Agent Payments Protocol (AP2)** | Generating tamper-proof Verifiable Digital Credentials (VDCs) |
| **Universal Commerce Protocol (UCP)** | Validating vendor checkout lifecycles |
| **Google Cloud Storage (GCS)** | Invoice file ingestion bucket |
| **Google Cloud Firestore** | Transaction state tracking and audit logs |
| **Google BigQuery** | Centralized data warehouse for audited ledger analytics |
| **Agents CLI & Agent Runtime** | Deployment pipeline to cloud-managed service |

## Project Structure

```
invoice-auditor-agent/
│
├── config/
│   └── company_policy.json       # MCP context file (spending limits & compliance rules)
│
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── extractor.py          # Data Extractor Agent (Gemini Multimodal core)
│   │   └── auditor.py            # Compliance Auditor Agent (A2A execution logic)
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── mcp_server.py         # Local MCP Server tool to fetch business rules
│   │   ├── ap2_payment.py        # Agent Payments Protocol handler (VDCs & Mandates)
│   │   └── ucp_commerce.py       # Universal Commerce Protocol connector (Vendor check)
│   │
│   ├── agent.py                  # Root agent & orchestration pipeline
│   ├── cloud_sync.py             # Firestore & BigQuery cloud sync module
│   └── main.py                   # System orchestrator & agent interaction pipeline
│
├── .env                          # Strictly local: Google Cloud & Gemini credentials
├── agent.toml                    # Agents CLI Deployment Manifest for Agent Runtime
├── agents-cli-manifest.yaml      # Agents CLI project configuration
├── requirements.txt              # Project library dependencies
├── pyproject.toml                # Python project configuration
└── README.md                     # This file
```

## How It Works — Step by Step

### 1. Invoice Ingestion
Raw invoice files (images/PDFs) are uploaded to a **Google Cloud Storage** bucket.

### 2. Data Extraction (Extractor Agent)
The **Extractor Agent** uses **Gemini's multimodal** capabilities to process the raw invoice and output structured JSON:
```json
{
  "invoice_id": "INV-2026-993",
  "vendor": "TechStore",
  "category": "hardware",
  "line_items": [{"description": "MacBook Pro M4", "amount": 149.99}],
  "total_amount_usd": 149.99
}
```

### 3. Compliance Audit (Auditor Agent)
The **Compliance Auditor** receives the extracted data via **A2A Protocol** and:

- **MCP Check**: Fetches enterprise spending limits from `config/company_policy.json`
- **UCP Verification**: Validates the vendor's checkout state via UCP endpoint
- **AP2 Execution**: Issues a cryptographically signed payment mandate (VDC) if compliant

### 4. Cloud Sync
- **Firestore**: Logs the transaction state and audit results
- **BigQuery**: Streams the final audited ledger for analytics

### 5. Final Output
The system returns a unified execution ledger block:
```json
{
  "deployment_telemetry": {
    "agent_id": "adk-invoice-auditor-prod-86",
    "runtime_environment": "Kaggle_Agent_Runtime_v3",
    "deployment_status": "ACTIVE_RUNNING"
  },
  "transaction_lifecycle": {
    "audit_verdict": {"status": "APPROVED", "flags_raised": 0},
    "ap2_execution": {"mandate_status": "GENERATED_AND_SIGNED"}
  },
  "cloud_database_sync": {
    "firestore_log": {"status": "SAVED"},
    "bigquery_stream": {"status": "SUCCESS"}
  }
}
```

## Setup & Installation

### Prerequisites
- Python 3.11+
- Google Cloud account with enabled APIs
- Agents CLI (`uv tool install google-agents-cli`)

### Install Dependencies
```bash
uv sync
```

### Configure Environment
```bash
# Copy and fill in your credentials
cp .env.example .env
# Edit .env with your Google Cloud Project ID, Gemini API key, etc.
```

### Run Locally
```bash
# Interactive playground
agents-cli playground

# Or run the test script
uv run python test_run.py
```

### Deploy to Agent Runtime
```bash
agents-cli deploy --region us-east1
```

## Hard Constraints

- **Zero Hardcoded Secrets**: All credentials injected via environment variables
- **Strict Boundary Mandates**: AP2 payment credentials must match extracted invoice totals
- **Cloud-Managed Production**: Final system runs as persistent Agent Runtime service, not local scripts

## License

This project was built as part of the Kaggle AI Agents course capstone project.
