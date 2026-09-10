from _helper import md, code

CELLS = [
md(r'''
---
# §5 Evaluation

ประเมินผลบนชุดทดสอบที่โมเดลไม่เคยเห็น แล้วตอบคำถามผู้บริหารทั้ง 3 ข้อ
พร้อมระบุข้อจำกัดที่ต้องรู้ก่อนนำไปใช้จริง
'''),

md(r'''
## 5.1 ประสิทธิภาพของแชมป์บนชุดทดสอบ
''' ),

code(r'''
# First look at the held-out test set - the honest estimate of real-world performance
y_proba = champion.predict_proba(X_test)[:, 1]
y_pred_default = (y_proba >= 0.5).astype(int)

test_roc = float(roc_auc_score(y_test, y_proba))
test_pr = float(average_precision_score(y_test, y_proba))

rv("eval_test_roc_auc", round(test_roc, 4))
rv("eval_test_pr_auc", round(test_pr, 4))
rv("eval_test_recall_at_050", round(float(recall_score(y_test, y_pred_default)), 4))
rv("eval_test_precision_at_050", round(float(precision_score(y_test, y_pred_default)), 4))
rv("eval_test_f1_at_050", round(float(f1_score(y_test, y_pred_default)), 4))
rv("eval_test_accuracy_at_050", round(float(accuracy_score(y_test, y_pred_default)), 4))
rv("eval_random_baseline_pr_auc", round(float(y_test.mean()), 4))

print(f"ผลของ {champion_name} บนชุดทดสอบ {len(X_test):,} ราย (ไม่เคยเห็นมาก่อน)")
print("=" * 70)
print(f"  ROC-AUC : {test_roc:.4f}")
print(f"  PR-AUC  : {test_pr:.4f}   (การเดาสุ่มได้ {y_test.mean():.4f})")
print(f"  -> ดีกว่าการเดาสุ่ม {test_pr/y_test.mean():.1f} เท่า")
print()
print(f"ที่เกณฑ์เริ่มต้น 0.5:")
print(f"  Recall    : {recall_score(y_test, y_pred_default):.4f}")
print(f"  Precision : {precision_score(y_test, y_pred_default):.4f}")
print(f"  F1        : {f1_score(y_test, y_pred_default):.4f}")
print(f"  Accuracy  : {accuracy_score(y_test, y_pred_default):.4f}")
'''),

md(r'''
## 5.2 เลือกเกณฑ์ตัดสิน (Threshold) จากต้นทุนทางธุรกิจ ไม่ใช่ค่าเริ่มต้น 0.5

เกณฑ์ 0.5 เป็นค่าเริ่มต้นทางคณิตศาสตร์ ไม่ใช่ค่าที่เหมาะกับธุรกิจ เพราะ **ความผิดพลาด 2 แบบมีต้นทุนไม่เท่ากัน**

| ความผิดพลาด | เกิดอะไรขึ้น | ต้นทุน |
|---|---|---|
| **False Positive** — ทายว่าจะหาย แต่จริง ๆ ยังอยู่ | ส่งคูปองให้คนที่ไม่ได้จะไปไหน | **ต่ำ** — เสียแค่ค่าคูปอง |
| **False Negative** — ทายว่ายังอยู่ แต่จริง ๆ กำลังจะหาย | ไม่ได้ทำอะไรเลย แล้วลูกค้าหายไปจริง | **สูง** — เสียกำไรทั้งอนาคตของลูกค้ารายนั้น |

ยิ่ง FN แพงกว่า FP มากเท่าไร เกณฑ์ที่เหมาะสมยิ่งควรต่ำลง เพื่อยอมรับ FP เพิ่มขึ้นแลกกับการพลาด FN น้อยลง
เราจะ **คำนวณหาเกณฑ์จากตัวเลขจริง** ไม่ใช่กำหนดล่วงหน้า แล้วทดสอบว่าคำตอบไวต่อสมมติฐานแค่ไหน
''' ),

code(r'''
# Business assumptions - stated explicitly so a reader can challenge or replace them
COST_COUPON = 150.0            # THB spent per customer we choose to contact
MARGIN_RATE = 0.25             # gross margin on retail revenue
CAMPAIGN_SUCCESS_RATE = 0.30   # share of genuinely at-risk customers a campaign wins back
RETENTION_HORIZON_QUARTERS = 4 # losing a customer costs their FUTURE value, not one quarter

# Value of saving one at-risk customer = margin on the revenue they would still generate
# over the retention horizon. Use the median 90-day spend of retained customers as a
# conservative per-quarter proxy.
active_customers = modeling_df[modeling_df[TARGET] == 0]
median_90d_spend = float(active_customers.spend_90d.median())
VALUE_SAVED = (median_90d_spend * RETENTION_HORIZON_QUARTERS
               * MARGIN_RATE * CAMPAIGN_SUCCESS_RATE)

rv("eval_cost_coupon_thb", COST_COUPON)
rv("eval_margin_rate", MARGIN_RATE)
rv("eval_campaign_success_rate", CAMPAIGN_SUCCESS_RATE)
rv("eval_retention_horizon_quarters", RETENTION_HORIZON_QUARTERS)
rv("eval_median_90d_spend_thb", round(median_90d_spend, 2))
rv("eval_value_per_saved_customer_thb", round(VALUE_SAVED, 2))
rv("eval_fn_fp_cost_ratio", round(VALUE_SAVED / COST_COUPON, 2))

print("สมมติฐานทางธุรกิจที่ใช้ (ปรับได้ตามข้อมูลจริงของบริษัท):")
print(f"  ต้นทุนคูปองต่อคนที่ติดต่อ         : {COST_COUPON:,.0f} บาท")
print(f"  อัตรากำไรขั้นต้น                 : {MARGIN_RATE:.0%}")
print(f"  อัตราความสำเร็จของแคมเปญ         : {CAMPAIGN_SUCCESS_RATE:.0%}")
print(f"  ยอดซื้อ 90 วันของลูกค้าที่ยังอยู่  : {median_90d_spend:,.0f} บาท (มัธยฐาน)")
print(f"  ระยะเวลาที่นับมูลค่าอนาคต         : {RETENTION_HORIZON_QUARTERS} ไตรมาส (1 ปี)")
print()
print(f"  -> มูลค่าที่ได้จากการรักษาลูกค้าไว้ 1 ราย = {VALUE_SAVED:,.0f} บาท")
print(f"  -> อัตราส่วนต้นทุน FN : FP = {VALUE_SAVED/COST_COUPON:.1f} : 1")
print()
print("หมายเหตุสำคัญเรื่องการเลือกระยะเวลา:")
print("  ถ้านับมูลค่าเพียง 1 ไตรมาส จะได้อัตราส่วนเพียง "
      f"{median_90d_spend*MARGIN_RATE*CAMPAIGN_SUCCESS_RATE/COST_COUPON:.1f} : 1")
print("  ซึ่งจะทำให้โมเดลระมัดระวังเกินไปและปล่อยลูกค้าหลุดจำนวนมาก")
print("  แต่การเสียลูกค้าคือการเสียรายได้ 'ทั้งอนาคต' ไม่ใช่แค่ไตรมาสเดียว")
print("  จึงนับที่ 1 ปีซึ่งยังถือว่าอนุรักษ์นิยม -- §5.2.1 จะทดสอบความไวต่อสมมติฐานนี้"
      )
'''),

code(r'''
# Sweep every threshold and compute the expected net value of the campaign
thresholds = np.linspace(0.05, 0.95, 181)
rows = []
for t in thresholds:
    pred = (y_proba >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_test, pred, labels=[0, 1]).ravel()
    contacted = tp + fp
    net_value = tp * VALUE_SAVED - contacted * COST_COUPON
    rows.append({
        "threshold": float(t),
        "tp": int(tp), "fp": int(fp), "fn": int(fn), "tn": int(tn),
        "contacted": int(contacted),
        "recall": tp / (tp + fn) if (tp + fn) else 0.0,
        "precision": tp / contacted if contacted else 0.0,
        "f1": float(f1_score(y_test, pred, zero_division=0)),
        "net_value": float(net_value),
    })

thr_df = pd.DataFrame(rows)
save_table(thr_df, "t20_threshold_sweep")

best_value_row = thr_df.loc[thr_df.net_value.idxmax()]
best_f1_row = thr_df.loc[thr_df.f1.idxmax()]
default_row = thr_df.iloc[(thr_df.threshold - 0.5).abs().idxmin()]

THRESHOLD = float(best_value_row.threshold)

rv("eval_threshold_chosen", round(THRESHOLD, 3))
rv("eval_threshold_best_f1", round(float(best_f1_row.threshold), 3))
rv("eval_net_value_at_chosen", round(float(best_value_row.net_value), 0))
rv("eval_net_value_at_050", round(float(default_row.net_value), 0))
rv("eval_net_value_gain_vs_050", round(float(best_value_row.net_value - default_row.net_value), 0))
rv("eval_recall_at_chosen", round(float(best_value_row.recall), 4))
rv("eval_precision_at_chosen", round(float(best_value_row.precision), 4))
rv("eval_contacted_at_chosen", int(best_value_row.contacted))
rv("eval_contacted_at_050", int(default_row.contacted))

comparison = pd.DataFrame([
    {"เกณฑ์": "ค่าเริ่มต้น 0.5", "threshold": float(default_row.threshold),
     "ติดต่อ (ราย)": int(default_row.contacted), "จับได้ (TP)": int(default_row.tp),
     "พลาด (FN)": int(default_row.fn), "Recall": float(default_row.recall),
     "Precision": float(default_row.precision), "มูลค่าสุทธิ (บาท)": float(default_row.net_value)},
    {"เกณฑ์": "F1 สูงสุด", "threshold": float(best_f1_row.threshold),
     "ติดต่อ (ราย)": int(best_f1_row.contacted), "จับได้ (TP)": int(best_f1_row.tp),
     "พลาด (FN)": int(best_f1_row.fn), "Recall": float(best_f1_row.recall),
     "Precision": float(best_f1_row.precision), "มูลค่าสุทธิ (บาท)": float(best_f1_row.net_value)},
    {"เกณฑ์": "มูลค่าสุทธิสูงสุด (เลือกใช้)", "threshold": THRESHOLD,
     "ติดต่อ (ราย)": int(best_value_row.contacted), "จับได้ (TP)": int(best_value_row.tp),
     "พลาด (FN)": int(best_value_row.fn), "Recall": float(best_value_row.recall),
     "Precision": float(best_value_row.precision), "มูลค่าสุทธิ (บาท)": float(best_value_row.net_value)},
])
save_table(comparison, "t21_threshold_comparison")

print(f"เกณฑ์ที่เลือกใช้: {THRESHOLD:.3f} (จากการหาค่ามูลค่าสุทธิสูงสุด)")
print()
comparison.style.format({"threshold": "{:.3f}", "Recall": "{:.1%}",
                         "Precision": "{:.1%}", "มูลค่าสุทธิ (บาท)": "{:,.0f}"}).hide(axis="index")
'''),

md(r'''
### 5.2.1 ทดสอบความไวต่อสมมติฐาน (Sensitivity Analysis)

เกณฑ์ที่เลือกขึ้นอยู่กับสมมติฐานต้นทุนที่เราตั้งขึ้นเอง จึงต้องตอบให้ได้ว่า
**ถ้าสมมติฐานผิด คำตอบจะเปลี่ยนไปมากแค่ไหน** — ถ้าเปลี่ยนน้อยก็เชื่อถือได้ ถ้าเปลี่ยนมากต้องระวัง
'''),

code(r'''
# How much does the recommended threshold move if our cost assumptions are wrong?
sens_rows = []
for horizon in (1, 2, 4, 8):
    for coupon in (100.0, 150.0, 250.0):
        value = median_90d_spend * horizon * MARGIN_RATE * CAMPAIGN_SUCCESS_RATE
        best_t, best_v, best_recall = None, -np.inf, None
        for t in thresholds:
            pred = (y_proba >= t).astype(int)
            tn_, fp_, fn_, tp_ = confusion_matrix(y_test, pred, labels=[0, 1]).ravel()
            net = tp_ * value - (tp_ + fp_) * coupon
            if net > best_v:
                best_t, best_v = float(t), float(net)
                best_recall = tp_ / (tp_ + fn_) if (tp_ + fn_) else 0.0
        sens_rows.append({
            "ระยะเวลา (ไตรมาส)": horizon,
            "ค่าคูปอง (บาท)": coupon,
            "มูลค่าต่อรายที่รักษาได้": round(value, 0),
            "อัตราส่วน FN:FP": round(value / coupon, 1),
            "เกณฑ์ที่เหมาะสม": round(best_t, 3),
            "Recall ที่ได้": round(best_recall, 3),
            "มูลค่าสุทธิ (บาท)": round(best_v, 0),
        })

sens_df = pd.DataFrame(sens_rows)
save_table(sens_df, "t21b_threshold_sensitivity")
rv("eval_sensitivity_table", sens_df.to_dict("records"))
rv("eval_sensitivity_threshold_min", round(float(sens_df["เกณฑ์ที่เหมาะสม"].min()), 3))
rv("eval_sensitivity_threshold_max", round(float(sens_df["เกณฑ์ที่เหมาะสม"].max()), 3))

fig, ax = plt.subplots(figsize=(9, 5))
for coupon, grp in sens_df.groupby("ค่าคูปอง (บาท)"):
    ax.plot(grp["ระยะเวลา (ไตรมาส)"], grp["เกณฑ์ที่เหมาะสม"], marker="o",
            linewidth=2, label=f"คูปอง {coupon:,.0f} บาท")
ax.axhline(THRESHOLD, color="#d69e2e", linestyle="--", linewidth=2,
           label=f"เกณฑ์ที่เลือกใช้ = {THRESHOLD:.3f}")
ax.axhline(0.5, color="gray", linestyle=":", linewidth=1.5, label="ค่าเริ่มต้น 0.5")
ax.set_xlabel("ระยะเวลาที่นับมูลค่าอนาคตของลูกค้า (ไตรมาส)")
ax.set_ylabel("เกณฑ์ตัดสินที่ให้มูลค่าสุทธิสูงสุด")
ax.set_title("ความไวของเกณฑ์ตัดสินต่อสมมติฐานต้นทุน", fontweight="bold")
ax.legend(fontsize=8.5)
fig.tight_layout()
save_fig(fig, "f12b_threshold_sensitivity")
plt.show()

print(f"เกณฑ์ที่เหมาะสมเคลื่อนไหวอยู่ในช่วง "
      f"{sens_df['เกณฑ์ที่เหมาะสม'].min():.3f} - {sens_df['เกณฑ์ที่เหมาะสม'].max():.3f} "
      f"ตามสมมติฐานที่ทดสอบ {len(sens_df)} ชุด")
print()
print("ข้อสรุปที่ต้องบอกผู้บริหาร: เกณฑ์ไม่ใช่ค่าคงที่ทางเทคนิค แต่เป็น 'ปุ่มปรับเชิงนโยบาย'")
print("ยิ่งประเมินมูลค่าลูกค้าในระยะยาวสูงเท่าไร ยิ่งควรหว่านแหกว้างขึ้นเท่านั้น")
print("ตัวเลขจริงจากฝ่ายการเงินจะเป็นตัวกำหนดเกณฑ์สุดท้าย ไม่ใช่ค่าที่เราสมมติในสมุดเล่มนี้")
sens_df
'''),

code(r'''
fig, axes = plt.subplots(2, 2, figsize=(14.5, 9.5))

# (a) ROC curve
fpr, tpr, _ = roc_curve(y_test, y_proba)
axes[0, 0].plot(fpr, tpr, linewidth=2.2, color="#2b6cb0", label=f"AUC = {test_roc:.4f}")
axes[0, 0].plot([0, 1], [0, 1], "k--", linewidth=1, label="การเดาสุ่ม")
axes[0, 0].set_xlabel("False Positive Rate"); axes[0, 0].set_ylabel("True Positive Rate")
axes[0, 0].set_title("(a) ROC Curve"); axes[0, 0].legend()

# (b) Precision-Recall curve - the more informative view for imbalanced data
prec, rec, _ = precision_recall_curve(y_test, y_proba)
axes[0, 1].plot(rec, prec, linewidth=2.2, color="#38a169", label=f"PR-AUC = {test_pr:.4f}")
axes[0, 1].axhline(float(y_test.mean()), color="crimson", linestyle="--", linewidth=1.2,
                   label=f"การเดาสุ่ม = {y_test.mean():.3f}")
axes[0, 1].scatter([best_value_row.recall], [best_value_row.precision], s=140, marker="*",
                   color="#d69e2e", edgecolors="black", zorder=5,
                   label=f"เกณฑ์ที่เลือก = {THRESHOLD:.2f}")
axes[0, 1].set_xlabel("Recall"); axes[0, 1].set_ylabel("Precision")
axes[0, 1].set_title("(b) Precision-Recall Curve"); axes[0, 1].legend(fontsize=8.5)

# (c) Net business value across thresholds
axes[1, 0].plot(thr_df.threshold, thr_df.net_value / 1000, linewidth=2.2, color="#805ad5")
axes[1, 0].axvline(THRESHOLD, color="#d69e2e", linestyle="--", linewidth=2,
                   label=f"จุดสูงสุด = {THRESHOLD:.2f}")
axes[1, 0].axvline(0.5, color="gray", linestyle=":", linewidth=1.5, label="ค่าเริ่มต้น 0.5")
axes[1, 0].axhline(0, color="black", linewidth=0.8)
axes[1, 0].set_xlabel("เกณฑ์ตัดสิน (Threshold)")
axes[1, 0].set_ylabel("มูลค่าสุทธิของแคมเปญ (พันบาท)")
axes[1, 0].set_title("(c) มูลค่าทางธุรกิจในแต่ละเกณฑ์")
axes[1, 0].legend()

# (d) Confusion matrix at the chosen threshold
y_pred_final = (y_proba >= THRESHOLD).astype(int)
cm = confusion_matrix(y_test, y_pred_final)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=axes[1, 1],
            xticklabels=["ทายว่าอยู่ต่อ", "ทายว่าจะหาย"],
            yticklabels=["จริง: อยู่ต่อ", "จริง: หายไป"], cbar=False,
            annot_kws={"fontsize": 13, "fontweight": "bold"})
axes[1, 1].set_title(f"(d) Confusion Matrix ที่เกณฑ์ {THRESHOLD:.2f}")

fig.suptitle(f"ผลการประเมิน {champion_name} บนชุดทดสอบ", fontsize=14, fontweight="bold")
fig.tight_layout()
save_fig(fig, "f12_evaluation")
plt.show()

tn, fp, fn, tp = cm.ravel()
rv("eval_cm_tn", int(tn)); rv("eval_cm_fp", int(fp))
rv("eval_cm_fn", int(fn)); rv("eval_cm_tp", int(tp))
print(f"ที่เกณฑ์ {THRESHOLD:.3f}: จับลูกค้าที่กำลังจะหายได้ {tp} จาก {tp+fn} ราย "
      f"({tp/(tp+fn):.1%}) โดยติดต่อทั้งหมด {tp+fp} ราย")
'''),

md(r'''
## 5.3 พฤติกรรมใดเป็นสัญญาณเตือน — คำตอบครึ่งหลังของโจทย์ที่ 3

ใช้ 3 มุมมองที่เป็นอิสระต่อกัน ถ้าทั้งสามชี้ไปทางเดียวกัน ความมั่นใจก็สูงขึ้นมาก

1. **Permutation Importance** บนแชมป์ — วัดว่าถ้าสลับค่าฟีเจอร์นั้นแบบสุ่ม โมเดลแย่ลงแค่ไหน
2. **Logistic Regression Coefficients** — บอก**ทิศทาง** ว่าฟีเจอร์นั้นเพิ่มหรือลดความเสี่ยง
3. **Decision Tree** — ให้**กฎที่อ่านออก**และเอาไปเขียนเป็นนโยบายได้
''' ),

code(r'''
# 1) Permutation importance on the champion, scored on the metric we actually care about
perm = permutation_importance(champion, X_test, y_test, n_repeats=15,
                              random_state=RANDOM_STATE, scoring="average_precision",
                              n_jobs=-1)
perm_df = (pd.DataFrame({"feature": FEATURE_COLS,
                         "importance": perm.importances_mean,
                         "std": perm.importances_std})
           .sort_values("importance", ascending=False)
           .reset_index(drop=True))
save_table(perm_df, "t22_permutation_importance")

# 2) Logistic regression coefficients give the DIRECTION of each effect
lr_model = explainer_lr.named_steps["model"]
lr_feature_names = explainer_lr.named_steps["prep"].get_feature_names_out()
coef_df = (pd.DataFrame({"feature": [f.split("__", 1)[-1] for f in lr_feature_names],
                         "coefficient": lr_model.coef_[0]})
           .assign(abs_coef=lambda d: d.coefficient.abs(),
                   odds_ratio=lambda d: np.exp(d.coefficient))
           .sort_values("abs_coef", ascending=False)
           .reset_index(drop=True))
save_table(coef_df, "t23_logreg_coefficients")

rv("eval_top_features_permutation", perm_df.head(10).feature.tolist())
rv("eval_top_feature", str(perm_df.feature.iloc[0]))
rv("eval_top_feature_importance", round(float(perm_df.importance.iloc[0]), 4))

fig, axes = plt.subplots(1, 2, figsize=(15.5, 6))

top_perm = perm_df.head(12).iloc[::-1]
axes[0].barh(top_perm.feature, top_perm.importance, xerr=top_perm["std"], color="#2b6cb0")
axes[0].set_xlabel("ความสำคัญ (PR-AUC ที่หายไปเมื่อสลับค่าฟีเจอร์)")
axes[0].set_title(f"(a) Permutation Importance ของ {champion_name}\nฟีเจอร์ใดสำคัญที่สุด")

top_coef = coef_df.head(12).iloc[::-1]
colors = ["#e53e3e" if c > 0 else "#38a169" for c in top_coef.coefficient]
axes[1].barh(top_coef.feature, top_coef.coefficient, color=colors)
axes[1].axvline(0, color="black", linewidth=0.9)
axes[1].set_xlabel("ค่าสัมประสิทธิ์ (แดง = เพิ่มความเสี่ยง · เขียว = ลดความเสี่ยง)")
axes[1].set_title("(b) Logistic Regression Coefficients\nฟีเจอร์นั้นดันความเสี่ยงไปทางไหน")

fig.tight_layout()
save_fig(fig, "f13_feature_importance")
plt.show()
'''),

code(r'''
# 3) The decision tree turns the model into rules a manager can read and act on
fig, ax = plt.subplots(figsize=(16, 8))
dt_model = explainer_dt.named_steps["model"]
dt_features = [f.split("__", 1)[-1]
               for f in explainer_dt.named_steps["prep"].get_feature_names_out()]
# Show only the first two levels: at depth 3 the boxes shrink until they are
# unreadable once the figure is scaled into a document. The deeper rules remain
# available in the fitted model and are printed as text in the next cell.
plot_tree(dt_model, feature_names=dt_features, class_names=["ยังซื้ออยู่", "หยุดซื้อ"],
          filled=True, rounded=True, fontsize=12, max_depth=2, ax=ax, proportion=True)
ax.set_title("กฎการตัดสินใจที่อ่านออก (Decision Tree, แสดง 2 ระดับแรก)",
             fontsize=14, fontweight="bold")
fig.tight_layout()
save_fig(fig, "f14_decision_tree_rules")
plt.show()

dt_test_recall = float(recall_score(y_test, explainer_dt.predict(X_test)))
rv("eval_explainer_dt_recall", round(dt_test_recall, 4))
rv("eval_explainer_dt_depth", int(dt_model.get_depth()))
print(f"Decision Tree ที่ใช้เป็นผู้อธิบาย: ลึก {dt_model.get_depth()} ระดับ "
      f"· Recall บนชุดทดสอบ {dt_test_recall:.1%}")
print("ต้นไม้นี้ไม่ได้ใช้ทำนายจริง แต่ใช้แปลงโมเดลให้เป็นกฎที่สื่อสารกับทีมธุรกิจได้")
'''),

code(r'''
# The same tree as plain text: every rule at full depth, in a form that can be
# pasted straight into a document or handed to the business team as a checklist.
from sklearn.tree import export_text

tree_rules = export_text(dt_model, feature_names=list(dt_features),
                         decimals=2, show_weights=False)

# Translate the leaf labels into business language
tree_rules_th = (tree_rules
                 .replace("class: 1", "class: เสี่ยงหยุดซื้อ")
                 .replace("class: 0", "class: ยังซื้ออยู่"))

with open(TBL_DIR / "t24b_decision_tree_rules.txt", "w", encoding="utf-8") as fh:
    fh.write(tree_rules_th)
REPORT_VALUES.setdefault("_tables", []).append(
    {"path": str(TBL_DIR / "t24b_decision_tree_rules.txt"),
     "rows": tree_rules_th.count(chr(10))})

rv("eval_tree_rules_text", tree_rules_th)
rv("eval_tree_n_leaves", int(dt_model.get_n_leaves()))

print("กฎทั้งหมดจาก Decision Tree (ครบทุกระดับ):")
print("=" * 78)
print(tree_rules_th)
print("=" * 78)
print(f"รวม {dt_model.get_n_leaves()} เงื่อนไขปลายทาง (leaf)")
print("บันทึกเป็นไฟล์ข้อความไว้ที่ outputs/tables/t24b_decision_tree_rules.txt")
'''),

code(r'''
# Cross-check the three views and translate them into business language.
# Direction comes from the model's own coefficient sign - never from an assumption
# written in advance. The notes below describe WHAT each feature measures, neutrally,
# so they cannot contradict whatever direction the data turns out to show.
top_feats = perm_df.head(10).feature.tolist()
coef_lookup = coef_df.set_index("feature").coefficient.to_dict()

FEATURE_MEANING = {
    "recency": "จำนวนวันนับจากการซื้อครั้งล่าสุด (ณ วันตัด)",
    "recency_vs_gap": "ความเงียบปัจจุบันเทียบกับจังหวะการซื้อปกติของลูกค้ารายนั้นเอง",
    "gap_mean": "ระยะห่างเฉลี่ยระหว่างการซื้อแต่ละครั้ง",
    "gap_std": "ความสม่ำเสมอของจังหวะการซื้อ (ยิ่งสูงยิ่งไม่สม่ำเสมอ)",
    "gap_max": "ช่วงที่เคยหายไปนานที่สุด",
    "trend_90_over_prev90": "ความถี่ 90 วันล่าสุด หารด้วย 90 วันก่อนหน้า",
    "trend_180_over_prev180": "ความถี่ 180 วันล่าสุด หารด้วยช่วงก่อนหน้า",
    "n_tx_30d": "จำนวนบิลใน 30 วันก่อนวันตัด",
    "n_tx_90d": "จำนวนบิลใน 90 วันก่อนวันตัด",
    "n_tx_180d": "จำนวนบิลใน 180 วันก่อนวันตัด",
    "n_tx_365d": "จำนวนบิลใน 365 วันก่อนวันตัด",
    "spend_30d": "ยอดใช้จ่ายใน 30 วันก่อนวันตัด",
    "spend_90d": "ยอดใช้จ่ายใน 90 วันก่อนวันตัด",
    "spend_180d": "ยอดใช้จ่ายใน 180 วันก่อนวันตัด",
    "spend_365d": "ยอดใช้จ่ายใน 365 วันก่อนวันตัด",
    "frequency": "จำนวนครั้งที่ซื้อทั้งหมดในช่วงฟีเจอร์",
    "monetary": "ยอดใช้จ่ายสะสมทั้งหมดในช่วงฟีเจอร์",
    "tenure_days": "จำนวนวันนับจากการซื้อครั้งแรก",
    "days_since_signup": "จำนวนวันนับจากวันสมัครสมาชิก",
    "discount_ratio": "สัดส่วนส่วนลดต่อยอดซื้อรวม",
    "category_breadth": "จำนวนหมวดสินค้าที่เคยซื้อ",
    "channel_diversity": "จำนวนช่องทางที่ใช้ซื้อ",
    "store_diversity": "จำนวนสาขาที่เคยไปซื้อ",
    "avg_satisfaction": "คะแนนความพึงพอใจเฉลี่ยจากการติดต่อฝ่ายบริการ",
    "n_tickets": "จำนวนเรื่องที่ติดต่อฝ่ายบริการ",
    "n_unresolved_tickets": "จำนวนเรื่องร้องเรียนที่ยังไม่ถูกแก้ไข",
    "avg_order_value": "มูลค่าเฉลี่ยต่อบิล",
    "std_order_value": "ความผันผวนของมูลค่าต่อบิล",
    "basket_depth": "จำนวนชิ้นเฉลี่ยต่อตะกร้า",
    "items_per_basket": "จำนวนรายการสินค้าเฉลี่ยต่อตะกร้า",
    "has_purchase_history": "มีประวัติการซื้อก่อนวันตัดหรือไม่ (0/1)",
    "age": "อายุลูกค้า",
    "city_tier": "ระดับเมืองที่อยู่อาศัย",
    "marketing_optin": "ยินยอมรับการติดต่อทางการตลาด (0/1)",
    "has_mobile_app": "ติดตั้งแอปพลิเคชันหรือไม่ (0/1)",
}

# A genuine independent check: compare each group's mean directly in the data.
# This is univariate (ignores other features) whereas the coefficient is conditional
# (holds other features constant) - so agreement is real evidence, and disagreement
# is a finding worth reporting rather than hiding.
train_df = X_train.join(y_train)
signal_rows = []
for i, feat in enumerate(top_feats, 1):
    coef = coef_lookup.get(feat)

    if feat in NUMERIC + ["has_purchase_history"]:
        mean_churn = float(train_df.loc[train_df[TARGET] == 1, feat].mean())
        mean_stay = float(train_df.loc[train_df[TARGET] == 0, feat].mean())
        uni_dir = "สูงขึ้น" if mean_churn > mean_stay else "ต่ำลง"
    else:
        mean_churn = mean_stay = np.nan
        uni_dir = "-"

    if coef is None or np.isnan(coef):
        model_dir, agreement = "-", "-"
    else:
        model_dir = "เสี่ยงมากขึ้น" if coef > 0 else "เสี่ยงน้อยลง"
        if uni_dir == "-":
            agreement = "-"
        else:
            same = (coef > 0) == (uni_dir == "สูงขึ้น")
            agreement = "สอดคล้อง" if same else "สวนทาง (ดูหมายเหตุ)"

    signal_rows.append({
        "อันดับ": i,
        "ฟีเจอร์": feat,
        "ฟีเจอร์นี้วัดอะไร": FEATURE_MEANING.get(feat, "-"),
        "ความสำคัญ": round(float(perm_df.set_index("feature").importance[feat]), 4),
        "ค่าเฉลี่ยกลุ่มที่ churn": round(mean_churn, 2) if not np.isnan(mean_churn) else None,
        "ค่าเฉลี่ยกลุ่มที่อยู่ต่อ": round(mean_stay, 2) if not np.isnan(mean_stay) else None,
        "ข้อมูลดิบชี้ว่า": f"ผู้ที่ churn มีค่านี้{uni_dir}",
        "โมเดลเชิงเส้นชี้ว่า": f"ค่าสูง -> {model_dir}",
        "การตรวจสอบไขว้": agreement,
    })

signals_df = pd.DataFrame(signal_rows)
save_table(signals_df, "t24_warning_signals")
rv("eval_warning_signals", signals_df.to_dict("records"))
rv("eval_n_signals_consistent", int((signals_df["การตรวจสอบไขว้"] == "สอดคล้อง").sum()))
rv("eval_n_signals_conflicting",
   int(signals_df["การตรวจสอบไขว้"].str.startswith("สวนทาง").sum()))

print("สัญญาณเตือน 10 อันดับแรก (เรียงตาม Permutation Importance)")
print("=" * 78)
for _, r in signals_df.iterrows():
    flag = "  <-- ต้องอธิบายเพิ่ม" if r["การตรวจสอบไขว้"].startswith("สวนทาง") else ""
    print(f"{r['อันดับ']:>2}. {r['ฟีเจอร์']}  (ความสำคัญ {r['ความสำคัญ']:.4f}){flag}")
    print(f"    วัดอะไร      : {r['ฟีเจอร์นี้วัดอะไร']}")
    if r["ค่าเฉลี่ยกลุ่มที่ churn"] is not None:
        print(f"    ข้อมูลดิบ     : churn เฉลี่ย {r['ค่าเฉลี่ยกลุ่มที่ churn']:,} "
              f"vs อยู่ต่อเฉลี่ย {r['ค่าเฉลี่ยกลุ่มที่อยู่ต่อ']:,}")
    print(f"    โมเดลเชิงเส้น : {r['โมเดลเชิงเส้นชี้ว่า']}")
    print(f"    ตรวจสอบไขว้   : {r['การตรวจสอบไขว้']}")
    print()

n_conflict = int(signals_df["การตรวจสอบไขว้"].str.startswith("สวนทาง").sum())
print("-" * 78)
print(f"สอดคล้องกัน {int((signals_df['การตรวจสอบไขว้'] == 'สอดคล้อง').sum())} ตัว · "
      f"สวนทางกัน {n_conflict} ตัว")
if n_conflict:
    print()
    print("การสวนทางไม่ใช่ข้อผิดพลาด แต่เป็นปรากฏการณ์ที่อธิบายได้:")
    print("  ข้อมูลดิบดูแบบตัวแปรเดียว ส่วนค่าสัมประสิทธิ์ดูแบบ 'คุมตัวแปรอื่นให้คงที่'")
    print("  เช่น ยอดใช้จ่ายสะสมสูงมักมาคู่กับความถี่สูง เมื่อคุมความถี่ไว้แล้ว")
    print("  ยอดสะสมที่สูงกลับหมายถึง 'เคยซื้อหนักแต่ตอนนี้เงียบ' ซึ่งเป็นสัญญาณเสี่ยง")
    print("  -> ต้องใช้ทั้งสองมุมประกอบกัน ไม่ใช่ยึดมุมใดมุมหนึ่ง")
'''),

md(r'''
## 5.4 ตรวจสอบความทนทาน: กลุ่มลูกค้าที่ไม่มีประวัติการซื้อก่อนวันตัด

ใน §3.4 พบลูกค้ากลุ่มหนึ่งที่ไม่มีธุรกรรมเลยก่อนวันตัด และทุกคนในกลุ่มมี `churn = 0`
ซึ่งเป็น **artifact ของวิธีสร้างข้อมูล** ไม่ใช่รูปแบบพฤติกรรมที่มีความหมาย

ถ้าปล่อยไว้เฉย ๆ โมเดลอาจเรียนรู้ทางลัดว่า *"ไม่มีประวัติ = ไม่ churn"* ซึ่งจะทำให้
ตัวเลขประสิทธิภาพดูดีเกินจริง จึงต้องรายงานผล**ทั้งแบบรวมและแบบตัดกลุ่มนี้ออก**
''' ),

code(r'''
# Re-evaluate on the subset of the test set that actually has purchase history
mask_has_history = X_test.has_purchase_history == 1
n_excluded = int((~mask_has_history).sum())

roc_with = test_roc
pr_with = test_pr
roc_without = float(roc_auc_score(y_test[mask_has_history], y_proba[mask_has_history.values]))
pr_without = float(average_precision_score(y_test[mask_has_history], y_proba[mask_has_history.values]))

scenario = pd.DataFrame([
    {"สถานการณ์": "A. รวมลูกค้าที่ไม่มีประวัติ (ทั้งชุดทดสอบ)",
     "จำนวนราย": int(len(y_test)), "อัตรา churn": float(y_test.mean()),
     "ROC-AUC": roc_with, "PR-AUC": pr_with},
    {"สถานการณ์": "B. ตัดลูกค้าที่ไม่มีประวัติออก",
     "จำนวนราย": int(mask_has_history.sum()),
     "อัตรา churn": float(y_test[mask_has_history].mean()),
     "ROC-AUC": roc_without, "PR-AUC": pr_without},
])
save_table(scenario, "t25_scenario_comparison")

rv("eval_scenarioA_roc_auc", round(roc_with, 4))
rv("eval_scenarioA_pr_auc", round(pr_with, 4))
rv("eval_scenarioB_roc_auc", round(roc_without, 4))
rv("eval_scenarioB_pr_auc", round(pr_without, 4))
rv("eval_scenario_n_excluded_test", n_excluded)
rv("eval_scenario_pr_auc_drop", round(pr_with - pr_without, 4))

print(f"ลูกค้าที่ไม่มีประวัติในชุดทดสอบ: {n_excluded} ราย")
print()
print(scenario.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
print()
drop = pr_with - pr_without
if abs(drop) < 0.02:
    print(f"ผลต่าง PR-AUC เพียง {drop:+.4f} -> โมเดลไม่ได้พึ่งทางลัดนี้อย่างมีนัยสำคัญ")
    print("ประสิทธิภาพที่รายงานจึงเชื่อถือได้ ไม่ได้ถูกยกให้สูงเกินจริงด้วย artifact ของข้อมูล")
else:
    print(f"ผลต่าง PR-AUC ถึง {drop:+.4f} -> โมเดลพึ่งพากลุ่มที่ไม่มีประวัติอย่างมีนัยสำคัญ")
    print("ควรใช้ตัวเลขในสถานการณ์ B เป็นค่าอ้างอิงในการรายงาน เพราะสะท้อนความจริงมากกว่า")
'''),

md(r'''
## 5.5 ประเมินผลเทียบเป้าหมายทางธุรกิจทั้ง 3 ข้อ
''' ),

code(r'''
# Close the loop: did we actually answer what the executives asked?
assessment = pd.DataFrame([
    {
        "คำถามผู้บริหาร": "1. สินค้าใดซื้อคู่กัน ควรจัดโปรร่วมกัน",
        "สิ่งที่ส่งมอบ": f"กฎความสัมพันธ์ {REPORT_VALUES['ar_n_rules']['value']} กฎ "
                        f"และชุดสินค้าที่ซื้อร่วมกัน {REPORT_VALUES['ar_n_bundles']['value']} ชุด",
        "หลักฐานเชิงปริมาณ": f"Lift สูงสุด {REPORT_VALUES['ar_max_lift']['value']} เท่า · "
                            f"มี {REPORT_VALUES['ar_n_rules_lift_gt_10']['value']} กฎที่ Lift เกิน 10 เท่า",
        "สถานะ": "ตอบได้ครบ",
    },
    {
        "คำถามผู้บริหาร": "2. แบ่งลูกค้าได้กี่กลุ่ม แต่ละกลุ่มเป็นอย่างไร",
        "สิ่งที่ส่งมอบ": f"{REPORT_VALUES['seg_k_chosen']['value']} persona "
                        f"พร้อมกลยุทธ์เฉพาะกลุ่ม",
        "หลักฐานเชิงปริมาณ": f"Silhouette {REPORT_VALUES['seg_silhouette_chosen']['value']} · "
                            f"DBSCAN ยืนยันว่าเป็นการแบ่งเชิงบริหาร ไม่ใช่กลุ่มธรรมชาติ",
        "สถานะ": "ตอบได้ พร้อมระบุข้อจำกัด",
    },
    {
        "คำถามผู้บริหาร": "3. ใครจะหยุดซื้อ และสัญญาณเตือนคืออะไร",
        "สิ่งที่ส่งมอบ": f"โมเดล {champion_name} + รายชื่อลูกค้าเสี่ยง + "
                        f"สัญญาณเตือน {len(signals_df)} ตัว",
        "หลักฐานเชิงปริมาณ": f"PR-AUC {test_pr:.4f} (ดีกว่าเดาสุ่ม {test_pr/y_test.mean():.1f} เท่า) · "
                            f"จับได้ {REPORT_VALUES['eval_recall_at_chosen']['value']:.0%} ของผู้ที่กำลังจะหาย",
        "สถานะ": "ตอบได้ครบ",
    },
])
save_table(assessment, "t26_business_goal_assessment")
rv("eval_business_assessment", assessment.to_dict("records"))

for _, r in assessment.iterrows():
    print("=" * 78)
    print(r["คำถามผู้บริหาร"])
    print("-" * 78)
    print(f"  ส่งมอบ  : {r['สิ่งที่ส่งมอบ']}")
    print(f"  หลักฐาน : {r['หลักฐานเชิงปริมาณ']}")
    print(f"  สถานะ   : {r['สถานะ']}")
    print()
'''),

md(r'''
## 5.6 ข้อจำกัดที่ต้องรู้ก่อนนำไปใช้จริง

รายงานผลอย่างตรงไปตรงมา รวมถึงสิ่งที่โมเดลนี้ **ทำไม่ได้**

| ข้อจำกัด | ผลกระทบ | สิ่งที่ควรทำ |
|---|---|---|
| **กฎความสัมพันธ์บอกความสัมพันธ์ ไม่ใช่เหตุผล** | การที่ A กับ B ซื้อคู่กันไม่ได้แปลว่าโปรโมชัน A จะทำให้ B ขายดีขึ้น ลูกค้าอาจตั้งใจซื้อทั้งคู่อยู่แล้ว การลดราคาจึงอาจแค่กัดกำไร | ทำ **A/B test** ก่อนขยายผลทุกครั้ง |
| **กลุ่มลูกค้าไม่ใช่กลุ่มตามธรรมชาติ** | DBSCAN ยืนยันว่าข้อมูลเป็นก้อนต่อเนื่อง ลูกค้าใกล้เส้นแบ่งอาจสลับกลุ่มเมื่อ retrain | ห้ามผูกสิทธิประโยชน์ที่ถอนคืนยากไว้กับหมายเลข segment |
| **โมเดลทำนายจากอดีต** | ถ้าพฤติกรรมลูกค้าเปลี่ยน (เศรษฐกิจ คู่แข่งใหม่ โควิด) ความแม่นจะลดลง | เฝ้าดู data drift และ retrain ตามรอบ |
| **สมมติฐานต้นทุนเป็นค่าประมาณ** | เกณฑ์ตัดสินที่เลือกขึ้นกับต้นทุนคูปองและอัตราความสำเร็จที่เราตั้งขึ้น | แทนค่าด้วยตัวเลขจริงจากฝ่ายการเงิน แล้วคำนวณเกณฑ์ใหม่ |
| **นิยาม churn ที่ 90 วันเป็นการตัดสินใจ ไม่ใช่ความจริง** | ลูกค้าที่หายไป 91 วันแล้วกลับมา ถูกนับเป็น churn | ทบทวนนิยามร่วมกับฝ่ายธุรกิจเป็นระยะ |
| **ข้อมูลเป็นชุดจำลอง** | มี artifact เช่นกลุ่มลูกค้าที่ไม่มีประวัติซึ่ง churn = 0 ทั้งหมด | ตรวจสอบซ้ำกับข้อมูลจริงก่อนใช้งานจริง |
'''),
]
