"""Core KPI calculations for the synthetic marketplace portfolio."""
from __future__ import annotations

import pandas as pd


def enrich_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Return row-level business metrics with safe division."""
    out = df.copy()
    out["cvr"] = (out["orders"] / out["sessions"].replace(0, pd.NA)).fillna(0)
    out["cpc"] = (out["ad_spend"] / out["ad_clicks"].replace(0, pd.NA)).fillna(0)
    out["roas"] = (out["ad_revenue"] / out["ad_spend"].replace(0, pd.NA)).fillna(0)
    out["acos"] = (out["ad_spend"] / out["ad_revenue"].replace(0, pd.NA)).fillna(0)
    out["margin_value"] = out["revenue"] * out["gross_margin_pct"] - out["ad_spend"]
    daily_units = out["units"] / out["period_days"].clip(lower=1)
    out["days_of_cover"] = (out["inventory_units"] / daily_units.replace(0, pd.NA)).fillna(999)
    return out


def portfolio_summary(df: pd.DataFrame) -> dict:
    """Aggregate the most useful executive KPIs."""
    x = enrich_metrics(df)
    revenue = float(x["revenue"].sum())
    spend = float(x["ad_spend"].sum())
    ad_revenue = float(x["ad_revenue"].sum())
    sessions = int(x["sessions"].sum())
    orders = int(x["orders"].sum())
    return {
        "revenue": round(revenue, 2),
        "orders": orders,
        "sessions": sessions,
        "conversion_rate": round(orders / sessions, 4) if sessions else 0,
        "ad_spend": round(spend, 2),
        "roas": round(ad_revenue / spend, 2) if spend else 0,
        "acos": round(spend / ad_revenue, 4) if ad_revenue else 0,
        "contribution_after_ads": round(float(x["margin_value"].sum()), 2),
    }


def marketplace_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate performance by marketplace."""
    x = enrich_metrics(df)
    rows = []
    for marketplace, g in x.groupby("marketplace"):
        rows.append({"marketplace": marketplace, **portfolio_summary(g)})
    return pd.DataFrame(rows).sort_values("revenue", ascending=False)


def detect_signals(df: pd.DataFrame) -> pd.DataFrame:
    """Create interpretable risk/opportunity flags for every SKU-marketplace row."""
    x = enrich_metrics(df)
    median_cvr = x["cvr"].median()
    median_roas = x["roas"].median()

    def signals(row):
        flags = []
        if row.days_of_cover < 7:
            flags.append("stockout_risk")
        if row.acos > 0.40 and row.ad_spend > 0:
            flags.append("high_acos")
        if row.cvr < median_cvr * 0.75:
            flags.append("weak_conversion")
        if row.roas > median_roas * 1.25 and row.budget_utilization > 0.9:
            flags.append("scale_candidate")
        if row.revenue_change_pct < -0.15:
            flags.append("revenue_decline")
        if row.sessions_change_pct < -0.15:
            flags.append("traffic_decline")
        if row.price_index_vs_competitor > 1.10:
            flags.append("price_gap")
        return flags

    x["signals"] = x.apply(signals, axis=1)
    x["signal_count"] = x["signals"].str.len()
    return x
