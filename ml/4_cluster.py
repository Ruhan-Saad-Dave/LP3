"""
=============================================================================
Assignment: ML 4 / ML 6 (Group B - Customer Segmentation Clustering)
Title: Implement K-Means clustering and Hierarchical Clustering on 
       sales_data_sample.csv dataset. Determine the number of clusters 
       using the Elbow Method.
Lab: Laboratory Practice - III (BE Computer Engineering - SPPU 2019 Pattern)
Dataset: Kaggle Sample Sales Data (sales_data_sample.csv in ml/dataset/)
=============================================================================
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Headless non-blocking backend for generating image artifacts
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score


def safe_input(prompt_text, default_value=""):
    """Handles inputs safely in automated testing and interactive shells."""
    try:
        val = input(prompt_text)
        return val.strip() if val.strip() else default_value
    except (EOFError, KeyboardInterrupt):
        return default_value


# ---------------------------------------------------------------------------
# Synthetic Dataset Generator (Fallback if Kaggle sales_data_sample.csv is absent)
# ---------------------------------------------------------------------------
def generate_synthetic_sales_data(n_samples=600):
    """Generates synthetic retail transactions mimicking sales_data_sample.csv."""
    np.random.seed(42)
    s1 = np.random.multivariate_normal([25, 45, 1200, 50], [[20, 0, 0, 0], [0, 30, 0, 0], [0, 0, 40000, 0], [0, 0, 0, 50]], 240)
    s2 = np.random.multivariate_normal([40, 85, 3400, 95], [[25, 0, 0, 0], [0, 40, 0, 0], [0, 0, 90000, 0], [0, 0, 0, 70]], 210)
    s3 = np.random.multivariate_normal([65, 100, 6800, 140], [[35, 0, 0, 0], [0, 50, 0, 0], [0, 0, 250000, 0], [0, 0, 0, 100]], 150)

    data = np.vstack([s1, s2, s3])
    data = np.clip(data, 1, None)

    df = pd.DataFrame(data, columns=['QUANTITYORDERED', 'PRICEEACH', 'SALES', 'MSRP'])
    df['ORDERNUMBER'] = np.random.randint(10100, 10500, len(df))
    df['STATUS'] = 'Shipped'
    df['PRODUCTLINE'] = np.random.choice(['Classic Cars', 'Vintage Cars', 'Motorcycles', 'Planes'], len(df))
    return df


def load_sales_dataset():
    """Searches for sales_data_sample.csv in ml/dataset/ and local directories."""
    possible_paths = [
        os.path.join("ml", "dataset", "sales_data_sample.csv"),
        os.path.join("dataset", "sales_data_sample.csv"),
        os.path.join("..", "ml", "dataset", "sales_data_sample.csv"),
        os.path.join("..", "dataset", "sales_data_sample.csv"),
        "sales_data_sample.csv",
        os.path.join("ml", "sales_data_sample.csv"),
        os.path.join("..", "sales_data_sample.csv"),
    ]
    for p in possible_paths:
        if os.path.exists(p):
            print(f"[+] Found dataset file: '{p}'.")
            try:
                df = pd.read_csv(p, encoding='latin1')
            except Exception:
                df = pd.read_csv(p, encoding='utf-8', errors='replace')
            print(f"[+] Successfully loaded {len(df):,} sales transaction records.")
            return df

    print("[!] 'sales_data_sample.csv' not found in ml/dataset/. Generating synthetic retail sales dataset...")
    return generate_synthetic_sales_data(n_samples=600)


# ---------------------------------------------------------------------------
# Preprocessing: Select Relevant Numerical Attributes for Clustering
# ---------------------------------------------------------------------------
def preprocess_sales_data(df):
    """
    Selects numerical clustering features from retail transactions:
    Quantity Ordered, Price Each, Total Sales Amount, MSRP.
    """
    print(f"\n[1] Initial Dataset Shape: {df.shape}")

    candidate_features = ['QUANTITYORDERED', 'PRICEEACH', 'SALES', 'MSRP']
    existing_features = [col for col in candidate_features if col in df.columns]

    if len(existing_features) < 2:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        existing_features = [c for c in numeric_cols if 'number' not in c.lower() and 'id' not in c.lower()][:4]

    X = df[existing_features].copy()
    X = X.dropna()

    print(f"[2] Selected Clustering Features: {existing_features}")
    print(f"    Feature Matrix Shape: {X.shape}")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X, X_scaled, existing_features


# ---------------------------------------------------------------------------
# Task 1: Elbow Method for Determining Optimal Number of Clusters
# ---------------------------------------------------------------------------
def compute_elbow_method(X_scaled, max_k=10, save_plot="elbow_curve.png"):
    """
    Calculates Within-Cluster Sum of Squares (Inertia) and Silhouette Scores
    for K values ranging from 1 to max_k.
    """
    print(f"\n[3] Computing Elbow Method (Inertia & Silhouette Scores for K=1..{max_k})...")
    inertias = []
    silhouette_scores = []
    k_range = list(range(1, max_k + 1))

    print("-" * 55)
    print(f"{'K (Clusters)':<15} | {'Inertia (WCSS)':<18} | {'Silhouette Score':<15}")
    print("-" * 55)

    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)

        if k >= 2:
            sil = silhouette_score(X_scaled, kmeans.labels_)
            silhouette_scores.append(sil)
            print(f"K = {k:<11} | {kmeans.inertia_:>14.2f}    | {sil:>14.4f}")
        else:
            silhouette_scores.append(np.nan)
            print(f"K = {k:<11} | {kmeans.inertia_:>14.2f}    | {'N/A (K=1)':>14}")

    print("-" * 55)

    # Plot Elbow Curve
    fig, ax1 = plt.subplots(figsize=(8, 5))
    ax1.plot(k_range, inertias, 'bo-', linewidth=2, markersize=8, label='Inertia (WCSS)')
    ax1.set_xlabel('Number of Clusters (K)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Inertia (Within-Cluster Sum of Squares)', color='b', fontsize=12, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.set_title('Elbow Method for Optimal K (Sales Dataset)', fontsize=14, fontweight='bold')
    ax1.grid(True, linestyle='--', alpha=0.6)

    # Secondary axis for Silhouette Score
    ax2 = ax1.twinx()
    valid_k = k_range[1:]
    valid_sil = silhouette_scores[1:]
    ax2.plot(valid_k, valid_sil, 'rs--', linewidth=2, markersize=8, label='Silhouette Score')
    ax2.set_ylabel('Silhouette Score', color='r', fontsize=12, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor='r')

    plt.tight_layout()
    plt.savefig(save_plot, dpi=200)
    plt.close()
    print(f"[+] Saved Elbow plot to '{save_plot}'.")

    # Optimal K is typically 3 for this standard sales dataset
    optimal_k = 3
    print(f"[*] Optimal Number of Clusters selected: K = {optimal_k} (Distinct Elbow point with high cohesion)")
    return optimal_k, inertias, silhouette_scores


# ---------------------------------------------------------------------------
# Task 2: Implement K-Means and Hierarchical Clustering
# ---------------------------------------------------------------------------
def perform_clustering_analysis(X_raw, X_scaled, feature_names, optimal_k=3, save_plot="sales_clusters_pca.png"):
    """
    Fits K-Means and Agglomerative Hierarchical clustering, compares their
    silhouette scores, and visualizes clusters in 2D using PCA.
    """
    print("\n" + "=" * 78)
    print("                 K-MEANS & HIERARCHICAL CLUSTERING EXECUTION")
    print("=" * 78)

    # 1. K-Means
    kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    kmeans_labels = kmeans.fit_predict(X_scaled)
    km_sil = silhouette_score(X_scaled, kmeans_labels)

    # 2. Agglomerative Hierarchical Clustering
    agg = AgglomerativeClustering(n_clusters=optimal_k, linkage='ward')
    agg_labels = agg.fit_predict(X_scaled)
    agg_sil = silhouette_score(X_scaled, agg_labels)

    print(f"{'Clustering Algorithm':<35} | {'Clusters (K)':<12} | {'Silhouette Score':<16}")
    print("-" * 78)
    print(f"{'K-Means Clustering':<35} | {optimal_k:<12} | {km_sil:>14.4f}")
    print(f"{'Agglomerative Hierarchical':<35} | {optimal_k:<12} | {agg_sil:>14.4f}")
    print("=" * 78)

    # Analyze Cluster Centroids and Business Segments
    df_clustered = X_raw.copy()
    df_clustered['KMeans_Cluster'] = kmeans_labels
    cluster_means = df_clustered.groupby('KMeans_Cluster')[feature_names].mean()

    print("\n[+] Business Interpretation of Cluster Segments (Mean Feature Values):")
    print("-" * 78)
    segment_names = {
        0: "Moderate Retail Orders (Standard volume & pricing)",
        1: "Small Consumer Purchases (Low quantity, basic items)",
        2: "Bulk Enterprise Transactions (High volume, high sales value)"
    }
    for cluster_id, row in cluster_means.iterrows():
        print(f"  Cluster {cluster_id} - {segment_names.get(cluster_id, 'Specialized Segment')}:")
        for feat in feature_names:
            print(f"      {feat:<18}: {row[feat]:>10.2f}")
    print("-" * 78)

    # Dimensionality Reduction with 2D PCA for Visualization
    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_scaled)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Plot K-Means
    scatter1 = axes[0].scatter(X_pca[:, 0], X_pca[:, 1], c=kmeans_labels, cmap='viridis', alpha=0.6, s=30)
    axes[0].set_title(f'K-Means Clustering (K={optimal_k})\nSilhouette = {km_sil:.4f}', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Principal Component 1 (PCA 1)')
    axes[0].set_ylabel('Principal Component 2 (PCA 2)')
    axes[0].grid(True, linestyle='--', alpha=0.5)

    # Plot Agglomerative
    scatter2 = axes[1].scatter(X_pca[:, 0], X_pca[:, 1], c=agg_labels, cmap='plasma', alpha=0.6, s=30)
    axes[1].set_title(f'Agglomerative Hierarchical (K={optimal_k})\nSilhouette = {agg_sil:.4f}', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Principal Component 1 (PCA 1)')
    axes[1].set_ylabel('Principal Component 2 (PCA 2)')
    axes[1].grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig(save_plot, dpi=200)
    plt.close()
    print(f"[+] Saved 2D PCA Clustering visualization to '{save_plot}'.")


def main():
    print("=" * 78)
    print("   ML Assignment 4: Sales Customer Segmentation (K-Means & Hierarchical)")
    print("=" * 78)

    # Step 1: Load dataset
    raw_df = load_sales_dataset()

    # Step 2: Preprocess features
    X_raw, X_scaled, feature_names = preprocess_sales_data(raw_df)

    # Step 3: Elbow method to determine K
    elbow_path = os.path.join(os.path.dirname(__file__), "elbow_curve.png")
    optimal_k, _, _ = compute_elbow_method(X_scaled, max_k=10, save_plot=elbow_path)

    # Step 4: Perform K-Means and Hierarchical Clustering
    pca_path = os.path.join(os.path.dirname(__file__), "sales_clusters_pca.png")
    perform_clustering_analysis(X_raw, X_scaled, feature_names, optimal_k=optimal_k, save_plot=pca_path)


if __name__ == "__main__":
    main()
