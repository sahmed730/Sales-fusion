# AI Insights Generation Logic

## Overview
The FusionMart Executive Command Center features a dynamic "AI Insights" panel. This panel translates complex machine learning outputs from XGBoost and Isolation Forest models into boardroom-ready natural language.

## Data Sources
1. `forecast_results/revenue_forecast.csv` (Prophet/XGBoost Revenue Trends)
2. `forecast_results/underperforming_regions.csv` (Isolation Forest Anomalies)
3. `forecast_results/demand_forecast_samples.csv` (Product-level XGBoost Predictions)

## Dynamic Insight Generation (DAX & Smart Narrative Logic)

### 1. Revenue Trajectory Insight
**Logic:** Compares the rolling average of the last 7 days of actuals against the next 7 days of forecast.
**Template:** 
> "Revenue is expected to [Increase/Decrease] by [X]% over the next week, driven by projected sales of ₹[Y] Cr."
**Example Output:**
> *Revenue is expected to Increase by 12% over the next week, driven by projected sales of ₹9.2 Cr.*

### 2. Regional Anomaly Detection Insight
**Logic:** Scans the `underperforming_regions` table for the most recent month where `anomaly == -1` and `performance_gap < 0`. Sorts by largest absolute gap.
**Template:** 
> "⚠️ Anomaly Detected: [Region] underperformed by ₹[Z] Cr against AI expectations last month. Immediate pipeline review recommended."
**Example Output:**
> *⚠️ Anomaly Detected: South India underperformed by ₹22.84 Cr against AI expectations last month. Immediate pipeline review recommended.*

### 3. Product Demand Surge Insight
**Logic:** Identifies products in `demand_forecast_samples` where `Predicted_Demand` exceeds historical averages by >15%.
**Template:**
> "📈 Demand Surge: [Product Name] demand is increasing. Estimated [Quantity] units required next cycle to prevent stockouts."
**Example Output:**
> *📈 Demand Surge: FusionPhone X demand is increasing. Estimated 4,500 units required next cycle to prevent stockouts.*

### 4. Inventory Action Recommendation
**Logic:** Combines high demand forecast with regional performance dips.
**Template:**
> "💡 AI Recommendation: Initiate targeted [Campaign/Restock] for [Category] in [Region] to capture predicted ₹[Gap] Cr market potential."
**Example Output:**
> *💡 AI Recommendation: Initiate targeted restock for Smartphones in South India to capture predicted ₹22.84 Cr market potential.*
