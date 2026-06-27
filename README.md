# 🚀 Sales-Fusion: Agentic AI Analytics Platform

**Sales-Fusion** is a portfolio-grade, self-optimizing retail analytics platform powered by an Agentic AI workflow framework (based on Nimrod Fisher’s Data Analytics Skills). 

This project transforms traditional, fragmented data scripts into a fully automated, dockerized, and cloud-ready intelligence engine capable of dynamic forecasting, anomaly detection, cohort analysis, and natural-language narrative generation.

---

## 🌟 Key Capabilities

1. **Automated Data Quality & Validation**
   - Automatically audits incoming CSV files (`sales.csv`, `inventory.csv`) against predefined business rules (e.g., Revenue > 0).
   - Generates reconciliation reports and ensures data schema integrity before analysis begins.
2. **Advanced Agentic Analysis**
   - **Revenue Forecasting**: Utilizes Meta's `Prophet` to predict daily revenue, incorporating marketing campaigns as holidays.
   - **Demand Prediction**: Leverages `XGBoost` for granular SKU-level demand planning, outputting precise feature importances.
   - **Regional Anomaly Detection**: Uses `K-Means Clustering` and `Isolation Forests` to detect underperforming regions and identify root causes.
   - **Cohort & Funnel Analysis**: Tracks customer retention rates and maps conversion drop-offs.
3. **Data Storytelling & Visualization**
   - Synthesizes raw analytical output into C-Suite ready `insights.md` and `executive_summary.md` reports.
   - Calculates **Financial Impact (ROI)** for every insight generated.
   - Presents all data through a stunning, interactive **Streamlit Dashboard** built with a custom Glassmorphism UI.
4. **Cloud-Ready Deployment**
   - Fully Dockerized environment (`docker-compose`).
   - GitHub Actions CI/CD pipelines configured for continuous testing and automated deployments.
   - FastAPI integration serving insights over JWT-secured REST endpoints.

---

## 🏗️ Project Architecture

```text
sales-fusion/
├── api/                          # FastAPI backend endpoints
├── app.py                        # Streamlit Executive Dashboard
├── data/                         # Raw datasets & auto-generated data_dictionary.md
├── docs/                         # Knowledge Base (Semantic Model, Methodology, etc.)
├── models/                       # Serialized ML Models (Tracked via DVC)
├── notebooks/                    # Automated EDA Notebooks
├── reports/                      # Auto-generated forecasts, anomalies, and insights
├── scripts/                      # Core Agentic Python Modules (Prophet, XGBoost, etc.)
├── templates/                    # Workflows (Context Packagers, Peer Reviews)
├── Dockerfile                    # Container configuration
├── docker-compose.yml            # Multi-service orchestration
└── requirements.txt              # Python dependencies
```

---

## 🚀 Getting Started

### 1. Run via Docker (Recommended)
Ensure you have Docker installed on your machine.
```bash
# Build and spin up the entire platform (Streamlit & FastAPI)
docker-compose up --build
```
- **Streamlit Dashboard**: `http://localhost:8501`
- **FastAPI Endpoints**: `http://localhost:8000`

### 2. Run Locally (Python Virtual Env)
If you prefer running without Docker:
```bash
# Install requirements
pip install -r requirements.txt

# Run Analytics Pipeline (Example)
python scripts/data_quality/audit_all.py
python scripts/revenue_forecast.py

# Launch the Executive Dashboard
streamlit run app.py

# Launch the API
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

---

## 🧠 Documentation & Knowledge Base

For a complete understanding of how our AI agent reasons and operates, please refer to the `docs/` folder:
- **[Semantic Model](docs/semantic_model.md)**: Standardized definitions for Revenue, Profit, and Forecast Accuracy.
- **[Analysis Methodology](docs/analysis_methodology.md)**: A breakdown of the math behind Prophet, XGBoost, and Isolation Forests.
- **[Business Translator](docs/business_translations.md)**: Maps technical AI jargon to stakeholder-friendly terms.
- **[Assumptions Log](docs/assumptions.md)**: The foundational logic the AI relies on when dealing with imperfect data.

---

## 🤝 Contributing
Please review our `CONTRIBUTING.md` and utilize the `templates/peer_review.md` checklist when submitting pull requests. All new analysis modules must pass the automated GitHub Actions CI pipeline.

**Maintainer**: Umar Saddiq Ahmed Ali Sayyed
