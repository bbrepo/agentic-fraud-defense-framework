# Agentic AI Fraud Defense Framework

A runnable research prototype that operationalizes the five-layer architecture proposed in the paper **“A Framework for Agentic AI-Driven Financial Fraud Detection, Investigation, and Risk Mitigation in Real-Time Payment Ecosystems.”**

> **Scope:** This repository is a research/demo implementation. It is not a production payment system, does not process real financial data, and does not claim the illustrative performance figures from the paper as measured results.

## Architecture

The implementation mirrors the paper's five layers:

1. **L1 — Real-Time Ingestion**
   - Receives payment events, device signals, and KYC-related fields.
   - Demo implementation exposes a FastAPI endpoint and an in-memory event stream abstraction.

2. **L2 — Feature & Graph Store**
   - Builds transaction velocity, amount deviation, geolocation/device consistency, and recent-history features.
   - Maintains an account-device-merchant-counterparty transaction graph.

3. **L3 — Detection & Reasoning**
   - **Tabular scorer:** fast feature-based risk score.
   - **Sequence scorer:** behavioral deviation over recent account activity.
   - **Graph scorer:** relational risk based on suspicious neighborhoods and shared entities.
   - **Explainer:** produces human-readable reasons for the composite score.

4. **L4 — Agentic Orchestration**
   - **Triage Agent:** ranks and routes alerts.
   - **Investigator Agent:** gathers graph, device, and historical evidence.
   - **Response Agent:** selects a proportionate action: `RELEASE`, `STEP_UP`, `SOFT_HOLD`, or `ESCALATE`.

5. **L5 — Governance & Risk**
   - Policy guardrails bound autonomous actions.
   - Every decision is written to an audit trail.
   - High-impact cases can be forced to human review.
   - Analyst feedback can be fed back into the system.

The closed loop is:

**Sense → Reason → Decide → Act → Learn**

## Why this repository is useful

This project converts a conceptual research framework into an executable software artifact that demonstrates:

- layered fraud-defense architecture;
- low-latency-oriented decision flow;
- graph-aware investigation;
- explainable risk decisions;
- bounded agent autonomy;
- human-in-the-loop escalation;
- auditability and policy governance;
- continual-learning feedback hooks.

## Quick start

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the API

```bash
uvicorn app.main:app --reload
```

Open:

- Swagger UI: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

### 4. Score a transaction

```bash
curl -X POST "http://127.0.0.1:8000/v1/transactions/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "tx-demo-001",
    "account_id": "acct-100",
    "merchant_id": "merchant-77",
    "counterparty_id": "cp-22",
    "device_id": "device-new",
    "amount": 1250.00,
    "currency": "USD",
    "country": "US",
    "channel": "RTP",
    "timestamp": "2026-08-20T18:30:00Z",
    "kyc_score": 0.82
  }'
```

## Demo

Run a synthetic scenario:

```bash
python -m app.demo
```

The demo creates a normal behavioral baseline, then injects a suspicious real-time payment with a new device, high amount, and graph risk. It prints:

- detector scores,
- triage decision,
- investigation evidence,
- response action,
- explanation,
- governance result,
- audit record ID.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/v1/transactions/evaluate` | Run full agentic decision loop |
| POST | `/v1/feedback` | Submit analyst feedback / outcome |
| GET | `/v1/audit/{transaction_id}` | Retrieve audit records |
| GET | `/v1/graph/account/{account_id}` | Inspect graph neighborhood |

## Example decision object

```json
{
  "transaction_id": "tx-demo-001",
  "composite_risk": 0.87,
  "risk_level": "HIGH",
  "action": "SOFT_HOLD",
  "human_review_required": true,
  "explanation": [
    "Amount is materially above the account's recent baseline.",
    "Transaction originated from a previously unseen device.",
    "Counterparty neighborhood contains elevated-risk relationships."
  ]
}
```

## Design principles

### Bounded autonomy
The response agent cannot execute arbitrary actions. It chooses only from a policy-defined action envelope.

### Explainability by default
Every decision includes reasons; explanations are not an optional dashboard feature.

### Defense in depth
The system combines tabular, temporal, and graph signals rather than depending on one model.

### Human authority
Policy can force escalation when risk, uncertainty, amount, or action impact exceeds configurable thresholds.

### Auditability
Inputs, detector scores, agent outputs, policy version, action, and feedback are logged.

## Repository layout

```text
agentic-fraud-defense-framework/
├── app/
│   ├── agents/
│   ├── core/
│   ├── detectors/
│   ├── governance/
│   ├── services/
│   ├── demo.py
│   ├── main.py
│   ├── models.py
│   └── settings.py
├── docs/
│   ├── ARCHITECTURE.md
│   ├── EB2_NIW_PROJECT_SUMMARY.md
│   └── MODEL_CARD.md
├── tests/
├── .github/workflows/
├── Dockerfile
├── LICENSE
├── pyproject.toml
└── requirements.txt
```

## Extending the prototype

The interfaces are intentionally replaceable. Future implementations can swap in:

- XGBoost / LightGBM for tabular scoring;
- LSTM / Transformer sequence models;
- Neo4j / Amazon Neptune for graph storage;
- graph neural networks for coordinated-fraud detection;
- SHAP for local explanations;
- Kafka / Pulsar for streaming ingestion;
- Redis / Feast for online feature serving;
- MLflow for model registry and lineage;
- constrained reinforcement learning for response-policy optimization;
- federated learning for cross-institution collaboration.

## Responsible-use note

Financial decisions can materially affect people. Before any real deployment, this prototype would require security review, privacy controls, fairness testing, model validation, regulatory review, incident response procedures, data-governance controls, and clearly defined human appeal/override processes.

## Citation

If you build on the academic framework, cite the original paper:

> Biswas, B., et al. (2026). *A Framework for Agentic AI-Driven Financial Fraud Detection, Investigation, and Risk Mitigation in Real-Time Payment Ecosystems.* International Journal of Computer Information Systems and Industrial Management Applications, 18(3s), 1029–1040.

