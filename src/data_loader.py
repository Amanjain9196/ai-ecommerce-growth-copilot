"""Load and validate marketplace input data."""
from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {
    "date", "period_days", "marketplace", "sku", "product", "revenue", "orders",
    "units", "sessions", "ad_spend", "ad_clicks", "ad_revenue", "inventory_units",
    "gross_margin_pct", "budget_utilization", "revenue_change_pct", "sessions_change_pct",
    "price_index_vs_competitor",
}


def load_data(path: str | Path = "data/synthetic_marketplace_data.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    df["date"] = pd.to_datetime(df["date"])
    return df
