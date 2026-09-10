from _helper import md, code

CELLS = [
md(r'''
---
# §4 Modeling

---
## §4.1 โจทย์ที่ 1 — Increase Basket Size (Association Rule Mining)

> **คำถามผู้บริหาร:** *สินค้าใดมักถูกซื้อคู่กัน และควรนำมาจัดโปรโมชันร่วมกันเพื่อกระตุ้นยอดขายต่อบิล*

### ตัวชี้วัดที่ใช้ตัดสินกฎ

| ตัวชี้วัด | ความหมาย | ใช้ตอบคำถามว่า |
|---|---|---|
| **Support** | สัดส่วนบิลที่มีสินค้าชุดนี้ครบ | คุ้มที่จะทำโปรไหม? ถ้าเจอน้อยเกินก็ไม่มีผลต่อยอดขาย |
| **Confidence** | ซื้อ A แล้วซื้อ B ด้วยกี่ % | ความน่าเชื่อถือของกฎ **แต่ถูกหลอกด้วยสินค้าขายดีได้** |
| **Lift** | ซื้อ A แล้วโอกาสซื้อ B เพิ่มขึ้นกี่เท่า | **มีความสัมพันธ์จริงหรือแค่บังเอิญ** — Lift > 1 เท่านั้นจึงมีความหมาย |

**ค่าเริ่มต้นที่ใช้:** `min_support = 0.01` (กฎต้องปรากฏอย่างน้อย 1% ของบิล มิฉะนั้นเล็กเกินกว่าจะทำโปร)
และ `min_confidence = 0.3` ตามที่ `DATA_DICTIONARY.md` แนะนำ
'''),

code(r'''
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules

MIN_SUPPORT = 0.01
MIN_CONFIDENCE = 0.3
MAX_LEN = 3  # rules of up to 3 items stay interpretable and actionable for merchandising

rv("ar_min_support", MIN_SUPPORT)
rv("ar_min_confidence", MIN_CONFIDENCE)
rv("ar_max_len", MAX_LEN)

# --- Benchmark: Apriori vs FP-Growth ---
# Both algorithms are guaranteed to return the SAME frequent itemsets; they differ only
# in how they search. Time each over several repeats, because a single run at this data
# size is dominated by noise.
N_REPEATS = 5


def time_miner(fn, **kwargs):
    fn(basket_matrix, **kwargs)  # warm-up: keep first-call overhead out of the comparison
    times = []
    for _ in range(N_REPEATS):
        t0 = time.perf_counter()
        out = fn(basket_matrix, **kwargs)
        times.append(time.perf_counter() - t0)
    return out, float(np.median(times)), float(np.std(times))


itemsets_apriori, time_apriori, sd_apriori = time_miner(
    apriori, min_support=MIN_SUPPORT, use_colnames=True, max_len=MAX_LEN)
itemsets_fp, time_fpgrowth, sd_fpgrowth = time_miner(
    fpgrowth, min_support=MIN_SUPPORT, use_colnames=True, max_len=MAX_LEN)

# Verify the two algorithms really do agree - this is the point of the comparison
set_apriori = set(itemsets_apriori.itemsets.apply(frozenset))
set_fp = set(itemsets_fp.itemsets.apply(frozenset))
identical = set_apriori == set_fp

faster = "FP-Growth" if time_fpgrowth < time_apriori else "Apriori"
ratio = max(time_apriori, time_fpgrowth) / min(time_apriori, time_fpgrowth)

rv("ar_n_itemsets", int(len(itemsets_fp)))
rv("ar_time_apriori_sec", round(time_apriori, 4))
rv("ar_time_fpgrowth_sec", round(time_fpgrowth, 4))
rv("ar_benchmark_repeats", N_REPEATS)
rv("ar_faster_algorithm", faster)
rv("ar_speed_ratio", round(ratio, 2))
rv("ar_algorithms_agree", bool(identical))

print(f"จำนวน frequent itemsets ที่พบ: {len(itemsets_fp):,} ชุด")
print(f"(วัดเวลา {N_REPEATS} รอบ รายงานค่ามัธยฐาน)")
print(f"  Apriori   : {time_apriori:7.4f} วินาที  (SD {sd_apriori:.4f})")
print(f"  FP-Growth : {time_fpgrowth:7.4f} วินาที  (SD {sd_fpgrowth:.4f})")
print(f"  -> ได้ itemsets ชุดเดียวกันทุกประการ: {identical}")
print(f"  -> ในชุดข้อมูลนี้ {faster} เร็วกว่า {ratio:.2f} เท่า")
print()
print("ข้อสังเกตที่ต้องรายงานตามจริง:")
print("  ตำราระบุว่า FP-Growth ควรเร็วกว่า Apriori เพราะไม่ต้องสร้าง candidate itemset")
print("  แต่ข้อได้เปรียบนั้นจะเห็นผลเมื่อจำนวนไอเทมมากและ min_support ต่ำ")
print(f"  ชุดข้อมูลนี้มีเพียง {basket_matrix.shape[1]} สินค้า และจำกัด max_len={MAX_LEN}")
print("  พื้นที่การค้นหาจึงเล็กเกินกว่าที่ความต่างเชิงอัลกอริทึมจะแสดงผล")
print("  -> ทั้งสองตัวใช้ได้เท่ากันในงานนี้ เลือกตัวใดก็ได้ผลลัพธ์เดียวกัน")
print("  -> ใช้ FP-Growth ต่อไป เพราะรองรับการขยายขนาดข้อมูลในอนาคตได้ดีกว่า")
'''),

code(r'''
# Generate rules from the frequent itemsets, then rank by lift
rules = association_rules(itemsets_fp, metric="confidence", min_threshold=MIN_CONFIDENCE)
rules = rules.sort_values("lift", ascending=False).reset_index(drop=True)


def fmt_itemset(s):
    # Render a frozenset as a readable comma-separated string
    return ", ".join(sorted(s))


rules["antecedents_str"] = rules.antecedents.apply(fmt_itemset)
rules["consequents_str"] = rules.consequents.apply(fmt_itemset)

rv("ar_n_rules", int(len(rules)))
rv("ar_max_lift", round(float(rules.lift.max()), 2))
rv("ar_min_lift", round(float(rules.lift.min()), 2))
rv("ar_n_rules_lift_gt_2", int((rules.lift > 2).sum()))
rv("ar_n_rules_lift_gt_5", int((rules.lift > 5).sum()))
rv("ar_n_rules_lift_gt_10", int((rules.lift > 10).sum()))

print(f"จำนวนกฎที่ผ่านเกณฑ์ (support>={MIN_SUPPORT}, confidence>={MIN_CONFIDENCE}): {len(rules)} กฎ")
print(f"  Lift สูงสุด : {rules.lift.max():.2f} เท่า")
print(f"  Lift ต่ำสุด : {rules.lift.min():.2f} เท่า")
print(f"  กฎที่ Lift > 2  : {(rules.lift > 2).sum()} กฎ")
print(f"  กฎที่ Lift > 5  : {(rules.lift > 5).sum()} กฎ")
print(f"  กฎที่ Lift > 10 : {(rules.lift > 10).sum()} กฎ")
'''),

code(r'''
# Top rules by lift, formatted for the report
top_rules = rules.head(15)[["antecedents_str", "consequents_str",
                            "support", "confidence", "lift"]].copy()
top_rules.columns = ["ถ้าซื้อ (Antecedent)", "มักซื้อด้วย (Consequent)",
                     "Support", "Confidence", "Lift"]
top_rules.insert(0, "อันดับ", range(1, len(top_rules) + 1))
top_rules["ตีความ"] = top_rules["Lift"].apply(
    lambda x: f"โอกาสซื้อเพิ่มขึ้น {x:.1f} เท่าจากปกติ")

save_table(rules[["antecedents_str", "consequents_str", "support",
                  "confidence", "lift", "leverage", "conviction"]], "t08_association_rules_all")
save_table(top_rules, "t09_association_rules_top15")

rv("ar_top1_antecedent", str(top_rules.iloc[0, 1]))
rv("ar_top1_consequent", str(top_rules.iloc[0, 2]))
rv("ar_top1_lift", round(float(top_rules.iloc[0, 5]), 2))
rv("ar_top1_confidence", round(float(top_rules.iloc[0, 4]), 4))
rv("ar_top1_support", round(float(top_rules.iloc[0, 3]), 4))

top_rules.style.format({"Support": "{:.4f}", "Confidence": "{:.3f}", "Lift": "{:.2f}"}).hide(axis="index")
'''),

code(r'''
# Identify natural product bundles: connected groups of items that co-occur strongly.
# Rather than reading 90+ rules one by one, group the items that appear together in
# high-lift rules - those groups ARE the promotion bundles the business can launch.
STRONG_LIFT = 5.0
strong = rules[rules.lift >= STRONG_LIFT]

# Union-Find to merge overlapping item groups into bundles
parent = {}


def find(x):
    parent.setdefault(x, x)
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[ra] = rb


for _, r in strong.iterrows():
    members = list(r.antecedents | r.consequents)
    for m in members[1:]:
        union(members[0], m)

bundles = {}
for item in parent:
    bundles.setdefault(find(item), []).append(item)
bundles = {k: sorted(v) for k, v in bundles.items() if len(v) >= 2}

# Measure each bundle's business footprint
bundle_rows = []
for i, (_, members) in enumerate(sorted(bundles.items(), key=lambda kv: -len(kv[1])), 1):
    mask = basket_matrix[members].all(axis=1)
    n_baskets = int(mask.sum())
    member_lifts = strong[strong.apply(
        lambda r: bool((r.antecedents | r.consequents) & set(members)), axis=1)].lift
    cat = products_raw[products_raw.product_name.isin(members)].category.mode()
    bundle_rows.append({
        "ชุดที่": i,
        "หมวดสินค้า": cat.iloc[0] if len(cat) else "-",
        "สินค้าในชุด": ", ".join(members),
        "จำนวนสินค้า": len(members),
        "บิลที่ซื้อครบชุด": n_baskets,
        "% ของบิลทั้งหมด": round(n_baskets / len(basket_matrix) * 100, 2),
        "Lift สูงสุดในชุด": round(float(member_lifts.max()), 2) if len(member_lifts) else np.nan,
    })

bundle_df = pd.DataFrame(bundle_rows)
save_table(bundle_df, "t10_product_bundles")

rv("ar_strong_lift_threshold", STRONG_LIFT)
rv("ar_n_bundles", int(len(bundle_df)))
rv("ar_bundle_names", bundle_df["หมวดสินค้า"].tolist())
rv("ar_bundle_sizes", bundle_df["จำนวนสินค้า"].tolist())

print(f"พบชุดสินค้าที่ซื้อร่วมกันแน่นแฟ้น (Lift >= {STRONG_LIFT}) จำนวน {len(bundle_df)} ชุด:")
print()
bundle_df
'''),

code(r'''
fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))

# (a) The classic support-confidence scatter, coloured by lift
sc = axes[0].scatter(rules.support, rules.confidence, c=rules.lift,
                     s=55, cmap="viridis", alpha=0.85, edgecolors="white", linewidth=0.5)
axes[0].set_xlabel("Support (สัดส่วนบิลที่พบชุดสินค้านี้)")
axes[0].set_ylabel("Confidence (ซื้อ A แล้วซื้อ B กี่ %)")
axes[0].set_title("(a) กฎทั้งหมดในมิติ Support-Confidence-Lift")
plt.colorbar(sc, ax=axes[0], label="Lift")

# (b) Top rules ranked by lift
top10 = rules.head(10).iloc[::-1]
lbl = [f"{a} → {c}" for a, c in zip(top10.antecedents_str, top10.consequents_str)]
lbl = [x if len(x) <= 52 else x[:49] + "..." for x in lbl]
bars = axes[1].barh(range(len(top10)), top10.lift.values, color="#2b6cb0")
axes[1].set_yticks(range(len(top10)))
axes[1].set_yticklabels(lbl, fontsize=8.5)
axes[1].axvline(1.0, color="crimson", linestyle="--", linewidth=1.5,
                label="Lift = 1 (ไม่มีความสัมพันธ์)")
axes[1].set_xlabel("Lift (เท่า)")
axes[1].set_title("(b) 10 กฎที่แข็งแรงที่สุด")
axes[1].legend(loc="lower right")
for b, v in zip(bars, top10.lift.values):
    axes[1].text(v, b.get_y() + b.get_height() / 2, f" {v:.1f}x",
                 va="center", fontsize=8.5, fontweight="bold")

fig.tight_layout()
save_fig(fig, "f05_association_rules")
plt.show()
'''),

code(r'''
# Category-level co-occurrence: which departments pull each other into the same basket?
# This drives store-layout and cross-department campaign decisions.
cat_itemsets = fpgrowth(basket_matrix_cat, min_support=0.02, use_colnames=True, max_len=2)
cat_rules = association_rules(cat_itemsets, metric="lift", min_threshold=1.0)
cat_rules = cat_rules[(cat_rules.antecedents.apply(len) == 1)
                      & (cat_rules.consequents.apply(len) == 1)]

lift_matrix = pd.DataFrame(
    np.nan, index=basket_matrix_cat.columns, columns=basket_matrix_cat.columns, dtype=float)
for _, r in cat_rules.iterrows():
    lift_matrix.loc[list(r.antecedents)[0], list(r.consequents)[0]] = r.lift

fig, ax = plt.subplots(figsize=(11, 8.5))
sns.heatmap(lift_matrix, annot=True, fmt=".2f", cmap="RdYlGn", center=1.0,
            linewidths=0.5, ax=ax, cbar_kws={"label": "Lift"},
            annot_kws={"fontsize": 7.5})
ax.set_title("ความสัมพันธ์ระหว่างหมวดสินค้า (Lift)\n"
             "เขียว = ซื้อคู่กันบ่อยกว่าปกติ · แดง = มักไม่ซื้อคู่กัน",
             fontweight="bold")
ax.set_xlabel("หมวดที่ซื้อตาม (Consequent)")
ax.set_ylabel("หมวดที่ซื้อก่อน (Antecedent)")
fig.tight_layout()
save_fig(fig, "f06_category_lift_heatmap")
plt.show()

cat_top = cat_rules.nlargest(8, "lift").copy()
cat_top["คู่หมวดสินค้า"] = [f"{list(a)[0]} → {list(c)[0]}"
                            for a, c in zip(cat_top.antecedents, cat_top.consequents)]
cat_out = cat_top[["คู่หมวดสินค้า", "support", "confidence", "lift"]]
save_table(cat_out, "t11_category_rules_top")

rv("ar_cat_n_rules", int(len(cat_rules)))
rv("ar_cat_top_pair", str(cat_top["คู่หมวดสินค้า"].iloc[0]))
rv("ar_cat_top_lift", round(float(cat_top.lift.iloc[0]), 2))
cat_out.style.format({"support": "{:.4f}", "confidence": "{:.3f}", "lift": "{:.2f}"}).hide(axis="index")
'''),

code(r'''
# Quantify the revenue opportunity: for the strongest rules, how much money is sitting
# in baskets that contain the antecedent but NOT the consequent? That is the gap a
# cross-sell promotion is designed to close.
opportunity = []
for _, r in rules.head(20).iterrows():
    ante = list(r.antecedents)
    cons = list(r.consequents)
    has_ante = basket_matrix[ante].all(axis=1)
    has_cons = basket_matrix[cons].all(axis=1)
    missed = int((has_ante & ~has_cons).sum())
    cons_price = products_raw.set_index("product_name").unit_price.reindex(cons).sum()
    opportunity.append({
        "ถ้าซื้อ": ", ".join(sorted(ante)),
        "ควรเสนอ": ", ".join(sorted(cons)),
        "Lift": round(float(r.lift), 2),
        "Confidence": round(float(r.confidence), 3),
        "บิลที่ซื้อ A แต่ไม่ซื้อ B": missed,
        "มูลค่า B (บาท)": float(cons_price),
        "โอกาสรายได้ (บาท)": round(missed * float(cons_price), 0),
    })

opp_df = (pd.DataFrame(opportunity)
          .sort_values("โอกาสรายได้ (บาท)", ascending=False)
          .reset_index(drop=True))
save_table(opp_df, "t12_crosssell_opportunity")

total_opp = float(opp_df["โอกาสรายได้ (บาท)"].sum())
rv("ar_crosssell_total_opportunity_thb", round(total_opp, 0))
rv("ar_crosssell_top_opportunity_thb", round(float(opp_df["โอกาสรายได้ (บาท)"].iloc[0]), 0))
rv("ar_crosssell_top_pair",
   f"{opp_df['ถ้าซื้อ'].iloc[0]} -> {opp_df['ควรเสนอ'].iloc[0]}")

print("โอกาสทางรายได้จากการขายพ่วง (คิดจาก 20 กฎที่แข็งแรงที่สุด)")
print(f"มูลค่ารวมสูงสุดตามทฤษฎี: {total_opp:,.0f} บาท")
print()
print("หมายเหตุ: ตัวเลขนี้คือเพดานบน สมมติว่าปิดการขายได้ 100% ซึ่งเป็นไปไม่ได้จริง")
print("          ใช้เพื่อ 'จัดลำดับความสำคัญ' ว่าควรทำโปรคู่ไหนก่อน ไม่ใช่พยากรณ์รายได้")
opp_df.head(10)
'''),
]
