import pandas as pd

from src.analytics import enrich_metrics, portfolio_summary
from src.recommendations import generate_recommendations


def sample():
    return pd.DataFrame([{
        "date": "2026-08-12", "period_days": 7, "marketplace": "Marketplace A",
        "sku": "SKU-X", "product": "Demo Product", "revenue": 1000, "orders": 10,
        "units": 14, "sessions": 100, "ad_spend": 100, "ad_clicks": 20,
        "ad_revenue": 400, "inventory_units": 10, "gross_margin_pct": .5,
        "budget_utilization": .95, "revenue_change_pct": -.2, "sessions_change_pct": -.2,
        "price_index_vs_competitor": 1.15,
    }])


def test_kpis_are_calculated():
    row = enrich_metrics(sample()).iloc[0]
    assert row.cvr == 0.1
    assert row.roas == 4
    assert row.acos == 0.25
    assert row.days_of_cover == 5


def test_portfolio_summary():
    result = portfolio_summary(sample())
    assert result["revenue"] == 1000
    assert result["orders"] == 10
    assert result["roas"] == 4


def test_recommendation_prioritizes_stockout():
    rec = generate_recommendations(sample())[0]
    assert "stockout_risk" in rec["signals"]
    assert rec["priority_score"] >= 5
