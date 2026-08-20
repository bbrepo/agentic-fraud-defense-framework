from app.models import FeatureVector

class SequenceScorer:
    """Behavioral scorer representing the paper's sequence-model role."""

    def score(self, f: FeatureVector) -> tuple[float, list[str]]:
        score = min(1.0, 0.08 + 0.9 * f.sequence_deviation)
        reasons = []
        if score >= 0.5:
            reasons.append("Recent behavior deviates from the account's temporal pattern.")
        return score, reasons
