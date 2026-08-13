"""Natural-language copilot with an optional OpenAI narrative layer."""
from __future__ import annotations

import json
import os
from src.analytics import portfolio_summary
from src.recommendations import generate_recommendations


def build_context(df) -> dict:
    return {
        "portfolio_summary": portfolio_summary(df),
        "top_recommendations": generate_recommendations(df, limit=5),
    }


def deterministic_answer(question: str, df) -> str:
    context = build_context(df)
    summary = context["portfolio_summary"]
    recs = context["top_recommendations"]
    q = question.lower()

    if "roas" in q or "acos" in q or "ad" in q:
        intro = f"Portfolio ROAS is {summary['roas']:.2f} and ACOS is {summary['acos']:.1%}."
    elif "revenue" in q or "sales" in q:
        intro = f"Synthetic portfolio revenue is {summary['revenue']:,.0f} across {summary['orders']:,} orders."
    else:
        intro = "I reviewed sales, advertising, inventory, conversion and pricing signals together."

    if not recs:
        return intro + " No material action flags were detected."
    top = recs[0]
    return (
        f"{intro} Highest priority: {top['product']} ({top['sku']}) on {top['marketplace']} "
        f"because of {', '.join(top['signals']).replace('_', ' ')}. "
        f"Recommended next step: {top['recommended_actions'][0]} Confidence: {top['confidence']}."
    )


def answer(question: str, df) -> str:
    """Use OpenAI when configured; otherwise keep the portfolio demo fully functional."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return deterministic_answer(question, df)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        context = json.dumps(build_context(df), default=str)
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
            instructions=(
                "You are an e-commerce growth copilot. Use only the supplied synthetic data context. "
                "Be concise, quantify claims, separate evidence from hypotheses, and never invent facts."
            ),
            input=f"Business context: {context}\n\nQuestion: {question}",
        )
        return response.output_text
    except Exception:
        return deterministic_answer(question, df)
