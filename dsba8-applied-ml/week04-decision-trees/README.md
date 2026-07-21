# 📦 Week 4 — Decision Trees
> **Date:** 21 July | **Topic:** Decision Tree Classification, ID3, C4.5, CART, and Regression Trees

---

## 🎯 Learning Objectives

- Understand the intuition behind **Decision Trees** and how they split data to make predictions.
- Learn the mathematical differences between the **ID3, C4.5, and CART** algorithms.
- Compute **Entropy**, **Information Gain**, and **Gini Impurity** to determine optimal splits.
- Apply Decision Trees for classification tasks (Heart Failure, Iris datasets) and regression tasks.
- Visualize trained Decision Trees to interpret model rules.

---

## 📚 Key Concepts

| Concept | Description |
|---|---|
| **Decision Tree** | A flowchart-like tree structure where internal nodes represent feature tests, branches represent outcomes, and leaf nodes represent class labels. |
| **Entropy** | A measure of impurity, chaos, or randomness in a group of data points. |
| **Information Gain (ID3)** | The expected reduction in entropy caused by partitioning the data using a specific feature. |
| **Gain Ratio (C4.5)** | A modification of Information Gain that reduces its bias towards features with a high number of unique categories. |
| **Gini Impurity (CART)** | A measure of how often a randomly chosen element would be incorrectly labeled if it was labeled randomly according to the class distribution in the node. |

---

## 🛠️ Quick Setup

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, plot_tree
from sklearn.metrics import accuracy_score, classification_report
```

---

## 💡 Lab 1 — Decision Tree on Heart Failure Prediction

In this lab, we use the `heart.csv` dataset to predict whether a patient is at risk of heart failure using a Decision Tree Classifier.

### Step 1: Load and Prepare Data

```python
df = pd.read_csv('heart.csv')
X = df.drop('HeartDisease', axis=1)
y = df['HeartDisease']

# One-Hot Encode categorical variables
X = pd.get_dummies(X, drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

### Step 2: Train & Evaluate CART Model (Gini)

```python
dt = DecisionTreeClassifier(max_depth=3, random_state=42)
dt.fit(X_train, y_train)

y_pred = dt.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
```

---

## 💡 Lab 2 — Decision Tree on Iris Dataset

In this lab, we use the classic Iris dataset to visualize how Decision Trees make splits using Gini Impurity.

> 👉 *See the `DecisionTree_Iris.ipynb` notebook for full code execution and interactive tree visualizations!*

---

## 📁 Files in This Week

| File | Description |
|---|---|
| `lab-week04/DecisionTree_Heart_Failure_Prediction_code.ipynb` | Decision Tree lab for heart failure prediction |
| `lab-week04/DecisionTree_Iris.ipynb` | Decision Tree lab for Iris classification |
| `lab-week04/heart.csv` | Dataset for Heart Failure Prediction |
| `slides/05 Decision Tree Classifier.pdf` | Lecture slides covering Decision Tree theory |
| `TA_session/TARecapSession_Week3_4.ipynb` | TA Recap covering Week 3 & 4 (Custom C4.5, Data-Driven Up-selling) |
| `TA_session/CreditCardCustomer.csv` | Dataset used in the TA Recap |

---

*Applied Machine Learning — DSBA8 | Week 4*
