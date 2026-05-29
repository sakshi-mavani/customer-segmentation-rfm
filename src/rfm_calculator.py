import pandas as pd
import sqlite3
from datetime import datetime

from src.data_cleaning import get_clean_data


def calculate_rfm(orders: pd.DataFrame,
                  order_items: pd.DataFrame,
                  customers: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate RFM scores for each customer.
    Returns a DataFrame with RFM scores.
    """

    # Step 1: Merge orders with customers
    df = orders.merge(customers, on='customer_id', how='inner')

    # Step 2: Merge with order_items
    df = df.merge(order_items, on='order_id', how='inner')

    # Step 3: Calculate RFM
    snapshot_date = df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)

    rfm = df.groupby('customer_unique_id').agg(
        Recency=('order_purchase_timestamp', lambda x: (snapshot_date - x.max()).days),
        Frequency=('order_id', 'nunique'),
        Monetary=('price', 'sum')
    ).reset_index()

    return rfm

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


def assign_segments(rfm: pd.DataFrame, n_clusters: int = 4) -> pd.DataFrame:
    """
    Apply KMeans clustering on RFM scores.
    Returns RFM DataFrame with Segment column added.
    """

    # Step 1: Scale RFM values
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])

    # Step 2: Apply KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)

    # Step 3: Label segments based on Monetary mean
    cluster_summary = rfm.groupby('Cluster')['Monetary'].mean().sort_values(ascending=False)
    segment_labels = {
        cluster_summary.index[0]: 'VIP',
        cluster_summary.index[1]: 'Loyal',
        cluster_summary.index[2]: 'At-Risk',
        cluster_summary.index[3]: 'Lost'
    }
    rfm['Segment'] = rfm['Cluster'].map(segment_labels)
    rfm = rfm.drop(columns='Cluster')

    return rfm
