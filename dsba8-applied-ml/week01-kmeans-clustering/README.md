# 📦 Week 1 — K-Means Clustering
> **Date:** 30 June | **Topic:** Data Preprocessing & K-Means Clustering

---

## 🎯 Learning Objectives

- Understand the concept of **clustering** and unsupervised learning
- Apply **K-Means** algorithm to segment data into groups
- Use the **Elbow Method** to find the optimal number of clusters
- Evaluate clustering quality using **WCSS / Inertia**

---

## 📚 Key Concepts

| Concept | Description |
|---|---|
| **Clustering** | Grouping similar data points together without labels |
| **Centroid** | The center point of each cluster |
| **WCSS / Inertia** | Within-Cluster Sum of Squares — measures how tight clusters are |
| **Elbow Method** | Plot WCSS vs. K to find the "elbow" (optimal K) |
| **Silhouette Score** | Measures how similar a point is to its own cluster vs. others (range: -1 to 1) |

---

## 🛠️ Quick Setup

```python
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from yellowbrick.cluster import KElbowVisualizer
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
```

---

## 💡 Lab 1 — Customer Segmentation (Example Code)

### Step 1: Create the Dataset

```python
import pandas as pd
from sklearn.cluster import KMeans

data = {
    'age': [42, 18, 23, 49, 37, 51, 40, 20],
    'eng': [7,   3,  2,  1,  7,  1,  6,  4]
}
df = pd.DataFrame(data)
print(df)
```

### Step 2: Build & Fit the K-Means Model

```python
# Create K-Means model with k=3 clusters
model = KMeans(n_clusters=3, random_state=42)
model.fit(df)
```

### Step 3: Inspect the Results

```python
# Cluster centroids (center of each group)
print("Centroids:\n", model.cluster_centers_)

# Which cluster each data point belongs to
print("Labels:", model.labels_)
```

### Step 4: Add Labels Back to DataFrame

```python
df['cluster'] = model.labels_
print(df)
```

### Step 5: (Optional) Visualize

```python
import matplotlib.pyplot as plt

colors = ['red', 'blue', 'green']
for cluster_id in range(3):
    subset = df[df['cluster'] == cluster_id]
    plt.scatter(subset['age'], subset['eng'],
                label=f'Cluster {cluster_id}', color=colors[cluster_id], s=100)

# Plot centroids
centroids = model.cluster_centers_
plt.scatter(centroids[:, 0], centroids[:, 1],
            marker='X', s=200, color='black', label='Centroids', zorder=5)

plt.xlabel('Age')
plt.ylabel('Engagement')
plt.title('K-Means Customer Segmentation')
plt.legend()
plt.show()
```

### Step 6: Check WCSS (Inertia)

```python
print("WCSS (Inertia):", model.inertia_)
```

---

## 💡 Lab 2 — Grains Clustering (with Elbow Method)

### Dataset

```python
data = {
    'sugar':   [6, 8, 5, 0, 8, 10, 14, 8, 6, 5, 12, 1, 9, 7, 13],
    'cal':     [70, 120, 70, 50, 110, 110, 110, 130, 90, 90, 120, 110, 120, 110, 110],
    'protein': [4, 3, 4, 4, 2, 2, 2, 3, 2, 3, 1, 6, 1, 3, 1],
    'fat':     [1, 5, 1, 0, 2, 2, 0, 2, 1, 0, 2, 2, 3, 2, 1],
    'sodium':  [130, 15, 260, 140, 200, 180, 125, 210, 200, 210, 220, 290, 210, 140, 180]
}
X = pd.DataFrame(data)
```

### Find Optimal K with Elbow Method

```python
from yellowbrick.cluster import KElbowVisualizer

model = KMeans(random_state=42)
visualizer = KElbowVisualizer(model, k=(2, 8))
visualizer.fit(X)
visualizer.show()

optimal_k = visualizer.elbow_value_
print(f"Optimal K: {optimal_k}")
```

### Final Clustering

```python
final_model = KMeans(n_clusters=optimal_k, random_state=42)
final_model.fit(X)
X['cluster'] = final_model.labels_
```

### Performance Metrics

```python
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

labels = final_model.labels_

sil   = silhouette_score(X.drop('cluster', axis=1), labels)
dbi   = davies_bouldin_score(X.drop('cluster', axis=1), labels)
chi   = calinski_harabasz_score(X.drop('cluster', axis=1), labels)

print(f"Silhouette Score  : {sil:.4f}  (higher = better, max 1.0)")
print(f"Davies-Bouldin    : {dbi:.4f}  (lower  = better, min 0.0)")
print(f"Calinski-Harabasz : {chi:.4f}  (higher = better)")
```

### Compare K Values

```python
results = []

for k in range(2, 8):
    km = KMeans(n_clusters=k, random_state=42)
    km.fit(X.drop('cluster', axis=1) if 'cluster' in X.columns else X)
    lbl = km.labels_
    results.append({
        'k': k,
        'silhouette': silhouette_score(X.drop('cluster', axis=1), lbl),
        'dbi': davies_bouldin_score(X.drop('cluster', axis=1), lbl),
        'chi': calinski_harabasz_score(X.drop('cluster', axis=1), lbl),
    })

print(pd.DataFrame(results).set_index('k'))
```

---

## 📌 Tips & Common Mistakes

> ⚠️ **K-Means requires numeric features only** — encode categorical variables first!

> 💡 **Scale your data** before clustering if features have very different ranges (use `StandardScaler`)

> 🔁 **Random initialization matters** — use `random_state=42` for reproducibility

> 📊 **Silhouette Score > 0.5** is generally considered a good clustering result

---

## 📁 Files in This Week

| File | Description |
|---|---|
| `K-means Clustering.ipynb` | Main lab notebook |
| `01 Intro ML & K-means Clustering.pdf` | Lecture slides |

---

*Applied Machine Learning — DSBA8 | Week 1*
