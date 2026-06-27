# 📖 Semantic Model (KPI Definitions)

This document defines the core Key Performance Indicators (KPIs) used across the Sales-Fusion Agentic AI Platform. Consistent definitions ensure all models, dashboards, and reports are aligned.

## 1. Core Financial Metrics

### **Revenue**
- **Definition**: The total monetary value generated from completed sales transactions.
- **Formula**: `SUM(sales_amount)` or `SUM(quantity * price)` depending on the base table.
- **Business Logic**: Excludes refunded orders and taxes (if applicable). This is the top-line performance indicator.

### **Profit (Gross Profit)**
- **Definition**: The remaining monetary value after subtracting the cost of goods sold (COGS) from Revenue.
- **Formula**: `SUM(Revenue - (quantity * cost))`
- **Business Logic**: Used to evaluate the profitability of products, regions, and campaigns.

## 2. Inventory & Operations Metrics

### **Stock Level**
- **Definition**: The current number of units available for a specific product.
- **Formula**: `Current stock from inventory.csv`

### **Reorder Gap**
- **Definition**: The difference between the current stock level and the minimum reorder threshold.
- **Formula**: `stock - reorder_level`
- **Business Logic**: If `Reorder Gap < 0`, a restock alert should be triggered immediately.

## 3. Data Science & Forecasting Metrics

### **Forecast Accuracy (MAPE)**
- **Definition**: Mean Absolute Percentage Error. It measures how accurate the forecasts are compared to actual historical data.
- **Formula**: `Mean(|Actual - Forecast| / Actual) * 100`
- **Business Logic**: Lower is better. A MAPE under 15% is considered highly accurate for retail demand forecasting.

### **Anomaly Score**
- **Definition**: A calculated score by the Isolation Forest model that dictates how unusual a specific data point is compared to the norm.
- **Formula**: Handled via `sklearn.ensemble.IsolationForest`.
- **Business Logic**: Points marked as `-1` are anomalies.
