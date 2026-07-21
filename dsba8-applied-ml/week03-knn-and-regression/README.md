# 📦 Week 3 — K-Nearest Neighbor & Regression
> **Date:** 14 July | **Topic:** KNN Classification, Linear Regression, and Logistic Regression

---

## 🎯 Learning Objectives

- Understand how the **K-Nearest Neighbors (KNN)** algorithm works for classification.
- Evaluate KNN models on binary and multi-class datasets using confusion matrices and accuracy.
- Learn the foundations of **Linear Regression** for predicting continuous outcomes.
- Learn how **Logistic Regression** is used for classification problems by mapping predictions to probabilities using the sigmoid function.

---

## 📚 Key Concepts

| Concept | Description |
|---|---|
| **K-Nearest Neighbors (KNN)** | A non-parametric method used for classification and regression. It assigns a class based on the majority vote of the 'K' closest data points. |
| **Distance Metrics** | Measures like Euclidean, Manhattan, or Minkowski distance used to find the 'nearest' neighbors. |
| **Linear Regression** | Models the relationship between dependent and independent variables by fitting a linear equation to observed data (finding the line of best fit). |
| **Logistic Regression** | Used for binary classification. It models the probability that an instance belongs to a specific class. |
| **Binary vs Multi-Class** | Binary classification has 2 possible outcomes (e.g., Good vs Bad Wine). Multi-class has >2 outcomes (e.g., Iris Setosa vs Versicolor vs Virginica). |

---

## 🛠️ Quick Setup

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
```

---

## 💡 Lab 1 — KNN on Wine Quality (Binary Class)

In this lab, we use the `winequality-red (binary).csv` dataset to classify wine quality as either "good" or "bad".

### Step 1: Load and Prepare Data

```python
df = pd.read_csv('winequality-red (binary).csv')
X = df.drop('quality', axis=1)
y = df['quality']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

### Step 2: Train KNN Model

```python
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)
```

### Step 3: Evaluate

```python
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
```

---

## 💡 Lab 2 — KNN on Iris Dataset (Multi-Class)

In this lab, we use the `iris.csv` dataset to classify irises into one of three species.

```python
# The workflow is identical, but the output targets 3 distinct classes
df_iris = pd.read_csv('iris.csv')
X_iris = df_iris.drop('Species', axis=1)
y_iris = df_iris['Species']

X_train_i, X_test_i, y_train_i, y_test_i = train_test_split(X_iris, y_iris, test_size=0.2, random_state=42)

knn_iris = KNeighborsClassifier(n_neighbors=3)
knn_iris.fit(X_train_i, y_train_i)
y_pred_i = knn_iris.predict(X_test_i)

print(f"Accuracy: {accuracy_score(y_test_i, y_pred_i):.2f}")
```

---

## 💡 Lab 3 — Linear & Logistic Regression

This lab covers continuous prediction and binary probability mapping. 

> 👉 *See the `Regression_(Linear,_Logistic).ipynb` notebook for full code execution and visualizations!*

---

## 📁 Files in This Week

| File | Description |
|---|---|
| `Classification_KNN_Lab1_WineQuality_(BinaryClass).ipynb` | Binary classification lab using KNN |
| `Classification_KNN_Lab2_Iris_(MultiClass).ipynb` | Multi-class classification lab using KNN |
| `Regression_(Linear,_Logistic).ipynb` | Linear & Logistic Regression lab |
| `winequality-red (binary).csv` | Dataset for Lab 1 |
| `iris.csv` | Dataset for Lab 2 |
| `04 KNN.pdf` | Lecture slides (KNN) |
| `03 Regression_(Linear,_Logistic).pdf` | Lecture slides (Regression) |

---

*Applied Machine Learning — DSBA8 | Week 3*
