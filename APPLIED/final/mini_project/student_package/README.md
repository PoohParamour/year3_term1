# Retail Customer Analytics Dataset (CRISP-DM Assignment)

Welcome to the Retail Customer Analytics dataset! This project provides an omni-channel retail transaction dataset spanning a 24-month observation window (`2024-09-01` to `2026-08-31`).

---

## 📌 Project Objectives & 3 Core Tasks
Your objective is to apply the **Data Science Life Cycle (CRISP-DM)** across 3 analytical tasks:

1. **Customer Segmentation (Unsupervised Learning):**
   - Perform RFM analysis (Recency, Frequency, Monetary) alongside extended behavioral features (Average Order Value, Discount Sensitivity, Customer Tenure, Category Breadth, Basket Depth).
   - Normalize/transform skewed metrics, scale features, and explore data with PCA.
   - Cluster customers using K-Means / DBSCAN and synthesize actionable business personas.

2. **Churn Prediction (Supervised Learning):**
   - Predict which customers are at risk of lapsing based on their historical purchasing rhythm.
   - **Ground Truth Churn Definition:**
     $$\text{churn} = 1 \iff \text{recency\_days} > 90 \iff \text{No valid purchase between 2026-06-02 and 2026-08-31}$$
   - ⚠️ **Critical Leakage Boundary:**
     To prevent data leakage, all input features ($X$) must be constructed **strictly on or before 2026-06-01**. The columns `recency_days`, `last_purchase_date`, and `total_transactions` in `churn_labels.csv` reflect the full outcome window and must **NEVER** be used as input features.
   - Evaluate models using ROC-AUC, PR-AUC, and Recall (overall churn rate is ~25%).

3. **Association Rule Mining & Market Basket Analysis:**
   - Mine frequent itemsets and association rules using Apriori / FP-Growth.
   - Filter strong rules using Support, Confidence, and Lift metrics.
   - Provide strategic retail merchandising and bundle-pricing recommendations.

---

## 📁 Package Contents
- `customers.csv`: 3,000 registered customers (contains demographics, membership tiers, and data quality challenges).
- `products.csv`: 89 SKUs across 15 retail departments.
- `transactions.csv`: ~67,000 basket headers (Note: `is_return == 1` indicates product returns; filter them out before modeling).
- `transaction_items.csv`: ~375,000 basket line items.
- `support_tickets.csv`: ~1,600 customer support tickets and CSAT satisfaction scores.
- `churn_labels.csv`: Ground-truth churn target label (`churn = 1` vs `0`) for each customer.
- `DATA_DICTIONARY.md`: Complete column definitions, table schemas, and data quality guide.

Good luck with your analysis!
