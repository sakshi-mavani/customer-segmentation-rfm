import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import os

PLOTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'plots')

def plot_rfm_distribution(rfm: pd.DataFrame) -> None:
    """
    Plot distribution of Recency, Frequency, and Monetary values.
    Saves plots to outputs/plots/
    
    """

    fig, axes = plt.subplots(1, 3, figsize=(18,5))
    fig.suptitle('RFM Distribution', fontsize=16)

    # Recency

    sns.histplot(rfm['Recency'], ax=axes[0], color='blue', kde=True)
    axes[0].set_title('Recency (days)')

    # Frequency

    sns.histplot(rfm['Frequency'], ax=axes[1], color='blue', kde=True)
    axes[1].set_title('Frequency (orders)')

    # Monetary
    sns.histplot(rfm['Monetary'], ax=axes[2], color='blue', kde=True)
    axes[2].set_title('Monetary (BRL)')

    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'rfm_distribution.png'), dpi=150)
    plt.close()

def plot_customer_segments(rfm: pd.DataFrame) -> None:
    """
    Scatter plot — Recency vs Monetary, colored by Frequency.
    Saves plot to outputs/plots/
    """

    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(
        rfm['Recency'],
        rfm['Monetary'],
        c=rfm['Frequency'],
        cmap='viridis',
        alpha=0.5
    )
    plt.colorbar(scatter, label='Frequency')
    plt.xlabel('Recency (days)')
    plt.ylabel('Monetary (BRL)')
    plt.title('Customer Segments — Recency vs Monetary')
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'customer_segments.png'), dpi=150)
    plt.close()

def plot_top_customers(rfm: pd.DataFrame, top_n: int = 10) -> None:
    """
    Bar plot — Top N customers by Monetary value.
    Saves plot to outputs/plots/
    """

    top = rfm.nlargest(top_n, 'Monetary')

    plt.figure(figsize=(12, 6))
    sns.barplot(data=top, x='customer_unique_id', y='Monetary', hue='customer_unique_id', palette='Blues_d', legend=False)
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Customer ID')
    plt.ylabel('Monetary Value (BRL)')
    plt.title(f'Top {top_n} Customers by Monetary Value')
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'top_customers.png'), dpi=150)
    plt.close()

