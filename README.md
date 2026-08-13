# AI E-commerce Growth Copilot

An AI-native decision-support system for e-commerce operators. It combines sales, advertising, inventory, pricing and marketplace signals to explain performance changes and recommend the next best actions.

> **Portfolio note:** all datasets in this repository are synthetic. The project is inspired by common marketplace operating patterns, but contains no employer-confidential data, account IDs, contacts, credentials, internal commercial terms, or real company performance figures.

## Why this project

Marketplace operators often work across disconnected dashboards: sales, ads, inventory, pricing, catalog health and promotions. The hard part is not seeing the metrics; it is deciding **what changed, why it changed, and what to do next**.

This copilot turns structured marketplace data into an executive-ready workflow:

1. **Observe** — ingest marketplace performance data.
2. **Diagnose** — calculate KPI movements and flag anomalies.
3. **Reason** — connect likely drivers across ads, conversion, stock and pricing.
4. **Recommend** — rank actions by expected impact, urgency and confidence.
5. **Explain** — answer business questions in plain English.

## Demo questions

- Why did revenue drop yesterday?
- Which SKU needs immediate attention?
- Where are we wasting ad spend?
- Which product is at risk of stock-out?
- What are the top five actions for today?
- Which marketplace is underperforming and why?

## Architecture

```text
Synthetic marketplace feeds
        │
        ▼
Data loader + validation
        │
        ▼
KPI & anomaly engine
        │
        ├───────────────┐
        ▼               ▼
Recommendation engine  Context builder
        │               │
        └──────┬────────┘
               ▼
          AI Copilot
               │
        ┌──────┴──────┐
        ▼             ▼
   Streamlit UI    FastAPI API
```

## What the v1 demonstrates

- E-commerce KPI modeling: revenue, orders, CVR, CPC, ROAS, ACOS, contribution margin and days of cover
- Multi-signal diagnosis across sales, ads, inventory and price
- Rule-based recommendations with transparent reasoning
- Optional LLM narrative layer using the OpenAI API
- Streamlit dashboard for operator workflows
- FastAPI endpoint for machine-to-machine access
- Synthetic data generation and privacy-safe portfolio design
- Unit tests and GitHub Actions CI

## Project structure

```text
.
├── app.py                    # Streamlit dashboard
├── api.py                    # FastAPI service
├── data/
│   └── synthetic_marketplace_data.csv
├── src/
│   ├── analytics.py          # KPI + anomaly logic
│   ├── copilot.py            # Natural-language answer layer
│   ├── data_loader.py        # Input validation
│   └── recommendations.py    # Action prioritization
├── tests/
│   └── test_analytics.py
├── .github/workflows/ci.yml
├── requirements.txt
└── Dockerfile
```

## Quick start

```bash
git clone https://github.com/Amanjain9196/ai-ecommerce-growth-copilot.git
cd ai-ecommerce-growth-copilot
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The core analytics and recommendations work without any API key.

For AI-generated executive narratives, create a `.env` file:

```bash
OPENAI_API_KEY=your_key_here
```

Then run the app again. If no API key is present, the copilot falls back to a deterministic explanation engine so the demo remains functional.

## Decision logic

The v1 uses transparent heuristics rather than hiding all reasoning inside an LLM. Examples:

- **High ACOS + weak CVR** → reduce inefficient spend before scaling.
- **Strong ROAS + budget-constrained campaigns** → consider increasing budget.
- **Low days of cover + healthy demand** → prioritize replenishment.
- **Revenue decline + stable traffic + lower CVR** → investigate listing, price or offer changes.
- **Traffic decline + stable CVR** → investigate ad reach, ranking or demand softness.

This separation matters: deterministic business logic produces auditable signals, while the LLM is used for synthesis and communication.

## Sample output

```text
Priority 1 — SKU-104 / Marketplace C
Risk: stock-out in ~4 days while demand remains above portfolio median.
Action: replenish inventory before increasing ad spend.
Confidence: high

Priority 2 — SKU-102 / Marketplace A
Issue: ACOS increased while conversion fell.
Action: reduce inefficient keyword spend and inspect listing/price competitiveness.
Confidence: medium-high
```

## API

Run:

```bash
uvicorn api:app --reload
```

Example endpoint:

```text
GET /health
GET /summary
GET /recommendations
POST /ask
```

## Roadmap

- Marketplace-specific adapters for Amazon, Flipkart and Meesho-style exports
- CSV upload with automatic schema mapping
- Time-series anomaly detection
- Competitor price and review intelligence
- Agentic workflow for daily business reviews
- Recommendation evaluation framework
- Human approval loop before any execution
- Slack/email briefing integration

## Design principle

**AI should not merely summarize dashboards. It should reduce the distance between a signal and a business decision.**

## License

MIT
