from _helper import md, code

CELLS = [
md(r'''
---
# §2 Data Understanding

โหลดข้อมูลทั้ง 6 ตาราง สำรวจโครงสร้าง ตรวจคุณภาพ และทำ EDA เพื่อหาข้อค้นพบที่จะกำหนดวิธีเตรียมข้อมูลใน §3
'''),

md(r'''
## 2.1 โหลดข้อมูลและตรวจโครงสร้าง

ความสัมพันธ์ระหว่างตาราง:

```
customers ──< transactions ──< transaction_items >── products
    │              │
    └──< support_tickets    churn_labels (1 แถวต่อ 1 ลูกค้า)
```
'''),

code(r'''
# Load all six tables. Dates are parsed on read so downstream code never re-parses.
customers_raw = pd.read_csv(DATA_DIR / "customers.csv", parse_dates=["signup_date"])
products_raw = pd.read_csv(DATA_DIR / "products.csv")
transactions_raw = pd.read_csv(DATA_DIR / "transactions.csv", parse_dates=["transaction_date"])
items_raw = pd.read_csv(DATA_DIR / "transaction_items.csv")
tickets_raw = pd.read_csv(DATA_DIR / "support_tickets.csv", parse_dates=["ticket_date"])
churn_raw = pd.read_csv(
    DATA_DIR / "churn_labels.csv",
    parse_dates=["reference_date", "first_purchase_date", "last_purchase_date"],
)

overview = pd.DataFrame([
    {"table": "customers", "rows": len(customers_raw), "cols": customers_raw.shape[1]},
    {"table": "products", "rows": len(products_raw), "cols": products_raw.shape[1]},
    {"table": "transactions", "rows": len(transactions_raw), "cols": transactions_raw.shape[1]},
    {"table": "transaction_items", "rows": len(items_raw), "cols": items_raw.shape[1]},
    {"table": "support_tickets", "rows": len(tickets_raw), "cols": tickets_raw.shape[1]},
    {"table": "churn_labels", "rows": len(churn_raw), "cols": churn_raw.shape[1]},
])

rv("raw_n_customers", len(customers_raw))
rv("raw_n_products", len(products_raw))
rv("raw_n_transactions", len(transactions_raw))
rv("raw_n_items", len(items_raw))
rv("raw_n_tickets", len(tickets_raw))
rv("raw_n_churn_rows", len(churn_raw))
save_table(overview, "t01_table_overview")
overview
'''),

code(r'''
# Structure of the two central tables
print("=" * 70)
print("transactions.csv")
print("=" * 70)
transactions_raw.info()
print()
print("=" * 70)
print("customers.csv")
print("=" * 70)
customers_raw.info()
'''),

code(r'''
# Observation window and reference-date sanity check against the data dictionary
obs_min = transactions_raw.transaction_date.min()
obs_max = transactions_raw.transaction_date.max()
rv("obs_window_start", str(obs_min.date()))
rv("obs_window_end", str(obs_max.date()))
rv("obs_window_months", round((obs_max - obs_min).days / 30.44, 1))

print(f"Observation window : {obs_min.date()} -> {obs_max.date()}")
print(f"Span               : {(obs_max - obs_min).days} days "
      f"({(obs_max - obs_min).days / 30.44:.1f} months)")
print(f"Reference date     : {REFERENCE_DATE.date()}  "
      f"(matches data dictionary: {obs_max == REFERENCE_DATE})")
print(f"churn_labels reference_date is unique: "
      f"{churn_raw.reference_date.nunique() == 1} -> {churn_raw.reference_date.iloc[0].date()}")
'''),

md(r'''
## 2.2 ตรวจสอบคุณภาพข้อมูล (Data Quality Audit)

`DATA_DICTIONARY.md` ระบุว่าชุดข้อมูลนี้ **จงใจใส่ปัญหาคุณภาพข้อมูลไว้** เพื่อเป็นแบบฝึกหัดขั้น Data Preparation
เราจะตรวจทีละข้อและวัดปริมาณจริง แทนที่จะเชื่อตามเอกสาร
''' ),

code(r'''
# Quantify every data-quality issue rather than trusting the documentation
audit = []

# 1. Duplicate rows
dup_cust_pk = int(customers_raw.customer_id.duplicated().sum())
dup_cust_full = int(customers_raw.duplicated().sum())
dup_tx_pk = int(transactions_raw.transaction_id.duplicated().sum())
dup_tx_full = int(transactions_raw.duplicated().sum())
audit.append(["customers", "แถวซ้ำ (ซ้ำทั้งแถว)", dup_cust_full, f"{dup_cust_full/len(customers_raw):.2%}"])
audit.append(["transactions", "แถวซ้ำ (ซ้ำทั้งแถว)", dup_tx_full, f"{dup_tx_full/len(transactions_raw):.2%}"])

# 2. Missing values in customers
for col in ["age", "region", "income_bracket", "gender", "membership_tier"]:
    n_missing = int(customers_raw[col].isna().sum())
    if n_missing:
        audit.append(["customers", f"ค่าว่าง: {col}", n_missing, f"{n_missing/len(customers_raw):.2%}"])

# 3. Inconsistent categorical encoding
gender_variants = sorted(customers_raw.gender.dropna().unique().tolist())
audit.append(["customers", "gender สะกดไม่สอดคล้อง", len(gender_variants), ", ".join(gender_variants)])

# 4. Impossible values
impossible_age = int((customers_raw.age > 100).sum())
audit.append(["customers", "อายุเป็นไปไม่ได้ (>100 ปี)", impossible_age,
              f"สูงสุด {customers_raw.age.max():.0f} ปี"])

# 5. Return transactions
n_returns = int((transactions_raw.is_return == 1).sum())
audit.append(["transactions", "รายการคืนสินค้า (is_return=1)", n_returns,
              f"{n_returns/len(transactions_raw):.2%}"])

# 6. Quantity outliers in line items.
# Detect them by distance from the typical value rather than by percentile: §3.2 shows
# the percentile approach picks a threshold inside the range of ordinary purchases.
qty_median = float(items_raw.quantity.median())
n_qty_out = int((items_raw.quantity > qty_median * 10).sum())
audit.append(["transaction_items", "quantity สูงเกิน 10 เท่าของค่ามัธยฐาน", n_qty_out,
              f"สูงสุด {items_raw.quantity.max()} ชิ้น (มัธยฐาน {qty_median:.0f} ชิ้น)"])
audit.append(["transaction_items", "quantity ติดลบ (จากการคืนสินค้า)",
              int((items_raw.quantity < 0).sum()), "คาดหวังไว้แล้ว: มาจากบิลคืนสินค้า"])

audit_df = pd.DataFrame(audit, columns=["ตาราง", "ปัญหาที่พบ", "จำนวน", "รายละเอียด"])

rv("dq_dup_customers", dup_cust_full)
rv("dq_dup_transactions", dup_tx_full)
rv("dq_gender_variants", len(gender_variants), "จำนวนรูปแบบการสะกดของคอลัมน์ gender")
rv("dq_gender_variant_list", gender_variants)
rv("dq_impossible_age", impossible_age)
rv("dq_max_age_raw", float(customers_raw.age.max()))
rv("dq_n_returns", n_returns)
rv("dq_missing_age_pct", round(float(customers_raw.age.isna().mean()) * 100, 2))
rv("dq_missing_region_pct", round(float(customers_raw.region.isna().mean()) * 100, 2))
rv("dq_missing_income_pct", round(float(customers_raw.income_bracket.isna().mean()) * 100, 2))
rv("dq_max_quantity_raw", int(items_raw.quantity.max()))
rv("dq_median_quantity", float(items_raw.quantity.median()))
save_table(audit_df, "t02_data_quality_audit")
audit_df
'''),

code(r'''
# Referential integrity: do all foreign keys resolve?
tx_ids = set(transactions_raw.transaction_id)
cust_ids = set(customers_raw.customer_id)
prod_ids = set(products_raw.product_id)

integrity = pd.DataFrame([
    ["transactions.customer_id -> customers", int((~transactions_raw.customer_id.isin(cust_ids)).sum())],
    ["transaction_items.transaction_id -> transactions", int((~items_raw.transaction_id.isin(tx_ids)).sum())],
    ["transaction_items.product_id -> products", int((~items_raw.product_id.isin(prod_ids)).sum())],
    ["support_tickets.customer_id -> customers", int((~tickets_raw.customer_id.isin(cust_ids)).sum())],
    ["churn_labels.customer_id -> customers", int((~churn_raw.customer_id.isin(cust_ids)).sum())],
], columns=["ความสัมพันธ์ (Foreign Key)", "จำนวนแถวที่หาคู่ไม่เจอ"])

rv("integrity_orphan_total", int(integrity["จำนวนแถวที่หาคู่ไม่เจอ"].sum()))
save_table(integrity, "t03_referential_integrity")
print("ถ้าทุกแถวเป็น 0 แปลว่าความสัมพันธ์ระหว่างตารางสมบูรณ์ ไม่มีแถวกำพร้า")
integrity
'''),

md(r'''
## 2.3 สำรวจข้อมูลเชิงธุรกิจ (EDA)
'''),

code(r'''
# Work on de-duplicated purchases for EDA so charts are not distorted by duplicate rows.
# (Full cleaning happens in §3; this is just enough to make the exploration honest.)
tx_eda = transactions_raw.drop_duplicates("transaction_id")
tx_eda = tx_eda[tx_eda.is_return == 0]

fig, axes = plt.subplots(2, 2, figsize=(14, 9))

# (a) Monthly net revenue - is the business growing, flat, or declining?
monthly = (tx_eda.set_index("transaction_date")
           .net_amount.resample("MS").sum().div(1e6))
axes[0, 0].plot(monthly.index, monthly.values, marker="o", linewidth=2, color="#2b6cb0")
axes[0, 0].set_title("(a) รายได้สุทธิรายเดือน (ล้านบาท)")
axes[0, 0].set_ylabel("ล้านบาท")
axes[0, 0].tick_params(axis="x", rotation=45)

# (b) Revenue by channel
ch = tx_eda.groupby("channel").net_amount.sum().div(1e6).sort_values()
axes[0, 1].barh(ch.index, ch.values, color="#38a169")
axes[0, 1].set_title("(b) รายได้ตามช่องทางการขาย (ล้านบาท)")
axes[0, 1].set_xlabel("ล้านบาท")

# (c) Basket size distribution - the metric business question 1 wants to move
axes[1, 0].hist(tx_eda.n_items, bins=range(1, int(tx_eda.n_items.max()) + 2),
                color="#dd6b20", edgecolor="white")
axes[1, 0].axvline(tx_eda.n_items.mean(), color="crimson", linestyle="--", linewidth=2,
                   label=f"ค่าเฉลี่ย = {tx_eda.n_items.mean():.2f} รายการ")
axes[1, 0].set_title("(c) การกระจายของขนาดตะกร้า (จำนวนรายการต่อบิล)")
axes[1, 0].set_xlabel("จำนวนรายการสินค้าต่อบิล")
axes[1, 0].legend()

# (d) Payment method mix
pm = tx_eda.payment_method.value_counts()
axes[1, 1].pie(pm.values, labels=pm.index, autopct="%1.1f%%", startangle=90,
               colors=sns.color_palette("deep", len(pm)))
axes[1, 1].set_title("(d) สัดส่วนวิธีการชำระเงิน")

fig.suptitle("ภาพรวมธุรกิจจากข้อมูลธุรกรรม", fontsize=14, fontweight="bold")
fig.tight_layout()
save_fig(fig, "f01_business_overview")
plt.show()

rv("eda_mean_basket_items", round(float(tx_eda.n_items.mean()), 2))
rv("eda_median_basket_items", float(tx_eda.n_items.median()))
rv("eda_mean_basket_value", round(float(tx_eda.net_amount.mean()), 2))
rv("eda_total_revenue_thb", round(float(tx_eda.net_amount.sum()), 2))
rv("eda_top_channel", str(ch.idxmax()))
print(f"ขนาดตะกร้าเฉลี่ย : {tx_eda.n_items.mean():.2f} รายการ/บิล")
print(f"มูลค่าเฉลี่ยต่อบิล: {tx_eda.net_amount.mean():,.2f} บาท")
print(f"รายได้รวม        : {tx_eda.net_amount.sum()/1e6:,.2f} ล้านบาท")
'''),

code(r'''
# Category performance - which departments drive revenue, and how often do they appear in baskets?
items_eda = items_raw[items_raw.transaction_id.isin(set(tx_eda.transaction_id))]
items_cat = items_eda.merge(products_raw, on="product_id")

cat_stats = (items_cat.groupby("category")
             .agg(revenue=("line_amount", "sum"),
                  units=("quantity", "sum"),
                  baskets=("transaction_id", "nunique"))
             .assign(basket_penetration=lambda d: d.baskets / tx_eda.transaction_id.nunique())
             .sort_values("revenue", ascending=False))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].barh(cat_stats.index[::-1], cat_stats.revenue.values[::-1] / 1e6, color="#2b6cb0")
axes[0].set_title("รายได้ตามหมวดสินค้า (ล้านบาท)")
axes[0].set_xlabel("ล้านบาท")

pen = cat_stats.basket_penetration.sort_values()
axes[1].barh(pen.index, pen.values * 100, color="#805ad5")
axes[1].set_title("อัตราการปรากฏในตะกร้า (% ของบิลทั้งหมด)")
axes[1].set_xlabel("% ของบิล")

fig.tight_layout()
save_fig(fig, "f02_category_performance")
plt.show()

rv("eda_n_categories", int(cat_stats.shape[0]))
rv("eda_top_category_revenue", str(cat_stats.index[0]))
rv("eda_top_category_penetration", str(pen.index[-1]))
rv("eda_top_category_penetration_pct", round(float(pen.iloc[-1]) * 100, 1))
save_table(cat_stats.reset_index(), "t04_category_stats")
cat_stats.style.format({"revenue": "{:,.0f}", "units": "{:,.0f}",
                        "baskets": "{:,.0f}", "basket_penetration": "{:.1%}"})
'''),

md(r'''
## 2.4 ความเบ้ของ RFM — ข้อค้นพบที่กำหนดวิธีเตรียมข้อมูล

ก่อนทำ clustering ต้องดูรูปร่างการกระจายของตัวแปรก่อน เพราะ K-Means ใช้ระยะทางแบบยุคลิด
ซึ่งอ่อนไหวต่อค่าสุดโต่งอย่างมาก กราฟด้านล่างเป็น**หลักฐานเชิงประจักษ์**ที่ใช้ตัดสินใจว่าต้อง log-transform หรือไม่
'''),

code(r'''
# Quick RFM (full version built in §3) purely to inspect distribution shape
_g = tx_eda.groupby("customer_id")
rfm_peek = pd.DataFrame({
    "Recency": (REFERENCE_DATE - _g.transaction_date.max()).dt.days,
    "Frequency": _g.size(),
    "Monetary": _g.net_amount.sum(),
})

from scipy.stats import skew

from matplotlib.ticker import FuncFormatter


def compact_number(x, _pos):
    # Render large axis values compactly so tick labels do not run into each other
    if abs(x) >= 1_000_000:
        return f"{x/1_000_000:.1f}M"
    if abs(x) >= 1_000:
        return f"{x/1_000:.0f}K"
    return f"{x:.0f}"


fig, axes = plt.subplots(2, 3, figsize=(15, 7))
for i, col in enumerate(["Recency", "Frequency", "Monetary"]):
    s_raw = float(skew(rfm_peek[col]))
    axes[0, i].hist(rfm_peek[col], bins=40, color="#e53e3e", edgecolor="white")
    axes[0, i].set_title(f"{col} — ค่าดิบ\n(ความเบ้ = {s_raw:.2f})")
    axes[0, i].xaxis.set_major_formatter(FuncFormatter(compact_number))
    axes[0, i].tick_params(axis="x", labelrotation=30)

    logged = np.log1p(rfm_peek[col])
    s_log = float(skew(logged))
    axes[1, i].hist(logged, bins=40, color="#38a169", edgecolor="white")
    axes[1, i].set_title(f"{col} — หลัง log1p\n(ความเบ้ = {s_log:.2f})")

    rv(f"skew_{col.lower()}_raw", round(s_raw, 3))
    rv(f"skew_{col.lower()}_log", round(s_log, 3))

fig.suptitle("ความเบ้ของ RFM ก่อนและหลังการแปลงลอการิทึม", fontsize=14, fontweight="bold")
fig.tight_layout()
save_fig(fig, "f03_rfm_skewness")
plt.show()

skew_tbl = pd.DataFrame({
    "ตัวแปร": ["Recency", "Frequency", "Monetary"],
    "ความเบ้ (ค่าดิบ)": [REPORT_VALUES[f"skew_{c}_raw"]["value"] for c in ["recency", "frequency", "monetary"]],
    "ความเบ้ (หลัง log1p)": [REPORT_VALUES[f"skew_{c}_log"]["value"] for c in ["recency", "frequency", "monetary"]],
})
save_table(skew_tbl, "t05_rfm_skewness")
print("ยิ่งค่าความเบ้ใกล้ 0 ยิ่งใกล้การแจกแจงปกติ ซึ่งเหมาะกับอัลกอริทึมที่ใช้ระยะทาง เช่น K-Means")
skew_tbl
'''),

code(r'''
# The churn label: how imbalanced is it? This drives the choice of evaluation metric.
churn_rate = float(churn_raw.churn.mean())
rv("churn_rate", round(churn_rate, 4))
rv("churn_n_positive", int(churn_raw.churn.sum()))
rv("churn_n_negative", int((churn_raw.churn == 0).sum()))
rv("churn_majority_baseline_accuracy", round(1 - churn_rate, 4),
   "Accuracy ที่ได้จากการทายว่าไม่มีใคร churn เลย - แสดงว่าทำไม Accuracy ใช้ไม่ได้")

fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
counts = churn_raw.churn.value_counts().sort_index()
axes[0].bar(["ยังซื้ออยู่ (0)", "หยุดซื้อแล้ว (1)"], counts.values,
            color=["#38a169", "#e53e3e"])
for i, v in enumerate(counts.values):
    axes[0].text(i, v, f"{v:,}\n({v/len(churn_raw):.1%})", ha="center", va="bottom", fontweight="bold")
axes[0].set_title(f"การกระจายของ label (อัตรา churn = {churn_rate:.1%})")
axes[0].set_ylim(0, counts.max() * 1.18)

axes[1].hist(churn_raw.recency_days, bins=50, color="#4a5568", edgecolor="white")
axes[1].axvline(CHURN_HORIZON_DAYS, color="crimson", linestyle="--", linewidth=2,
                label=f"เส้นแบ่ง churn = {CHURN_HORIZON_DAYS} วัน")
axes[1].set_title("recency_days กับเส้นแบ่งนิยาม churn")
axes[1].set_xlabel("จำนวนวันนับจากการซื้อครั้งล่าสุด")
axes[1].legend()

fig.tight_layout()
save_fig(fig, "f04_churn_balance")
plt.show()

# Verify the label is exactly reproducible from the definition (a trust check on the data)
label_check = (churn_raw.recency_days > CHURN_HORIZON_DAYS).astype(int)
matches = bool((label_check == churn_raw.churn).all())
rv("churn_label_reproducible", matches)
print(f"label ตรงกับนิยาม 'recency_days > {CHURN_HORIZON_DAYS}' ทุกแถว: {matches}")
print(f"ถ้าทายว่าไม่มีใคร churn เลย จะได้ Accuracy = {1-churn_rate:.1%} "
      f"ซึ่งสูงแต่ไร้ประโยชน์ -> จึงต้องใช้ PR-AUC และ Recall แทน")
'''),
]
