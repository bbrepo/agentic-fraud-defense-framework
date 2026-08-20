from __future__ import annotations
from app.core.event_store import EventStore
from app.core.graph_store import TransactionGraph
from app.models import FeatureVector, InvestigationResult, Transaction

class InvestigatorAgent:
    def __init__(self, events: EventStore, graph: TransactionGraph):
        self.events = events
        self.graph = graph

    def run(self, tx: Transaction, f: FeatureVector) -> InvestigationResult:
        history = self.events.recent(tx.account_id)
        graph_context = self.graph.neighborhood(tx.account_id, radius=2)

        evidence = {
            "recent_transaction_count": len(history),
            "avg_recent_amount": f.avg_amount_recent,
            "new_device": f.new_device,
            "country_changed": f.country_changed,
            "tx_count_10m": f.tx_count_10m,
            "graph_degree": graph_context["degree"],
            "flagged_graph_nodes": graph_context["flagged_nodes"],
        }

        signals = []
        if f.new_device:
            signals.append("new device")
        if f.country_changed:
            signals.append("geographic change")
        if abs(f.amount_z) > 2:
            signals.append("amount deviation")
        if graph_context["flagged_nodes"]:
            signals.append("flagged graph proximity")
        if not signals:
            signals.append("no major corroborating signal")

        summary = "Investigation assembled: " + ", ".join(signals) + "."
        return InvestigationResult(evidence=evidence, summary=summary)
