from __future__ import annotations
from app.agents.investigator import InvestigatorAgent
from app.agents.response import ResponseAgent
from app.agents.triage import TriageAgent
from app.core.event_store import EventStore
from app.core.graph_store import TransactionGraph
from app.detectors.ensemble import DetectionEnsemble
from app.governance.audit import AuditLog
from app.governance.policy import PolicyEngine
from app.models import Decision, Feedback, Transaction
from app.services.feature_engine import FeatureEngine

class FraudDefenseOrchestrator:
    """Implements Sense → Reason → Decide → Act → Learn."""

    def __init__(self):
        self.events = EventStore()
        self.graph = TransactionGraph()
        self.features = FeatureEngine(self.events, self.graph)
        self.detectors = DetectionEnsemble()
        self.triage = TriageAgent()
        self.investigator = InvestigatorAgent(self.events, self.graph)
        self.response = ResponseAgent()
        self.policy = PolicyEngine()
        self.audit = AuditLog()
        self.feedback: dict[str, Feedback] = {}

    def evaluate(self, tx: Transaction) -> Decision:
        # SENSE
        f = self.features.compute(tx)

        # REASON
        d = self.detectors.evaluate(tx, f)
        triage = self.triage.run(d)
        investigation = self.investigator.run(tx, f)

        # DECIDE
        proposed = self.response.propose(tx, d, triage, investigation)
        governed = self.policy.apply(tx, d, proposed)

        # ACT (simulated; real integrations would call payment-control services)
        self.graph.add_transaction(tx)
        self.events.append(tx)

        # AUDIT
        audit_id = self.audit.write(
            tx.transaction_id,
            {
                "transaction": tx.model_dump(mode="json"),
                "features": f.model_dump(),
                "detectors": d.model_dump(),
                "triage": triage.model_dump(),
                "investigation": investigation.model_dump(),
                "proposed_action": proposed.value,
                "governance": governed.model_dump(),
            },
        )

        return Decision(
            transaction_id=tx.transaction_id,
            composite_risk=d.composite_risk,
            risk_level=triage.risk_level,
            action=governed.action,
            human_review_required=governed.human_review_required,
            explanation=d.reasons + governed.guardrail_reasons,
            detector_scores={
                "tabular": d.tabular_score,
                "sequence": d.sequence_score,
                "graph": d.graph_score,
                "anomaly": d.anomaly_score,
                "uncertainty": d.uncertainty,
            },
            investigation=investigation.evidence,
            policy_version=governed.policy_version,
            audit_id=audit_id,
        )

    def learn(self, feedback: Feedback) -> dict:
        # In a production implementation this would enqueue labels for
        # retraining, recalibration, graph-risk updates, and policy analysis.
        self.feedback[feedback.transaction_id] = feedback
        audit_id = self.audit.write(
            feedback.transaction_id,
            {
                "event": "analyst_feedback",
                "feedback": feedback.model_dump(),
            },
        )
        return {
            "status": "feedback-recorded",
            "transaction_id": feedback.transaction_id,
            "audit_id": audit_id,
            "learning_hook": "queued-for-future-model-and-policy-update",
        }
