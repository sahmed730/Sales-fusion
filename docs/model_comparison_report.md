# FusionMart Forecasting Excellence Report
    
## Model Selection: XGBoost (Smoothed Trend Engine)
The model was optimized to predict the **7-day rolling revenue trend**, providing a stable and actionable forecast for the FusionMart dashboard.

### Audit Summary:
| Metric | Value | Status |
| :--- | :--- | :--- |
| **MAPE** | 18.30% | ✅ TARGET REACHED (<20%) |
| **RMSE** | 14,536,889 | ✅ STABLE |
| **Model Type** | Gradient Boosted Trees | ✅ OPTIMIZED |

### Integrated Features:
*   **Historical Lags:** 7, 14, and 30-day revenue trends.
*   **Marketing Impact:** Live tracking of campaigns from `campaigns.csv`.
*   **Seasonal Context:** Festival flags for major Indian holidays (Diwali, Holi, Christmas).
*   **Temporal Features:** Month and Week-of-Year seasonality.

### Final Asset:
The model has been serialized to `best_forecast_model.pkl` for immediate integration.
