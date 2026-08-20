from __future__ import annotations
import networkx as nx
from app.models import Transaction

class TransactionGraph:
    """
    In-memory heterogeneous graph.
    Nodes: accounts, devices, merchants, counterparties.
    Edges capture observed transaction relationships.
    """

    def __init__(self):
        self.graph = nx.Graph()
        self.flagged_nodes: set[str] = set()

    @staticmethod
    def _node(kind: str, value: str) -> str:
        return f"{kind}:{value}"

    def add_transaction(self, tx: Transaction) -> None:
        acct = self._node("account", tx.account_id)
        dev = self._node("device", tx.device_id)
        mer = self._node("merchant", tx.merchant_id)
        cp = self._node("counterparty", tx.counterparty_id)

        self.graph.add_node(acct, kind="account")
        self.graph.add_node(dev, kind="device")
        self.graph.add_node(mer, kind="merchant")
        self.graph.add_node(cp, kind="counterparty")

        for other, relation in [
            (dev, "uses_device"),
            (mer, "pays_merchant"),
            (cp, "pays_counterparty"),
        ]:
            if self.graph.has_edge(acct, other):
                self.graph[acct][other]["count"] += 1
                self.graph[acct][other]["amount"] += tx.amount
            else:
                self.graph.add_edge(
                    acct, other, relation=relation, count=1, amount=tx.amount
                )

    def mark_flagged(self, kind: str, value: str) -> None:
        self.flagged_nodes.add(self._node(kind, value))

    def neighborhood(self, account_id: str, radius: int = 2) -> dict:
        acct = self._node("account", account_id)
        if acct not in self.graph:
            return {"nodes": [], "flagged_nodes": [], "degree": 0}
        nodes = list(nx.single_source_shortest_path_length(
            self.graph, acct, cutoff=radius
        ).keys())
        flagged = [n for n in nodes if n in self.flagged_nodes]
        return {
            "nodes": nodes,
            "flagged_nodes": flagged,
            "degree": self.graph.degree(acct),
        }

    def risk_for_transaction(self, tx: Transaction) -> float:
        candidates = [
            self._node("device", tx.device_id),
            self._node("merchant", tx.merchant_id),
            self._node("counterparty", tx.counterparty_id),
        ]
        direct_flag = any(n in self.flagged_nodes for n in candidates)

        acct = self._node("account", tx.account_id)
        nearby_flag_count = 0
        if acct in self.graph:
            neighborhood = nx.single_source_shortest_path_length(
                self.graph, acct, cutoff=2
            )
            nearby_flag_count = sum(
                1 for node in neighborhood if node in self.flagged_nodes
            )

        score = 0.65 if direct_flag else 0.0
        score += min(0.35, nearby_flag_count * 0.12)
        return min(1.0, score)
