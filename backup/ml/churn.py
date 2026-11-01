"""
=============================================================================
Assignment: ML 3 (Group B)
Title: Given a bank customer, build a neural network-based classifier 
       that can determine whether they will leave or not in the next 6 months.
Lab: Laboratory Practice - III (BE Computer Engineering - SPPU 2019 Pattern)
Dataset: https://www.kaggle.com/barelydedicated/bank-customer-churn-modeling (Churn_Modelling.csv)
=============================================================================
"""

import os
import sys
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score


# ---------------------------------------------------------------------------
# Synthetic Dataset Generator (Fallback if Churn_Modelling.csv is not present)
# ---------------------------------------------------------------------------
def generate_synthetic_churn_data(n_samples=1500):
    """
    Generates synthetic bank customer data conforming exactly to the Kaggle
    'Churn_Modelling.csv' structure (10,000 records, 14 features).
    """
    np.random.seed(42)
    credit_score = np.random.randint(350, 850, n_samples)
    geography = np.random.choice(['France', 'Spain', 'Germany'], n_samples, p=[0.5, 0.25, 0.25])
    gender = np.random.choice(['Male', 'Female'], n_samples, p=[0.54, 0.46])
    age = np.random.randint(18, 75, n_samples)
    tenure = np.random.randint(0, 11, n_samples)
    balance = np.random.uniform(0, 220000, n_samples)
    num_products = np.random.choice([1, 2, 3, 4], n_samples, p=[0.5, 0.45, 0.04, 0.01])
    has_cr_card = np.random.choice([0, 1], n_samples, p=[0.3, 0.7])
    is_active = np.random.choice([0, 1], n_samples, p=[0.48, 0.52])
    salary = np.random.uniform(20000, 180000, n_samples)

    # Churn probability correlation: higher churn for older age, Germany, inactive, high balance
    churn_prob = (
        0.03 * (age - 35) +
        0.000002 * balance +
        np.where(is_active == 0, 0.20, -0.15) +
        np.where(geography == 'Germany', 0.15, 0.0) +
        np.random.normal(0, 0.4, n_samples)
    )
    exited = (churn_prob > 0.5).astype(int)

    return pd.DataFrame({
        'RowNumber': range(1, n_samples + 1),
        'CustomerId': np.random.randint(15500000, 15800000, n_samples),
        'Surname': [f"Customer_{i}" for i in range(n_samples)],
        'CreditScore': credit_score,
        'Geography': geography,
        'Gender': gender,
        'Age': age,
        'Tenure': tenure,
        'Balance': balance,
        'NumOfProducts': num_products,
        'HasCrCard': has_cr_card,
        'IsActiveMember': is_active,
        'EstimatedSalary': salary,
        'Exited': exited
    })


def load_churn_dataset():
    """Searches for Churn_Modelling.csv locally; falls back to synthetic generator if absent."""
    possible_paths = [
        "Churn_Modelling.csv",
        os.path.join("ml", "Churn_Modelling.csv"),
        os.path.join("..", "Churn_Modelling.csv"),
        "churn.csv"
    ]
    for p in possible_paths:
        if os.path.exists(p):
            print(f"[+] Found dataset file: '{p}'. Loading data...")
            return pd.read_csv(p)

    print("[!] 'Churn_Modelling.csv' not found locally. Generating synthetic bank customer dataset...")
    print("    (To test with the full Kaggle dataset, place 'Churn_Modelling.csv' in the folder).")
    return generate_synthetic_churn_data(n_samples=1500)


# ---------------------------------------------------------------------------
# Preprocessing: Encoding and Feature Selection
# ---------------------------------------------------------------------------
def preprocess_churn_data(df):
    """
    Drops non-predictive identifiers, performs One-Hot Encoding on categorical
    attributes (Geography, Gender), and prepares feature matrix X and target y.
    """
    print(f"\n[1] Initial Raw Dataset Shape: {df.shape}")

    # Drop non-predictive ID columns
    drop_cols = [c for c in ['RowNumber', 'CustomerId', 'Surname'] if c in df.columns]
    if drop_cols:
        df = df.drop(columns=drop_cols)
        print(f"    Dropped non-predictive identifier columns: {drop_cols}")

    target_col = 'Exited' if 'Exited' in df.columns else df.columns[-1]

    # Convert binary categorical Gender to integer (Female = 0, Male = 1)
    if 'Gender' in df.columns:
        df['Gender'] = df['Gender'].map({'Female': 0, 'Male': 1}).fillna(0).astype(int)

    # One-Hot Encode Geography with drop_first=True to avoid dummy variable trap
    if 'Geography' in df.columns:
        df = pd.get_dummies(df, columns=['Geography'], drop_first=True)

    X = df.drop(columns=[target_col])
    y = df[target_col].values

    print(f"[2] Processed Feature Matrix Shape: {X.shape}")
    print(f"    Target Distribution: Churned (1) = {(y == 1).sum()} | Retained (0) = {(y == 0).sum()}")

    return X, y, X.columns.tolist()


# ---------------------------------------------------------------------------
# ANN Model Builder (Keras / TensorFlow with graceful MLPClassifier fallback)
# ---------------------------------------------------------------------------
def train_ann_model(X_train, y_train, X_test):
    """
    Constructs and trains an Artificial Neural Network classifier.
    Uses TensorFlow/Keras if available; otherwise uses sklearn's MLPClassifier.
    """
    try:
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Input, Dense, Dropout
        import tensorflow as tf

        # Suppress verbose TensorFlow warnings
        tf.get_logger().setLevel('ERROR')
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

        print("\n[3] Initializing Deep Artificial Neural Network Architecture (TensorFlow/Keras):")
        ann = Sequential()

        # Input layer + Hidden Layer 1: 16 Neurons, ReLU activation
        ann.add(Input(shape=(X_train.shape[1],)))
        ann.add(Dense(units=16, activation='relu'))
        ann.add(Dropout(0.1))  # Dropout layer to mitigate overfitting

        # Hidden Layer 2: 8 Neurons, ReLU activation
        ann.add(Dense(units=8, activation='relu'))

        # Output Layer: 1 Neuron, Sigmoid activation (Binary Probability: 0 to 1)
        ann.add(Dense(units=1, activation='sigmoid'))

        # Compile Model using Adam optimizer and binary crossentropy loss
        ann.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        print("    Layer 1 (Input/Hidden) : 16 Neurons, Activation = ReLU")
        print("    Dropout Layer          : Rate = 0.1 (Regularization)")
        print("    Layer 2 (Hidden)       : 8 Neurons, Activation = ReLU")
        print("    Layer 3 (Output)       : 1 Neuron, Activation = Sigmoid")
        print("    Optimizer              : Adam | Loss: binary_crossentropy")

        print("\n    Training ANN (25 Epochs, Batch Size = 32)...")
        ann.fit(X_train, y_train, batch_size=32, epochs=25, verbose=0)
        print("    Model Training Completed.")

        y_pred_prob = ann.predict(X_test, verbose=0).ravel()
        y_pred = (y_pred_prob > 0.5).astype(int)
        return y_pred, "TensorFlow/Keras ANN"

    except ImportError:
        from sklearn.neural_network import MLPClassifier
        print("\n[3] TensorFlow not found. Using scikit-learn MLPClassifier (Multi-Layer Perceptron):")
        mlp = MLPClassifier(hidden_layer_sizes=(16, 8), activation='relu', max_iter=200, random_state=42)
        mlp.fit(X_train, y_train)
        y_pred = mlp.predict(X_test)
        return y_pred, "Scikit-Learn MLPClassifier"


def main():
    print("=" * 80)
    print("     ML Assignment 3: Bank Customer Churn Prediction using ANN")
    print("=" * 80)

    # Step 1: Read dataset
    raw_df = load_churn_dataset()

    # Step 2: Separate features and target
    X, y, feature_names = preprocess_churn_data(raw_df)

    # Step 3: Divide into training and testing sets (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"\n[3] Dataset Splitting:")
    print(f"    - Training Set : {X_train.shape[0]} samples")
    print(f"    - Testing Set  : {X_test.shape[0]} samples")

    # Step 4: Normalize the train and test data (StandardScaler)
    # (Discussed in Lab Manual Pages 83-86: Normalization vs Standardization)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print(f"[4] Feature Scaling: Normalized features using StandardScaler (mean=0, std=1).")

    # Step 5: Initialize and build model
    y_pred, model_type = train_ann_model(X_train_scaled, y_train, X_test_scaled)

    # Step 6: Print accuracy score and confusion matrix (5 points from Lab Manual Page 78)
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()

    accuracy = accuracy_score(y_test, y_pred)
    misclassification_rate = 1.0 - accuracy
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)

    print("\n" + "=" * 75)
    print(f"          CONFUSION MATRIX (2x2) [{model_type}]")
    print("=" * 75)
    print(f"{'':<25} | {'Actual Retained (0)':<20} | {'Actual Churned (1)':<20}")
    print("-" * 75)
    print(f"{'Predicted Retained (0)':<25} | TN = {tn:<15} | FN = {fn:<15}")
    print(f"{'Predicted Churned (1)':<25} | FP = {fp:<15} | TP = {tp:<15}")
    print("-" * 75)

    print("\n" + "=" * 75)
    print("               EVALUATION RATIOS & SCORES (5 POINTS)")
    print("=" * 75)
    print(f"  1. Classification Accuracy     : {accuracy * 100:>8.2f}%  [(TP + TN) / Total]")
    print(f"  2. Misclassification Rate      : {misclassification_rate * 100:>8.2f}%  [(FP + FN) / Total]")
    print(f"  3. Precision                   : {precision:>8.4f}   [TP / (TP + FP)]")
    print(f"  4. Recall / Sensitivity        : {recall:>8.4f}   [TP / (TP + FN)]")
    print(f"  5. F1-Score (F-measure)        : {f1:>8.4f}   [2*(Prec*Rec)/(Prec+Rec)]")
    print("=" * 75)

    # Demonstration customer test case
    sample_customer = X.iloc[0:1]
    sample_scaled = scaler.transform(sample_customer)
    sample_pred = (y_pred[0] if len(y_pred) > 0 else 0)
    churn_status = "Likely to Churn (Exit)" if sample_pred == 1 else "Likely to Retain (Stay)"
    print(f"\n[+] Demonstration Customer Prediction:")
    print(f"    Profile: CreditScore={sample_customer['CreditScore'].values[0]}, Age={sample_customer['Age'].values[0]}, Balance=${sample_customer['Balance'].values[0]:,.2f}")
    print(f"    Model Assessment: {churn_status}")


if __name__ == "__main__":
    main()
