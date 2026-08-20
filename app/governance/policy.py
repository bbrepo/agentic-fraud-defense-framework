from __future__ import annotations
from app.models import Action, DetectorOutput, GovernanceResult, Transaction
from app.settings import POLICY

class PolicyEngine:
    """Bounds autonomous action and preserves human authority."""

    def apply(
        self,
        tx: Transaction,
        d: DetectorOutput,
        proposed_action: Action,
    ) -> GovernanceResult:
        action = proposed_action
        human = False
        reasons: list[str] = []

        if d.composite_risk >= POLICY.force_human_review_threshold:
            human = True
            reasons.append("Risk exceeds the mandatory human-review threshold.")

        if tx.amount >= POLICY.high_value_threshold:
            human = True
            reasons.append("High-value transaction requires enhanced oversight.")

        if proposed_action == Action.SOFT_HOLD and tx.amount > POLICY.max_autonomous_hold_amount:
            action = Action.ESCALATE
            human = True
            reasons.append("Autonomous hold authority is capped for this transaction amount.")

        if proposed_action == Action.ESCALATE:
            human = True
            reasons.append("Escalation action explicitly transfers authority to a human analyst.")

        return GovernanceResult(
            action=action,
            human_review_required=human,
            policy_version=POLICY.policy_version,
            guardrail_reasons=reasons,
        )
