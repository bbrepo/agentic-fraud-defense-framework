# Architecture Mapping to the Paper

This repository is organized as a direct software mapping of the paper's proposed five-layer architecture.

## L1 — Real-Time Ingestion

**Paper role:** ingest payment-rail messages, stream-bus events, device signals, and KYC/identity signals.

**Prototype implementation:**
- `app/main.py` — FastAPI ingestion boundary.
- `app/models.py` — normalized transaction event.
- `app/core/event_store.py` — ordered account-level history for the demo.

A production implementation could replace the HTTP boundary with Kafka, Pulsar, or another durable streaming bus.

## L2 — Feature & Graph Store

**Paper role:** transform raw events into fraud-relevant features and maintain a graph connecting accounts, devices, merchants, and counterparties.

**Prototype implementation:**
- `app/services/feature_engine.py`
- `app/core/graph_store.py`

Current features include:
- recent transaction velocity,
- short-window amount sum,
- amount deviation,
- unseen device,
- geographic change,
- behavioral sequence deviation,
- graph-neighborhood risk.

## L3 — Detection & Reasoning

The paper deliberately uses multiple analytical components rather than one monolithic model.

**Prototype components:**
- `TabularScorer`
- `SequenceScorer`
- `GraphScorer`
- `AnomalyScorer`
- `DetectionEnsemble`

The code uses deterministic research-prototype scorers so that the repository is runnable without a proprietary financial dataset. The interfaces are designed so trained XGBoost, Transformer, GNN, or anomaly models can be dropped in later.

## L4 — Agentic Orchestration

The paper assigns specialized responsibilities to three agents.

### Triage Agent
Ranks risk and routes the alert.

Implementation: `app/agents/triage.py`

### Investigator Agent
Assembles corroborating evidence from recent history and transaction-graph context.

Implementation: `app/agents/investigator.py`

### Response Agent
Chooses a proportionate action.

Implementation: `app/agents/response.py`

Authorized prototype actions:
- `RELEASE`
- `STEP_UP`
- `SOFT_HOLD`
- `ESCALATE`

## L5 — Governance & Risk

The paper treats governance as a first-class layer.

Prototype controls:
- human-review thresholds;
- high-value transaction escalation;
- cap on autonomous soft holds;
- versioned policy;
- complete audit record;
- feedback logging for future learning.

Implementation:
- `app/governance/policy.py`
- `app/governance/audit.py`

## Closed Decision Loop

`FraudDefenseOrchestrator` implements the paper's cycle:

1. **Sense** — receive transaction and compute context.
2. **Reason** — run multi-signal detection and investigation.
3. **Decide** — triage, propose response, apply governance.
4. **Act** — simulate release/challenge/hold/escalation.
5. **Learn** — accept analyst feedback for future model/policy updates.

## Productionization Roadmap

The current code is intentionally dataset-independent. A defensible next phase would be:

1. stream benchmark or synthetic transactions through Kafka;
2. implement online feature serving in Redis/Feast;
3. train calibrated XGBoost and Transformer models;
4. persist the graph in Neo4j/Neptune;
5. add SHAP explanations;
6. add MLflow model/version lineage;
7. perform latency benchmarks;
8. measure precision, recall, F1, PR-AUC/ROC-AUC, false-positive rate, and analyst time;
9. run fairness and drift monitoring;
10. perform a shadow-mode pilot before allowing any autonomous payment action.
