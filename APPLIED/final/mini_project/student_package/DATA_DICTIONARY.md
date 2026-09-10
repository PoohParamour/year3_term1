# Retail Customer Analytics Dataset — Data Dictionary
**Reference Date (วันอ้างอิง): 31 August 2026**
Observation window: 2024-09-01 → 2026-08-31 (24 months) · Currency: THB

5 tables, joined on `customer_id` / `transaction_id` / `product_id`.

```
customers ──< transactions ──< transaction_items >── products
    │                │
    └──< support_tickets   churn_labels (1 row per customer)
```

---

## 1. `customers.csv` — 3,000 customers (+ duplicate rows, see Data Quality)

| Column | Type | Description |
|---|---|---|
| `customer_id` | string | Primary key, `C10001`… |
| `signup_date` | date | Membership registration date (can precede the observation window) |
| `gender` | string | **Inconsistent encoding** — `Male/M/male/Female/F/female` |
| `age` | float | Age at reference date. Has missing values and impossible outliers |
| `region` | string | Bangkok / Central / North / Northeast / East / South. Has missing values |
| `city_tier` | int | 1 = metro, 2 = provincial city, 3 = rural |
| `income_bracket` | string | `<20k`, `20-40k`, `40-70k`, `70-120k`, `>120k` THB/month. Has missing values |
| `membership_tier` | string | Bronze / Silver / Gold / Platinum |
| `preferred_channel` | string | In-Store / Online Web / Mobile App (stated preference) |
| `marketing_optin` | 0/1 | Consented to marketing contact |
| `has_mobile_app` | 0/1 | App installed |

## 2. `products.csv` — 89 SKUs

| Column | Type | Description |
|---|---|---|
| `product_id` | string | Primary key, `P1000`… |
| `product_name` | string | SKU name |
| `category` | string | 15 categories (Bakery, Dairy, Pantry, Coffee & Tea, Fresh Food, Snacks, Beverages, Alcohol, Personal Care, Baby, Household, Pet, Health, Electronics) |
| `unit_price` | int | List price (THB). Actual paid price is in `transaction_items` |

## 3. `transactions.csv` — ~67,000 rows (basket header)

| Column | Type | Description |
|---|---|---|
| `transaction_id` | string | Primary key, `T2xxxxx` (purchases), `T9xxxxx` (returns) |
| `customer_id` | string | FK → customers |
| `transaction_date` | date | `YYYY-MM-DD` |
| `channel` | string | In-Store / Online Web / Mobile App (channel actually used) |
| `store_id` | string | `ST001`–`ST025`, or `ONLINE` |
| `payment_method` | string | Cash / Credit Card / Mobile Banking / e-Wallet |
| `n_items` | int | Distinct line items |
| `total_units` | int | Sum of quantities |
| `gross_amount` | float | Before discount |
| `discount_amount` | float | Total promotion discount |
| `net_amount` | float | `gross_amount − discount_amount` — the amount actually paid |
| `is_return` | 0/1 | **1 = product return** (negative amounts). Filter these out before RFM / churn / basket analysis |

## 4. `transaction_items.csv` — ~375,000 rows (basket lines)

| Column | Type | Description |
|---|---|---|
| `transaction_id` | string | FK → transactions |
| `line_no` | int | Line number within the basket |
| `product_id` | string | FK → products |
| `quantity` | int | Units bought (negative on return transactions). Contains extreme outliers |
| `unit_price` | float | Price actually charged (differs from list price: customer price tier + promotions) |
| `discount_amount` | float | Discount on this line |
| `line_amount` | float | `unit_price × quantity − discount_amount` |

## 5. `support_tickets.csv` — ~1,600 rows

| Column | Type | Description |
|---|---|---|
| `ticket_id` | string | Primary key |
| `customer_id` | string | FK → customers |
| `ticket_date` | date | |
| `issue_type` | string | Delivery Delay / Damaged Item / Wrong Item / Refund Request / Payment Issue / App-Website Problem / Membership Points |
| `contact_channel` | string | Call Center / Chat / Email / Social |
| `is_resolved` | 0/1 | |
| `satisfaction_score` | int | 1–5 |

## 6. `churn_labels.csv` — 3,000 rows (target variable)

| Column | Type | Description |
|---|---|---|
| `customer_id` | string | Primary key |
| `reference_date` | date | Always `2026-08-31` |
| `first_purchase_date` | date | First purchase (excluding returns) |
| `last_purchase_date` | date | Last purchase (excluding returns) |
| `recency_days` | int | `reference_date − last_purchase_date` |
| `tenure_days` | int | `reference_date − first_purchase_date` |
| `total_transactions` | int | Purchase count over the whole window |
| `churn` | 0/1 | **1 = Churned, 0 = Active** |

---

## Churn definition — read this before modelling

```
churn = 1  ⟺  recency_days > 90  ⟺  no purchase between 2026-06-02 and 2026-08-31
```

The label is derived **only from purchase transactions** (`is_return = 0`), so it is exactly
reproducible from `transactions.csv`.

**⚠️ Leakage warning.** Because the label is defined by the last 90 days, any feature computed
using data from **2026-06-02 onwards** leaks the answer. Use a two-window design:

| Window | Dates | Use |
|---|---|---|
| Feature window | 2024-09-01 → **2026-06-01** | build every X variable here |
| Outcome window | **2026-06-02** → 2026-08-31 | defines `churn` only — never used as a feature |

So `recency_days` and `last_purchase_date` from `churn_labels.csv` are **targets, not features**.
Recompute recency as of 2026-06-01 instead.

Overall churn rate ≈ **24.8 %** (743 / 3,000) — imbalanced, so report ROC-AUC / PR-AUC /
recall, not accuracy alone.

---

## Data quality issues (deliberate — this is the Data Preparation exercise)

| Issue | Where | Roughly |
|---|---|---|
| Duplicate rows | `customers.csv` (15), `transactions.csv` (~270) | dedupe on the primary key |
| Missing values | `age` ~4.5 %, `income_bracket` ~5.5 %, `region` ~2.5 % | |
| Inconsistent categories | `customers.gender` — 8 spellings of 2 values | standardise |
| Impossible values | 8 customers with `age` 120–180 | |
| Return transactions | `is_return = 1`, ~700 rows, negative amounts | exclude from RFM / churn / market-basket |
| Quantity outliers | 25 lines in `transaction_items` with 20–60× normal quantity | |

---

## Suggested use per task

**Customer Segmentation (KMeans / DBSCAN, weeks 1–2)**
Build RFM from `transactions` (recency vs 2026-08-31, frequency = purchase count,
monetary = sum of `net_amount`). Log-transform + standardise before clustering — the
distributions are heavily skewed. Extra features that improve separation: average basket
value, discount ratio, tenure, distinct categories bought, items per basket.

**Churn Prediction (weeks 3–7)**
Target `churn_labels.churn`, features from the feature window only. Useful families:
purchase counts in the last 30/90/180/365 days before 2026-06-01, trend ratios between
consecutive windows, spend and basket statistics, discount dependence, category and channel
diversity, support-ticket counts and satisfaction, plus customer demographics.

**Association Rules (Apriori / FP-Growth, weeks 9–10)**
One basket = one `transaction_id`; items = `product_name` from `transaction_items` joined to
`products`. Start at `min_support = 0.01`, `min_confidence = 0.3`, rank by lift.

**Sequential Patterns (week 11)**
Sort each customer's transactions by date and mine ordered sequences of products across
baskets. Several multi-step purchase journeys exist in the data.
