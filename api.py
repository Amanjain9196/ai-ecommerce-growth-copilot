from fastapi import FastAPI
from pydantic import BaseModel

from src.analytics import portfolio_summary
from src.copilot import answer
from src.data_loader import load_data
from src.recommendations import generate_recommendations

app = FastAPI(title="AI E-commerce Growth Copilot API", version="0.1.0")


class Question(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok", "data_policy": "synthetic-demo"}


@app.get("/summary")
def summary():
    return portfolio_summary(load_data())


@app.get("/recommendations")
def recommendations():
    return generate_recommendations(load_data())


@app.post("/ask")
def ask(payload: Question):
    return {"answer": answer(payload.question, load_data())}
