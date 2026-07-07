# 📋 Smart Invoice Auditor & Autonomous Settlement Agent

A production-grade, cloud-deployed **Multi-Agent AI system** built with the Google Agent Development Kit (ADK) and deployed via the Agents CLI to the Agent Runtime environment for the **Kaggle 5-Day AI Agents Intensive (July 2026)**.

---

## 🚀 Live Project Links
* **Live Agent Runtime / App URL:** [👉 Click Here to View Live Project](https://invoice-auditor-agent-985903483121.us-east1.run.app/)
* **Video Demo Walkthrough:** [🎬 Watch Video Walkthrough](https://drive.google.com/file/d/1o9ZYD4vni4Upyv4-6e-7o4u7U4SfuNpy/view?usp=sharing)
* **Kaggle Notebook Repository:** [📓 View Project Notebook on Kaggle](https://www.kaggle.com/code/fozia86/smart-ai-invoice-auditor-capstone-project-adk))

---

## 💡 What It Does

This system serves **small-to-medium businesses (SMBs)** and corporate finance departments by automating the entire procurement invoice lifecycle through cooperative AI agents:

1. **Ingesting:** Raw invoices (images/PDFs) are fetched from Google Cloud Storage (GCS).
2. **Extracting:** Structured transaction metadata is extracted using multimodal Gemini models.
3. **Auditing:** Compliance is audited against granular enterprise policies via Model Context Protocol (MCP).
4. **Verifying:** Vendor checkout states are validated via the Universal Commerce Protocol (UCP).
5. **Executing:** Secure, cryptographically signed payment mandates are generated via Agent Payments Protocol (AP2).
6. **Logging:** All operations are tracked in Google Cloud Firestore and streamed to BigQuery for advanced ledger analytics.

## 🏗️ Architecture Diagram
┌─────────────────────────────────────────────────────────┐
│                 Agent Runtime (Cloud)                   │
│                                                         │
│  ┌──────────────┐   A2A Protocol   ┌─────────────────┐  │
│  │  Extractor   │ ──────────────► │  Compliance     │  │
│  │  Agent      │  Structured     │  Auditor Agent  │  │
│  │  (Gemini     │  JSON Handoff   │                 │  │
│  │   Multimodal)│                 │  ┌─────────────┐ │  │
│  └──────┬───────┘                 │  │ MCP Server  │ │  │
│         │                         │  │ (Policy)    │ │  │
│         │                         │  ├─────────────┤ │  │
│    GCS Bucket                     │  │ UCP Tool    │ │  │
│    (Invoices)                     │  │ (Vendor)    │ │  │
│                                   │  ├─────────────┤ │  │
│                                   │  │ AP2 Tool    │ │  │
│                                   │  │ (Payments)  │ │  │
│                                   │  └─────────────┘ │  │
│                                   └────────┬────────┘  │
│                                            │            │
│                    ┌───────────────────────┼──────┐     │
│                    │         Cloud Sync    │      │     │
│                    │                       ▼      │     │
│                    │  Firestore ◄──── Audit Log   │     │
│                    │  BigQuery  ◄──── Ledger Stream    │     │
│                    └──────────────────────────────┘     │
└─────────────────────────────────────────────────────────┘

---

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| **Agent Development Kit (ADK)** | Framework for building agent personas and defining cognitive skills |
| **Gemini (Multimodal)** | Foundation model for deep extraction from raw invoice images/PDFs |
| **Agent-to-Agent (A2A) Protocol** | Secure structured JSON communication between Extractor and Auditor agents |
| **Model Context Protocol (MCP)** | Grounding the Auditor with live enterprise rules from `config/company_policy.json` |
| **Agent Payments Protocol (AP2)** | Generating tamper-proof Verifiable Digital Credentials (VDCs) for settlement |
| **Universal Commerce Protocol (UCP)** | Validating real-time vendor checkout lifecycles |
| **Google Cloud Storage (GCS)** | Serverless invoice file ingestion storage layer |
| **Google Cloud Firestore** | NoSQL transactional state tracking and operational audit logs |
| **Google BigQuery** | Enterprise data warehouse for streaming analytical ledgers |
| **Agents CLI & Agent Runtime** | Unified deployment pipeline and managed cloud orchestration service |

---

## 📂 Project Structure

```text
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
└── README.md                     # This documentation file
⚙️ How It Works — Step by Step
1. Invoice Ingestion
Raw invoice documents are uploaded directly into a secure Google Cloud Storage bucket to trigger the orchestration framework.

2. Intelligent Data Extraction
The Extractor Agent leverages Gemini's multimodal parsing capabilities to interpret the document and transform unstructured assets into highly validated JSON structures:
{
  "invoice_id": "INV-2026-993",
  "vendor": "TechStore",
  "category": "hardware",
  "line_items": [{"description": "MacBook Pro M4", "amount": 149.99}],
  "total_amount_usd": 149.99
}

3. Compliance & Settlement Audit
The Compliance Auditor Agent intercepts the payload via the secure A2A Protocol loop and evaluates operational rules:

MCP Evaluation: Queries the business context to dynamically parse constraints inside config/company_policy.json.

UCP Verification: Connects to the active trade network ledger to verify vendor clearance fields.

AP2 Settlement Execution: Signs and issues a cryptographically secure Verifiable Digital Credential (VDC) automated mandate if all parameters clear compliance.

4. Cloud Sync & Telemetry
Simultaneously, the pipeline streams states down to the persistence layers:

Firestore: Updates the immediate operational transaction logs.

BigQuery: Injects analytics blocks into rows for reporting dashboards.

5. Final Engine Output Block
The orchestration process outputs a final execution block structured as follows:
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

Setup & Installation
Prerequisites
Python 3.11+

Active Google Cloud Account with required APIs enabled

Agents CLI (uv tool install google-agents-cli)

Install Dependencies
Bash
uv sync
Configure Environment
Bash
# Copy the placeholder environment file
cp .env.example .env
# Open and configure .env with your Project ID, Gemini API Keys, and Service accounts
Local Playground Testing
Bash
# Launch interactive agent playground
agents-cli playground

# Or execute the standard test suite script directly
uv run python test_run.py
Deploy to Agent Runtime Production
Bash
agents-cli deploy --region us-east1
🔒 Hard Production Constraints
Zero Hardcoded Secrets: All system credentials, keys, and endpoints are securely injected exclusively using externalized runtime environments.

Strict Boundary Mandates: AP2 micro-payment authorization parameters are dynamically restricted to match verified invoice ledger quantities.

Cloud-Managed Execution: The live architecture is deployed as a persistent, autonomous cloud-native service rather than transient local task runners.

📄 License
This project was successfully designed and compiled as a Capstone Project for the official Kaggle 5-Day AI Agents Intensive course. All rights reserved.
---

## 🏗️ Architecture Diagram
