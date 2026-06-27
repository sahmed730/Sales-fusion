# 📊 Sales-Fusion Data Dictionary
**Auto-generated on: 2026-06-27**

## 📁 Datasets

### campaigns.csv
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| campaign_id | str | - | CAMP001 |
| campaign_name | str | - | Diwali Dhamaka 2021 |
| campaign_start | str | - | 2021-10-25 |
| campaign_end | str | - | 2021-11-05 |

---

### company_names.csv
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| Company Name | str | - | HCL |

---

### customer_product_purchases_india.csv
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| Customer Unique ID | str | - | CUST00001 |
| Customer Name | str | - | Sunita Iyer |
| Product Name | str | - | Mi Smart Band 5 |
| Category | str | - | Electronics |
| Serial No | str | - | MI S506466 |
| Expiry Date | str | - | nan |
| Original Stock Purchase Date | str | - | 2025-02-04 |
| Purchase Date | str | - | 2025-02-09 |
| MRP (INR) | int64 | - | 2421 |
| Price Paid (INR) | float64 | - | 2258.79 |
| Discount (%) | float64 | - | 6.7 |
| Supplier Company | str | - | Xiaomi India |
| Supplier Email | str | - | service.in@xiaomi.com |
| Payment Method | str | - | Cash |
| Warranty Period (months) | int64 | - | 12 |
| Product Condition | str | - | New |
| Shipping Address | str | - | 580 Example Rd, Surat, GJ |
| Customer Email | str | - | sunita.iyer@email.com |
| Contact Number | int64 | - | 7527489918 |
| Order Status | str | - | Shipped |
| Return Eligibility | str | - | No |
| Notes | str | - | Handle with care |

---

### customers.csv
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| customer_id | str | - | C00001 |
| customer_name | str | - | Aarti Patel |
| age | float64 | - | 26.0 |
| gender | str | - | M |
| city | str | - | Gurugram |
| state | str | - | Haryana |
| region | str | - | North India |
| customer_segment | str | - | Retail |
| registration_date | str | - | 2024-10-17 |

---

### data.CSV
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| name | str | - | Brian Castro |
| age | int64 | - | 18 |
| street | str | - | 09942 Spencer River |
| city | str | - | Greggshire |
| state | str | - | Vermont |
| zip | int64 | - | 38216 |
| lng | float64 | - | -33.059534 |
| lat | float64 | - | 50.4823035 |

---

### inventory.csv
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| inventory_id | str | - | INV000001 |
| product_id | str | - | P009 |
| warehouse | str | - | Delhi_WH |
| opening_stock | int64 | - | 3581 |
| closing_stock | int64 | - | 7537 |
| restock_quantity | int64 | - | 9040 |
| inventory_date | str | - | 2021-01-01 |
| event_type | float64 | - | nan |
| event_description | float64 | - | nan |

---

### inventory_data.csv
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| UNIQUE_ID_OF_PRODUCT | str | - | P001 |
| CATEGORY_OF_PRODUCT | str | - | Grocery |
| PRODUCT_NAME | str | - | Fortune Oil 1L |
| NO_OF_STOCK_UNIT_PURCHASED_BY_STORE | int64 | - | 414 |
| NO_OF_STOCK_LEFT | int64 | - | 218 |
| UNIT_COST_FROM_COMPANY_TO_STORE | float64 | - | 53.47 |
| MRP | float64 | - | 79.27 |
| DISCOUNT_GIVEN_BY_COMPANY_TO_STORE | float64 | - | 8.26 |
| ACTUAL_PRICE_TO_CUSTOMER | float64 | - | 73.0 |
| EXPIRY_DATE_OF_PRODUCT | str | - | 2026-08-05 |
| DATE_OF_STOCK_PURCHASED | str | - | 2025-07-22 |
| PURCHASED_COMPANY_NAME | str | - | Hindustan Unilever |
| COMPANY_EMAIL_FOR_ORDERING | str | - | orders@hul.com |

---

### products.csv
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| product_id | str | - | P001 |
| product_name | str | - | FusionBook Air |
| category | str | - | Laptops |
| launch_date | str | - | 2021-01-15 |
| cost_price | int64 | - | 45000 |
| selling_price | int64 | - | 60000 |
| profit_margin | float64 | - | 0.25 |
| warranty_period | int64 | - | 12 |

---

### sales.csv
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| sale_id | str | - | S000001 |
| order_id | str | - | ORD149252 |
| customer_id | str | - | C13966 |
| product_id | str | - | P010 |
| product_name | str | - | Fusion Charger |
| category | str | - | Accessories |
| quantity | int64 | - | 3 |
| unit_price | int64 | - | 1500 |
| discount_percent | float64 | - | 0.0 |
| sales_amount | float64 | - | 4500.0 |
| cost_amount | int64 | - | 1500 |
| profit | float64 | - | 3000.0 |
| payment_method | str | - | Credit Card |
| sales_channel | str | - | Store |
| salesperson_id | str | - | SP096 |
| city | str | - | Amritsar |
| state | str | - | Punjab |
| region | str | - | North India |
| order_date | str | - | 2021-01-01 |
| event_type | float64 | - | nan |
| event_description | float64 | - | nan |

---

