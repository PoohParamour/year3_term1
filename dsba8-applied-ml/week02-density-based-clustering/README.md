# 📦 Week 2 — Density-Based Clustering (DBSCAN)
> **Date:** 7 July | **Topic:** DBSCAN on Synthetic Dataset (make_moons)

---

## 🎯 Learning Objectives

- Understand how **DBSCAN** works and how it differs from K-Means
- Choose **epsilon (ε)** using the K-distance plot elbow method
- Set **MinPts** based on data dimensionality
- Identify **noise points** (label = `-1`) and count clusters
- Evaluate results with **Silhouette, DBI, CHI, and DBCV**

---

## 📚 Key Concepts

| Concept | Description |
|---|---|
| **Core Point** | Has ≥ `MinPts` neighbors within radius `ε` |
| **Border Point** | Within `ε` of a core point but has < `MinPts` neighbors |
| **Noise Point** | Not a core point, not reachable from any core point → label = `-1` |
| **Epsilon (ε)** | Neighborhood radius. Found using the K-distance plot "elbow" |
| **MinPts** | Min neighbors for a dense region. Rule: `MinPts ≥ dimensions + 1` |
| **DBCV** | Density-Based Clustering Validation — best metric for DBSCAN (handles noise) |

---

## 🛠️ Quick Setup

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.cluster import DBSCAN, KMeans
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
```

---

## 💡 Lab — DBSCAN on make_moons Dataset

### Step 1: Generate Sample Data

```python
X, _ = make_moons(n_samples=200, noise=0.05, random_state=42)

plt.figure(figsize=(10, 6))
plt.scatter(X[:, 0], X[:, 1])
plt.title('Moon-shaped Dataset')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.show()
```

> ⚠️ K-Means cannot cluster this correctly — it assumes spherical clusters. DBSCAN finds any shape.

---

### Step 2: Choose MinPts and Epsilon

**MinPts rule:**
```
MinPts ≥ dimensions + 1
# 2D data → MinPts ≥ 3  (use 5 as a robust default)
```

**Find Epsilon with K-distance Plot:**

```python
from sklearn.neighbors import NearestNeighbors

nn = NearestNeighbors(n_neighbors=5)  # MinPts - 1 = 4, but use MinPts = 5
nbrs = nn.fit(X)
distances, indices = nbrs.kneighbors(X)

# Sort distances to 5th nearest neighbor, smallest to largest
distances = np.sort(distances, axis=0)
distances = distances[:, -1]

plt.figure(figsize=(10, 6))
plt.plot(distances)
plt.title('Kneighbors Distance Graph')
plt.xlabel('Data Points (sorted)')
plt.ylabel('Epsilon value')
plt.show()
```

> 💡 Look for the **"elbow"** — the point where the curve bends sharply. That distance is your `ε`.

---

### Step 3: Run DBSCAN

```python
df = pd.DataFrame(X)

dbs = DBSCAN(eps=0.15, min_samples=5)
dbs.fit(df)

dbscan_labels = dbs.labels_
df['dbscan_labels'] = dbscan_labels
print(df.head())
```

---

### Step 4: Inspect Results

```python
# Count noise points (label = -1)
labels_list = list(df['dbscan_labels'])
n_noise = labels_list.count(-1)
print("Number of noise points:", n_noise)

# Count clusters (exclude -1)
total_labels = np.unique(dbscan_labels)
n_clusters = sum(1 for n in total_labels if n != -1)
print("Number of clusters:", n_clusters)

# Show noise point rows
print(df[df['dbscan_labels'] == -1])
```

---

### Step 5: Visualize DBSCAN Results

```python
plt.figure(figsize=(10, 6))
scatter = plt.scatter(X[:, 0], X[:, 1], c=dbscan_labels, cmap='viridis')
plt.colorbar(scatter)
plt.title('DBSCAN Clustering Results')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.show()
```

---

### Step 6: Clustering Performance Evaluation

```python
X_features = df.iloc[:, :-1]
```

**Silhouette Score** — higher is better (range: -1 to 1):
```python
from sklearn.metrics import silhouette_score
s_score = silhouette_score(X_features, dbscan_labels)
print(f"Silhouette coefficient: {s_score:.3f}")
```

**Davies-Bouldin Index (DBI)** — lower is better (0 is perfect):
```python
from sklearn.metrics import davies_bouldin_score
dbi_score = davies_bouldin_score(X_features, dbscan_labels)
print(f"Davies-Bouldin Index: {dbi_score:.3f}")
```

**Calinski-Harabasz Index (CHI)** — higher is better:
```python
from sklearn.metrics import calinski_harabasz_score
chi_score = calinski_harabasz_score(X_features, dbscan_labels)
print(f"Calinski-Harabasz Index: {chi_score:.3f}")
```

**DBCV** — designed specifically for density-based clustering, handles noise (`-1`) correctly:

```python
# !pip install hdbscan
from hdbscan.validity import validity_index

dbcv_score = validity_index(X_features.values.astype(float), dbscan_labels)
print(f"DBCV Score: {dbcv_score:.3f}")
```

| Score | Interpretation |
|---|---|
| Close to **1.0** | Clusters well-separated with high internal density |
| Close to **0** | Clusters barely separable |
| **Negative** | Poor clustering — density overlap between clusters |

**Per-cluster DBCV breakdown:**

```python
# per_cluster_scores=True returns score for each individual cluster
score, per_cluster = validity_index(
    X_features.values.astype(float),
    dbscan_labels,
    per_cluster_scores=True
)

print(f"Overall DBCV : {score:.3f}")
for i, s in enumerate(per_cluster):
    print(f"  Cluster {i}  : {s:.3f}")
```

Example output:
```
Overall DBCV : 0.419
  Cluster 0  : 0.349
  Cluster 1  : 0.515
```

> 💡 **Overall ≠ simple average** — DBCV uses a **weighted average by cluster size** (excluding noise points):
>
> `Overall DBCV = Σ (|Cᵢ| / |C|) × DBCV(Cᵢ)`
>
> Simple average would be `(0.349 + 0.515) / 2 = 0.432` ≠ `0.419`
> → Cluster 0 has more points (~57.8% of non-noise), so it pulls the overall score closer to 0.349

**Visualize the clusters (indirect DBCV visualization):**

```python
# Color by cluster label to see how well density regions are separated
plt.figure(figsize=(10, 5))
scatter = plt.scatter(X[:, 0], X[:, 1], c=dbscan_labels, cmap='plasma', s=50, alpha=0.8)
plt.colorbar(scatter, label='Cluster (-1 = noise)')
plt.title(f'DBSCAN Clusters — DBCV Score: {dbcv_score:.3f}')
plt.show()
```

> ⚠️ There is no dedicated DBCV plot — the density scatter is the closest visual equivalent. Use the numeric score + per-cluster breakdown for interpretation.

---

### Step 7: Compare DBSCAN vs K-Means

```python
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=2, random_state=42)
kmeans_labels = kmeans.fit_predict(X)

# Visualize K-Means result
plt.figure(figsize=(10, 6))
scatter = plt.scatter(X[:, 0], X[:, 1], c=kmeans_labels, cmap='viridis')
plt.colorbar(scatter)
plt.title('K-Means Clustering Results')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.show()

# Compare metrics
s_km  = silhouette_score(X_features, kmeans_labels)
db_km = davies_bouldin_score(X_features, kmeans_labels)
ch_km = calinski_harabasz_score(X_features, kmeans_labels)

print(f"Silhouette  : DBSCAN={s_score:.3f}  |  K-Means={s_km:.3f}")
print(f"DBI         : DBSCAN={dbi_score:.3f}  |  K-Means={db_km:.3f}")
print(f"CHI         : DBSCAN={chi_score:.3f}  |  K-Means={ch_km:.3f}")
```

| Metric | Goal | DBSCAN | K-Means | Winner |
|---|---|---|---|---|
| **Silhouette Score** | Higher → better | — | — | DBSCAN ✅ |
| **Davies-Bouldin Index** | Lower → better | — | — | DBSCAN ✅ |
| **Calinski-Harabasz** | Higher → better | — | — | Context-dependent |
| **DBCV** | Higher → better | applicable ✅ | N/A ❌ | DBSCAN ✅ |

> 💡 On moon-shaped data, DBSCAN always wins because K-Means forces circular boundaries that don't fit the crescent shape.

---

## 📌 Tips & Common Mistakes

> ⚠️ **DBCV requires `hdbscan`** — install it first with `pip install hdbscan`

> 💡 **Silhouette / DBI / CHI** exclude noise points automatically — but they assume compact clusters, so scores may be misleading for DBSCAN

> 🔍 **K-distance plot** — pick ε at the *sharpest elbow*, not just any bend

> ⚠️ **DBSCAN is sensitive to `ε` and `MinPts`** — always tune both; small changes can merge clusters or create noise

> 📊 **Cluster label = -1 means noise**, not an actual cluster

---

## 📁 Files in This Week

| File | Description |
|---|---|
| `DBSCAN Clustering_Synthetic dataset.ipynb` | Main lab notebook |
| `02 DBSCAN.pdf` | Lecture slides |

---

*Applied Machine Learning — DSBA8 | Week 2*
