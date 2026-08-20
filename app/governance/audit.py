from __future__ import annotations
from collections import defaultdict
from datetime import datetime, timezone
import uuid

class AuditLog:
    def __init__(self):
        self.records: dict[str, list[dict]] = defaultdict(list)

    def write(self, transaction_id: str, record: dict) -> str:
        audit_id = str(uuid.uuid4())
        item = {
            "audit_id": audit_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **record,
        }
        self.records[transaction_id].append(item)
        return audit_id

    def for_transaction(self, transaction_id: str) -> list[dict]:
        return self.records.get(transaction_id, [])
