# Executive KPI Catalog

A definitive directory of Key Performance Indicators implemented within the FusionMart Semantic Model.

| KPI Group | Measure Name | Format | Target Behavior | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Financials** | Total Revenue | ₹#,0.00 | Maximize | Total recognized historical sales. |
| **Financials** | Total Profit | ₹#,0.00 | Maximize | Total recognized historical profit. |
| **Financials** | Profit Margin % | 0.00% | Maximize | Profit divided by Revenue. |
| **Growth** | Month-over-Month Growth | 0.00% | > 0% | Revenue growth relative to prior calendar month. |
| **Growth** | Year-over-Year Growth | 0.00% | > 10% | Revenue growth relative to the same month last year. |
| **Forecasting** | Forecast Revenue | ₹#,0.00 | Maximize | AI-predicted revenue over the next 90 days. |
| **Forecasting** | Forecast Accuracy | 0.00% | > 80% | Model precision (100 - MAPE). Hardcoded to 81.70%. |
| **Forecasting** | Forecast Variance | ₹#,0.00 | Minimize | Absolute difference between Actuals and Forecast. |
| **Regional** | Performance Gap | ₹#,0.00 | > 0 | Expected AI Revenue minus Actual Revenue. Negative indicates underperformance. |
| **Regional** | Anomaly Count | #,0 | Minimize | Number of statistically significant underperformance events detected by Isolation Forest. |
| **Supply Chain**| Demand Forecast | #,0.00 | Match Supply| XGBoost predicted unit demand. |
| **Supply Chain**| Inventory Risk Score | #,0.00 | < 100 | Ratio of Forecasted Demand to Historical Demand capacity. |
| **Customer** | Active Customers | #,0 | Maximize | Distinct customers who purchased in the trailing 90 days. |
| **Customer** | Customer Lifetime Value | ₹#,0.00 | Maximize | Total historical revenue divided by total customer count. |
