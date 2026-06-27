# 🧠 Analysis Assumptions Log

Whenever data is incomplete or ambiguous, our Agentic AI workflows make predefined assumptions to continue execution. This log tracks those foundational assumptions.

| ID | Assumption | Rationale | Impact Area |
|---|---|---|---|
| A01 | Missing `customer_id` defaults to "Guest" | Some POS transactions do not capture customer details. Rather than dropping revenue, we classify them as unidentifiable guests. | Cohort & Funnel Analysis |
| A02 | Campaign impact is evenly distributed | We assume a marketing campaign's impact is uniform across its start and end dates. | Revenue Forecasting (`Prophet`) |
| A03 | Negative revenue rows are data entry errors | If validation scripts find negative revenue, we assume it's a mistake (unless flagged as a return) and filter it out. | Data Validation (`validate_sales.py`) |
| A04 | Missing stock values imply `0` | If the inventory database returns a null value for stock, we assume the item is completely out of stock. | Inventory Management |
| A05 | Regions map to standardized territories | Misspelled regions (e.g. "S. India" vs "South India") are assumed to be separate entities unless a mapping table is provided. | Regional Analysis |
