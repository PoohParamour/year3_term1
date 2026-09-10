from _helper import md, code

CELLS = [
md(r'''
---
# §6 Deployment

แปลงผลการวิเคราะห์เป็นสิ่งที่ทีมงานนำไปใช้ได้ทันที พร้อมแผนดูแลรักษาหลังนำไปใช้จริง
'''),

md(r'''
## 6.1 รายชื่อลูกค้าเสี่ยงสูง — ส่งทีม CRM ใช้งานได้ทันที

ไฟล์นี้คือผลลัพธ์ที่จับต้องได้ที่สุดของทั้งโปรเจกต์: รายชื่อลูกค้าที่ควรติดต่อ
พร้อมเหตุผลรายบุคคลว่า**ทำไม**ระบบถึงคิดว่าเสี่ยง เพื่อให้พนักงานรู้ว่าควรคุยเรื่องอะไร
'''),

code(r'''
# Score every customer, not just the test set - this is the production hand-off
all_proba = champion.predict_proba(X_all)[:, 1]

risk = pd.DataFrame({
    "customer_id": X_all.index,
    "churn_probability": all_proba,
}).set_index("customer_id")

risk["risk_tier"] = pd.cut(
    risk.churn_probability,
    bins=[-0.001, 0.2, THRESHOLD, 0.7, 1.001],
    labels=["ต่ำ", "เฝ้าระวัง", "สูง", "วิกฤต"])

# Attach the segment persona so CRM knows which playbook to use
seg_name_map = {int(r["กลุ่ม"]): r["ชื่อ Persona"] for _, r in persona_df.iterrows()}
risk["segment"] = customer_features.segment.reindex(risk.index)
risk["persona"] = risk.segment.map(seg_name_map)

# Attach the behavioural facts a human needs in order to have a useful conversation
for col in ["recency", "frequency", "monetary", "avg_order_value",
            "n_tx_90d", "trend_90_over_prev90", "discount_ratio",
            "n_unresolved_tickets", "avg_satisfaction"]:
    risk[col] = churn_features[col].reindex(risk.index)


def top_reasons(row):
    # Per-customer explanation: which warning signals are actually firing for THIS person?
    reasons = []
    if pd.isna(row.frequency):
        return "ไม่มีประวัติการซื้อก่อนวันตัด (ลูกค้าใหม่)"
    if row.recency > 60:
        reasons.append(f"ไม่ซื้อมา {row.recency:.0f} วัน")
    if pd.notna(row.trend_90_over_prev90) and row.trend_90_over_prev90 < 0.6:
        reasons.append("ความถี่ 90 วันล่าสุดลดลงชัดเจน")
    if pd.notna(row.n_tx_90d) and row.n_tx_90d == 0:
        reasons.append("ไม่มีการซื้อเลยใน 90 วันล่าสุด")
    if pd.notna(row.avg_satisfaction) and row.avg_satisfaction <= 2:
        reasons.append(f"คะแนนความพึงพอใจต่ำ ({row.avg_satisfaction:.1f}/5)")
    if pd.notna(row.n_unresolved_tickets) and row.n_unresolved_tickets > 0:
        reasons.append(f"มีเรื่องร้องเรียนค้าง {row.n_unresolved_tickets:.0f} เรื่อง")
    if pd.notna(row.discount_ratio) and row.discount_ratio > 0.10:
        reasons.append(f"ซื้อเมื่อมีส่วนลดเป็นหลัก ({row.discount_ratio:.0%})")
    return " · ".join(reasons) if reasons else "ความเสี่ยงมาจากรูปแบบรวมหลายปัจจัย"


risk["warning_signals"] = risk.apply(top_reasons, axis=1)

ACTION_BY_TIER = {
    "วิกฤต": "โทรหาโดยพนักงานภายใน 48 ชม. + ข้อเสนอเฉพาะบุคคล",
    "สูง": "อีเมล/แอปแบบเฉพาะบุคคล + คูปองตามหมวดที่เคยซื้อ",
    "เฝ้าระวัง": "ใส่ในแคมเปญอัตโนมัติ ติดตามผลรายเดือน",
    "ต่ำ": "ไม่ต้องดำเนินการเป็นพิเศษ",
}
risk["recommended_action"] = risk.risk_tier.map(ACTION_BY_TIER)

risk = risk.sort_values("churn_probability", ascending=False)
save_table(risk.reset_index(), "t27_customer_risk_list")

tier_counts = risk.risk_tier.value_counts().reindex(["วิกฤต", "สูง", "เฝ้าระวัง", "ต่ำ"])
n_actionable = int(tier_counts[["วิกฤต", "สูง"]].sum())

rv("deploy_n_scored", int(len(risk)))
rv("deploy_tier_counts", {str(k): int(v) for k, v in tier_counts.items()})
rv("deploy_n_actionable", n_actionable)
rv("deploy_threshold_used", round(THRESHOLD, 3))

print(f"ให้คะแนนความเสี่ยงลูกค้าครบทั้ง {len(risk):,} ราย")
print()
for tier, n in tier_counts.items():
    print(f"  {tier:<10}: {n:>5,} ราย ({n/len(risk):>5.1%})  -> {ACTION_BY_TIER[tier]}")
print()
print(f"ต้องดำเนินการทันที (วิกฤต + สูง): {n_actionable:,} ราย")
'''),

code(r'''
# Preview what the CRM team actually receives
preview = (risk.head(12)[["churn_probability", "risk_tier", "persona", "recency",
                          "monetary", "warning_signals", "recommended_action"]]
           .reset_index())
preview.columns = ["รหัสลูกค้า", "ความน่าจะเป็น", "ระดับความเสี่ยง", "กลุ่มลูกค้า",
                   "ไม่ซื้อมา (วัน)", "ยอดสะสม (บาท)", "สัญญาณเตือนที่พบ", "สิ่งที่ควรทำ"]
print("ตัวอย่างรายชื่อ 12 อันดับแรก "
      "(ไฟล์เต็มอยู่ที่ outputs/tables/t27_customer_risk_list.csv)")
preview.style.format({"ความน่าจะเป็น": "{:.3f}", "ไม่ซื้อมา (วัน)": "{:.0f}",
                      "ยอดสะสม (บาท)": "{:,.0f}"}).hide(axis="index")
'''),

code(r'''
# Where is the money at risk? Combine probability with each customer's value.
risk["value_at_risk"] = risk.churn_probability * risk.monetary.fillna(0)
var_by_tier = risk.groupby("risk_tier", observed=True).agg(
    n=("churn_probability", "size"),
    total_monetary=("monetary", "sum"),
    value_at_risk=("value_at_risk", "sum"))
save_table(var_by_tier.reset_index(), "t29_value_at_risk_by_tier")

total_var = float(risk.value_at_risk.sum())
actionable_var = float(risk[risk.risk_tier.isin(["วิกฤต", "สูง"])].value_at_risk.sum())
rv("deploy_total_value_at_risk_thb", round(total_var, 0))
rv("deploy_actionable_value_at_risk_thb", round(actionable_var, 0))

fig, axes = plt.subplots(1, 2, figsize=(14, 4.8))
colors_tier = {"วิกฤต": "#c53030", "สูง": "#dd6b20", "เฝ้าระวัง": "#d69e2e", "ต่ำ": "#38a169"}
axes[0].bar(tier_counts.index, tier_counts.values,
            color=[colors_tier[t] for t in tier_counts.index])
for i, v in enumerate(tier_counts.values):
    axes[0].text(i, v, f"{v:,}", ha="center", va="bottom", fontweight="bold")
axes[0].set_title("(a) จำนวนลูกค้าในแต่ละระดับความเสี่ยง")
axes[0].set_ylabel("จำนวนราย")

vr = var_by_tier.value_at_risk.reindex(["วิกฤต", "สูง", "เฝ้าระวัง", "ต่ำ"]) / 1e6
axes[1].bar(vr.index, vr.values, color=[colors_tier[t] for t in vr.index])
for i, v in enumerate(vr.values):
    axes[1].text(i, v, f"{v:.1f}", ha="center", va="bottom", fontweight="bold")
axes[1].set_title("(b) มูลค่าที่มีความเสี่ยง (ล้านบาท)")
axes[1].set_ylabel("ล้านบาท")

fig.tight_layout()
save_fig(fig, "f15_risk_distribution")
plt.show()

print(f"มูลค่าที่มีความเสี่ยงรวม     : {total_var/1e6:,.2f} ล้านบาท")
print(f"อยู่ในกลุ่มที่ต้องลงมือทันที : {actionable_var/1e6:,.2f} ล้านบาท "
      f"({actionable_var/total_var:.0%} ของทั้งหมด)")
print()
print("นิยาม: มูลค่าที่มีความเสี่ยง = ความน่าจะเป็นที่จะหาย x ยอดใช้จ่ายสะสมของลูกค้ารายนั้น")
print("       เป็นตัวเลขไว้ 'จัดลำดับความสำคัญ' ไม่ใช่พยากรณ์ความสูญเสียที่จะเกิดขึ้นจริง")
'''),

md(r'''
## 6.2 ข้อเสนอเชิงกลยุทธ์ต่อผู้บริหาร
'''),

code(r'''
# Tie every recommendation back to a number produced in this notebook
V = {k: v["value"] for k, v in REPORT_VALUES.items() if not k.startswith("_")}

top_bundle = bundle_df.iloc[0]
champ_row = persona_df[persona_df["ชื่อ Persona"].str.contains("Champions")]
risk_row = persona_df[persona_df["ชื่อ Persona"].str.contains("At-Risk")]

if len(champ_row) and len(risk_row):
    seg_evidence = (f"กลุ่ม Champions มีเพียง {champ_row['% ของลูกค้า'].iloc[0]} ของลูกค้า "
                    f"แต่สร้างรายได้ถึง {champ_row['% ของรายได้'].iloc[0]} · "
                    f"ขณะที่กลุ่ม At-Risk High-Value มีอัตรา churn "
                    f"{risk_row['อัตรา churn'].iloc[0]}")
else:
    seg_evidence = "ดูตาราง persona ใน §4.2"

recommendations = [
    {
        "ข้อ": 1,
        "โจทย์": "เพิ่มยอดขายต่อบิล",
        "ข้อเสนอ": f"จัดชุดโปรโมชัน {V['ar_n_bundles']} ชุดตามกลุ่มสินค้าที่ซื้อร่วมกัน "
                   f"เริ่มจากหมวด {top_bundle['หมวดสินค้า']} ซึ่งมีความสัมพันธ์แน่นที่สุด",
        "หลักฐาน": f"กฎความสัมพันธ์ {V['ar_n_rules']} ข้อ · Lift สูงสุด {V['ar_max_lift']} เท่า · "
                   f"มี {V['ar_n_rules_lift_gt_10']} กฎที่ Lift เกิน 10 เท่า",
        "วิธีวัดผล": "ทดสอบ A/B วัดจำนวนรายการต่อบิลและกำไรขั้นต้นต่อบิล",
        "ความเสี่ยง": "กฎบอกความสัมพันธ์ ไม่ใช่เหตุและผล ลูกค้าอาจตั้งใจซื้อคู่กันอยู่แล้ว "
                     "การลดราคาจึงอาจกัดกำไรโดยไม่เพิ่มยอดขาย",
    },
    {
        "ข้อ": 2,
        "โจทย์": "ยิงโปรโมชันให้ตรงกลุ่ม",
        "ข้อเสนอ": f"แบ่งงบการตลาดตาม {V['seg_k_chosen']} persona "
                   f"โดยให้งบ retention กับกลุ่ม At-Risk High-Value เป็นอันดับแรก",
        "หลักฐาน": seg_evidence,
        "วิธีวัดผล": "เทียบ ROI ของแคมเปญรายกลุ่มกับการยิงแบบหว่านแหทั้งฐานลูกค้า",
        "ความเสี่ยง": "กลุ่มเหล่านี้ไม่ใช่กลุ่มธรรมชาติ (ยืนยันด้วย DBSCAN ใน §4.2) "
                     "ลูกค้าใกล้เส้นแบ่งอาจสลับกลุ่มเมื่อ retrain "
                     "จึงไม่ควรผูกสิทธิประโยชน์ถาวรไว้กับหมายเลข segment",
    },
    {
        "ข้อ": 3,
        "โจทย์": "รักษาลูกค้าเดิม",
        "ข้อเสนอ": f"เดินแคมเปญ retention กับลูกค้า {V['deploy_n_actionable']:,} ราย "
                   f"ที่โมเดลจัดอยู่ในระดับเสี่ยงสูงและวิกฤต",
        "หลักฐาน": f"PR-AUC {V['eval_test_pr_auc']} บนชุดทดสอบ · "
                   f"จับผู้ที่กำลังจะหายได้ {V['eval_recall_at_chosen']:.0%} · "
                   f"มูลค่าที่มีความเสี่ยงในกลุ่มนี้ "
                   f"{V['deploy_actionable_value_at_risk_thb']/1e6:,.1f} ล้านบาท",
        "วิธีวัดผล": "กันกลุ่มควบคุมไว้ไม่ส่งแคมเปญ แล้วเทียบอัตราการกลับมาซื้อจริง",
        "ความเสี่ยง": f"เกณฑ์ตัดสิน {V['eval_threshold_chosen']} ไวต่อสมมติฐานต้นทุนมาก "
                     f"(เคลื่อนได้ในช่วง {V['eval_sensitivity_threshold_min']}"
                     f"-{V['eval_sensitivity_threshold_max']}) "
                     f"ต้องยืนยันตัวเลขต้นทุนกับฝ่ายการเงินก่อนใช้จริง",
    },
]

rec_df = pd.DataFrame(recommendations)
save_table(rec_df, "t28_strategic_recommendations")
rv("deploy_recommendations", rec_df.to_dict("records"))

for r in recommendations:
    print("=" * 78)
    print(f"ข้อเสนอที่ {r['ข้อ']} — {r['โจทย์']}")
    print("=" * 78)
    print(f"  ข้อเสนอ    : {r['ข้อเสนอ']}")
    print(f"  หลักฐาน    : {r['หลักฐาน']}")
    print(f"  วิธีวัดผล  : {r['วิธีวัดผล']}")
    print(f"  ความเสี่ยง : {r['ความเสี่ยง']}")
    print()
'''),

md(r'''
## 6.3 แผนการนำไปใช้จริงและการดูแลรักษา

### จังหวะการทำงานที่แนะนำ

| ความถี่ | กิจกรรม | ผู้รับผิดชอบ |
|---|---|---|
| **รายสัปดาห์** | ให้คะแนนความเสี่ยงลูกค้าใหม่ · ส่งรายชื่อกลุ่มวิกฤตให้ทีม CRM | ทีมข้อมูล → CRM |
| **รายเดือน** | ทบทวนผลแคมเปญเทียบกลุ่มควบคุม · ตรวจว่าการกระจายของฟีเจอร์เปลี่ยนไปหรือไม่ | ทีมข้อมูล |
| **รายไตรมาส** | ฝึกโมเดลใหม่ทั้งหมด · ทบทวนจำนวน segment · ทบทวนกฎความสัมพันธ์ตามฤดูกาล | ทีมข้อมูล |
| **รายปี** | ทบทวนนิยาม churn (90 วัน) และสมมติฐานต้นทุนร่วมกับฝ่ายธุรกิจ | ทีมข้อมูล + ฝ่ายธุรกิจ |

### สัญญาณที่บอกว่าต้องฝึกโมเดลใหม่ทันที ไม่ต้องรอถึงรอบ

- PR-AUC บนข้อมูลใหม่ตกลงเกิน 10% จากค่าที่บันทึกไว้ใน `outputs/report_values.json`
- การกระจายของฟีเจอร์สำคัญ (โดยเฉพาะ `recency` และ `frequency`) เปลี่ยนอย่างมีนัยสำคัญ
- อัตรา churn จริงเบี่ยงจากที่โมเดลทำนายเกิน 5 จุดเปอร์เซ็นต์
- มีเหตุการณ์ใหญ่ที่เปลี่ยนพฤติกรรมผู้บริโภค (คู่แข่งรายใหม่ · วิกฤตเศรษฐกิจ · เปลี่ยนนโยบายราคา)

### สิ่งที่ต้องทำก่อนใช้งานจริง

1. **ทดสอบแบบมีกลุ่มควบคุม** — อย่าส่งแคมเปญให้ทุกคนในรายชื่อ กันไว้ราว 20% เพื่อวัดผลกระทบจริง
   มิฉะนั้นจะแยกไม่ออกว่าลูกค้ากลับมาเพราะแคมเปญ หรือเขาจะกลับมาอยู่แล้ว
2. **ยืนยันตัวเลขต้นทุนกับฝ่ายการเงิน** — เกณฑ์ตัดสินไวต่อสมมติฐานมาก (ดูผลทดสอบใน §5.2.1)
3. **ตรวจสอบความยินยอมและความเป็นส่วนตัว** — ติดต่อเฉพาะลูกค้าที่ `marketing_optin = 1`
4. **ตรวจสอบความเป็นธรรม** — ตรวจว่าโมเดลไม่ได้เลือกปฏิบัติต่อกลุ่มประชากรใดอย่างไม่เป็นธรรม
5. **เตรียมแผนสำรอง** — ถ้าระบบให้คะแนนล่ม ใช้กฎจาก Decision Tree ใน §5.3 ทดแทนได้ทันที
'''),

code(r'''
# Persist every number the report will quote, so each figure in the write-up
# can be traced back to this exact run.
dump_report_values()

n_values = len([k for k in REPORT_VALUES if not k.startswith("_")])
n_figs = len(REPORT_VALUES.get("_figures", []))
n_tbls = len(REPORT_VALUES.get("_tables", []))

print()
print("=" * 70)
print("สรุปผลลัพธ์ที่ notebook นี้ผลิตออกมา")
print("=" * 70)
print(f"  ค่าตัวเลขสำหรับรายงาน : {n_values} ค่า -> outputs/report_values.json")
print(f"  รูปภาพ               : {n_figs} ไฟล์ -> outputs/figures/")
print(f"  ตาราง                : {n_tbls} ไฟล์ -> outputs/tables/")
print()
print("ทุกตัวเลขที่ปรากฏในรายงานถูกดึงมาจากไฟล์เหล่านี้เท่านั้น")
'''),

md(r'''
---
# สรุปผลการดำเนินงานตามกระบวนการ CRISP-DM

| ขั้นตอน | สิ่งที่ทำ | ผลลัพธ์สำคัญ |
|---|---|---|
| **1. Business Understanding** | แปลงคำถามผู้บริหาร 3 ข้อเป็นโจทย์ ML พร้อมระบุเหตุผลการเลือกเทคนิค | กำหนดเส้นแบ่งการรั่วไหลของข้อมูลตั้งแต่ต้น |
| **2. Data Understanding** | สำรวจ 6 ตาราง · ตรวจคุณภาพข้อมูล · EDA | พบปัญหาคุณภาพครบทุกข้อและวัดปริมาณได้จริง |
| **3. Data Preparation** | ทำความสะอาด · สร้าง 3 ชุดข้อมูล · ตรวจ leakage อัตโนมัติ | ชุดข้อมูลที่พิสูจน์ได้ด้วยโค้ดว่าไม่รั่ว |
| **4. Modeling** | Association Rules · Clustering · Classification 9 โมเดล + จูน + Stacking | เลือกโมเดลจากผลการทดลองจริง ไม่ใช่จากความเชื่อ |
| **5. Evaluation** | ประเมินบนชุดทดสอบ · ปรับเกณฑ์ตามต้นทุน · ทดสอบความไว · หาสัญญาณเตือน | ตอบครบทั้ง 3 คำถาม พร้อมระบุข้อจำกัด |
| **6. Deployment** | รายชื่อลูกค้าเสี่ยง · ข้อเสนอเชิงกลยุทธ์ · แผน monitoring | ส่งมอบสิ่งที่ทีมงานนำไปใช้ได้ทันที |

### ข้อค้นพบเชิงระเบียบวิธีที่ควรค่าแก่การเน้นย้ำ

1. **ค่าเริ่มต้นไม่ใช่ค่าที่ถูกต้องเสมอไป** — เกณฑ์ตัดสิน 0.5 ให้มูลค่าทางธุรกิจต่ำกว่า
   เกณฑ์ที่คำนวณจากต้นทุนจริงอย่างมีนัยสำคัญ
2. **การตรวจสอบสมมติฐานมีค่าเท่ากับผลลัพธ์** — DBSCAN ไม่ได้ให้ segment ที่ดีกว่า K-Means
   แต่บอกเราว่าควร*ตีความ* segment ที่ได้อย่างไร ซึ่งสำคัญไม่แพ้ตัวผลลัพธ์
3. **ผลลบก็คือผลลัพธ์** — Stacking ไม่ได้ช่วย และการรายงานตามจริงพร้อมเหตุผล
   มีค่ากว่าการยัดเทคนิคเข้าไปเพื่อให้ดูซับซ้อน
4. **โมเดลที่แม่นที่สุดไม่ใช่โมเดลที่อธิบายได้ดีที่สุด** — จึงใช้ทั้งสองบทบาทคู่กัน
   แทนที่จะเลือกอย่างใดอย่างหนึ่ง
'''),
]
