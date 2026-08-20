from __future__ import annotations
from app.detectors.tabular import TabularScorer
from app.detectors.sequence import SequenceScorer
from app.detectors.graph import GraphScorer
from app.detectors.anomaly import AnomalyScorer
from app.models import DetectorOutput, FeatureVector, Transaction

class DetectionEnsemble:
    def __init__(self):
        self.tabular = TabularScorer()
        self.sequence = SequenceScorer()
        self.graph = GraphScorer()
        self.anomaly = AnomalyScorer()

    def evaluate(self, tx: Transaction, f: FeatureVector) -> DetectorOutput:
        t, tr = self.tabular.score(tx, f)
        s, sr = self.sequence.score(f)
        g, gr = self.graph.score(f)
        a, ar = self.anomaly.score(f)

        # Research-prototype weighting. Replace with validated calibration in production.
        composite = 0.38 * t + 0.24 * s + 0.23 * g + 0.15 * a
        disagreement = max(t, s, g, a) - min(t, s, g, a)
        uncertainty = min(1.0, 0.15 + 0.7 * disagreement)

        reasons = list(dict.fromkeys(tr + sr + gr + ar))
        if not reasons:
            reasons = ["No material risk deviation detected across the active controls."]

        return DetectorOutput(
            tabular_score=round(t, 4),
            sequence_score=round(s, 4),
            graph_score=round(g, 4),
            anomaly_score=round(a, 4),
            composite_risk=round(composite, 4),
            uncertainty=round(uncertainty, 4),
            reasons=reasons,
        )
