# 📦 Week 7 — Neural Networks
> **Date:** 11 August | **Topic:** Multilayer Perceptrons (MLPs), Scikit-Learn vs TensorFlow/Keras

---

## 🎯 Learning Objectives

- Understand the architecture of Artificial Neural Networks (ANNs) and Multilayer Perceptrons (MLPs).
- Learn about activation functions, forward propagation, and backpropagation.
- Implement basic Neural Networks using `scikit-learn` (`MLPClassifier`).
- Implement and train Deep Learning models using `TensorFlow` and `Keras`.
- Compare the ease of use and flexibility between traditional ML libraries and Deep Learning frameworks.

---

## 📚 Key Concepts

| Concept | Description |
|---|---|
| **Neuron / Perceptron** | The basic building block of a Neural Network, which takes inputs, applies weights and a bias, and passes it through an activation function. |
| **Hidden Layers** | Layers of neurons between the input and output layers where the network learns complex patterns. |
| **Activation Function** | Mathematical equations (like ReLU, Sigmoid, Softmax) that determine the output of a neural network node and introduce non-linearity. |
| **Backpropagation** | The algorithm used to train neural networks by calculating the gradient of the loss function and updating the weights backward. |

---

## 🛠️ Quick Setup

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Scikit-Learn MLP
from sklearn.neural_network import MLPClassifier

# TensorFlow / Keras
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
```

---

## 📁 Files in This Week

| File | Description |
|---|---|
| `lab-week07/MultiLayer_Perceptron_s_(MLPs).ipynb` | Introduction to Multilayer Perceptrons |
| `lab-week07/sklearn_MLPClassifier.ipynb` | Implementing MLPs using Scikit-Learn |
| `lab-week07/TensorflowNeuralNetwork_Iris.ipynb` | Implementing Deep Learning models with TensorFlow/Keras on the Iris dataset |
| `slides/07 Neural Networks.pdf` | Lecture slides covering Neural Network theory and architecture |

---

*Applied Machine Learning — DSBA8 | Week 7*
