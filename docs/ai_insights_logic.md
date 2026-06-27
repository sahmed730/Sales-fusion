# AI Insights Logic Architecture

The AI Insights panel utilizes DAX string concatenation to translate backend machine learning outputs into natural language.

## 1. The Strategy
Instead of requiring executives to interpret scatter plots of Isolation Forest anomalies or XGBoost regression lines, the model compiles the critical findings into direct sentences.

## 2. Core Generative Measures

### Revenue Outlook
**DAX Implementation:**
```dax
"Revenue is expected to reach " & FORMAT([Forecast Revenue], "₹#,0.00") & " representing a variance of " & FORMAT([Forecast Variance %], "0.0%")
```
**Trigger:** Always active. Provides baseline forward-looking context.

### Underperforming Region Alert
**DAX Implementation:**
```dax
IF(
    [Performance Gap] < 0, 
    "Alert: " & FIRSTNONBLANK(Regions[region], 1) & " is missing targets by " & FORMAT([Performance Gap], "₹#,0"), 
    "All regions meeting baseline targets."
)
```
**Trigger:** Activates dynamically when a region is filtered where the Isolation Forest model has flagged a negative gap between `expected_revenue` and `actual_revenue`.

### Inventory Recommendation
**DAX Implementation:**
```dax
IF(
    [Inventory Risk Score] > 110, 
    "Immediate restock recommended for high-risk categories.", 
    "Inventory levels are within optimal coverage targets."
)
```
**Trigger:** Warns the supply chain team when the `Demand Forecast` (XGBoost) significantly outpaces historical `Actual Demand`, causing the Risk Score to breach 110%.

### Executive Recommendation
**DAX Implementation:**
```dax
"Focus marketing spend on " & [Best Performing Region] & " while addressing supply chain constraints highlighted in anomaly reports."
```
**Trigger:** Automatically identifies the #1 rank region and prescribes it for marketing acceleration, marrying descriptive analytics with strategic action.
