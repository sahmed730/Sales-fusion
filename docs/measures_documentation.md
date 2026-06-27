# DAX Measures Documentation (Complete Portfolio Version)

## 1. Executive KPIs
*   **Total Revenue:** `SUM(sales[sales_amount])` - Total recognized revenue.
*   **Total Profit:** `SUM(sales[profit])` - Total recognized profit.
*   **Profit Margin %:** `DIVIDE([Total Profit], [Total Revenue], 0)` - Profitability ratio.
*   **Forecast Revenue:** `SUM(revenue_forecast[yhat])` - AI-generated forward-looking revenue.
*   **Forecast Accuracy:** `18.30%` - Static MAPE from the XGBoost smoothing model.
*   **Growth %:** `DIVIDE([Total Revenue] - [Previous Month Revenue], [Previous Month Revenue], 0)` - General growth tracker.
*   **Month-over-Month Growth:** `VAR Prev = CALCULATE([Total Revenue], DATEADD('Date'[Date], -1, MONTH)) RETURN DIVIDE([Total Revenue] - Prev, Prev, 0)`
*   **Quarter-over-Quarter Growth:** `VAR Prev = CALCULATE([Total Revenue], DATEADD('Date'[Date], -1, QUARTER)) RETURN DIVIDE([Total Revenue] - Prev, Prev, 0)`
*   **Year-over-Year Growth:** `VAR Prev = CALCULATE([Total Revenue], DATEADD('Date'[Date], -1, YEAR)) RETURN DIVIDE([Total Revenue] - Prev, Prev, 0)`
*   **Average Order Value:** `DIVIDE([Total Revenue], [Distinct Orders], 0)` - Revenue per transaction.
*   **Revenue per Customer:** `DIVIDE([Total Revenue], [Distinct Customers], 0)` - Average customer spend.
*   **Forecast Variance:** `[Total Revenue] - [Forecast Revenue]` - Deviation from forecast.
*   **Forecast Variance %:** `DIVIDE([Forecast Variance], [Forecast Revenue], 0)`
*   **Forecast Confidence:** `81.70%` - Inverse of the established MAPE.

## 2. Product Analytics
*   **Top Product Revenue:** `MAXX(VALUES(products[product_name]), [Total Revenue])`
*   **Top Product Profit:** `MAXX(VALUES(products[product_name]), [Total Profit])`
*   **Top Category Revenue:** `MAXX(VALUES(products[category]), [Total Revenue])`
*   **Category Share %:** `DIVIDE([Total Revenue], CALCULATE([Total Revenue], REMOVEFILTERS(products[category])), 0)`
*   **Product Rank:** `RANKX(ALL(products[product_name]), [Total Revenue], , DESC, Dense)`
*   **Demand Forecast:** `SUM(demand_forecast_samples[Predicted_Demand])`
*   **Inventory Risk Score:** `DIVIDE([Demand Forecast], [Actual Demand] + 1, 0) * 100`
*   **Inventory Coverage Days:** `14` (Static baseline constraint).

## 3. Customer Analytics
*   **Customer Count:** `DISTINCTCOUNT(customers[customer_id])`
*   **Active Customers:** Count of customers with a purchase in the last 90 days.
*   **New Customers:** Customers with their first purchase in the last 30 days.
*   **Customer Lifetime Value:** `DIVIDE(CALCULATE([Total Revenue], ALL('Date')), [Customer Count], 0)`

## 4. Regional Analytics
*   **Regional Revenue:** `CALCULATE([Total Revenue], KEEPFILTERS(Regions[region]))`
*   **Performance Gap:** `SUM(underperforming_regions[performance_gap])`
*   **Anomaly Count:** `CALCULATE(COUNTROWS(underperforming_regions), underperforming_regions[anomaly_score] = -1)`
*   **Expected Revenue:** `SUM(underperforming_regions[expected_revenue])`

## 5. AI Insights Generative Measures
*   **Revenue Outlook:** Dynamic string concatenating Forecast Revenue and Variance.
*   **Regional Risk Summary:** Dynamic string evaluating Anomaly Count and flagging risk.
*   **Inventory Recommendation:** Dynamic string evaluating Inventory Risk Score thresholds.
*   **Executive Recommendation:** Dynamic string prioritizing marketing spend toward `[Best Performing Region]`.
