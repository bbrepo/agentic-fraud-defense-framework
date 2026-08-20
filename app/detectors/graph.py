from app.models import FeatureVector

class GraphScorer:
    """Relational risk scorer representing graph-based coordinated-fraud detection."""

    def score(self, f: FeatureVector) -> tuple[float, list[str]]:
        score = min(1.0, 0.05 + 0.95 * f.graph_risk)
        reasons = []
        if score >= 0.5:
            reasons.append("Counterparty neighborhood contains elevated-risk relationships.")
        return score, reasons
