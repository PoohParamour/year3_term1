# 🏆 Kaggle InClass Competition: Pokémon Legendary Prediction

Welcome to the Week 7 Competition! 
In this competition, your task is to predict whether a Pokémon is **Legendary** (`Is_Legendary = 1`) or not (`0`) based on its numerical stats and image.

## 📂 Dataset Structure
- `data/train.csv`: Contains Pokémon stats and the target variable (`Is_Legendary`).
- `data/test.csv`: Contains Pokémon stats (the target is hidden!).
- `data/images/`: Contains the sprites for all Pokémon in the dataset.
- `data/sample_submission.csv`: An example of what your submission file should look like.

## 🚀 Baseline Model
Check out the `Baseline_Model.ipynb` to see how to build a **Multi-Modal Neural Network** using PyTorch that processes both tabular data (Linear Layers) and images (Flattening) at the same time!

## 🎯 How to Host on Kaggle (For Instructors)
1. Go to **Kaggle -> Host -> InClass Competition**.
2. Upload the `train.csv`, `test.csv`, `sample_submission.csv` (and the `images` folder as a zip archive).
3. Set the evaluation metric to **F1-Score**.
4. Upload the hidden `solution.csv` as the answer key for the test set.
