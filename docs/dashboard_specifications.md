# 📊 Dashboard Specification V2 (Streamlit)

This document defines the layout and structure for the interactive Streamlit dashboard (`app.py`), replacing the legacy HTML mockup.

## 1. Global Configurations
- **Theme**: Dark Mode (Glassmorphism aesthetics)
- **Primary Color**: `#4F46E5` (Indigo)
- **Secondary Color**: `#10B981` (Emerald)
- **Typography**: Inter (via CSS)

## 2. Navigation Architecture (Sidebar)
1. **Executive Command Center**: High-level KPIs and forecasts.
2. **Demand Planning**: Product-level XGBoost forecasts and inventory alerts.
3. **Regional Intelligence**: K-Means clustering and anomaly detection.
4. **AI Insights**: The natural language narratives and executive summaries.

## 3. View Details

### Executive Command Center
- **Top Row**: 3 KPI Cards (Total Revenue, YoY Growth, Forecast Accuracy).
- **Middle Row**: Prophet Revenue Forecast (90-day future) Line Chart.
- **Bottom Row**: Marketing Campaign Overlay (showing revenue spikes during campaigns).

### Regional Intelligence
- **Top Row**: Map or Bar Chart of Revenue by Region.
- **Middle Row**: Scatter plot of Regions (Revenue vs Quantity) colored by K-Means cluster.
- **Bottom Row**: Alert table listing any anomalies detected by the Isolation Forest.
