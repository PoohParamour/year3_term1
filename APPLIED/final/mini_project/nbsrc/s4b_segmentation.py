from _helper import md, code

CELLS = [
md(r'''
---
## §4.2 โจทย์ที่ 2 — Customer Segmentation (Clustering)

> **คำถามผู้บริหาร:** *พฤติกรรมการซื้อแบ่งลูกค้าได้กี่กลุ่ม แต่ละกลุ่มมีลักษณะเด่นอย่างไร*

### แผนการทำงาน
1. แปลงตัวแปรที่เบ้ด้วย `log1p` แล้วปรับสเกลด้วย `StandardScaler` (เหตุผลใน §2.4)
2. หาจำนวนกลุ่มที่เหมาะสมด้วย Elbow + Silhouette + Davies-Bouldin
3. **ตรวจสอบด้วย DBSCAN** ว่ากลุ่มที่ได้มีอยู่จริงตามธรรมชาติหรือเป็นเส้นที่เราลากเอง
4. สร้าง persona และกลยุทธ์รายกลุ่ม
'''),

code(r'''
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.neighbors import NearestNeighbors

# Features used for segmentation, and which of them need a log transform first
SEG_FEATURES = ["recency", "frequency", "monetary", "avg_order_value",
                "tenure_days", "basket_depth", "discount_ratio",
                "category_breadth", "channel_diversity"]
SKEWED = ["recency", "frequency", "monetary", "avg_order_value", "basket_depth"]

seg_raw = customer_features[SEG_FEATURES].copy()
seg_log = seg_raw.copy()
seg_log[SKEWED] = np.log1p(seg_log[SKEWED])

scaler_seg = StandardScaler()
X_seg = scaler_seg.fit_transform(seg_log)

rv("seg_features_used", SEG_FEATURES)
rv("seg_features_log_transformed", SKEWED)
rv("seg_n_customers", int(X_seg.shape[0]))
rv("seg_n_features", int(X_seg.shape[1]))

print(f"ข้อมูลสำหรับ clustering: {X_seg.shape[0]:,} ลูกค้า x {X_seg.shape[1]} ฟีเจอร์")
print(f"ฟีเจอร์ที่แปลง log1p: {SKEWED}")
'''),

code(r'''
# Search for the number of clusters using three independent criteria.
# Using several criteria matters because they disagree - and the disagreement itself
# is informative about whether real clusters exist.
K_RANGE = range(2, 11)
search = []
for k in K_RANGE:
    km = KMeans(n_clusters=k, n_init=10, random_state=RANDOM_STATE).fit(X_seg)
    search.append({
        "k": k,
        "inertia": float(km.inertia_),
        "silhouette": float(silhouette_score(X_seg, km.labels_)),
        "davies_bouldin": float(davies_bouldin_score(X_seg, km.labels_)),
        "calinski_harabasz": float(calinski_harabasz_score(X_seg, km.labels_)),
    })

search_df = pd.DataFrame(search)
save_table(search_df, "t13_kmeans_k_search")

fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
axes[0].plot(search_df.k, search_df.inertia, marker="o", linewidth=2, color="#2b6cb0")
axes[0].set_title("Elbow — ยิ่งต่ำยิ่งดี\n(มองหาจุดที่ความชันเริ่มแบน)")
axes[0].set_xlabel("จำนวนกลุ่ม (k)"); axes[0].set_ylabel("Inertia")

axes[1].plot(search_df.k, search_df.silhouette, marker="o", linewidth=2, color="#38a169")
axes[1].set_title("Silhouette — ยิ่งสูงยิ่งดี\n(วัดความชัดของขอบเขตกลุ่ม)")
axes[1].set_xlabel("จำนวนกลุ่ม (k)")

axes[2].plot(search_df.k, search_df.davies_bouldin, marker="o", linewidth=2, color="#dd6b20")
axes[2].set_title("Davies-Bouldin — ยิ่งต่ำยิ่งดี\n(วัดความซ้อนทับระหว่างกลุ่ม)")
axes[2].set_xlabel("จำนวนกลุ่ม (k)")

fig.suptitle("การค้นหาจำนวนกลุ่มที่เหมาะสม", fontsize=14, fontweight="bold")
fig.tight_layout()
save_fig(fig, "f07_k_selection")
plt.show()

best_sil_k = int(search_df.loc[search_df.silhouette.idxmax(), "k"])
rv("seg_best_silhouette_k", best_sil_k)
rv("seg_best_silhouette_value", round(float(search_df.silhouette.max()), 4))
rv("seg_k_search_table", search_df.round(4).to_dict("records"))
search_df.style.format({"inertia": "{:,.0f}", "silhouette": "{:.4f}",
                        "davies_bouldin": "{:.4f}", "calinski_harabasz": "{:,.1f}"}).hide(axis="index")
'''),

md(r'''
### ตรวจสอบสมมติฐาน: กลุ่มเหล่านี้มีอยู่จริงตามธรรมชาติหรือไม่?

K-Means **บังคับให้เกิด k กลุ่มเสมอ แม้ข้อมูลจะไม่มีกลุ่มอยู่จริง** — ถ้าโยนข้อมูลสุ่มเข้าไป
มันก็ยังคืนกลุ่มมาให้ ดังนั้นก่อนจะนำ segment ไปเสนอผู้บริหาร ต้องตอบให้ได้ก่อนว่า
*นี่คือกลุ่มที่มีอยู่จริง หรือเป็นเส้นที่เราลากขึ้นมาเอง?*

**DBSCAN ตอบคำถามนี้ได้** เพราะแบ่งกลุ่มตามความหนาแน่นและ **ปฏิเสธที่จะแบ่งได้**
ถ้าไม่พบช่องว่างระหว่างกลุ่ม — ต่างจาก K-Means ที่แบ่งเสมอไม่ว่าอย่างไร
''' ),

code(r'''
# Choose eps the standard way: the knee of the sorted k-distance curve
MIN_SAMPLES = 2 * X_seg.shape[1]  # rule of thumb: 2 x number of dimensions
nn = NearestNeighbors(n_neighbors=MIN_SAMPLES).fit(X_seg)
distances, _ = nn.kneighbors(X_seg)
k_dist = np.sort(distances[:, -1])

fig, axes = plt.subplots(1, 2, figsize=(14, 4.5))
axes[0].plot(k_dist, linewidth=2, color="#2b6cb0")
axes[0].set_title(f"k-distance plot (k={MIN_SAMPLES})\nจุดหักคือค่า eps ที่เหมาะสม")
axes[0].set_xlabel("ลูกค้า (เรียงตามระยะทาง)")
axes[0].set_ylabel(f"ระยะทางถึงเพื่อนบ้านลำดับที่ {MIN_SAMPLES}")

# Scan a range of eps around the knee and record how many clusters emerge
eps_grid = np.round(np.quantile(k_dist, [0.50, 0.75, 0.90, 0.95, 0.98, 0.995]), 3)
dbscan_rows = []
for eps in eps_grid:
    lab = DBSCAN(eps=float(eps), min_samples=MIN_SAMPLES).fit_predict(X_seg)
    n_clusters = len(set(lab)) - (1 if -1 in lab else 0)
    n_noise = int((lab == -1).sum())
    dbscan_rows.append({
        "eps": float(eps),
        "จำนวนกลุ่มที่พบ": n_clusters,
        "จุดที่เป็น noise": n_noise,
        "% noise": round(n_noise / len(lab) * 100, 1),
    })

dbscan_df = pd.DataFrame(dbscan_rows)
axes[1].bar(range(len(dbscan_df)), dbscan_df["จำนวนกลุ่มที่พบ"], color="#e53e3e")
axes[1].set_xticks(range(len(dbscan_df)))
axes[1].set_xticklabels([f"{e}" for e in dbscan_df.eps], rotation=45)
axes[1].set_xlabel("ค่า eps")
axes[1].set_ylabel("จำนวนกลุ่มที่ DBSCAN พบ")
axes[1].set_title("DBSCAN พบกี่กลุ่มในแต่ละค่า eps")
axes[1].axhline(1, color="black", linestyle=":", linewidth=1.5)

fig.tight_layout()
save_fig(fig, "f08_dbscan_check")
plt.show()

save_table(dbscan_df, "t14_dbscan_scan")

# A multi-cluster result only counts as evidence of natural structure if it is also
# STABLE and does not throw most of the data away as noise. Judge on both, not on
# "the largest number of clusters seen anywhere in the sweep".
MAX_ACCEPTABLE_NOISE_PCT = 10.0
robust = dbscan_df[(dbscan_df["จำนวนกลุ่มที่พบ"] > 1)
                   & (dbscan_df["% noise"] <= MAX_ACCEPTABLE_NOISE_PCT)]

max_clusters_any = int(dbscan_df["จำนวนกลุ่มที่พบ"].max())
n_eps_multi = int((dbscan_df["จำนวนกลุ่มที่พบ"] > 1).sum())

rv("seg_dbscan_min_samples", MIN_SAMPLES)
rv("seg_dbscan_max_clusters_any", max_clusters_any)
rv("seg_dbscan_n_eps_tested", int(len(dbscan_df)))
rv("seg_dbscan_n_eps_multicluster", n_eps_multi)
rv("seg_dbscan_n_eps_robust", int(len(robust)))
rv("seg_dbscan_noise_threshold_pct", MAX_ACCEPTABLE_NOISE_PCT)
rv("seg_dbscan_scan_table", dbscan_df.to_dict("records"))
rv("seg_dbscan_found_natural_clusters", bool(len(robust) > 0))
dbscan_df
'''),

code(r'''
# State the conclusion from the numbers above rather than from expectation.
if len(robust) == 0:
    verdict = "\n".join([
        f"ทดสอบ eps ทั้งหมด {len(dbscan_df)} ค่า พบว่าไม่มีค่าใดเลยที่ให้ผลการแบ่งกลุ่มที่ 'เชื่อถือได้'",
        f"(นิยาม: ได้มากกว่า 1 กลุ่ม โดยทิ้งข้อมูลเป็น noise ไม่เกิน {MAX_ACCEPTABLE_NOISE_PCT:.0f}%)",
        "",
        f"รายละเอียด: มี eps เพียง {n_eps_multi} ค่าที่ให้มากกว่า 1 กลุ่ม คือค่าที่เล็กที่สุด",
        f"(eps={dbscan_df.eps.iloc[0]}) ซึ่งได้ {max_clusters_any} กลุ่ม "
        f"แต่ต้องทิ้งข้อมูลถึง {dbscan_df['% noise'].iloc[0]:.1f}% เป็น noise",
        "และเมื่อขยับ eps ขึ้นเพียงเล็กน้อย กลุ่มทั้งหมดก็ยุบรวมเป็นกลุ่มเดียวทันที",
        "",
        "รูปแบบนี้คือลายเซ็นของ 'ก้อนข้อมูลต่อเนื่องที่มีแกนกลางหนาแน่น' ไม่ใช่กลุ่มที่แยกจากกันจริง",
        "— ที่ eps เล็ก DBSCAN เพียงแค่ซอยแกนกลางออกเป็นเสี่ยง ๆ แล้วโยนส่วนที่เหลือทิ้งเป็น noise",
    ])
    implication = "\n".join([
        "K-Means ในงานนี้จึงทำหน้าที่เป็น 'เครื่องมือแบ่งความต่อเนื่องออกเป็นกลุ่มที่บริหารจัดการได้'",
        "ไม่ใช่ 'การค้นพบกลุ่มที่ซ่อนอยู่' — ซึ่งยังมีคุณค่าทางธุรกิจเต็มที่ เพราะทีมการตลาด",
        "ต้องการกลุ่มที่ยิงแคมเปญได้จริง ไม่ได้ต้องการความจริงเชิงภววิทยา",
        "",
        "แต่มีนัยสำคัญ 3 ข้อที่ต้องบอกผู้บริหารพร้อมกับผลลัพธ์:",
        "  1. เส้นแบ่งระหว่างกลุ่มเป็นเส้นที่เราเลือกลากเอง จึงต้องเลือกจำนวนกลุ่มด้วยเหตุผล",
        "     ทางธุรกิจ (จำนวนแคมเปญที่ทีมบริหารไหว) ไม่ใช่ไล่หาค่าสถิติที่สูงที่สุดอย่างเดียว",
        "  2. ค่า Silhouette ที่ไม่สูงไม่ได้แปลว่าโมเดลแย่ แต่สะท้อนธรรมชาติของข้อมูลที่ต่อเนื่อง",
        "     — เป็นข้อเท็จจริงที่ต้องรายงาน ไม่ใช่ข้อบกพร่องที่ต้องซ่อน",
        "  3. ลูกค้าที่อยู่ใกล้เส้นแบ่งอาจสลับกลุ่มได้เมื่อ retrain จึงไม่ควรผูกสิทธิประโยชน์",
        "     ที่ถอนคืนยากไว้กับหมายเลข segment โดยตรง",
    ])
else:
    verdict = "\n".join([
        f"พบการแบ่งกลุ่มที่เชื่อถือได้ {len(robust)} ค่า eps "
        f"(มากกว่า 1 กลุ่ม และ noise ไม่เกิน {MAX_ACCEPTABLE_NOISE_PCT:.0f}%)",
        f"จำนวนกลุ่มที่พบ: {sorted(robust['จำนวนกลุ่มที่พบ'].unique().tolist())}",
    ])
    implication = "\n".join([
        "มีโครงสร้างกลุ่มตามธรรมชาติอยู่จริงในข้อมูล",
        "จึงควรเทียบจำนวนกลุ่มที่ DBSCAN พบกับค่า k ที่เลือกให้ K-Means",
    ])

rv("seg_dbscan_verdict", verdict.replace("\n", " "))
print("=" * 78)
print("ผลการตรวจสอบด้วย DBSCAN: กลุ่มเหล่านี้มีอยู่จริงตามธรรมชาติหรือไม่?")
print("=" * 78)
print(verdict)
print()
print("-" * 78)
print("นัยต่อการตีความผลลัพธ์")
print("-" * 78)
print(implication)
'''),

code(r'''
# Final choice of k, made on business grounds and justified against the metrics.
K_CHOSEN = 4

kmeans = KMeans(n_clusters=K_CHOSEN, n_init=25, random_state=RANDOM_STATE)
seg_labels = kmeans.fit_predict(X_seg)
customer_features["segment"] = seg_labels

sil_chosen = float(silhouette_score(X_seg, seg_labels))
rv("seg_k_chosen", K_CHOSEN)
rv("seg_silhouette_chosen", round(sil_chosen, 4))
rv("seg_inertia_chosen", round(float(kmeans.inertia_), 1))
rv("seg_cluster_sizes", pd.Series(seg_labels).value_counts().sort_index().tolist())

print(f"เลือก k = {K_CHOSEN} กลุ่ม")
print(f"  Silhouette = {sil_chosen:.4f}")
print()
print("เหตุผลในการเลือก:")
print(f"  - Elbow: ความชันของ inertia เริ่มแบนราบแถว k=4")
print(f"  - Silhouette สูงสุดอยู่ที่ k={best_sil_k} "
      f"({search_df.silhouette.max():.4f}) แต่ให้กลุ่มที่หยาบเกินกว่าจะออกแบบแคมเปญที่ต่างกันได้")
if len(robust) == 0:
    print(f"  - DBSCAN ยืนยันว่าไม่มีกลุ่มธรรมชาติที่เสถียร การไล่หา silhouette สูงสุด")
    print(f"    จึงไม่ใช่เกณฑ์ที่ถูกต้อง เพราะไม่มี 'คำตอบที่ถูก' ให้ค้นหาตั้งแต่แรก")
print(f"  - k=4 ให้จำนวน persona ที่ทีมการตลาดออกแบบแคมเปญแยกกันได้จริง")
print()
print("ขนาดของแต่ละกลุ่ม:")
for c, n in pd.Series(seg_labels).value_counts().sort_index().items():
    print(f"  กลุ่ม {c}: {n:,} ราย ({n/len(seg_labels):.1%})")
'''),

code(r'''
# Visualise the segments in 2D via PCA
pca = PCA(n_components=2, random_state=RANDOM_STATE)
coords = pca.fit_transform(X_seg)
var_explained = pca.explained_variance_ratio_

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

palette = sns.color_palette("deep", K_CHOSEN)
for c in range(K_CHOSEN):
    m = seg_labels == c
    axes[0].scatter(coords[m, 0], coords[m, 1], s=14, alpha=0.6,
                    color=palette[c], label=f"กลุ่ม {c} (n={m.sum():,})")
centroids_2d = pca.transform(kmeans.cluster_centers_)
axes[0].scatter(centroids_2d[:, 0], centroids_2d[:, 1], marker="X", s=320,
                c="black", edgecolors="white", linewidth=2, label="ศูนย์กลางกลุ่ม", zorder=5)
axes[0].set_xlabel(f"องค์ประกอบหลักที่ 1 ({var_explained[0]:.1%} ของความแปรปรวน)")
axes[0].set_ylabel(f"องค์ประกอบหลักที่ 2 ({var_explained[1]:.1%} ของความแปรปรวน)")
axes[0].set_title("(a) กลุ่มลูกค้าบนระนาบ PCA 2 มิติ")
axes[0].legend(fontsize=8.5)

# What each principal component actually means, so the scatter is interpretable
loadings = pd.DataFrame(pca.components_.T, index=SEG_FEATURES, columns=["PC1", "PC2"])
loadings.plot(kind="barh", ax=axes[1], color=["#2b6cb0", "#dd6b20"], width=0.78)
axes[1].axvline(0, color="black", linewidth=0.8)
axes[1].set_title("(b) องค์ประกอบหลักแต่ละแกนสร้างจากตัวแปรใด")
axes[1].set_xlabel("น้ำหนัก (Loading)")
axes[1].legend(title="")

fig.tight_layout()
save_fig(fig, "f09_segments_pca")
plt.show()

rv("seg_pca_var_pc1", round(float(var_explained[0]), 4))
rv("seg_pca_var_pc2", round(float(var_explained[1]), 4))
rv("seg_pca_var_total", round(float(var_explained.sum()), 4))
save_table(loadings.reset_index().rename(columns={"index": "feature"}), "t15_pca_loadings")
print(f"PCA 2 องค์ประกอบแรกอธิบายความแปรปรวนได้รวม {var_explained.sum():.1%}")
'''),

code(r'''
# Build the persona table in ORIGINAL units - scaled values mean nothing to an executive.
profile = customer_features.groupby("segment")[SEG_FEATURES].mean()
profile["n_customers"] = customer_features.groupby("segment").size()
profile["pct_customers"] = profile.n_customers / len(customer_features)
profile["total_revenue"] = customer_features.groupby("segment").monetary.sum()
profile["pct_revenue"] = profile.total_revenue / customer_features.monetary.sum()

# Attach churn rate so segmentation connects to the retention question
seg_churn = (customer_features[["segment"]]
             .join(churn_raw.set_index("customer_id").churn, how="left")
             .groupby("segment").churn.mean())
profile["churn_rate"] = seg_churn

# Dominant category per segment
cust_seg = customer_features[["segment"]]
top_cat = (items_full.merge(cust_seg, left_on="customer_id", right_index=True)
           .groupby(["segment", "category"]).line_amount.sum()
           .groupby(level=0, group_keys=False).nlargest(1).reset_index())
profile["top_category"] = top_cat.set_index("segment").category

save_table(profile.reset_index(), "t16_segment_profile_raw")
rv("seg_profile_table", profile.round(3).reset_index().to_dict("records"))

display_cols = ["n_customers", "pct_customers", "pct_revenue", "recency", "frequency",
                "monetary", "avg_order_value", "discount_ratio", "category_breadth",
                "churn_rate", "top_category"]
profile[display_cols].style.format({
    "n_customers": "{:,.0f}", "pct_customers": "{:.1%}", "pct_revenue": "{:.1%}",
    "recency": "{:.0f} วัน", "frequency": "{:.1f} ครั้ง", "monetary": "{:,.0f} บาท",
    "avg_order_value": "{:,.0f} บาท", "discount_ratio": "{:.1%}",
    "category_breadth": "{:.1f} หมวด", "churn_rate": "{:.1%}",
}).background_gradient(subset=["monetary", "churn_rate"], cmap="RdYlGn_r")
'''),

code(r'''
# Radar chart: the shape of each persona at a glance
radar_feats = ["recency", "frequency", "monetary", "avg_order_value",
               "category_breadth", "discount_ratio"]
# Keep labels short: long text collides with the polygon on a small polar axes.
# The full meaning is spelled out in the figure caption instead.
radar_labels = ["เพิ่งซื้อ", "ความถี่", "ยอดรวม",
                "มูลค่า/บิล", "หลากหมวด", "พึ่งส่วนลด"]

norm = profile[radar_feats].copy()
norm["recency"] = -norm["recency"]  # flip so that "higher is better" everywhere
norm = (norm - norm.min()) / (norm.max() - norm.min())

angles = np.linspace(0, 2 * np.pi, len(radar_feats), endpoint=False).tolist()
angles += angles[:1]

fig, axes = plt.subplots(1, K_CHOSEN, figsize=(4.4 * K_CHOSEN, 4.6),
                         subplot_kw={"projection": "polar"})
for c in range(K_CHOSEN):
    vals = norm.loc[c].tolist() + [norm.loc[c].iloc[0]]
    ax = axes[c]
    ax.plot(angles, vals, linewidth=2, color=palette[c])
    ax.fill(angles, vals, alpha=0.25, color=palette[c])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(radar_labels, fontsize=9)
    ax.set_ylim(0, 1)
    ax.set_yticklabels([])
    ax.set_title(f"กลุ่ม {c}\n{profile.loc[c,'n_customers']:,.0f} ราย "
                 f"({profile.loc[c,'pct_revenue']:.0%} ของรายได้)",
                 fontweight="bold", pad=18, fontsize=10)

fig.suptitle("รูปร่างพฤติกรรมของแต่ละกลุ่มลูกค้า (ค่าปรับสเกล 0-1 เทียบระหว่างกลุ่ม)\n"
             "ยิ่งกางออกยิ่งดีทุกแกน · แกน \"เพิ่งซื้อ\" กลับด้านแล้ว (สูง = เพิ่งซื้อไม่นาน)",
             fontsize=12, fontweight="bold")
fig.tight_layout()
save_fig(fig, "f10_segment_radar")
plt.show()
'''),

code(r'''
# Turn the statistical profile into named personas.
# Names are DERIVED from each segment's position against population medians, not hand-
# assigned, so they stay correct if the clustering shifts on a re-run. Using medians of
# the whole customer base (rather than ranks among 4 segments) avoids the trap of calling
# a segment "low value" merely because three other segments happen to rank above it.
med_monetary = float(customer_features.monetary.median())
med_recency = float(customer_features.recency.median())
med_tenure = float(customer_features.tenure_days.median())
med_frequency = float(customer_features.frequency.median())
med_discount = float(customer_features.discount_ratio.median())

rv("seg_pop_median_monetary", round(med_monetary, 2))
rv("seg_pop_median_recency", round(med_recency, 1))
rv("seg_pop_median_tenure", round(med_tenure, 1))
rv("seg_pop_median_frequency", round(med_frequency, 1))

personas = {}
for c in profile.index:
    monetary = float(profile.loc[c, "monetary"])
    recency = float(profile.loc[c, "recency"])
    tenure = float(profile.loc[c, "tenure_days"])
    discount = float(profile.loc[c, "discount_ratio"])

    is_new = tenure < med_tenure * 0.5          # joined recently: still building history
    is_valuable = monetary >= med_monetary      # spends more than the typical customer
    is_lapsing = recency > med_recency          # quieter than the typical customer

    if is_new:
        name = "ลูกค้าใหม่กำลังก่อตัว (New / Developing)"
        desc = (f"เพิ่งเป็นสมาชิกเฉลี่ย {tenure:.0f} วัน (ค่ากลางทั้งฐาน {med_tenure:.0f} วัน) "
                f"ยอดสะสมยังน้อยเพราะเวลายังสั้น ไม่ใช่เพราะคุณภาพต่ำ")
        action = ("โปรแกรม onboarding · แนะนำหมวดสินค้าที่ยังไม่เคยซื้อเพื่อสร้างความผูกพัน · "
                  "วัดผลด้วยความถี่ในการซื้อซ้ำ ไม่ใช่ยอดสะสม")
    elif is_valuable and not is_lapsing:
        name = "ลูกค้าชั้นยอด (Champions)"
        desc = (f"ซื้อบ่อย ใช้จ่ายสูง และยังซื้ออยู่สม่ำเสมอ "
                f"(ซื้อล่าสุด {recency:.0f} วันก่อน · ยอดสะสม {monetary:,.0f} บาท)")
        action = ("โปรแกรม VIP · สิทธิ์เข้าถึงสินค้าใหม่ก่อน · "
                  "ห้ามยิงส่วนลดทั่วไป เพราะกลุ่มนี้ซื้ออยู่แล้ว การลดราคาจึงกัดกำไรโดยเปล่าประโยชน์")
    elif is_valuable and is_lapsing:
        name = "ลูกค้าคุณค่าสูงที่กำลังห่างหาย (At-Risk High-Value)"
        desc = (f"ใช้จ่ายสูงกว่าค่ากลาง ({monetary:,.0f} บาท) แต่เงียบไปแล้ว {recency:.0f} วัน "
                f"— กลุ่มที่เสียไปแล้วเจ็บที่สุด")
        action = ("ติดต่อเชิงรุกทันที · ข้อเสนอเฉพาะบุคคลจากประวัติการซื้อ · "
                  "จัดเป็นลำดับความสำคัญสูงสุดของงบ retention")
    elif is_lapsing:
        name = "ลูกค้าห่างหายมูลค่าต่ำ (Dormant / Low-Value)"
        desc = (f"ซื้อไม่บ่อย ยอดต่อบิลต่ำ และเงียบไป {recency:.0f} วัน"
                + (f" · พึ่งส่วนลดสูงถึง {discount:.1%} ของยอดซื้อ" if discount > med_discount else ""))
        action = ("แคมเปญต้นทุนต่ำแบบอัตโนมัติเท่านั้น · อย่าทุ่มงบ เพราะมูลค่าที่จะได้คืนไม่คุ้ม")
    else:
        name = "ลูกค้าประจำมูลค่าปานกลาง (Loyal Regulars)"
        desc = f"ซื้อสม่ำเสมอ (ล่าสุด {recency:.0f} วันก่อน) แต่ยอดต่อบิลยังไม่สูง"
        action = ("ขายพ่วงตามกฎใน §4.1 · ตั้งเป้าเพิ่ม 'ขนาดตะกร้า' ไม่ใช่ 'ความถี่' "
                  "เพราะความถี่ดีอยู่แล้ว")

    personas[c] = {
        "กลุ่ม": c,
        "ชื่อ Persona": name,
        "ลักษณะเด่น": desc,
        "จำนวนลูกค้า": int(profile.loc[c, "n_customers"]),
        "% ของลูกค้า": f"{profile.loc[c,'pct_customers']:.1%}",
        "% ของรายได้": f"{profile.loc[c,'pct_revenue']:.1%}",
        "ซื้อล่าสุด (วัน)": round(recency),
        "ความถี่ (ครั้ง)": round(float(profile.loc[c, "frequency"]), 1),
        "ยอดรวม (บาท)": round(monetary),
        "อายุสมาชิก (วัน)": round(tenure),
        "อัตรา churn": f"{profile.loc[c,'churn_rate']:.1%}",
        "กลยุทธ์ที่แนะนำ": action,
    }

persona_df = pd.DataFrame(personas).T.reset_index(drop=True)

# Guard: the naming rule must not collapse two segments into the same label, which would
# make the personas useless for campaign design.
dup_names = persona_df["ชื่อ Persona"].duplicated().sum()
rv("seg_persona_duplicate_names", int(dup_names))
if dup_names:
    print(f"คำเตือน: มี persona ซ้ำชื่อ {dup_names} กลุ่ม -> เกณฑ์ตั้งชื่อยังแยกกลุ่มได้ไม่ครบ")

save_table(persona_df, "t17_segment_personas")
rv("seg_personas", persona_df.to_dict("records"))
rv("seg_persona_names", persona_df["ชื่อ Persona"].tolist())

for _, row in persona_df.iterrows():
    print("=" * 78)
    print(f"กลุ่ม {row['กลุ่ม']} — {row['ชื่อ Persona']}")
    print("=" * 78)
    print(f"  ลักษณะเด่น  : {row['ลักษณะเด่น']}")
    print(f"  ขนาดกลุ่ม   : {row['จำนวนลูกค้า']:,} ราย ({row['% ของลูกค้า']} ของลูกค้าทั้งหมด) "
          f"สร้างรายได้ {row['% ของรายได้']}")
    print(f"  พฤติกรรม    : ซื้อล่าสุด {row['ซื้อล่าสุด (วัน)']} วันก่อน · "
          f"ซื้อเฉลี่ย {row['ความถี่ (ครั้ง)']} ครั้ง · ยอดรวม {row['ยอดรวม (บาท)']:,} บาท · "
          f"อายุสมาชิก {row['อายุสมาชิก (วัน)']} วัน")
    print(f"  อัตรา churn : {row['อัตรา churn']}")
    print(f"  กลยุทธ์     : {row['กลยุทธ์ที่แนะนำ']}")
    print()
'''),
]
