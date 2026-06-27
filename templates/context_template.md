# Context for AI Analysis

*Use this template when assigning a new task to the AI Agent to ensure it has all the necessary boundaries and context.*

## 📁 Data
- **Dataset**: `sales.csv`
- **Location**: `data/sales.csv`
- **Schema**: Transaction ID, Date, Product ID, Revenue, Quantity, Region

## 🎯 Business Context
- **Objective**: We need to understand why South India underperformed last month.
- **KPIs to Optimize**: Average Order Value (AOV), Revenue.
- **Known Assumptions**: The marketing campaign "Summer Splash" was active but targeted mostly North India.

## 🔧 Technical Context
- **Tools**: Python (Pandas), Scikit-Learn
- **Allowed Skills**: `root-cause-investigation`, `programmatic-eda`
- **Constraints**: Do not train a new forecasting model; only analyze historical data for the last 90 days.
