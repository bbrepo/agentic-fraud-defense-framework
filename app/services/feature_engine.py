from __future__ import annotations
import math
from statistics import mean, pstdev
from app.core.event_store import EventStore
from app.core.graph_store import TransactionGraph
from app.models import FeatureVector, Transaction

class FeatureEngine:
    def __init__(self, events: EventStore, graph: TransactionGraph):
        self.events = events
        self.graph = graph

    def compute(self, tx: Transaction) -> FeatureVector:
        history = self.events.recent(tx.account_id)
        ten_min = self.events.recent_within(tx, 10)

        amounts = [h.amount for h in history]
        avg_amount = mean(amounts) if amounts else tx.amount
        std_amount = pstdev(amounts) if len(amounts) >= 2 else max(avg_amount * 0.25, 1.0)
        amount_z = (tx.amount - avg_amount) / max(std_amount, 1.0)

        devices = {h.device_id for h in history}
        countries = {h.country for h in history}

        new_device = bool(history) and tx.device_id not in devices
        country_changed = bool(history) and tx.country not in countries

        recent5 = history[-5:]
        seq_dev = 0.0
        if recent5:
            amount_component = min(1.0, abs(tx.amount - avg_amount) / max(avg_amount, 1.0))
            device_component = 0.35 if new_device else 0.0
            geo_component = 0.35 if country_changed else 0.0
            seq_dev = min(1.0, 0.55 * amount_component + device_component + geo_component)

        graph_risk = self.graph.risk_for_transaction(tx)

        return FeatureVector(
            amount_z=round(amount_z, 4),
            tx_count_10m=len(ten_min),
            amount_sum_10m=round(sum(x.amount for x in ten_min), 2),
            new_device=new_device,
            country_changed=country_changed,
            avg_amount_recent=round(avg_amount, 2),
            sequence_deviation=round(seq_dev, 4),
            graph_risk=round(graph_risk, 4),
        )
