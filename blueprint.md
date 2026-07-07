# [Smart Invoice Auditor & Autonomous Settlement Agent] Specification

## Goal

This project is a production-grade, cloud-deployed Multi-Agent AI system built with the course Agent Development Kit (ADK) and deployed via the Agents CLI to the official Agent Runtime environment. It serves small-to-medium businesses (SMBs) and corporate finance departments by securely uploading raw invoices to Google Cloud Storage (GCS), extracting transaction data using multimodal Gemini models, auditing compliance via local Model Context Protocol (MCP) servers, logging operational status in Google Cloud Firestore, and—upon validation—initiating secure machine-to-machine financial execution via the Agent Payments Protocol (AP2) and Universal Commerce Protocol (UCP), with final ledger analytics streamed directly into Google BigQuery.
## Context

The agent architecture utilizes the complete Kaggle course toolkit, Google Cloud ecosystem, and protocol stack across its deployment lifecycle:

Antigravity IDE & Gemini CLI: The unified workspace for writing agent code, managing environment variables, and testing localized model reasoning.

Agent Development Kit (ADK): The framework used to build distinct agent personas (Extractor and Compliance Auditor) and define their native skills.

Agent-to-Agent (A2A) Protocol: Governs internal secure communication, data handoffs, and credential sharing between operational agents.

Model Context Protocol (MCP): Powers the data connectors that ground the Compliance Auditor with live context from local configuration files like config/company_policy.json.

Agent Payments Protocol (AP2) & Universal Commerce Protocol (UCP): The commerce primitives responsible for generating tamper-proof Closed Payment Mandates and verifying transaction checkout lifecycles with external vendors.

Agents CLI & Agent Runtime: The deployment pipeline used to validate, package, and deploy the local ADK configuration into a managed live cloud process.

Google Cloud Storage (GCS): Acts as the ingestion bucket for raw incoming invoice files (images/PDFs).

Google Cloud Firestore: The primary NoSQL database used to track transactional states, active agent sessions, and invoice approval workflows.

Google BigQuery: The centralized data warehouse where final audited ledger logs are streamed for corporate accounting and analytics.

## Requirements

- Initialize the dual-agent codebase using standard ADK paradigms inside the Antigravity workspace.

- Implement an active MCP server tool that pulls real-time enterprise rules and expense caps from config/company_policy.json.

- Leverage Gemini's multimodal inputs to process raw unstructured invoice files fetched directly from Google Cloud Storage (GCS).

- Configure A2A communication protocols so the Data Extractor passes sanitized, structured JSON data directly to the Compliance Auditor.

- Integrate UCP endpoints as a custom ADK Skill to perform an active out-of-band validation check against the merchant's inventory/cart state.

- Integrate AP2 libraries as a custom ADK Skill to issue cryptographically signed, restricted Verifiable Digital Credentials (VDCs) for compliant transactions.

- Log real-time transaction tracking metrics and audit state updates directly to a Google Cloud Firestore collection.

- Write a valid deployment manifest (agent.toml) that specifies the agent entry points, runtime protocols, and environment variables.

- Execute the official agents deploy command via the Agents CLI to successfully spin up the live agent on the Agent Runtime cluster.

- Stream the unified final audit ledger telemetry directly into a Google BigQuery table for long-term historical records.

## Hard constraints

Zero Hardcoded Secrets: All system credentials, Google Cloud service account keys, and Gemini API tokens must be injected into the Agent Runtime dynamically via environment variables; code-level strings are strictly prohibited.

Strict Boundary Mandates: Any AP2 payment credential generated in runtime must explicitly match the line-item total extracted from the invoice to prevent arbitrary agent spending.

No Direct Local Executions in Production: The final system evaluation must demonstrate the agent running as a persistent cloud-managed service within the Agent Runtime, not as a local shell script.

Kaggle Milestone Timeline: The production deployment, database logging verification, and the required 5-minute video presentation must be completed before the hard close on July 7, 2026.
## Out of scope
Building a graphical web front-end interface, mobile app, or dashboard (all validation inputs, deployment reporting, and logs run through the CLI and runtime outputs).

Routing live money through real-world corporate banking networks or processing production financial settlements (all AP2/UCP layers will target course-provided sandboxes).
## Expected output

When an invoice is processed through the active deployment in the Agent Runtime, the system returns a unified execution ledger block and syncs it across Google Cloud systems:


{
  "deployment_telemetry": {
    "agent_id": "adk-invoice-auditor-prod-86",
    "runtime_environment": "Kaggle_Agent_Runtime_v3",
    "deployment_status": "ACTIVE_RUNNING"
  },
  "transaction_lifecycle": {
    "timestamp": "2026-07-03T21:45:00Z",
    "raw_gcs_source": "gs://invoice-bucket-fozia86/raw/receipt_041.png",
    "ucp_handshake": {
      "session_id": "ucp_session_9941a",
      "status": "VERIFIED_MATCH"
    },
    "audit_verdict": {
      "status": "APPROVED",
      "mcp_context_used": "company_policy.json",
      "flags_raised": 0
    },
    "ap2_execution": {
      "mandate_status": "GENERATED_AND_SIGNED",
      "mandate_id": "MND-AP2-77312B",
      "spending_cap": 149.99,
      "currency": "USD",
      "cryptographic_proof": "sig:0x9e33b47c...a12b"
    }
  },
  "cloud_database_sync": {
    "firestore_log": {
      "collection": "transactions",
      "document_id": "TXN_77312B",
      "status": "SAVED"
    },
    "bigquery_stream": {
      "dataset": "finance_audit",
      "table": "ledger_stream",
      "status": "SUCCESS"
    }
  }
}
## Architecture

### System Overview

The Smart Invoice Auditor operates as a **dual-agent pipeline** orchestrated through a central root agent built on the Agent Development Kit (ADK). The root agent (`src/agent.py`) exposes a single `process_invoice` tool that drives the full transaction lifecycle from raw invoice ingestion to payment mandate generation and cloud telemetry sync.

### Agent Topology

```
┌─────────────────────────────────────────────────────────────────────┐
│                        ROOT AGENT (ADK)                            │
│               model: gemini-flash-latest                           │
│               tool:  process_invoice(gcs_uri)                      │
└──────────────┬──────────────────────────────────┬──────────────────┘
               │                                  │
       ┌───────▼────────┐               ┌────────▼─────────┐
       │  EXTRACTOR      │    A2A JSON   │  COMPLIANCE      │
       │  AGENT          │──────────────▶│  AUDITOR AGENT   │
       │                 │               │                  │
       │ • Gemini Multi- │               │ • MCP Policy     │
       │   modal Parsing │               │   Lookup         │
       │ • GCS Fetch     │               │ • UCP Vendor     │
       │ • Structured    │               │   Verification   │
       │   Data Output   │               │ • AP2 Mandate    │
       └─────────────────┘               │   Generation     │
                                         └────────┬─────────┘
                                                  │
                              ┌────────────────────┼──────────────────┐
                              │                    │                  │
                     ┌────────▼──────┐  ┌─────────▼──────┐  ┌───────▼────────┐
                     │  FIRESTORE    │  │  BIGQUERY       │  │  AP2 / UCP     │
                     │  Transaction  │  │  Ledger Stream  │  │  Settlement    │
                     │  Log          │  │  Analytics      │  │  Execution     │
                     └───────────────┘  └────────────────┘  └────────────────┘
```

### Data Flow

1. **Ingestion**: A raw invoice file (image/PDF) is uploaded to a designated GCS bucket (`gs://invoice-bucket-fozia86/raw/`).
2. **Extraction**: The Extractor Agent receives the GCS URI, fetches the file, and uses Gemini's multimodal capabilities to parse unstructured invoice data into a structured JSON payload containing vendor name, category, line items, and totals.
3. **A2A Handoff**: The structured JSON is passed from the Extractor to the Compliance Auditor via the Agent-to-Agent (A2A) protocol as a sanitized JSON string.
4. **MCP Policy Lookup**: The Auditor queries the local MCP server (`mcp_server.py`) which reads `config/company_policy.json` to retrieve the spending limits, approval thresholds, and allowed/blocked vendor lists for the invoice's category.
5. **Compliance Check**: The Auditor validates the invoice total against the policy's `max_limit`, checks for blocked vendors, and flags transactions exceeding `approval_required_above` thresholds.
6. **UCP Verification**: For approved invoices, the Auditor initiates an out-of-band vendor checkout verification via the Universal Commerce Protocol to confirm the merchant's cart/inventory state matches the invoice claim.
7. **AP2 Mandate Generation**: Upon successful UCP verification, the Auditor issues a cryptographically signed Closed Payment Mandate (VDC) via the Agent Payments Protocol, with the spending cap explicitly bound to the extracted invoice total.
8. **Cloud Sync**: The unified ledger block (deployment telemetry + transaction lifecycle + cloud sync status) is logged to Google Cloud Firestore for real-time state tracking and streamed to Google BigQuery for long-term analytics.

### Protocol Interactions

| Protocol | Role | Implementation |
|----------|------|----------------|
| **A2A** | Inter-agent data handoff between Extractor and Auditor | JSON serialization via function call parameter passing |
| **MCP** | Grounding the Auditor with live enterprise policy context | `mcp_server.py` reads `config/company_policy.json` at query time |
| **AP2** | Generating tamper-proof payment mandates for compliant transactions | `ap2_payment.py` issues VDCs with SHA-256 signed payloads |
| **UCP** | Validating vendor checkout state before payment authorization | `ucp_commerce.py` performs merchant inventory/cart verification |

## Tech Stack

### Core Frameworks & SDKs

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | ≥ 3.11, < 3.14 | Primary runtime language |
| Google ADK (`google-adk[gcp]`) | Latest | Agent Development Kit — agent definition, tool binding, orchestration |
| Gemini (`gemini-flash-latest`) | Latest | Multimodal LLM for invoice parsing and agent reasoning |
| MCP Server Core (`mcp-server-core`) | Latest | Model Context Protocol server for enterprise rule grounding |

### Google Cloud Services

| Service | Resource | Purpose |
|---------|----------|---------|
| Google Cloud Storage (GCS) | `invoice-bucket-fozia86` | Raw invoice file ingestion bucket |
| Google Cloud Firestore | Collection: `transactions` | Real-time transaction state tracking and audit logs |
| Google BigQuery | Dataset: `finance_audit`, Table: `ledger_stream` | Centralized ledger analytics and historical records |
| Vertex AI Agent Engine | Region: `us-east1` | Managed Agent Runtime for production deployment |
| Cloud Logging | — | Operational log aggregation |
| Cloud Build | — | Container build pipeline for deployment |

### Protocol Libraries

| Library | Purpose |
|---------|---------|
| `ap2_payment.py` | Agent Payments Protocol — VDC mandate generation with SHA-256 signatures |
| `ucp_commerce.py` | Universal Commerce Protocol — vendor checkout lifecycle verification |
| `superagi-mcp` | MCP client/server bindings for tool integration |

### Infrastructure & DevOps

| Tool | Purpose |
|------|---------|
| Agents CLI (`agents-cli`) | Deployment pipeline — validate, package, deploy to Agent Runtime |
| Terraform | Infrastructure as Code for GCP resource provisioning |
| OpenTelemetry | GenAI telemetry instrumentation with GCS export |
| Hatchling | Python build backend |
| Ruff | Linting and code formatting |
| pytest / pytest-asyncio | Testing framework |

### Environment Configuration

All secrets and runtime configuration are injected via environment variables (never hardcoded):

| Variable | Description |
|----------|-------------|
| `GOOGLE_CLOUD_PROJECT` | GCP project ID |
| `GOOGLE_CLOUD_LOCATION` | GCP region (e.g., `us-east1`) |
| `GOOGLE_GENAI_API_KEY` | Gemini API authentication token |
| `GCS_INVOICE_BUCKET` | GCS bucket for raw invoice files |
| `FIRESTORE_COLLECTION` | Firestore collection for transaction logs |
| `BIGQUERY_DATASET` | BigQuery dataset for ledger analytics |
| `BIGQUERY_TABLE` | BigQuery table for streaming audit records |

## Implementation Details

### Root Orchestrator (`src/agent.py`)

The root agent is the system's entry point, registered as an ADK `Agent` with a single `process_invoice` tool. When invoked with a GCS URI:

1. Calls `extract_invoice_data(gcs_uri)` from the Extractor module to parse the invoice.
2. Serializes the extraction result to JSON and passes it to `audit_and_execute(invoice_json_str)` in the Auditor module.
3. Calls `log_to_firestore()` and `stream_to_bigquery()` to sync the transaction to cloud databases.
4. Assembles the final unified ledger block containing `deployment_telemetry`, `transaction_lifecycle`, and `cloud_database_sync` segments.
5. Returns the complete JSON response matching the expected output schema.

The root agent is wrapped in an ADK `App` instance named `"src"` which serves as the Agents CLI entry point.

### Data Extractor Agent (`src/agents/extractor.py`)

Responsible for transforming raw unstructured invoice files into structured JSON. The extraction function:

- Accepts a GCS URI pointing to an invoice image or PDF.
- Leverages Gemini's multimodal input capabilities to parse visual/document content.
- Outputs a normalized JSON object with fields: `invoice_id`, `vendor`, `category`, `line_items` (array of `{description, amount}`), and `total_amount_usd`.
- Defines a standalone `extractor_agent` ADK Agent for potential direct A2A invocation.

### Compliance Auditor Agent (`src/agents/auditor.py`)

Executes the full compliance and settlement pipeline:

1. **Policy Retrieval**: Calls `get_company_policy(category)` via the MCP server to load the relevant spending rules from `config/company_policy.json`.
2. **Compliance Validation**: Compares the invoice total against `max_limit` for the category. Transactions exceeding the limit are immediately rejected with a `REJECTED` status.
3. **UCP Vendor Verification**: Initiates a `verify_vendor_checkout()` call to confirm the vendor's inventory/cart state aligns with the invoice claim. Returns a `session_id` and `VERIFIED_MATCH` status.
4. **AP2 Mandate Issuance**: Generates a cryptographically signed VDC via `issue_vdc_mandate()`, binding the `spending_cap` to the exact invoice total. The mandate includes a unique `MND-AP2-{hex}` identifier and a SHA-256 `cryptographic_proof` signature.
5. **Result Assembly**: Returns the full `transaction_lifecycle` object with nested `ucp_handshake`, `audit_verdict`, and `ap2_execution` blocks.

### MCP Server Tool (`src/tools/mcp_server.py`)

A local Model Context Protocol server that provides real-time enterprise context to the Compliance Auditor:

- Reads `config/company_policy.json` at query time (no caching — always reflects the latest policy state).
- Supports category-based lookups (`hardware`, `software`, `travel`, `general`).
- Falls back to the `general` category if the requested category is not found.
- Returns the full policy object including `max_limit`, `approval_required_above`, `allowed_vendors`, and references the global `blocked_vendors` list.

### AP2 Payment Handler (`src/tools/ap2_payment.py`)

Implements the Agent Payments Protocol for generating tamper-proof payment credentials:

- Generates a unique mandate ID using the format `MND-AP2-{6-character-hex}`.
- Constructs a payload containing `spending_cap`, `currency`, `vendor`, and `mandate_id`.
- Produces a SHA-256 cryptographic signature over the JSON-serialized payload.
- Returns a structured mandate object with `mandate_status: GENERATED_AND_SIGNED`, the cap, currency, and truncated `cryptographic_proof` prefixed with `sig:0x`.

### UCP Commerce Connector (`src/tools/ucp_commerce.py`)

Implements the Universal Commerce Protocol for out-of-band vendor verification:

- Accepts a `session_id`, `vendor_name`, and `expected_total`.
- Performs a validation check against the merchant's inventory/cart state.
- Returns a verification object with the `session_id` and `status: VERIFIED_MATCH` confirming the vendor's checkout lifecycle aligns with the invoice.

### Cloud Sync Module (`src/cloud_sync.py`)

Handles persistence of the unified ledger block to Google Cloud databases:

- **Firestore Logging**: Writes the transaction payload to the configured Firestore collection with a document ID derived from the transaction ID (e.g., `TXN_77312B`).
- **BigQuery Streaming**: Streams the final audit record to the `finance_audit.ledger_stream` BigQuery table for long-term analytical queries and corporate accounting.

### Agent Runtime Wrapper (`src/agent_runtime_app.py`)

Production deployment wrapper extending `AdkApp` from Vertex AI:

- **Setup**: Initializes Vertex AI SDK, configures OpenTelemetry instrumentation, and sets up Cloud Logging.
- **Feedback**: Registers a `/feedback` endpoint with Pydantic validation for user feedback collection.
- **Artifact Service**: Configures GCS-backed artifact storage (falls back to in-memory for local development).
- **Telemetry**: Integrates with OpenTelemetry for GenAI-specific instrumentation using `NO_CONTENT` mode (metadata only, no prompt/response data logged).

## Deployment

### Deployment Manifest (`agent.toml`)

The `agent.toml` file defines the complete deployment configuration for the Agents CLI:

```toml
[agent]
name = "invoice-auditor-agent"
version = "0.1.0"
model = "gemini-flash-latest"
runtime = "agent_runtime"
region = "us-east1"
```

Key configuration sections:
- **Sub-agents**: Declares both `extractor` and `auditor` agents with their module entry points.
- **Tools**: Registers `mcp_server`, `ap2_payment`, and `ucp_commerce` as available tools.
- **Protocols**: Enables A2A, MCP, AP2, and UCP protocol support.
- **Environment**: Maps all required environment variables for cloud resource access.
- **Cloud Resources**: Declares GCS bucket, Firestore collection, and BigQuery dataset/table bindings.

### Deployment Pipeline

1. **Local Development**: Run the ADK dev server locally via Agents CLI (`agents run`) on `127.0.0.1:18080` with in-memory session services for rapid iteration.
2. **Validation**: The Agents CLI validates the `agent.toml` manifest, verifies tool bindings, and checks environment variable requirements.
3. **Packaging**: The CLI packages the agent source code, dependencies, and configuration into a deployable artifact.
4. **Deployment**: Execute `agents deploy` to push the packaged agent to the Vertex AI Agent Engine (Reasoning Engine) in the `us-east1` region.
5. **Runtime**: The Agent Runtime manages the deployed agent as a persistent cloud service with auto-scaling (1–10 instances), 4 vCPU, and 8Gi RAM per instance.

### Infrastructure as Code (Terraform)

The `deployment/terraform/` directory contains a complete Terraform configuration for provisioning the GCP infrastructure:

| Resource | File | Description |
|----------|------|-------------|
| GCP APIs | `apis.tf` | Enables 10 required APIs (AI Platform, Cloud Build, Cloud Run, BigQuery, etc.) |
| IAM | `iam.tf` | Service account creation with scoped roles for Vertex AI, GCS, Firestore, BigQuery |
| Agent Runtime | `service.tf` | `google_vertex_ai_reasoning_engine` resource with scaling and resource limits |
| Storage | `storage.tf` | GCS bucket for operational logs |
| Telemetry | `telemetry.tf` | BigQuery dataset, log sinks, external tables, and completions SQL view |
| Variables | `vars/env.tfvars` | Concrete environment values (project ID, region) |

## Testing & Evaluation

### Test Strategy

The project employs a three-tier testing approach:

#### Unit Tests (`tests/unit/`)

- Validate individual tool functions in isolation (MCP policy lookup, AP2 mandate generation, UCP verification).
- Verify data transformation correctness between extraction output and auditor input schemas.

#### Integration Tests (`tests/integration/`)

- **Agent Streaming Test** (`test_agent.py`): Validates the root agent's ADK `Runner` integration with `InMemorySessionService`, ensuring SSE streaming responses contain expected text content.
- **Agent Runtime App Test** (`test_agent_runtime_app.py`): Tests the `AgentEngineApp` wrapper's async streaming pipeline and feedback registration endpoint (valid and invalid inputs) using `monkeypatch` for environment isolation.

#### Evaluation Framework (`tests/eval/`)

- **Configuration** (`eval_config.yaml`): Defines custom evaluation metrics:
  - `custom_response_quality`: LLM-as-judge metric that grades agent responses on a 1–5 scale for relevance, accuracy, and completeness.
  - `agent_turn_count`: Python function metric that counts conversation turns to measure efficiency.
- **Dataset** (`datasets/basic-dataset.json`): Evaluation test cases with expected input/output pairs for benchmarking agent performance.

### Running Tests

```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# Evaluation
agents eval --config tests/eval/eval_config.yaml
```

## Milestones & Timeline

| Milestone | Target Date | Deliverable | Status |
|-----------|-------------|-------------|--------|
| **M1: Project Initialization** | July 3, 2026 | ADK scaffold, agent.toml, project structure, config files | ✅ Complete |
| **M2: Core Agent Implementation** | July 3, 2026 | Extractor agent, Auditor agent, MCP server, AP2/UCP tools | ✅ Complete |
| **M3: Cloud Integration** | July 4, 2026 | Firestore logging, BigQuery streaming, GCS ingestion | 🔄 In Progress |
| **M4: Deployment to Agent Runtime** | July 5, 2026 | Successful `agents deploy`, live cloud-managed service | ⏳ Pending |
| **M5: End-to-End Validation** | July 6, 2026 | Full pipeline test on Agent Runtime, database verification | ⏳ Pending |
| **M6: Submission** | July 7, 2026 | 5-minute video presentation, Kaggle submission, documentation | ⏳ Pending |

### Critical Path

```
M1 (Scaffold) → M2 (Agents) → M3 (Cloud) → M4 (Deploy) → M5 (Validate) → M6 (Submit)
                                    │                           │
                                    └──── Terraform Apply ──────┘
```

**Hard Deadline**: July 7, 2026 — Production deployment, database logging verification, and 5-minute video presentation must all be completed.

## Structure

invoice-auditor-agent/
│
├── config/
│   └── company_policy.json       # MCP context file (spending limits & compliance rules)
│
├── src/
│   ├── agent.py                  # Root orchestrator — ADK Agent with process_invoice tool
│   ├── cloud_sync.py             # Firestore & BigQuery cloud sync module
│   ├── agent_runtime_app.py      # Vertex AI Agent Engine deployment wrapper
│   ├── __init__.py               # Package entry point — exports app for Agents CLI
│   │
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
│   └── app_utils/
│       ├── telemetry.py          # OpenTelemetry instrumentation for GenAI tracing
│       └── typing.py             # Pydantic models for feedback validation
│
├── tests/
│   ├── unit/
│   │   └── test_dummy.py         # Unit test placeholder
│   ├── integration/
│   │   ├── test_agent.py         # ADK agent streaming integration test
│   │   └── test_agent_runtime_app.py  # Agent Runtime wrapper tests
│   └── eval/
│       ├── eval_config.yaml      # Evaluation metrics configuration
│       └── datasets/
│           └── basic-dataset.json    # Eval test cases
│
├── deployment/
│   └── terraform/                # Complete IaC for GCP resource provisioning
│       ├── providers.tf          # Google provider configuration
│       ├── variables.tf          # Input variable definitions
│       ├── apis.tf               # GCP API enablement
│       ├── iam.tf                # Service account & role bindings
│       ├── service.tf            # Vertex AI Reasoning Engine resource
│       ├── storage.tf            # GCS logging bucket
│       ├── telemetry.tf          # BigQuery dataset, log sinks, tables
│       ├── outputs.tf            # Infrastructure output values
│       └── vars/
│           └── env.tfvars        # Concrete environment values
│
├── .env                          # Strictly local: Google Cloud & Gemini credentials
├── .gitignore                    # Git exclusion rules
├── agent.toml                    # Agents CLI Deployment Manifest for Agent Runtime
├── agents-cli-manifest.yaml      # Agents CLI project configuration
├── deployment_metadata.json      # Deployment state tracker
├── pyproject.toml                # Python project & build configuration
├── requirements.txt              # Project library dependencies
├── test_run.py                   # Manual end-to-end smoke test
├── GEMINI.md                     # AI coding agent development playbook
└── README.md                     # Documentation for Kaggle submission