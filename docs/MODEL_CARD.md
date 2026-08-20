# Model Card — Research Prototype

## Intended use
Demonstrate how multiple fraud signals can be orchestrated into an explainable, policy-bounded decision loop.

## Not intended for
- production payment authorization;
- consumer credit decisions;
- sanctions decisions;
- legal determinations;
- autonomous blocking of real customer funds.

## Data
The repository ships with no real customer or financial data. The demo uses synthetic transactions.

## Current detectors
The implementation uses deterministic proxy scorers for tabular, sequence, graph, and anomaly roles. These are architectural placeholders, not validated fraud models.

## Known limitations
- no benchmark dataset is bundled;
- no empirical performance claim is made;
- no calibrated probability output;
- no protected-class fairness evaluation;
- in-memory graph and event history;
- no distributed streaming infrastructure;
- no adversarial robustness validation;
- no formal constrained-policy optimization.

## Governance
The response agent is bounded by an explicit policy layer. High-risk and high-value transactions can be escalated for human review.

## Recommended validation before real-world use
Independent model validation, data-governance approval, privacy review, security review, fairness testing, performance and latency benchmarking, explainability validation, red teaming, regulatory review, and shadow deployment.
