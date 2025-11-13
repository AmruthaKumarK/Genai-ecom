from src.rag.embedder import load_index, query_index
from src.llm.client import call_llm
from src.utils.data_loader import load_data
from src.analytics.aggregations import sales_by_category, avg_order_value, top_products
import wikipedia

DATA = load_data()
INDEX, DOCS = load_index()

def is_analytics_query(q):
    ql = q.lower()
    keywords = ['average', 'avg', 'top', 'highest', 'lowest', 'sales', 'revenue', 'orders', 'trend', 'mean', 'median']
    return any(k in ql for k in keywords)

def handle_analytics(q):
    ql = q.lower()
    if 'average' in ql or 'avg order' in ql or 'avg' in ql:
        if 'electronics' in ql:
            cat = 'electronics'
        else:
            cat = None
        val = avg_order_value(DATA['orders'], DATA['order_items'], DATA['products'], category=cat)
        if val is None:
            return "I couldn't find relevant orders for that category or time range.", ['analytics:avg_order_value']
        return f"Average order value{(' for '+cat) if cat else ''}: {val:.2f}", ['analytics:avg_order_value']
    if 'top' in ql and 'product' in ql:
        top = top_products(DATA['order_items'], DATA['products'], top_n=10)
        return top.to_dict(orient='records'), ['analytics:top_products']
    if 'highest selling' in ql or 'top category' in ql or 'highest' in ql:
        top = sales_by_category(DATA['orders'], DATA['order_items'], DATA['products'], top_n=10)
        return top.to_dict(orient='records'), ['analytics:sales_by_category']
    if 'trend' in ql or 'over time' in ql:
        df = DATA['orders'].copy()
        df['month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)
        monthly = df.groupby('month')['order_revenue'].sum().reset_index().rename(columns={'order_revenue':'total_revenue'})
        return monthly.to_dict(orient='records'), ['analytics:trend']
    return None, []

def wiki_lookup(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except Exception:
        return None

def handle_query(q):
    if is_analytics_query(q):
        ans, sources = handle_analytics(q)
        return ans, sources
    if q.lower().strip().startswith(('what is', 'who is', 'tell me about', 'info on', 'information on')):
        summary = wiki_lookup(q)
        if summary:
            return summary, ['wiki']
    if INDEX is None or DOCS is None:
        prompt = f"""You are an e-commerce data assistant. The user asked: {q}\nIf possible, give short suggestions for how to analyze the Kaggle Brazilian e-commerce dataset in pandas."""
        ans = call_llm(prompt)
        return ans, ['llm:fallback']
    retrieved = query_index(INDEX, DOCS, q, top_k=5)
    context = "\n\n".join(retrieved)
    prompt = f"""You are an e-commerce analytics assistant. Use the following context (from our dataset):\n{context}\n\nUser question: {q}\nAnswer concisely and mention which context snippets you used."""
    ans = call_llm(prompt)
    return ans, ['rag:retrieved_docs']
