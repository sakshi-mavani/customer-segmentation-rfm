import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_cleaning import get_clean_data
from src.rfm_calculator import calculate_rfm
from src.visualizations import plot_rfm_distribution, plot_customer_segments, plot_top_customers
from src.rfm_calculator import assign_segments


def main():
    """
    Master function — runs the entire RFM pipeline.
    """

    # Step 1: Load and clean data
    print("Loading and cleaning data...")
    orders, order_items, customers = get_clean_data()
    print(f"Orders: {len(orders)} rows")
    print(f"Order Items: {len(order_items)} rows")
    print(f"Customers: {len(customers)} rows")

    # Step 2: Calculate RFM
    print("\nCalculating RFM scores...")
    rfm = calculate_rfm(orders, order_items, customers)
    print(f"RFM Table: {len(rfm)} customers")
    print(rfm.head())

    # Step 3: Assign Segments
    print("\nAssigning customer segments...")
    rfm = assign_segments(rfm)
    print(rfm['Segment'].value_counts())

    # Step 4: Save RFM scores
    print("\nSaving RFM scores...")
    rfm.to_csv('data/processed/rfm_scores.csv', index=False)
    print("Saved to data/processed/rfm_scores.csv")

    # Step 5: Generate visualizations
    print("\nGenerating visualizations...")
    plot_rfm_distribution(rfm)
    plot_customer_segments(rfm)
    plot_top_customers(rfm)
    print("Plots saved to outputs/plots/")

    print("\nDone! RFM pipeline complete.")


if __name__ == "__main__":
    main()


