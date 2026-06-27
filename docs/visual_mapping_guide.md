# Visual Mapping Guide

This mapping provides exact field-to-visual property mappings to ensure pixel-perfect reproduction of the dashboard design.

## Layout Hierarchy

### Global Slicers (Top Ribbon)
*   **Date:** `Date[Year]`, `Date[Quarter]`, `Date[Month Name]` (Dropdown/Between).
*   **Region:** `Regions[region]` (Tile).
*   **Category:** `products[category]` (Dropdown).

---

### Dashboard 1: Executive Command Center

#### Visual: Actual vs Forecast Revenue
*   **Visual Type:** Line and Stacked Column Chart
*   **Shared Axis (X):** `Date[Date]`
*   **Column Values (Y1):** `[Total Revenue]`
*   **Line Values (Y2):** `[Forecast Revenue]`
*   **Tooltips:** `[Month-over-Month Growth]`, `[Forecast Variance %]`
*   **Formatting:** Columns = Navy Blue. Line = Teal (Dashed).

#### Visual: Revenue by Region (Anomaly Highlight)
*   **Visual Type:** Clustered Bar Chart
*   **Y-Axis:** `Regions[region]`
*   **X-Axis:** `[Total Revenue]`
*   **Tooltips:** `[Performance Gap]`, `[Anomaly Count]`
*   **Conditional Formatting (Data Colors):** 
    *   Rules based on `[Anomaly Count]`. 
    *   If `[Anomaly Count] > 0` THEN Red, ELSE Light Blue.

#### Visual: Category Distribution
*   **Visual Type:** Donut Chart
*   **Legend:** `products[category]`
*   **Values:** `[Total Revenue]`
*   **Details:** Show Data Labels as `Category, Percent of Total`.

#### Visual: Top Products
*   **Visual Type:** Matrix
*   **Rows:** `products[product_name]`
*   **Values:** `[Total Revenue]`, `[Total Profit]`, `[Product Rank]`
*   **Formatting:** Data bars applied to `[Total Profit]` column (Green/Red divergence).

#### Visual: AI Insights Panel
*   **Visual Type:** Multi-row Card / Smart Narrative Text Box
*   **Values Inserted:** 
    *   `[Revenue Outlook]`
    *   `[Underperforming Region Alert]`
    *   `[Executive Recommendation]`
