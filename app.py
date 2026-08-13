import pandas as pd
import streamlit as st

from src.analytics import enrich_metrics, marketplace_summary, portfolio_summary
from src.copilot import answer
from src.data_loader import REQUIRED_COLUMNS, load_data
from src.recommendations import generate_recommendations

st.set_page_config(page_title="AI E-commerce Growth Copilot", page_icon="📈", layout="wide")
st.title("AI E-commerce Growth Copilot")
st.caption("Decision intelligence across sales, ads, inventory and pricing • synthetic demo data")

uploaded = st.sidebar.file_uploader("Upload compatible CSV", type=["csv"])
if uploaded:
    raw = pd.read_csv(uploaded)
    missing = REQUIRED_COLUMNS.difference(raw.columns)
    if missing:
        st.error(f"Missing columns: {sorted(missing)}")
        st.stop()
    raw["date"] = pd.to_datetime(raw["date"])
    df = raw
else:
    df = load_data()

summary = portfolio_summary(df)
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Revenue", f"₹{summary['revenue']/1000:.1f}K")
c2.metric("Orders", f"{summary['orders']:,}")
c3.metric("CVR", f"{summary['conversion_rate']:.1%}")
c4.metric("ROAS", f"{summary['roas']:.2f}x")
c5.metric("ACOS", f"{summary['acos']:.1%}")

st.subheader("Marketplace performance")
market = marketplace_summary(df)
st.dataframe(market, use_container_width=True, hide_index=True)

st.subheader("Revenue by marketplace")
st.bar_chart(market.set_index("marketplace")["revenue"])

st.subheader("Priority actions")
recs = generate_recommendations(df, limit=8)
for i, rec in enumerate(recs, 1):
    with st.expander(f"{i}. {rec['product']} • {rec['marketplace']} • score {rec['priority_score']}", expanded=i <= 3):
        st.write("**Signals:**", ", ".join(s.replace("_", " ") for s in rec["signals"]))
        st.write("**Confidence:**", rec["confidence"])
        for action in rec["recommended_actions"]:
            st.write("-", action)

st.subheader("Ask the copilot")
question = st.text_input("Business question", value="What are the top actions I should take today?")
if st.button("Analyze", type="primary"):
    with st.spinner("Connecting signals..."):
        st.write(answer(question, df))

with st.expander("Inspect enriched synthetic data"):
    st.dataframe(enrich_metrics(df), use_container_width=True, hide_index=True)
