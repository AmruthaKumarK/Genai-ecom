from src.utils.data_loader import load_data
from src.analytics.aggregations import sales_by_category, top_products

def create_docs(limit_products=200):
    data = load_data()
    orders = data['orders']
    order_items = data['order_items']
    products = data['products']

    docs = []
    docs.append(f"Orders table summary: total_orders={orders.shape[0]}, first_order={orders['order_purchase_timestamp'].min()}, last_order={orders['order_purchase_timestamp'].max()}.")
    try:
        top_cats = sales_by_category(orders, order_items, products, top_n=10)
        cats = top_cats['product_category_name'].astype(str).tolist()
        docs.append("Top categories by revenue: " + ", ".join(cats))
    except Exception:
        pass

    try:
        top_prod = top_products(order_items, products, top_n=limit_products)
        for _, r in top_prod.iterrows():
            prod_id = r['product_id']
            cat = r.get('product_category_name','NA')
            docs.append(f"Product {prod_id} in category {cat} has revenue {r['total_revenue']:.2f} and units_sold {int(r['units_sold'])}.")
    except Exception:
        for _, r in products.head(limit_products).iterrows():
            docs.append(f"Product {r['product_id']}: category {r.get('product_category_name','NA')}")

    return docs

if __name__ == '__main__':
    docs = create_docs()
    print('Generated', len(docs), 'docs')
