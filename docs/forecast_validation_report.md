# FusionMart AI Forecast Validation & Audit Report

## 1. Prophet: Revenue Forecasting Audit
Prophet was used to forecast overall daily revenue, incorporating marketing campaigns as holidays.

### Performance Metrics (Last 90 Days Backtest)
| Metric | Value | Interpretation |
| :--- | :--- | :--- |
| **MAE** | ₹22,810,737 | Average deviation per day. |
| **RMSE** | ₹32,772,532 | Penalizes larger errors; shows occasional high volatility. |
| **MAPE** | 62.05% | High percentage due to significant daily sales fluctuations. |

### Visual Analysis
*   **Actual vs Predicted:** The model follows the general trend but struggles with extreme daily peaks.
*   **Residual Analysis:** Residuals are relatively centered around zero but show increased variance at higher revenue levels (Heteroscedasticity).
*   **Overfitting Risk:** Low. The model captures seasonality well but is conservative on spikes, indicating it's generalizing rather than memorizing noise.

---

## 2. XGBoost: Product Demand Audit
XGBoost was employed for granular demand prediction (Product + Region).

### Performance Metrics
| Metric | Value | Interpretation |
| :--- | :--- | :--- |
| **MAE** | 23.83 units | Predicted quantity is off by ~24 units on average. |
| **RMSE** | 42.40 units | Indicates some products have highly unpredictable demand spikes. |
| **R² Score (Test)** | -0.13 | Negative R² on the test set suggests the model is struggling to generalize better than a simple mean. |
| **CV R² (Mean)** | 0.18 | Cross-validation shows positive predictive power (18%), indicating the test split might have contained unique temporal patterns. |

### Feature Importance (Top 5)
1.  **prev_demand:** The strongest predictor; demand is highly auto-regressive.
2.  **day:** Monthly cycles.
3.  **month:** Seasonal trends.
4.  **region_South India:** Significant regional demand variance.
5.  **category_Smartphones:** High volume category influence.

---

## 3. Regional Performance Audit (RF + Isolation Forest)
This multi-model approach identifies regions that are underperforming compared to their AI-calculated potential.

### Anomaly Summary by Region
| Region | Anomaly Count |
| :--- | :--- |
| **South India** | 7 |
| **West India** | 3 |
| **North India** | 2 |

### Top Anomalies (Underperformance)
| Month | Region | Actual Revenue | Expected | Performance Gap | Conf. Score |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 2021-10 | South India | ₹45.87 Cr | ₹68.71 Cr | -₹22.84 Cr | -0.091 |
| 2023-10 | South India | ₹46.01 Cr | ₹68.71 Cr | -₹22.70 Cr | -0.091 |
| 2024-10 | South India | ₹83.49 Cr | ₹68.71 Cr* | +₹14.78 Cr | -0.123 |

*\*Note: Positive gaps can also be flagged as anomalies if they are statistically extreme (Overperformance).*

### Audit Insights:
*   **South India Persistence:** South India consistently appears as the most volatile region, frequently triggering anomaly flags. This suggests that marketing campaigns or inventory levels in the South are not aligning with the region's high potential.
*   **Anomaly Confidence:** The Isolation Forest identifies October as a high-risk month across multiple years, likely due to shifting festival dates (Diwali) that fixed-month models struggle to track perfectly.

---

## 4. Final Recommendations
1.  **Refine Prophet:** Add "Payday" effects and specific "Festival Eve" regressors to reduce the 62% MAPE.
2.  **Improve XGBoost:** Add more lag features (7-day and 30-day rolling means) to improve the R² score beyond 18%.
3.  **Action on South India:** Investigate why October actuals frequently miss the "Expected" mark by >₹20 Crore. Check if logistics bottlenecks occur during the peak festive season.
