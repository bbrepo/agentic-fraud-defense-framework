from __future__ import annotations
from collections import defaultdict, deque
from datetime import timedelta
from app.models import Transaction

class EventStore:
    """In-memory event history used by the research prototype."""

    def __init__(self, max_history_per_account: int = 200):
        self.by_account: dict[str, deque[Transaction]] = defaultdict(
            lambda: deque(maxlen=max_history_per_account)
        )

    def recent(self, account_id: str) -> list[Transaction]:
        return list(self.by_account[account_id])

    def recent_within(self, tx: Transaction, minutes: int) -> list[Transaction]:
        cutoff = tx.timestamp - timedelta(minutes=minutes)
        return [x for x in self.by_account[tx.account_id] if x.timestamp >= cutoff]

    def append(self, tx: Transaction) -> None:
        self.by_account[tx.account_id].append(tx)
