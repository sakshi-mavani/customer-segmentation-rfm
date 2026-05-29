import pandas as pd
import os 

RAW_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')

def load_raw_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    '''
    Load the 3 CSVs needed for RFM analysis.
    Returns : (orders, order_items, customers)
    
    '''
    orders      = pd.read_csv(os.path.join(RAW_DIR, 'olist_orders_dataset.csv'))
    order_items = pd.read_csv(os.path.join(RAW_DIR, 'olist_order_items_dataset.csv'))
    customers   = pd.read_csv(os.path.join(RAW_DIR, 'olist_customers_dataset.csv'))
    return orders, order_items, customers
 
def clean_orders(orders: pd.DataFrame) -> pd.DataFrame:
    """
    - Drop rows where purchase timestamp is missing 
    - Parse dates 
    - Keep only delivered orders
    
    """

    orders = orders.dropna(subset=['order_purchase_timestamp'])
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    orders = orders[orders['order_status'] == 'delivered']
    orders = orders.drop_duplicates(subset = 'order_id')
    return orders 

def clean_order_items(order_items: pd.DataFrame) -> pd.DataFrame :
    """
    - Drop nulls
    - Keep only price column we need 
    
    """

    order_items = order_items.dropna(subset=['order_id', 'price'])
    order_items = order_items[order_items['price'] > 0]
    return order_items

def clean_customers(customers: pd.DataFrame) -> pd.DataFrame:
    """
    
    - Drop duplicate customers 
    - Keep only needed columns
    
    """

    customers = customers.dropna(subset= ['customer_unique_id'])
    customers = customers.drop_duplicates(subset= 'customer_unique_id')
    return customers [['customer_id', 'customer_unique_id']]

def get_clean_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Master functions - loads and cleans all data
    main.py will only call this function 
    
    """
    orders, order_items, customers = load_raw_data()
    orders = clean_orders(orders)
    order_items = clean_order_items(order_items)
    customers = clean_customers(customers)
    return orders, order_items, customers 