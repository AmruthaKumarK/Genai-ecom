import pandas as pd

def sales_by_category(orders, order_items, products, start_date=None, end_date=None, top_n=10):
    oi = order_items.merge(products[['product_id','product_category_name']], on='product_id', how='left')
    if start_date:
        oi = oi[oi['order_purchase_timestamp'] >= pd.to_datetime(start_date)]
    if end_date:
        oi = oi[oi['order_purchase_timestamp'] <= pd.to_datetime(end_date)]
    sales = oi.groupby('product_category_name')['price'].agg(total_revenue='sum', units_sold='count').reset_index()
    sales = sales.sort_values('total_revenue', ascending=False).head(top_n)
    return sales

def avg_order_value(orders, order_items=None, products=None, category=None):
    if category and order_items is not None and products is not None:
        oi = order_items.merge(products[['product_id','product_category_name']], on='product_id', how='left')
        order_ids = oi[oi['product_category_name'] == category]['order_id'].unique()
        subset = orders[orders['order_id'].isin(order_ids)]
    else:
        subset = orders
    if subset.empty:
        return None
    return float(subset['order_revenue'].mean())

def top_products(order_items, products, top_n=10):
    merged = order_items.merge(products[['product_id','product_category_name']], on='product_id', how='left')
    top = merged.groupby('product_id')['price'].agg(total_revenue='sum', units_sold='count').reset_index()
    top = top.sort_values('total_revenue', ascending=False).head(top_n)
    top = top.merge(products[['product_id','product_name_lenght','product_description_lenght','product_category_name']], on='product_id', how='left')
    return top
