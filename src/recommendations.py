"""Transparent action prioritization for marketplace operators."""
from __future__ import annotations

from src.analytics import detect_signals

WEIGHTS = {
    "stockout_risk": 5,
    "revenue_decline": 4,
    "high_acos": 3,
    "weak_conversion": 3,
    "traffic_decline": 3,
    "price_gap": 2,
    "scale_candidate": 2,
}

ACTIONS = {
    "stockout_risk": "Prioritize replenishment and avoid scaling demand until stock cover improves.",
    "high_acos": "Audit targeting and reduce inefficient ad spend before scaling.",
    "weak_conversion": "Inspect listing quality, offer, ratings and price competitiveness.",
    "scale_candidate": "Consider increasing budget while monitoring marginal ROAS.",
    "revenue_decline": "Diagnose whether the decline is driven by traffic, conversion, price or availability.",
    "traffic_decline": "Review ad reach, organic rank, demand trend and campaign eligibility.",
    "price_gap": "Review price/offer competitiveness before adding incremental media spend.",
}


def generate_recommendations(df, limit: int = 10) -> list[dict]:
    signaled = detect_signals(df)
    recommendations = []
    for _, row in signaled.iterrows():
        if not row.signals:
            continue
        score = sum(WEIGHTS[s] for s in row.signals)
        ordered = sorted(row.signals, key=lambda s: WEIGHTS[s], reverse=True)
        actions = [ACTIONS[s] for s in ordered]
        confidence = "high" if score >= 7 else "medium" if score >= 4 else "directional"
        recommendations.append({
            "marketplace": row.marketplace,
            "sku": row.sku,
            "product": row.product,
            "priority_score": score,
            "signals": ordered,
            "recommended_actions": actions,
            "confidence": confidence,
        })
    return sorted(recommendations, key=lambda r: r["priority_score"], reverse=True)[:limit]
