from dataclasses import dataclass

@dataclass(frozen=True)
class PolicySettings:
    policy_version: str = "2026.08-v1"
    medium_risk_threshold: float = 0.45
    high_risk_threshold: float = 0.70
    critical_risk_threshold: float = 0.88
    high_value_threshold: float = 5000.0
    force_human_review_threshold: float = 0.82
    max_autonomous_hold_amount: float = 2500.0

POLICY = PolicySettings()
