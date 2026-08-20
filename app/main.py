from fastapi import FastAPI, HTTPException
from app.models import Decision, Feedback, Transaction
from app.services.orchestrator import FraudDefenseOrchestrator

app = FastAPI(
    title="Agentic AI Fraud Defense Framework",
    version="0.1.0",
    description="Research prototype implementing a five-layer, human-governed agentic fraud-defense architecture.",
)

engine = FraudDefenseOrchestrator()

@app.get("/health")
def health():
    return {"status": "ok", "framework": "five-layer-agentic-fraud-defense"}

@app.post("/v1/transactions/evaluate", response_model=Decision)
def evaluate(tx: Transaction):
    return engine.evaluate(tx)

@app.post("/v1/feedback")
def feedback(item: Feedback):
    return engine.learn(item)

@app.get("/v1/audit/{transaction_id}")
def audit(transaction_id: str):
    return {"transaction_id": transaction_id, "records": engine.audit.for_transaction(transaction_id)}

@app.get("/v1/graph/account/{account_id}")
def graph(account_id: str):
    return engine.graph.neighborhood(account_id, radius=2)
