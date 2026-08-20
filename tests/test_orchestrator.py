from datetime import datetime, timedelta, timezone
from app.models import Action, Transaction
from app.services.orchestrator import FraudDefenseOrchestrator

def make_tx(txid, amount, timestamp, device="known", cp="normal"):
    return Transaction(
        transaction_id=txid,
        account_id="acct",
        merchant_id="merchant",
        counterparty_id=cp,
        device_id=device,
        amount=amount,
        currency="USD",
        country="US",
        channel="RTP",
        timestamp=timestamp,
        kyc_score=0.9,
    )

def test_low_risk_transaction_releases():
    engine = FraudDefenseOrchestrator()
    now = datetime.now(timezone.utc)
    decision = engine.evaluate(make_tx("t1", 50, now))
    assert decision.action == Action.RELEASE
    assert decision.composite_risk < 0.45

def test_suspicious_transaction_is_not_straight_through():
    engine = FraudDefenseOrchestrator()
    now = datetime.now(timezone.utc)

    for i, amount in enumerate([40, 45, 55, 50, 60]):
        engine.evaluate(make_tx(f"base-{i}", amount, now - timedelta(hours=6-i)))

    engine.graph.mark_flagged("counterparty", "risky")
    decision = engine.evaluate(make_tx("suspicious", 3000, now, device="new-device", cp="risky"))

    assert decision.composite_risk >= 0.45
    assert decision.action in {Action.STEP_UP, Action.SOFT_HOLD, Action.ESCALATE}
    assert len(decision.explanation) > 0

def test_feedback_is_audited():
    from app.models import Feedback
    engine = FraudDefenseOrchestrator()
    result = engine.learn(Feedback(transaction_id="x", confirmed_fraud=True, analyst_notes="confirmed"))
    assert result["status"] == "feedback-recorded"
    assert len(engine.audit.for_transaction("x")) == 1
