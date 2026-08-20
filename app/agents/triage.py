from app.models import DetectorOutput, RiskLevel, TriageResult
from app.settings import POLICY

class TriageAgent:
    def run(self, d: DetectorOutput) -> TriageResult:
        r = d.composite_risk
        if r >= POLICY.critical_risk_threshold:
            level, priority, route = RiskLevel.CRITICAL, 1, "immediate-human-review"
        elif r >= POLICY.high_risk_threshold:
            level, priority, route = RiskLevel.HIGH, 2, "high-risk"
        elif r >= POLICY.medium_risk_threshold:
            level, priority, route = RiskLevel.MEDIUM, 3, "enhanced-verification"
        else:
            level, priority, route = RiskLevel.LOW, 4, "straight-through"
        return TriageResult(risk_level=level, priority=priority, route=route)
