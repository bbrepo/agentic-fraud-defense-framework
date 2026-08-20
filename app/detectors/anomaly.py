from app.models import FeatureVector

class AnomalyScorer:
    """Label-free novelty proxy for unseen fraud patterns."""

    def score(self, f: FeatureVector) -> tuple[float, list[str]]:
        components = [
            min(1.0, max(0.0, abs(f.amount_z) / 5.0)),
            min(1.0, f.tx_count_10m / 8.0),
            1.0 if f.new_device else 0.0,
            1.0 if f.country_changed else 0.0,
        ]
        score = sum(components) / len(components)
        reasons = []
        if score >= 0.55:
            reasons.append("The transaction exhibits a novel combination of behavioral signals.")
        return min(1.0, score), reasons
