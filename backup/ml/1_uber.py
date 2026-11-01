"""
=============================================================================
Assignment: ML 1 (Group B)
Title: Predict the price of the Uber ride from a given pickup point to the 
       agreed drop-off location. Perform following tasks:
       1. Pre-process the dataset.
       2. Identify outliers.
       3. Check the correlation.
       4. Implement linear regression and random forest regression models.
       5. Evaluate the models and compare their respective scores like R2, RMSE, etc.
Lab: Laboratory Practice - III (BE Computer Engineering - SPPU 2019 Pattern)
Dataset: Kaggle Uber Fares Dataset (uber.csv in ml/dataset/)
=============================================================================
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def safe_input(prompt_text, default_value=""):
    """Handles inputs safely in automated testing and interactive shells."""
    try:
        val = input(prompt_text)
        return val.strip() if val.strip() else default_value
    except (EOFError, KeyboardInterrupt):
        return default_value


# ---------------------------------------------------------------------------
# Task 1: Haversine Distance Calculation (Great Circle Distance on Sphere)
# ---------------------------------------------------------------------------
def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the Haversine distance in kilometers between two GPS coordinate points.
    Formula:
        a = sin^2(dlat/2) + cos(lat1) * cos(lat2) * sin^2(dlon/2)
        c = 2 * arcsin(sqrt(a))
        distance = R * c  (where R = 6371 km)
    """
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))
    earth_radius_km = 6371.0
    return c * earth_radius_km


# ---------------------------------------------------------------------------
# Synthetic Dataset Generator (Fallback if Kaggle uber.csv is not present)
# ---------------------------------------------------------------------------
def generate_synthetic_uber_data(n_samples=5000):
    """Generates realistic synthetic Uber ride records mimicking the Kaggle dataset schema."""
    np.random.seed(42)
    p_lat = np.random.uniform(40.70, 40.82, n_samples)
    p_lon = np.random.uniform(-74.02, -73.92, n_samples)
    d_lat = p_lat + np.random.normal(0, 0.03, n_samples)
    d_lon = p_lon + np.random.normal(0, 0.03, n_samples)

    dist = calculate_haversine_distance(p_lat, p_lon, d_lat, d_lon)
    fares = 2.50 + (dist * 2.75) + np.random.normal(0, 1.25, n_samples)
    fares = np.maximum(fares, 2.50)

    dates = pd.date_range(start="2022-01-01", periods=n_samples, freq="15min")
    passengers = np.random.choice([1, 2, 3, 4, 5, 6], size=n_samples, p=[0.7, 0.15, 0.05, 0.04, 0.03, 0.03])

    df = pd.DataFrame({
        'key': [f"trip_{i}" for i in range(n_samples)],
        'fare_amount': fares,
        'pickup_datetime': dates.astype(str),
        'pickup_longitude': p_lon,
        'pickup_latitude': p_lat,
        'dropoff_longitude': d_lon,
        'dropoff_latitude': d_lat,
        'passenger_count': passengers
    })
    return df


def load_uber_dataset():
    """Searches for uber.csv in ml/dataset/ and local directories; falls back to synthetic data."""
    possible_paths = [
        os.path.join("ml", "dataset", "uber.csv"),
        os.path.join("dataset", "uber.csv"),
        os.path.join("..", "ml", "dataset", "uber.csv"),
        os.path.join("..", "dataset", "uber.csv"),
        "uber.csv",
        os.path.join("ml", "uber.csv"),
        os.path.join("..", "uber.csv"),
    ]
    for p in possible_paths:
        if os.path.exists(p):
            print(f"[+] Found dataset file: '{p}'.")
            print("    Loading dataset into memory...")
            df = pd.read_csv(p)
            print(f"[+] Successfully loaded {len(df):,} records.")
            return df

    print("[!] 'uber.csv' not found in ml/dataset/. Generating synthetic NYC Uber dataset...")
    return generate_synthetic_uber_data(n_samples=5000)


# ---------------------------------------------------------------------------
# Task 1 & 2: Preprocessing, Feature Engineering & Outlier Removal
# ---------------------------------------------------------------------------
def preprocess_and_detect_outliers(df, max_training_samples=50000):
    """
    Cleans raw dataset, filters geographic/fare outliers, extracts temporal features,
    and computes Haversine trip distance.
    """
    print(f"\n[1] Preprocessing: Initial shape = {df.shape}")

    # Drop null values
    df = df.dropna().copy()
    print(f"    After dropping null values: {df.shape}")

    # Parse pickup datetime
    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'], errors='coerce')
    df = df.dropna(subset=['pickup_datetime']).copy()

    # Temporal feature engineering
    df['hour'] = df['pickup_datetime'].dt.hour
    df['day_of_week'] = df['pickup_datetime'].dt.dayofweek
    df['year'] = df['pickup_datetime'].dt.year

    # Filter invalid GPS coordinates to realistic Greater New York City bounding box
    initial_geo = len(df)
    df = df[
        (df['pickup_latitude'].between(40.50, 40.95)) &
        (df['pickup_longitude'].between(-74.30, -73.65)) &
        (df['dropoff_latitude'].between(40.50, 40.95)) &
        (df['dropoff_longitude'].between(-74.30, -73.65))
    ]
    geo_outliers = initial_geo - len(df)
    print(f"[2] Outlier Detection (GPS Coordinates): Filtered {geo_outliers:,} invalid/out-of-bounds GPS records.")

    # Feature Engineering: Haversine distance in km
    df['distance_km'] = calculate_haversine_distance(
        df['pickup_latitude'], df['pickup_longitude'],
        df['dropoff_latitude'], df['dropoff_longitude']
    )

    # Filter impossible fare amounts, distances, and passenger counts
    fare_initial = len(df)
    df = df[(df['fare_amount'] >= 2.50) & (df['fare_amount'] <= 150.0)]
    df = df[(df['passenger_count'] >= 1) & (df['passenger_count'] <= 6)]
    df = df[(df['distance_km'] >= 0.1) & (df['distance_km'] <= 80.0)]
    fare_outliers = fare_initial - len(df)
    print(f"    Outlier Detection (Fares & Distance): Filtered {fare_outliers:,} extreme fare/distance outliers.")
    print(f"    Cleaned dataset shape = {df.shape}")

    # Subsample if dataset is very large to ensure lightning-fast training in viva exams
    if len(df) > max_training_samples:
        print(f"    Sampling {max_training_samples:,} representative records for fast high-accuracy training...")
        df = df.sample(n=max_training_samples, random_state=42)

    return df


# ---------------------------------------------------------------------------
# Task 3: Correlation Analysis
# ---------------------------------------------------------------------------
def check_correlation(df, features, target='fare_amount'):
    """Computes and prints correlation of features with target fare_amount."""
    corr_cols = features + [target]
    corr_matrix = df[corr_cols].corr()
    print("\n" + "=" * 70)
    print("                    CORRELATION WITH FARE AMOUNT")
    print("=" * 70)
    target_corr = corr_matrix[target].sort_values(ascending=False)
    for col, val in target_corr.items():
        print(f"  {col:<25} : {val:>8.4f}")
    print("=" * 70)
    return corr_matrix


# ---------------------------------------------------------------------------
# Task 4 & 5: Model Implementation & Evaluation (High Accuracy)
# ---------------------------------------------------------------------------
def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    """
    Trains Linear Regression and Random Forest Regressor models and evaluates them
    using R2, RMSE, and MAE.
    """
    print("\n[+] Training Linear Regression model...")
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)

    lr_rmse = np.sqrt(mean_squared_error(y_test, y_pred_lr))
    lr_mae = mean_absolute_error(y_test, y_pred_lr)
    lr_r2 = r2_score(y_test, y_pred_lr)

    print("[+] Training Random Forest Regressor (50 trees, max_depth=16)...")
    rf = RandomForestRegressor(n_estimators=50, max_depth=16, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)

    rf_rmse = np.sqrt(mean_squared_error(y_test, y_pred_rf))
    rf_mae = mean_absolute_error(y_test, y_pred_rf)
    rf_r2 = r2_score(y_test, y_pred_rf)

    print("\n" + "=" * 78)
    print("                 MODEL EVALUATION & ACCURACY COMPARISON")
    print("=" * 78)
    print(f"{'Model Architecture':<28} | {'RMSE ($)':<12} | {'MAE ($)':<12} | {'R2 Score (Accuracy)':<18}")
    print("-" * 78)
    print(f"{'Linear Regression':<28} | {lr_rmse:<12.4f} | {lr_mae:<12.4f} | {lr_r2:<18.4f} ({lr_r2*100:.2f}%)")
    print(f"{'Random Forest Regressor':<28} | {rf_rmse:<12.4f} | {rf_mae:<12.4f} | {rf_r2:<18.4f} ({rf_r2*100:.2f}%)")
    print("=" * 78)

    winner = "Random Forest Regressor" if rf_r2 > lr_r2 else "Linear Regression"
    print(f"[*] Best Performing Model : {winner}")
    print(f"    -> High Accuracy: {max(rf_r2, lr_r2)*100:.2f}% variance explained (R2 score).")
    print(f"    -> Low Average Error: ${min(rf_mae, lr_mae):.2f} MAE on unseen test trips.")


def main():
    print("=" * 78)
    print("     ML Assignment 1: Uber Ride Price Prediction (LR vs Random Forest)")
    print("=" * 78)

    # Step 1: Load dataset
    raw_df = load_uber_dataset()

    # Step 2: Preprocess & Outliers
    df = preprocess_and_detect_outliers(raw_df, max_training_samples=50000)

    # Feature columns
    features = [
        'pickup_longitude', 'pickup_latitude',
        'dropoff_longitude', 'dropoff_latitude',
        'passenger_count', 'distance_km',
        'hour', 'day_of_week', 'year'
    ]
    target = 'fare_amount'

    # Step 3: Check correlation
    check_correlation(df, features, target)

    # Step 4: Split data (80% train, 20% test)
    X = df[features]
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"\nTrain Set: {X_train.shape[0]:,} samples | Test Set: {X_test.shape[0]:,} samples")

    # Step 5: Train and compare models
    train_and_evaluate_models(X_train, X_test, y_train, y_test)


if __name__ == "__main__":
    main()
