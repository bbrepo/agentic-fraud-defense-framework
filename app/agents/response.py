from app.models import Action, DetectorOutput, InvestigationResult, RiskLevel, Transaction, TriageResult

class ResponseAgent:
    """Chooses a proportionate countermeasure before governance guardrails are applied."""

    def propose(
        self,
        tx: Transaction,
        d: DetectorOutput,
        triage: TriageResult,
        investigation: InvestigationResult,
    ) -> Action:
        if triage.risk_level == RiskLevel.CRITICAL:
            return Action.ESCALATE
        if triage.risk_level == RiskLevel.HIGH:
            return Action.SOFT_HOLD
        if triage.risk_level == RiskLevel.MEDIUM:
            return Action.STEP_UP
        return Action.RELEASE
