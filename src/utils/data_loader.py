import pandas as pd
import os

ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.normpath(os.path.join(ROOT, '..', 'data'))

def safe_read_csv(filename, **kwargs):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Required data file not found: {path}")
    return pd.read_csv(path, **kwargs)

def load_data():
    orders = safe_read_csv('olist_orders_dataset.csv', parse_dates=['order_purchase_timestamp'])
    order_items = safe_read_csv('olist_order_items_dataset.csv')
    products = safe_read_csv('olist_products_dataset.csv')
    customers = safe_read_csv('olist_customers_dataset.csv')
    payments = safe_read_csv('olist_order_payments_dataset.csv')

    order_items = order_items.merge(orders[['order_id','order_purchase_timestamp']], on='order_id', how='left')
    revenue = order_items.groupby('order_id')['price'].sum().reset_index().rename(columns={'price':'order_revenue'})
    orders = orders.merge(revenue, on='order_id', how='left')
    orders['order_revenue'] = orders['order_revenue'].fillna(0.0)

    return {
        'orders': orders,
        'order_items': order_items,
        'products': products,
        'customers': customers,
        'payments': payments
    }
