from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field

class Action(str, Enum):
    RELEASE = "RELEASE"
    STEP_UP = "STEP_UP"
    SOFT_HOLD = "SOFT_HOLD"
    ESCALATE = "ESCALATE"

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class Transaction(BaseModel):
    transaction_id: str
    account_id: str
    merchant_id: str
    counterparty_id: str
    device_id: str
    amount: float = Field(gt=0)
    currency: str = "USD"
    country: str = "US"
    channel: str = "RTP"
    timestamp: datetime
    kyc_score: float = Field(default=0.8, ge=0, le=1)

class FeatureVector(BaseModel):
    amount_z: float = 0.0
    tx_count_10m: int = 0
    amount_sum_10m: float = 0.0
    new_device: bool = False
    country_changed: bool = False
    avg_amount_recent: float = 0.0
    sequence_deviation: float = 0.0
    graph_risk: float = 0.0

class DetectorOutput(BaseModel):
    tabular_score: float
    sequence_score: float
    graph_score: float
    anomaly_score: float
    composite_risk: float
    uncertainty: float
    reasons: list[str]

class TriageResult(BaseModel):
    risk_level: RiskLevel
    priority: int
    route: str
    duplicate_suppressed: bool = False

class InvestigationResult(BaseModel):
    evidence: dict[str, Any]
    summary: str

class GovernanceResult(BaseModel):
    action: Action
    human_review_required: bool
    policy_version: str
    guardrail_reasons: list[str]

class Decision(BaseModel):
    transaction_id: str
    composite_risk: float
    risk_level: RiskLevel
    action: Action
    human_review_required: bool
    explanation: list[str]
    detector_scores: dict[str, float]
    investigation: dict[str, Any]
    policy_version: str
    audit_id: str

class Feedback(BaseModel):
    transaction_id: str
    confirmed_fraud: bool
    analyst_notes: str | None = None
