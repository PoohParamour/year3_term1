from _helper import md, code

CELLS = [
md(r'''
---
## §4.3 โจทย์ที่ 3 — Customer Retention (Churn Prediction)

> **คำถามผู้บริหาร:** *ลูกค้ารายใดมีแนวโน้มจะหยุดซื้อ และพฤติกรรมใดเป็นสัญญาณเตือน*

### กลยุทธ์: ใช้โมเดล 2 บทบาท

คำถามนี้ซ่อนคำถาม 2 ข้อที่ต้องการคุณสมบัติคนละแบบ จึงใช้โมเดลคนละกลุ่มตอบ

| บทบาท | ตอบคำถามว่า | ต้องการคุณสมบัติ |
|---|---|---|
| **แชมป์** | *ลูกค้ารายใด* จะหยุดซื้อ | จัดอันดับความเสี่ยงได้แม่นที่สุด |
| **ผู้อธิบาย** | *พฤติกรรมใด* เป็นสัญญาณเตือน | อธิบายเป็นภาษาที่ผู้บริหารเข้าใจได้ |

เราจะเทียบโมเดลทั้ง 9 ตัวที่เรียนมาด้วยเงื่อนไขเดียวกัน แล้วเลือกตัวแทนของแต่ละบทบาทจากผลจริง
'''),

code(r'''
from sklearn.model_selection import (train_test_split, StratifiedKFold,
                                     cross_validate, RandomizedSearchCV)
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import (RandomForestClassifier, ExtraTreesClassifier,
                              AdaBoostClassifier, GradientBoostingClassifier,
                              StackingClassifier)
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (roc_auc_score, average_precision_score, roc_curve,
                             precision_recall_curve, confusion_matrix,
                             classification_report, f1_score, recall_score,
                             precision_score, accuracy_score)
from sklearn.inspection import permutation_importance
from xgboost import XGBClassifier

X_all = modeling_df[FEATURE_COLS].copy()
y_all = modeling_df[TARGET].copy()

# Hold out a test set that no model sees until §5. Stratified to preserve the churn rate.
X_train, X_test, y_train, y_test = train_test_split(
    X_all, y_all, test_size=0.2, stratify=y_all, random_state=RANDOM_STATE)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

rv("churn_n_train", int(len(X_train)))
rv("churn_n_test", int(len(X_test)))
rv("churn_train_churn_rate", round(float(y_train.mean()), 4))
rv("churn_test_churn_rate", round(float(y_test.mean()), 4))
rv("churn_cv_folds", 5)

print(f"ชุดฝึก  : {len(X_train):,} ราย (อัตรา churn {y_train.mean():.1%})")
print(f"ชุดทดสอบ: {len(X_test):,} ราย (อัตรา churn {y_test.mean():.1%})")
print(f"ตรวจสอบไขว้: Stratified {cv.get_n_splits()}-Fold บนชุดฝึกเท่านั้น")
print()
print("ชุดทดสอบจะไม่ถูกแตะจนกว่าจะถึง §5 เพื่อให้ผลประเมินสะท้อนความสามารถจริง")
'''),

code(r'''
# One preprocessing pipeline shared by every model, so the comparison is fair:
# any difference in score comes from the algorithm, not from different preparation.
def make_preprocessor(scale=True):
    numeric_steps = [("impute", SimpleImputer(strategy="median"))]
    if scale:
        numeric_steps.append(("scale", StandardScaler()))
    return ColumnTransformer([
        ("num", Pipeline(numeric_steps), NUMERIC + ["has_purchase_history"]),
        ("cat", Pipeline([
            ("impute", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]), CATEGORICAL),
    ])


# Class imbalance is handled with class weights rather than synthetic oversampling:
# these predictions are used to send coupons to real people, so learning from
# fabricated customers is a risk we do not need to take.
pos_weight = float((y_train == 0).sum() / (y_train == 1).sum())
rv("churn_scale_pos_weight", round(pos_weight, 3))

MODELS = {
    "Logistic Regression": (LogisticRegression(max_iter=3000, class_weight="balanced",
                                               random_state=RANDOM_STATE), True),
    "K-Nearest Neighbors": (KNeighborsClassifier(n_neighbors=15), True),
    "Decision Tree": (DecisionTreeClassifier(max_depth=5, class_weight="balanced",
                                             random_state=RANDOM_STATE), False),
    "Random Forest": (RandomForestClassifier(n_estimators=300, class_weight="balanced",
                                             random_state=RANDOM_STATE, n_jobs=-1), False),
    "Extra Trees": (ExtraTreesClassifier(n_estimators=300, class_weight="balanced",
                                         random_state=RANDOM_STATE, n_jobs=-1), False),
    "AdaBoost": (AdaBoostClassifier(random_state=RANDOM_STATE), False),
    "Gradient Boosting": (GradientBoostingClassifier(random_state=RANDOM_STATE), False),
    "XGBoost": (XGBClassifier(n_estimators=300, learning_rate=0.1, max_depth=4,
                              scale_pos_weight=pos_weight, eval_metric="logloss",
                              random_state=RANDOM_STATE, n_jobs=-1), False),
    "Neural Network (MLP)": (MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=1000,
                                           random_state=RANDOM_STATE), True),
}

rv("churn_models_compared", list(MODELS.keys()))
print(f"เตรียมเทียบโมเดล {len(MODELS)} ตัวด้วยเงื่อนไขเดียวกัน:")
for i, name in enumerate(MODELS, 1):
    print(f"  {i}. {name}")
print()
print(f"อัตราส่วนถ่วงน้ำหนักคลาส (scale_pos_weight) = {pos_weight:.2f}")
'''),

code(r'''
# Compare every model under identical cross-validation
SCORING = ["roc_auc", "average_precision", "recall", "precision", "f1", "accuracy"]

results = []
fitted_pipelines = {}
for name, (estimator, needs_scaling) in MODELS.items():
    pipe = Pipeline([("prep", make_preprocessor(scale=needs_scaling)),
                     ("model", estimator)])
    t0 = time.perf_counter()
    scores = cross_validate(pipe, X_train, y_train, cv=cv, scoring=SCORING, n_jobs=-1)
    elapsed = time.perf_counter() - t0

    row = {"model": name}
    for s in SCORING:
        row[s] = float(scores[f"test_{s}"].mean())
        row[f"{s}_std"] = float(scores[f"test_{s}"].std())
    row["fit_time_sec"] = elapsed
    results.append(row)
    fitted_pipelines[name] = pipe
    print(f"  {name:<22} PR-AUC={row['average_precision']:.4f}  "
          f"ROC-AUC={row['roc_auc']:.4f}  Recall={row['recall']:.4f}  ({elapsed:.1f}s)")

cv_results = (pd.DataFrame(results)
              .sort_values("average_precision", ascending=False)
              .reset_index(drop=True))
save_table(cv_results, "t18_model_comparison_cv")
rv("churn_cv_results", cv_results.round(4).to_dict("records"))
print()
print("เรียงลำดับตาม PR-AUC เสร็จแล้ว")
'''),

code(r'''
# Present the comparison in report-ready form
disp = cv_results[["model", "roc_auc", "average_precision", "recall",
                   "precision", "f1", "accuracy", "fit_time_sec"]].copy()
disp.columns = ["โมเดล", "ROC-AUC", "PR-AUC", "Recall", "Precision", "F1",
                "Accuracy", "เวลา (วินาที)"]
disp.insert(0, "อันดับ", range(1, len(disp) + 1))

best_model_name = cv_results.model.iloc[0]
best_prauc = float(cv_results.average_precision.iloc[0])
rv("churn_best_model_cv", best_model_name)
rv("churn_best_prauc_cv", round(best_prauc, 4))
rv("churn_best_rocauc_cv", round(float(cv_results.roc_auc.iloc[0]), 4))

# Which model is best at RECALL specifically? Often not the same one - worth surfacing.
best_recall_row = cv_results.loc[cv_results.recall.idxmax()]
rv("churn_best_recall_model", str(best_recall_row.model))
rv("churn_best_recall_value", round(float(best_recall_row.recall), 4))

print(f"โมเดลที่ PR-AUC สูงสุด: {best_model_name} ({best_prauc:.4f})")
print(f"โมเดลที่ Recall สูงสุด: {best_recall_row.model} ({best_recall_row.recall:.4f})")
print()
print("ข้อสังเกต: สองอันนี้มักไม่ใช่โมเดลเดียวกัน เพราะ Recall ที่วัดตรงนี้ใช้เกณฑ์ 0.5")
print("           ซึ่งไม่ใช่เกณฑ์ที่เหมาะกับธุรกิจ — จะปรับเกณฑ์ตามต้นทุนจริงในขั้นถัดไป")

disp.style.format({"ROC-AUC": "{:.4f}", "PR-AUC": "{:.4f}", "Recall": "{:.4f}",
                   "Precision": "{:.4f}", "F1": "{:.4f}", "Accuracy": "{:.4f}",
                   "เวลา (วินาที)": "{:.1f}"}).background_gradient(
    subset=["PR-AUC", "ROC-AUC"], cmap="Greens").hide(axis="index")
'''),

code(r'''
fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))

order = cv_results.sort_values("average_precision")
ypos = np.arange(len(order))
axes[0].barh(ypos - 0.2, order.average_precision, height=0.4,
             xerr=order.average_precision_std, color="#2b6cb0", label="PR-AUC")
axes[0].barh(ypos + 0.2, order.roc_auc, height=0.4,
             xerr=order.roc_auc_std, color="#90cdf4", label="ROC-AUC")
axes[0].set_yticks(ypos)
axes[0].set_yticklabels(order.model, fontsize=9)
axes[0].axvline(float(y_train.mean()), color="crimson", linestyle="--", linewidth=1.5,
                label=f"PR-AUC ของการเดาสุ่ม = {y_train.mean():.3f}")
axes[0].set_xlabel("คะแนน (แถบคือส่วนเบี่ยงเบนมาตรฐานจาก 5 folds)")
axes[0].set_title("(a) เปรียบเทียบความสามารถของทุกโมเดล")
axes[0].legend(loc="lower right", fontsize=8.5)

axes[1].scatter(cv_results.fit_time_sec, cv_results.average_precision,
                s=110, color="#dd6b20", edgecolors="white", linewidth=1.5, zorder=3)
for _, r in cv_results.iterrows():
    axes[1].annotate(r.model, (r.fit_time_sec, r.average_precision),
                     fontsize=8, xytext=(6, 4), textcoords="offset points")
axes[1].set_xscale("log")
axes[1].set_xlabel("เวลาในการฝึก (วินาที, สเกลลอการิทึม)")
axes[1].set_ylabel("PR-AUC")
axes[1].set_title("(b) ความแม่นยำเทียบกับต้นทุนการคำนวณ")

fig.tight_layout()
save_fig(fig, "f11_model_comparison")
plt.show()
'''),

md(r'''
### ปรับจูนพารามิเตอร์ (Hyperparameter Tuning)

จูนเฉพาะ 3 โมเดลที่ทำคะแนนดีที่สุด เพราะการจูนทุกตัวใช้เวลาโดยไม่เพิ่มคุณค่า
ใช้ `RandomizedSearchCV` ซึ่งสุ่มตัวอย่างจากพื้นที่พารามิเตอร์ — คุ้มกว่า Grid Search
เมื่อพารามิเตอร์บางตัวไม่มีผลมากนัก และให้ผลใกล้เคียงกันในเวลาที่น้อยกว่ามาก
''' ),

code(r'''
# Tune only the top performers; scoring on average_precision to stay aligned with
# the metric that matters for an imbalanced problem.
PARAM_SPACES = {
    "Gradient Boosting": {
        "model__n_estimators": [100, 200, 300, 400],
        "model__learning_rate": [0.03, 0.05, 0.1, 0.15],
        "model__max_depth": [2, 3, 4, 5],
        "model__subsample": [0.8, 0.9, 1.0],
    },
    "XGBoost": {
        "model__n_estimators": [200, 300, 400, 500],
        "model__learning_rate": [0.03, 0.05, 0.1],
        "model__max_depth": [3, 4, 5, 6],
        "model__subsample": [0.7, 0.85, 1.0],
        "model__colsample_bytree": [0.7, 0.85, 1.0],
    },
    "Random Forest": {
        "model__n_estimators": [200, 300, 500],
        "model__max_depth": [None, 8, 12, 16],
        "model__min_samples_leaf": [1, 2, 4, 8],
        "model__max_features": ["sqrt", "log2", 0.5],
    },
    "Extra Trees": {
        "model__n_estimators": [200, 300, 500],
        "model__max_depth": [None, 8, 12, 16],
        "model__min_samples_leaf": [1, 2, 4, 8],
    },
}

top3 = [m for m in cv_results.model.head(3) if m in PARAM_SPACES]
tuned = {}
tuning_rows = []

for name in top3:
    base_est, needs_scaling = MODELS[name]
    pipe = Pipeline([("prep", make_preprocessor(scale=needs_scaling)),
                     ("model", base_est)])
    search = RandomizedSearchCV(pipe, PARAM_SPACES[name], n_iter=25, cv=cv,
                                scoring="average_precision", n_jobs=-1,
                                random_state=RANDOM_STATE)
    t0 = time.perf_counter()
    search.fit(X_train, y_train)
    elapsed = time.perf_counter() - t0

    before = float(cv_results.loc[cv_results.model == name, "average_precision"].iloc[0])
    tuned[name] = search.best_estimator_
    tuning_rows.append({
        "โมเดล": name,
        "PR-AUC ก่อนจูน": round(before, 4),
        "PR-AUC หลังจูน": round(float(search.best_score_), 4),
        "เปลี่ยนแปลง": round(float(search.best_score_) - before, 4),
        "เวลาที่ใช้ (วินาที)": round(elapsed, 1),
    })
    print(f"{name}: {before:.4f} -> {search.best_score_:.4f} "
          f"({search.best_score_ - before:+.4f}) ใน {elapsed:.0f} วินาที")
    print(f"  พารามิเตอร์ที่ดีที่สุด: "
          f"{ {k.replace('model__',''): v for k, v in search.best_params_.items()} }")

tuning_df = pd.DataFrame(tuning_rows)
save_table(tuning_df, "t19_tuning_results")
rv("churn_tuned_models", top3)
rv("churn_tuning_results", tuning_df.to_dict("records"))
tuning_df
'''),

code(r'''
# Stacking: can combining the tuned models beat the best single one?
# Report the answer honestly either way - a negative result is still a result.
stack_bases = [(n.lower().replace(" ", "_")[:12], tuned[n]) for n in top3]
stacking = StackingClassifier(
    estimators=stack_bases,
    final_estimator=LogisticRegression(max_iter=3000, class_weight="balanced",
                                       random_state=RANDOM_STATE),
    cv=cv, n_jobs=-1)

t0 = time.perf_counter()
stack_scores = cross_validate(stacking, X_train, y_train, cv=cv,
                              scoring=SCORING, n_jobs=-1)
stack_time = time.perf_counter() - t0
stack_prauc = float(stack_scores["test_average_precision"].mean())

best_tuned_name = max(tuned, key=lambda n: tuning_df.set_index("โมเดล").loc[n, "PR-AUC หลังจูน"])
best_tuned_prauc = float(tuning_df.set_index("โมเดล").loc[best_tuned_name, "PR-AUC หลังจูน"])
stack_gain = stack_prauc - best_tuned_prauc
stack_helps = stack_gain > 0.005  # meaningful improvement threshold

rv("churn_stacking_prauc", round(stack_prauc, 4))
rv("churn_stacking_gain", round(stack_gain, 4))
rv("churn_stacking_helps", bool(stack_helps))
rv("churn_stacking_time_sec", round(stack_time, 1))
rv("churn_best_tuned_model", best_tuned_name)
rv("churn_best_tuned_prauc", round(best_tuned_prauc, 4))

print(f"โมเดลเดี่ยวที่ดีที่สุดหลังจูน: {best_tuned_name} — PR-AUC {best_tuned_prauc:.4f}")
print(f"Stacking ({len(stack_bases)} โมเดล)            — PR-AUC {stack_prauc:.4f}")
print(f"ส่วนต่าง: {stack_gain:+.4f}   (ใช้เวลาฝึก {stack_time:.0f} วินาที)")
print()
if stack_helps:
    print("สรุป: Stacking ช่วยได้จริงอย่างมีนัยสำคัญ -> เลือก Stacking เป็นแชมป์")
else:
    print("สรุป: Stacking ไม่ได้ช่วยอย่างมีนัยสำคัญ (เกณฑ์ที่ตั้งไว้คือต้องดีขึ้นเกิน 0.005)")
    print()
    print("เหตุผลที่อธิบายได้: โมเดลฐานทั้งสามเป็นตระกูล tree-based ที่เรียนรู้จาก")
    print("ฟีเจอร์ชุดเดียวกัน จึงทำนายผิดที่ 'ลูกค้ากลุ่มเดียวกัน' — Stacking ได้ประโยชน์")
    print("เมื่อโมเดลฐานผิดคนละแบบและมาเติมเต็มกัน ซึ่งไม่ใช่กรณีนี้")
    print()
    print("-> เลือกโมเดลเดี่ยวเป็นแชมป์ เพราะได้ความแม่นเท่ากันแต่เร็วกว่า")
    print("   อธิบายง่ายกว่า และดูแลรักษาในระบบจริงง่ายกว่ามาก")
'''),

code(r'''
# Lock in the champion (best predictive ranking) and the explainers (interpretability)
if stack_helps:
    champion_name = "Stacking Ensemble"
    champion = stacking
else:
    champion_name = best_tuned_name
    champion = tuned[best_tuned_name]

champion.fit(X_train, y_train)

# Explainers are trained on the same data so their story matches the champion's world
explainer_lr = Pipeline([("prep", make_preprocessor(scale=True)),
                         ("model", LogisticRegression(max_iter=3000,
                                                      class_weight="balanced",
                                                      random_state=RANDOM_STATE))])
explainer_lr.fit(X_train, y_train)

explainer_dt = Pipeline([("prep", make_preprocessor(scale=False)),
                         ("model", DecisionTreeClassifier(max_depth=4,
                                                          class_weight="balanced",
                                                          min_samples_leaf=30,
                                                          random_state=RANDOM_STATE))])
explainer_dt.fit(X_train, y_train)

rv("churn_champion_model", champion_name)
print(f"แชมป์ (ใช้ทำนาย)     : {champion_name}")
print(f"ผู้อธิบาย (ใช้ตีความ) : Logistic Regression + Decision Tree (max_depth=4)")
print()
print("ทั้งสามโมเดลฝึกบนข้อมูลชุดเดียวกัน เพื่อให้คำอธิบายสอดคล้องกับตัวที่ใช้ทำนายจริง")
'''),
]
