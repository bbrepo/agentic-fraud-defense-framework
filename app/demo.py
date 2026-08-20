from datetime import datetime, timedelta, timezone
import json
from app.models import Transaction
from app.services.orchestrator import FraudDefenseOrchestrator

def tx(i, ts, amount, device="device-known", country="US", cp="cp-normal"):
    return Transaction(
        transaction_id=f"baseline-{i}",
        account_id="acct-100",
        merchant_id="merchant-demo",
        counterparty_id=cp,
        device_id=device,
        amount=amount,
        currency="USD",
        country=country,
        channel="RTP",
        timestamp=ts,
        kyc_score=0.92,
    )

def main():
    engine = FraudDefenseOrchestrator()
    now = datetime.now(timezone.utc)

    # Establish a normal account baseline.
    for i, amount in enumerate([42, 55, 61, 38, 73, 48], start=1):
        engine.evaluate(tx(i, now - timedelta(hours=12-i), amount))

    # Introduce relational risk.
    engine.graph.mark_flagged("counterparty", "cp-risky")

    suspicious = Transaction(
        transaction_id="tx-demo-001",
        account_id="acct-100",
        merchant_id="merchant-demo",
        counterparty_id="cp-risky",
        device_id="device-new",
        amount=1850.00,
        currency="USD",
        country="US",
        channel="RTP",
        timestamp=now,
        kyc_score=0.81,
    )

    decision = engine.evaluate(suspicious)
    print(json.dumps(decision.model_dump(mode="json"), indent=2))

if __name__ == "__main__":
    main()
