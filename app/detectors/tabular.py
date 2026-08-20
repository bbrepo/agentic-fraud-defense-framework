from __future__ import annotations
from app.models import FeatureVector, Transaction

class TabularScorer:
    """Fast explainable proxy for a production gradient-boosted model."""

    def score(self, tx: Transaction, f: FeatureVector) -> tuple[float, list[str]]:
        risk = 0.05
        reasons: list[str] = []

        if f.amount_z > 2.0:
            risk += min(0.35, 0.08 * f.amount_z)
            reasons.append("Amount is materially above the account's recent baseline.")

        if f.tx_count_10m >= 4:
            risk += min(0.25, 0.04 * f.tx_count_10m)
            reasons.append("Recent transaction velocity is elevated.")

        if f.new_device:
            risk += 0.18
            reasons.append("Transaction originated from a previously unseen device.")

        if f.country_changed:
            risk += 0.18
            reasons.append("Transaction geography differs from recent account behavior.")

        if tx.kyc_score < 0.55:
            risk += 0.18
            reasons.append("Identity/KYC confidence is below the preferred threshold.")

        return min(1.0, risk), reasons
