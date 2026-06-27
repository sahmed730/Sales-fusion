# 🗄️ Master Data Catalog

This catalog provides high-level metadata and governance information for all datasets used within the Sales-Fusion Agentic AI Platform.

*Note: For granular column-level schemas, see the auto-generated [Data Dictionary](../data/data_dictionary.md).*

## Primary Datasets

### 1. `sales.csv`
- **Description**: The master fact table containing all historical transaction records.
- **Source System**: FusionMart POS & E-commerce Backend
- **Update Frequency**: Daily Batch
- **Primary Keys**: `transaction_id` (assumed)
- **PII Presence**: Low (contains `customer_id`, but not raw names/emails)
- **Downstream Impact**: Used heavily by Revenue Forecast, Demand Forecast, Cohorts, Funnels, and Regional Analysis.

### 2. `inventory.csv`
- **Description**: Snapshot of current stock levels and reorder thresholds across warehouses.
- **Source System**: Warehouse Management System (WMS)
- **Update Frequency**: Hourly
- **Primary Keys**: `product_id`
- **PII Presence**: None

### 3. `campaigns.csv`
- **Description**: Historical log of marketing and promotional campaigns, including dates and budgets.
- **Source System**: Marketing CRM
- **Update Frequency**: Monthly
- **Downstream Impact**: Fed into Prophet as holiday regressors to explain demand spikes.

### 4. `customers.csv`
- **Description**: Dimension table containing customer profiles, loyalty tiers, and regional mappings.
- **Source System**: Customer Identity Platform
- **Primary Keys**: `customer_id`
- **PII Presence**: High (Names, Locations)
