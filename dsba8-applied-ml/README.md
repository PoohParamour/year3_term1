<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=Applied%20Machine%20Learning&fontSize=42&fontColor=fff&animation=twinkling&fontAlignY=38&desc=DSBA8%20%7C%20King%20Mongkut%27s%20Institute%20of%20Technology%20Ladkrabang&descAlignY=58&descSize=16" width="100%"/>

<p>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
  <img src="https://img.shields.io/badge/Jupyter-FA0F00?style=for-the-badge&logo=jupyter&logoColor=white"/>
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"/>
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white"/>
</p>

<p>
  <img src="https://img.shields.io/badge/Semester-1%2F2569-blueviolet?style=flat-square"/>
  <img src="https://img.shields.io/badge/Weeks-15-success?style=flat-square"/>
  <img src="https://img.shields.io/badge/Language-Python-blue?style=flat-square"/>
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square"/>
</p>

</div>

---

## 📖 About This Course

> **Applied Machine Learning** introduces students to core ML algorithms through hands-on labs using real-world datasets. Each week covers a new topic with practical Python exercises using **scikit-learn**, **pandas**, and visualization libraries.

---

## 📊 Student Progress Dashboard

Students can view their real-time lab completion status and grades on the TA dashboard:

👉 **[Check Your Lab Grades Here](https://webapp-tau-navy.vercel.app)**

---

## 🗓️ Course Schedule

| Week | Date | Topic | Materials |
|:---:|:---:|---|:---:|
| 1 | 30 Jun | K-Means Clustering + Data Preprocessing | [Week 1](./week01-kmeans-clustering/) |
| 2 | 7 Jul | Density-Based Clustering (DBSCAN) | [Week 2](./week02-density-based-clustering/) |
| 3 | 14 Jul | KNN + Linear/Logistic Regression | [Week 3](./week03-knn-and-regression/) |
| 4 | 21 Jul | Decision Trees | [Week 4](./week04-decision-trees/) |
| 5 | 28 Jul | TBD (Syllabus updated) | [Week 5](./week05-linear-logistic-regression/) |
| 6 | 4 Aug | Neural Networks | [Week 6](./week06-neural-networks/) |
| 7 | 11 Aug | Ensemble Classifier (Part 1) | [Week 7](./week07-ensemble-classifier-1/) |
| — | 18 Aug | 📝 **Midterm Exam** (Week 1–6) | — |
| 8 | 25 Aug | Ensemble Classifier (Part 2) | [Week 8](./week08-ensemble-classifier-2/) |
| — | 1 Sep | KMITL EXPO 2026 | — |
| 9 | 8 Sep | Association Rule: Apriori Algorithm | [Week 9](./week09-association-rule-apriori/) |
| 10 | 15 Sep | FPT Algorithm | [Week 10](./week10-fpt-algorithm/) |
| 11 | 22 Sep | Sequential Pattern Discovery | [Week 11](./week11-sequential-pattern-discovery/) |
| 12 | 29 Sep | Prescriptive Analytics + Recommender System | [Week 12](./week12-prescriptive-recommender/) |
| — | 6 Oct | 🧪 **Practical Exam** | — |
| 14 | 13 Oct | MLOps Lifecycle | [Week 14](./week14-mlops-lifecycle/) |
| 15 | 20 Oct | Term Project Presentation | [Week 15](./week15-term-project/) |
| — | 26 Oct | 📋 **Final Exam** | — |

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/E27-25/dsba8-applied-ml.git
cd dsba8-applied-ml
```

### 2. Install dependencies

```bash
pip install pandas numpy scikit-learn matplotlib seaborn yellowbrick jupyter
```

### 3. Launch Jupyter

```bash
jupyter notebook
```

---

## 📁 Repository Structure

<details>
<summary><b>Expand to view full repository tree</b></summary>

```text
dsba8-applied-ml/
│
├── README.md
├── app_ml_syllabus.jpg
│
├── week01-kmeans-clustering/              ← Week 1 (30 Jun) ✅
│   ├── slides/
│   │   └── 01 Intro ML & K-means Clustering.pdf
│   ├── lab-week01/
│   │   └── K-means Clustering.ipynb
│   └── README.md
│
├── week02-density-based-clustering/       ← Week 2 (7 Jul) ✅
│   ├── slides/
│   ├── lab-week02/
│   │   └── DBSCAN Clustering_Synthetic dataset.ipynb
│   ├── homework-week02/
│   └── README.md
├── week03-knn-and-regression/                 ← Week 3 (14 Jul) ✅
│   ├── slides/
│   │   ├── 03 Regression_(Linear,_Logistic).pdf
│   │   └── 04 KNN.pdf
│   ├── lab-week03/
│   │   ├── Classification_KNN_Lab1_WineQuality_(BinaryClass).ipynb
│   │   ├── Classification_KNN_Lab2_Iris_(MultiClass).ipynb
│   │   ├── Regression_(Linear,_Logistic).ipynb
│   │   ├── iris.csv
│   │   └── winequality-red (binary).csv
│   └── README.md
├── week04-decision-trees/                 ← Week 4 (21 Jul) ✅
│   ├── slides/
│   │   └── 05 Decision Tree Classifier.pdf
│   ├── lab-week04/
│   │   ├── DecisionTree_Heart_Failure_Prediction_code.ipynb
│   │   ├── DecisionTree_Iris.ipynb
│   │   └── heart.csv
│   └── README.md
├── week05-linear-logistic-regression/     ← Week 5 (28 Jul)
│   ├── slides/
│   ├── lab-week05/
│   └── README.md
├── week06-neural-networks/                ← Week 6 (4 Aug)
│   ├── slides/
│   ├── lab-week06/
│   └── README.md
├── week07-ensemble-classifier-1/          ← Week 7 (11 Aug)
│   ├── slides/
│   ├── lab-week07/
│   └── README.md
├── week08-ensemble-classifier-2/          ← Week 8 (25 Aug)
│   ├── slides/
│   ├── lab-week08/
│   └── README.md
├── week09-association-rule-apriori/       ← Week 9 (8 Sep)
│   ├── slides/
│   ├── lab-week09/
│   └── README.md
├── week10-fpt-algorithm/                  ← Week 10 (15 Sep)
│   ├── slides/
│   ├── lab-week10/
│   └── README.md
├── week11-sequential-pattern-discovery/   ← Week 11 (22 Sep)
│   ├── slides/
│   ├── lab-week11/
│   └── README.md
├── week12-prescriptive-recommender/       ← Week 12 (29 Sep)
│   ├── slides/
│   ├── lab-week12/
│   └── README.md
├── week14-mlops-lifecycle/                ← Week 14 (13 Oct)
│   ├── slides/
│   ├── lab-week14/
│   └── README.md
└── week15-term-project/                   ← Week 15 (20 Oct)
    ├── slides/
    ├── lab-week15/
    └── README.md
```

</details>

---

## 🧠 Topics Covered

<div align="center">

| 🤖 Unsupervised Learning | 📊 Supervised Learning | ⚙️ Advanced Topics |
|---|---|---|
| K-Means Clustering | K-Nearest Neighbor | Ensemble Methods |
| DBSCAN | Decision Trees | MLOps Lifecycle |
| Association Rules | Linear Regression | Recommender Systems |
| Sequential Patterns | Neural Networks | Data Mining Apps |

</div>

---

## 🛠️ Tools & Libraries

```python
from sklearn.cluster      import KMeans, DBSCAN
from sklearn.datasets     import make_moons
from sklearn.neighbors    import KNeighborsClassifier, NearestNeighbors
from sklearn.tree         import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble     import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics      import silhouette_score, accuracy_score, classification_report
from sklearn.metrics      import davies_bouldin_score, calinski_harabasz_score
from yellowbrick.cluster  import KElbowVisualizer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
```

---

## ✨ Course Highlights

<details>
<summary><b>Week 1 Highlight — K-Means at a Glance</b></summary>

```python
from sklearn.cluster import KMeans
import pandas as pd

df = pd.DataFrame({'age': [42, 18, 23, 49, 37, 51, 40, 20],
                   'eng': [7,   3,  2,  1,  7,  1,  6,  4]})

model = KMeans(n_clusters=3, random_state=42)
model.fit(df)

df['cluster'] = model.labels_
print(df)
print("Centroids:\n", model.cluster_centers_)
print("WCSS:", model.inertia_)
```

> 👉 See **[Week 1 full lab notes](./week01-kmeans-clustering/README.md)** for step-by-step guide with both Lab 1 & Lab 2!

</details>

<details>
<summary><b>Week 2 Highlight — DBSCAN at a Glance</b></summary>

```python
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_moons
import matplotlib.pyplot as plt

# Generate a synthetic "moons" dataset
X, _ = make_moons(n_samples=200, noise=0.05, random_state=42)

# Apply DBSCAN clustering
dbscan = DBSCAN(eps=0.2, min_samples=5)
clusters = dbscan.fit_predict(X)

# Visualizing the results
plt.scatter(X[:, 0], X[:, 1], c=clusters, cmap='viridis')
plt.title('DBSCAN Clustering on Moons Dataset')
plt.show()
```

> 👉 See **[Week 2 full lab notes](./week02-density-based-clustering/README.md)** for step-by-step guide with the synthetic dataset!

</details>

<details>
<summary><b>Week 3 Highlight — KNN & Regression at a Glance</b></summary>

**KNN Classification:**
```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris

# Load Iris dataset & Train KNN Model
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

# Predict & Evaluate
predictions = knn.predict(X_test)
print(f"KNN Accuracy: {accuracy_score(y_test, predictions):.2f}")
```

**Linear Regression:**
```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import numpy as np

# Generate random linear data
X_reg = np.array([[1], [2], [3], [4], [5]])
y_reg = np.array([1.5, 3.1, 4.8, 6.5, 7.9])

# Train Linear Regression Model
lr = LinearRegression()
lr.fit(X_reg, y_reg)

# Predict & Evaluate
print(f"R-squared: {r2_score(y_reg, lr.predict(X_reg)):.3f}")
```

**Logistic Regression:**
```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.datasets import make_classification

# Generate binary classification dataset
X_bin, y_bin = make_classification(n_samples=100, n_features=2, n_redundant=0, random_state=42)

# Train Logistic Regression Model
log_reg = LogisticRegression()
log_reg.fit(X_bin, y_bin)

# Predict & Evaluate
predictions = log_reg.predict(X_bin)
print("Confusion Matrix:\n", confusion_matrix(y_bin, predictions))
```

> 👉 See **[Week 3 full lab notes](./week03-knn-and-regression/README.md)** for detailed data preprocessing and multi-class classification!

</details>

<details>
<summary><b>Week 4 Highlight — Decision Trees at a Glance</b></summary>

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris

# Load Iris dataset
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train Decision Tree Model (ID3-like using Entropy)
dt = DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=42)
dt.fit(X_train, y_train)

# Predict & Evaluate
predictions = dt.predict(X_test)
print(f"Decision Tree Accuracy: {accuracy_score(y_test, predictions):.2f}")
```

> 👉 See **[Week 4 full lab notes](./week04-decision-trees/)** for detailed algorithms (ID3, C4.5, CART) and heart failure prediction!

</details>

---

## 📌 Important Dates

| Event | Date |
|---|---|
| First Class | 30 June 2026 |
| Midterm Exam | 18 August 2026 |
| KMITL EXPO | 1 September 2026 |
| Practical Exam | 6 October 2026 |
| Term Project Presentation | 20 October 2026 |
| Final Exam | 26 October 2026 |

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer&animation=twinkling" width="100%"/>

**Applied Machine Learning · DSBA8 · KMITL**

*Made with ❤️ for students*

</div>
