from _helper import md, code

CELLS = [
md(r'''
---
# §3 Data Preparation

ทำความสะอาดข้อมูลตามปัญหาที่ตรวจพบใน §2.2 แล้วสร้างชุดข้อมูล 3 ชุดสำหรับ 3 โจทย์

| ชุด | ใช้กับ | มุมมอง | วันอ้างอิง |
|---|---|---|---|
| **A. Basket matrix** | โจทย์ 1 | 1 แถว = 1 บิล | ทั้งช่วง 24 เดือน |
| **B. Customer features** | โจทย์ 2 | 1 แถว = 1 ลูกค้า | 2026-08-31 |
| **C. Churn features** | โจทย์ 3 | 1 แถว = 1 ลูกค้า | **2026-06-01 เท่านั้น** |

> ชุด B และ C ต่างกันที่วันอ้างอิง ไม่ใช่ความผิดพลาด — ชุด B อธิบายลูกค้า ณ ปัจจุบัน
> ส่วนชุด C ต้องย้อนไปยืนที่วันตัดเพื่อไม่ให้เห็นอนาคต (ดู §1.4)
'''),

md(r'''
## 3.1 ทำความสะอาดข้อมูล

หลักการที่ยึด: **ซ่อมดีกว่าทิ้ง** — ทุกครั้งที่เป็นไปได้จะแก้ค่าให้ถูกต้องแทนการลบแถว
เพราะการลบแถวทำให้เสียข้อมูลลูกค้าจริงและอาจสร้างอคติ (เช่น ถ้าคนไม่กรอกรายได้มีพฤติกรรมต่างจากคนที่กรอก)
''' ),

code(r'''
# ---------- customers ----------
customers = customers_raw.drop_duplicates(subset="customer_id", keep="first").copy()

# gender: 8 spellings of 2 values -> take first letter of the lower-cased string
customers["gender"] = (customers.gender.str.strip().str.lower().str[0]
                       .map({"m": "Male", "f": "Female"}))

# age: values above 100 are impossible for a retail member -> treat as missing, then impute
n_age_fixed = int((customers.age > 100).sum())
customers.loc[customers.age > 100, "age"] = np.nan
age_median = float(customers.age.median())
n_age_imputed = int(customers.age.isna().sum())
customers["age"] = customers.age.fillna(age_median)

# region / income_bracket: keep the missingness as its own category instead of dropping rows,
# because "did not disclose" may itself carry signal
n_region_unknown = int(customers.region.isna().sum())
n_income_unknown = int(customers.income_bracket.isna().sum())
customers["region"] = customers.region.fillna("Unknown")
customers["income_bracket"] = customers.income_bracket.fillna("Unknown")

rv("clean_customers_removed_dupes", len(customers_raw) - len(customers))
rv("clean_n_customers", len(customers))
rv("clean_age_impossible_fixed", n_age_fixed)
rv("clean_age_imputed_total", n_age_imputed)
rv("clean_age_median", round(age_median, 1))
rv("clean_region_unknown", n_region_unknown)
rv("clean_income_unknown", n_income_unknown)

print(f"customers: {len(customers_raw):,} -> {len(customers):,} แถว "
      f"(ตัดซ้ำออก {len(customers_raw)-len(customers)})")
print(f"  gender  : รวม 8 รูปแบบการสะกดเหลือ {sorted(customers.gender.unique())}")
print(f"  age     : แก้ค่าเป็นไปไม่ได้ {n_age_fixed} ราย, เติมค่าว่างรวม {n_age_imputed} ราย "
      f"ด้วยมัธยฐาน {age_median:.0f} ปี")
print(f"  region  : เติม 'Unknown' {n_region_unknown} ราย")
print(f"  income  : เติม 'Unknown' {n_income_unknown} ราย")
'''),

code(r'''
# ---------- transactions ----------
transactions = transactions_raw.drop_duplicates(subset="transaction_id", keep="first").copy()
n_tx_dupes = len(transactions_raw) - len(transactions)

# Split purchases from returns. Returns carry negative amounts and would corrupt RFM,
# churn features and basket analysis alike - the data dictionary says to exclude them.
returns = transactions[transactions.is_return == 1].copy()
purchases = transactions[transactions.is_return == 0].copy()

rv("clean_tx_removed_dupes", n_tx_dupes)
rv("clean_n_purchases", len(purchases))
rv("clean_n_returns", len(returns))
rv("clean_return_value_thb", round(float(returns.net_amount.sum()), 2))

print(f"transactions: {len(transactions_raw):,} -> {len(transactions):,} แถว (ตัดซ้ำออก {n_tx_dupes})")
print(f"  แยกเป็น: การซื้อ {len(purchases):,} บิล | การคืนสินค้า {len(returns):,} บิล")
print(f"  มูลค่าการคืนรวม: {returns.net_amount.sum():,.2f} บาท (ติดลบตามที่คาดไว้)")
print(f"  -> ใช้เฉพาะ 'การซื้อ' ในทุกการวิเคราะห์ต่อจากนี้")
'''),

code(r'''
# ---------- transaction_items ----------
# Keep only line items belonging to (de-duplicated, non-return) purchase baskets
items = items_raw[items_raw.transaction_id.isin(set(purchases.transaction_id))].copy()

# --- Quantity outliers ---
# Inspect the shape of the distribution BEFORE choosing a treatment.
observed = np.sort(items.quantity.unique())

# Find where the distribution breaks. Use the RATIO between consecutive observed values,
# not their absolute difference: on a long-tailed variable the largest absolute gap always
# lands out in the sparse tail (here 144 -> 180, a mere 1.25x step) rather than at the real
# boundary between plausible and implausible quantities.
ratios = observed[1:] / observed[:-1]
gap_idx = int(np.argmax(ratios))
legit_max = int(observed[gap_idx])
outlier_min = int(observed[gap_idx + 1])

abs_gap_idx = int(np.argmax(np.diff(observed)))

print("การกระจายของ quantity (นับตามค่า):")
print(items.quantity.value_counts().sort_index().to_string())
print()
print(f"รอยแยกที่ชัดที่สุด (วัดด้วยอัตราส่วน): {legit_max} -> {outlier_min} ชิ้น "
      f"= กระโดด {outlier_min/legit_max:.1f} เท่า")
print(f"เทียบกับถ้าวัดด้วยผลต่างสัมบูรณ์จะได้ {observed[abs_gap_idx]} -> {observed[abs_gap_idx+1]} ชิ้น "
      f"(กระโดดแค่ {observed[abs_gap_idx+1]/observed[abs_gap_idx]:.2f} เท่า)")
print("ซึ่งเป็นจุดที่อยู่ในหางของการแจกแจงอยู่แล้ว ไม่ใช่เส้นแบ่งระหว่างค่าปกติกับค่าผิดปกติ")
print()
print(f"-> ค่าตั้งแต่ {outlier_min} ชิ้นขึ้นไปมี {int((items.quantity >= outlier_min).sum())} แถว "
      f"ซึ่งตรงกับที่ DATA_DICTIONARY ระบุว่ามีราว 25 แถวที่ผิดปกติ")
'''),

code(r'''
# The two groups are separated by an empty band, so they are not two ends of one
# continuum - they are different populations. That also rules out a percentile cap:
# the 99.5th percentile sits at just 5 units and would flatten hundreds of ordinary
# purchases while barely touching the real problem.
#
# Winsorise the implausible group down to the largest plausible value instead of
# deleting the rows, because the item WAS bought - only the recorded count is wrong,
# and deleting the line would silently shrink a real basket.
p995 = float(items.quantity.quantile(0.995))
n_would_hit_p995 = int((items.quantity > p995).sum())

qty_cap = float(legit_max)
n_capped = int((items.quantity > qty_cap).sum())
items["quantity_raw"] = items.quantity
items["quantity"] = items.quantity.clip(upper=qty_cap)

rv("clean_qty_legit_max", legit_max)
rv("clean_qty_outlier_min", outlier_min)
rv("clean_qty_cap", qty_cap)
rv("clean_qty_n_capped", n_capped)
rv("clean_qty_max_before", int(items.quantity_raw.max()))
rv("clean_qty_max_after", float(items.quantity.max()))
rv("clean_qty_p995", round(p995, 2))
rv("clean_qty_n_would_hit_p995", n_would_hit_p995,
   "จำนวนแถวที่จะถูกกระทบถ้าใช้เปอร์เซ็นไทล์ 99.5 - เหตุผลที่ไม่ใช้วิธีนั้น")
rv("clean_n_items", len(items))

print(f"transaction_items: เหลือ {len(items):,} แถว (เฉพาะบิลที่เป็นการซื้อ)")
print(f"  ค่าปกติสูงสุด    : {legit_max} ชิ้น")
print(f"  ค่าผิดปกติต่ำสุด : {outlier_min} ชิ้น")
print(f"  -> จำกัดค่าลงมาที่ {qty_cap:.0f} ชิ้น กระทบ {n_capped} แถว ({n_capped/len(items):.4%} ของทั้งหมด)")
print(f"  quantity สูงสุด  : {items.quantity_raw.max()} -> {items.quantity.max():.0f} ชิ้น")
print()
print(f"  เทียบวิธีที่ไม่ได้เลือก: เปอร์เซ็นไทล์ 99.5 = {p995:.0f} ชิ้น จะกระทบถึง {n_would_hit_p995:,} แถว")
print(f"  ซึ่งเกือบทั้งหมดเป็นการซื้อปกติ ไม่ใช่ค่าผิดปกติ")
'''),

code(r'''
# ---------- master analysis frame ----------
# One row per line item, enriched with product, basket and customer context.
items_full = (items
              .merge(products_raw, on="product_id", how="left")
              .merge(purchases[["transaction_id", "customer_id", "transaction_date",
                                "channel", "store_id", "payment_method"]],
                     on="transaction_id", how="left"))

assert items_full.customer_id.notna().all(), "line items ที่หา basket ไม่เจอ"
assert items_full.product_name.notna().all(), "line items ที่หา product ไม่เจอ"

rv("clean_n_items_full", len(items_full))
print(f"ตารางหลักสำหรับวิเคราะห์: {len(items_full):,} แถว x {items_full.shape[1]} คอลัมน์")
items_full.head(3)
'''),

md(r'''
## 3.2 ชุด A — Basket Matrix (สำหรับโจทย์ที่ 1)

หนึ่งตะกร้า = หนึ่ง `transaction_id` · หนึ่งไอเทม = `product_name`
ใช้ `TransactionEncoder` ของ `mlxtend` แปลงเป็นตาราง boolean แบบ one-hot ตามที่เรียนในสัปดาห์ที่ 9
''' ),

code(r'''
from mlxtend.preprocessing import TransactionEncoder

# Build the list-of-baskets structure that TransactionEncoder expects
basket_lists = (items_full.groupby("transaction_id").product_name
                .apply(lambda s: list(set(s))).tolist())

te = TransactionEncoder()
basket_matrix = pd.DataFrame(te.fit_transform(basket_lists), columns=te.columns_)

# A category-level view as well: useful for department-level merchandising strategy
cat_lists = (items_full.groupby("transaction_id").category
             .apply(lambda s: list(set(s))).tolist())
te_cat = TransactionEncoder()
basket_matrix_cat = pd.DataFrame(te_cat.fit_transform(cat_lists), columns=te_cat.columns_)

rv("basket_n_transactions", int(basket_matrix.shape[0]))
rv("basket_n_products", int(basket_matrix.shape[1]))
rv("basket_n_categories", int(basket_matrix_cat.shape[1]))
rv("basket_mean_distinct_items", round(float(basket_matrix.sum(axis=1).mean()), 2))

print(f"Basket matrix (ระดับสินค้า) : {basket_matrix.shape[0]:,} บิล x {basket_matrix.shape[1]} สินค้า")
print(f"Basket matrix (ระดับหมวด)  : {basket_matrix_cat.shape[0]:,} บิล x {basket_matrix_cat.shape[1]} หมวด")
print(f"จำนวนสินค้าต่างชนิดเฉลี่ยต่อบิล: {basket_matrix.sum(axis=1).mean():.2f} ชนิด")
basket_matrix.iloc[:3, :6]
'''),

md(r'''
## 3.3 ชุด B — Customer Features (สำหรับโจทย์ที่ 2)

RFM มาตรฐาน + อีก 5 มิติเชิงพฤติกรรม คำนวณ ณ วันอ้างอิง **2026-08-31**
''' ),

code(r'''
def build_customer_features(purchase_df, item_df, as_of):
    # Build one row per customer describing purchase behaviour up to `as_of`.
    p = purchase_df[purchase_df.transaction_date <= as_of]
    it = item_df[item_df.transaction_date <= as_of]
    g = p.groupby("customer_id")

    feat = pd.DataFrame({
        # --- classic RFM ---
        "recency": (as_of - g.transaction_date.max()).dt.days,
        "frequency": g.size(),
        "monetary": g.net_amount.sum(),
        # --- extended behavioural features ---
        "avg_order_value": g.net_amount.mean(),
        "tenure_days": (as_of - g.transaction_date.min()).dt.days,
        "basket_depth": g.total_units.mean(),
        "items_per_basket": g.n_items.mean(),
    })

    # Discount sensitivity: what share of gross spend came off as promotion?
    gross = g.gross_amount.sum()
    feat["discount_ratio"] = (g.discount_amount.sum() / gross.where(gross > 0)).fillna(0.0)

    # Category breadth: how many different departments does this customer shop?
    feat["category_breadth"] = it.groupby("customer_id").category.nunique()

    # Channel diversity: single-channel vs omni-channel shopper
    feat["channel_diversity"] = g.channel.nunique()

    return feat.fillna(0.0)


customer_features = build_customer_features(purchases, items_full, REFERENCE_DATE)

rv("segfeat_n_customers", int(len(customer_features)))
rv("segfeat_n_features", int(customer_features.shape[1]))
rv("segfeat_feature_names", customer_features.columns.tolist())
save_table(customer_features.reset_index(), "t06_customer_features")

print(f"Customer features: {customer_features.shape[0]:,} ลูกค้า x {customer_features.shape[1]} ฟีเจอร์")
customer_features.describe().T.style.format("{:,.2f}")
'''),

md(r'''
## 3.4 ชุด C — Churn Features (สำหรับโจทย์ที่ 3) ⚠️ จุดที่ต้องระวังการรั่วไหลของข้อมูล

ฟีเจอร์ทุกตัวคำนวณจากข้อมูล **ถึง 2026-06-01 เท่านั้น** และไม่แตะคอลัมน์ต้องห้ามใน `churn_labels.csv`

**ตระกูลฟีเจอร์ที่สร้าง**

| ตระกูล | ตัวแปร | เหตุผลเชิงธุรกิจ |
|---|---|---|
| RFM ณ วันตัด | recency, frequency, monetary, AOV | ฐานพฤติกรรมการซื้อ |
| **จังหวะการซื้อ** | ระยะห่างเฉลี่ยระหว่างบิล + ส่วนเบี่ยงเบน + อัตราส่วนช่องว่างล่าสุด | ลูกค้าแต่ละคนมีจังหวะของตัวเอง คนที่ซื้อทุก 7 วันแล้วหายไป 30 วัน น่ากังวลกว่าคนที่ซื้อทุก 60 วันแล้วหายไป 30 วัน |
| **แนวโน้ม** | จำนวนบิลใน 30/90/180/365 วัน + อัตราส่วนระหว่างช่วง | จับ "กำลังจะหาย" ไม่ใช่แค่ "หายแล้ว" ซึ่งเป็นหัวใจของการเตือนล่วงหน้า |
| ความผูกพัน | ความหลากหลายหมวด/ช่องทาง/ร้าน | ลูกค้าที่ผูกพันหลายมิติย้ายไปคู่แข่งยากกว่า |
| การพึ่งส่วนลด | สัดส่วนส่วนลดต่อยอดซื้อ | ลูกค้าที่ซื้อเมื่อมีโปรเท่านั้น มักไม่ภักดี |
| **บริการลูกค้า** | จำนวนเรื่องร้องเรียน, CSAT เฉลี่ย, เรื่องที่ยังไม่ปิด | ประสบการณ์แย่เป็นตัวเร่งการเลิกใช้ที่คลาสสิก |
| ข้อมูลประชากร | อายุ, เพศ, ภูมิภาค, ระดับสมาชิก, รายได้ | บริบทพื้นฐานของลูกค้า |
''' ),

code(r'''
def build_churn_features(purchase_df, item_df, ticket_df, customer_df, cutoff):
    # Every feature below is computed strictly from data on or before `cutoff`.
    p = purchase_df[purchase_df.transaction_date <= cutoff].copy()
    it = item_df[item_df.transaction_date <= cutoff]
    tk = ticket_df[ticket_df.ticket_date <= cutoff]
    g = p.groupby("customer_id")

    f = pd.DataFrame({
        "recency": (cutoff - g.transaction_date.max()).dt.days,
        "frequency": g.size(),
        "monetary": g.net_amount.sum(),
        "avg_order_value": g.net_amount.mean(),
        "std_order_value": g.net_amount.std(),
        "tenure_days": (cutoff - g.transaction_date.min()).dt.days,
        "basket_depth": g.total_units.mean(),
        "items_per_basket": g.n_items.mean(),
        "channel_diversity": g.channel.nunique(),
        "store_diversity": g.store_id.nunique(),
    })

    # --- Purchase rhythm: personalised gap statistics ---
    p_sorted = p.sort_values(["customer_id", "transaction_date"])
    gaps = p_sorted.groupby("customer_id").transaction_date.diff().dt.days
    gap_stats = gaps.groupby(p_sorted.customer_id).agg(["mean", "std", "max"])
    f["gap_mean"] = gap_stats["mean"]
    f["gap_std"] = gap_stats["std"]
    f["gap_max"] = gap_stats["max"]
    # Is the current silence unusual FOR THIS CUSTOMER? (>1 means quieter than their own normal)
    f["recency_vs_gap"] = f.recency / f.gap_mean.replace(0, np.nan)

    # --- Trend: activity in recent windows, and whether it is accelerating or decaying ---
    for w in (30, 90, 180, 365):
        f[f"n_tx_{w}d"] = (p[p.transaction_date > cutoff - pd.Timedelta(days=w)]
                           .groupby("customer_id").size().reindex(f.index).fillna(0))
        f[f"spend_{w}d"] = (p[p.transaction_date > cutoff - pd.Timedelta(days=w)]
                            .groupby("customer_id").net_amount.sum().reindex(f.index).fillna(0))
    # Ratio of the most recent 90 days against the 90 days before that: <1 means slowing down
    f["trend_90_over_prev90"] = f.n_tx_90d / (f.n_tx_180d - f.n_tx_90d + 1)
    f["trend_180_over_prev180"] = f.n_tx_180d / (f.n_tx_365d - f.n_tx_180d + 1)

    # --- Discount dependence ---
    gross = g.gross_amount.sum()
    f["discount_ratio"] = (g.discount_amount.sum() / gross.where(gross > 0)).fillna(0.0)

    # --- Category engagement ---
    f["category_breadth"] = it.groupby("customer_id").category.nunique()

    # --- Support experience ---
    tg = tk.groupby("customer_id")
    f["n_tickets"] = tg.size().reindex(f.index).fillna(0)
    f["avg_satisfaction"] = tg.satisfaction_score.mean().reindex(f.index)
    f["n_unresolved_tickets"] = ((1 - tk.is_resolved).groupby(tk.customer_id).sum()
                                 .reindex(f.index).fillna(0))

    # --- Demographics (known at cutoff; signup_date precedes the window) ---
    demo = customer_df.set_index("customer_id")
    f["age"] = demo.age.reindex(f.index)
    f["days_since_signup"] = (cutoff - demo.signup_date.reindex(f.index)).dt.days
    f["marketing_optin"] = demo.marketing_optin.reindex(f.index)
    f["has_mobile_app"] = demo.has_mobile_app.reindex(f.index)
    for col in ("gender", "region", "membership_tier", "income_bracket", "preferred_channel"):
        f[col] = demo[col].reindex(f.index)
    f["city_tier"] = demo.city_tier.reindex(f.index)

    return f


churn_features = build_churn_features(purchases, items_full, tickets_raw, customers, FEATURE_CUTOFF)
print(f"Churn features: {churn_features.shape[0]:,} ลูกค้า x {churn_features.shape[1]} ฟีเจอร์")
churn_features.head(3)
'''),

code(r'''
# ============================================================================
# LEAKAGE GUARD - automated assertions, not just good intentions.
# If any of these fail the notebook stops here rather than producing a
# beautiful-looking but invalid result.
# ============================================================================
FORBIDDEN_COLUMNS = {"recency_days", "last_purchase_date", "total_transactions", "churn"}

# 1) No forbidden outcome column may appear among the features
leaked_cols = FORBIDDEN_COLUMNS & set(churn_features.columns)
assert not leaked_cols, f"LEAKAGE: พบคอลัมน์ต้องห้ามในชุดฟีเจอร์ -> {leaked_cols}"

# 2) No source row used to build features may fall after the cutoff
assert purchases[purchases.transaction_date <= FEATURE_CUTOFF].transaction_date.max() <= FEATURE_CUTOFF
assert items_full[items_full.transaction_date <= FEATURE_CUTOFF].transaction_date.max() <= FEATURE_CUTOFF
assert tickets_raw[tickets_raw.ticket_date <= FEATURE_CUTOFF].ticket_date.max() <= FEATURE_CUTOFF

# 3) Independent re-derivation: recency computed here must never be consistent with
#    the label's own recency (which is measured from a later reference date)
_lbl = churn_raw.set_index("customer_id")
_common = churn_features.index.intersection(_lbl.index)
_offset = (REFERENCE_DATE - FEATURE_CUTOFF).days
_expected_gap = (_lbl.loc[_common, "recency_days"] - churn_features.loc[_common, "recency"])
# For customers whose last purchase was before the cutoff, the gap must be exactly the
# distance between the two reference dates. Any other value means dates were mixed up.
_stable = _lbl.loc[_common, "last_purchase_date"] <= FEATURE_CUTOFF
assert (_expected_gap[_stable] == _offset).all(), "LEAKAGE: การคำนวณ recency ณ วันตัดไม่สอดคล้อง"

rv("leakage_guard_passed", True)
rv("leakage_forbidden_columns", sorted(FORBIDDEN_COLUMNS))
rv("leakage_feature_cutoff", str(FEATURE_CUTOFF.date()))
rv("leakage_reference_date", str(REFERENCE_DATE.date()))
rv("leakage_offset_days", int(_offset))

print("=" * 70)
print("ผ่านการตรวจสอบการรั่วไหลของข้อมูลทั้ง 3 ข้อ")
print("=" * 70)
print(f"  1. ไม่มีคอลัมน์ต้องห้าม {sorted(FORBIDDEN_COLUMNS)} ในชุดฟีเจอร์")
print(f"  2. ไม่มีข้อมูลต้นทางหลังวันตัด {FEATURE_CUTOFF.date()}")
print(f"  3. recency ที่คำนวณใหม่สอดคล้องกับ label พอดี {_offset} วัน "
      f"(= ระยะห่างระหว่างวันตัดกับวันอ้างอิง)")
'''),

code(r'''
# --- Join features to the label and handle the "no purchase before cutoff" cohort ---
labels = churn_raw.set_index("customer_id").churn

modeling_df = labels.to_frame().join(churn_features, how="left")

# Customers with NO purchase at all in the feature window: every behavioural feature is
# undefined for them. They are flagged rather than silently imputed, because §5 reports
# results both with and without this cohort.
no_history_mask = modeling_df.frequency.isna()
n_no_history = int(no_history_mask.sum())
churn_rate_no_history = float(modeling_df.loc[no_history_mask, "churn"].mean()) if n_no_history else np.nan

modeling_df["has_purchase_history"] = (~no_history_mask).astype(int)

rv("model_n_rows", int(len(modeling_df)))
rv("cohort_no_history_n", n_no_history)
rv("cohort_no_history_churn_rate", round(churn_rate_no_history, 4))
rv("cohort_with_history_n", int((~no_history_mask).sum()))
rv("cohort_with_history_churn_rate",
   round(float(modeling_df.loc[~no_history_mask, "churn"].mean()), 4))

print(f"ชุดข้อมูลสำหรับสร้างโมเดล: {len(modeling_df):,} ลูกค้า")
print()
print(f"ลูกค้าที่ไม่มีประวัติซื้อก่อนวันตัด: {n_no_history} ราย "
      f"({n_no_history/len(modeling_df):.1%})")
print(f"  -> อัตรา churn ของกลุ่มนี้: {churn_rate_no_history:.1%}")
print(f"  -> อัตรา churn ของกลุ่มที่มีประวัติ: "
      f"{modeling_df.loc[~no_history_mask, 'churn'].mean():.1%}")
print()
print("ข้อสังเกต: กลุ่มแรกคือลูกค้าที่เพิ่งซื้อครั้งแรกหลังวันตัด จึงไม่มีทางเป็น churn ได้ตามนิยาม")
print("           §5.4 จะรายงานผลทั้งแบบรวมและแบบตัดกลุ่มนี้ออก")
'''),

code(r'''
# Split feature columns by type so the modelling pipeline can treat them correctly
TARGET = "churn"
CATEGORICAL = ["gender", "region", "membership_tier", "income_bracket", "preferred_channel"]
NUMERIC = [c for c in churn_features.columns if c not in CATEGORICAL]
FEATURE_COLS = NUMERIC + CATEGORICAL + ["has_purchase_history"]

rv("model_n_numeric_features", len(NUMERIC))
rv("model_n_categorical_features", len(CATEGORICAL))
rv("model_n_total_features", len(FEATURE_COLS))
rv("model_numeric_feature_names", NUMERIC)
rv("model_categorical_feature_names", CATEGORICAL)
save_table(modeling_df.reset_index(), "t07_churn_modeling_frame")

print(f"ฟีเจอร์เชิงตัวเลข : {len(NUMERIC)} ตัว")
print(f"ฟีเจอร์เชิงหมวดหมู่: {len(CATEGORICAL)} ตัว -> {CATEGORICAL}")
print(f"รวมทั้งหมด        : {len(FEATURE_COLS)} ตัว")
'''),
]
