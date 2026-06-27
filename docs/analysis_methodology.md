# 🔬 Analysis Methodology

This document outlines the standard data science and statistical methodologies employed by the Sales-Fusion Agentic AI Platform.

## 1. Revenue Forecasting (Time Series)
- **Tool**: Meta's `Prophet` library.
- **Approach**: We utilize Prophet to model daily revenue, accounting for weekly and yearly seasonalities. 
- **Holiday Effects**: We inject our marketing campaigns (from `campaigns.csv`) as "holidays" to correctly attribute unexpected revenue spikes to marketing efforts rather than organic seasonality.

## 2. Demand Forecasting
- **Tool**: `XGBoostRegressor`
- **Approach**: Demand is forecasted down to the product/region level.
- **Feature Engineering**: We extract date parts (month, day, day of week) and one-hot encode regions and product categories. By extracting feature importances, we can explain the model's decision-making process to stakeholders.

## 3. Regional Anomaly Detection
- **Tool**: `K-Means Clustering` & `Isolation Forest`
- **Approach**: 
  1. We cluster regions using K-Means (based on total revenue, quantity, and average order value) to group similar performing territories.
  2. We run an Isolation Forest over these aggregated metrics to detect any region operating outside of normal parameters (anomalies).

## 4. Cohort & Funnel Analysis
- **Approach**: 
  - **Cohorts**: Customers are grouped by their acquisition month (first purchase). Retention is calculated by tracking their purchasing activity in subsequent months.
  - **Funnels**: Conversion rates are tracked logically across customer lifetime value milestones (e.g., First Purchase -> Repeat Purchaser -> Loyal Customer).
