import streamlit as st
from google import genai
from dotenv import load_dotenv
load_dotenv()
import os
from src.rag_query_handler import handle_query
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="GenAI E-Commerce Insights", layout="wide")
st.title("GenAI E-Commerce Insights")
st.markdown("Chat with the Brazilian Olist e-commerce dataset. Use the sidebar for quick actions.")

# UI state
if 'history' not in st.session_state:
    st.session_state.history = []  # list of (role, content, sources)

with st.sidebar:
    st.header("Quick actions")
    if st.button("Top categories (recent)"):
        q = "Which product category was the highest selling in the past 2 quarters?"
        ans, src = handle_query(q)
        st.session_state.history.append(('user', q, []))
        st.session_state.history.append(('assistant', ans, src))
    if st.button("Avg order value (Electronics)"):
        q = "What is the average order value for items in the Electronics category?"
        ans, src = handle_query(q)
        st.session_state.history.append(('user', q, []))
        st.session_state.history.append(('assistant', ans, src))
    if st.button("Top products (revenue)"):
        q = "Show top 5 products by revenue"
        ans, src = handle_query(q)
        st.session_state.history.append(('user', q, []))
        st.session_state.history.append(('assistant', ans, src))
    st.markdown('---')
    st.write('Tips: Try follow-ups. E.g., ask for top SKUs after asking about a category.')
    if st.button("Clear history"):
        st.session_state.history = []

st.markdown('---')
query = st.text_input("Ask a question about the dataset (analytics queries are handled by pandas):")
if st.button("Ask") and query.strip():
    st.session_state.history.append(('user', query, []))
    ans, src = handle_query(query)
    st.session_state.history.append(('assistant', ans, src))
    st.rerun()

# Display conversation
for role, content, sources in reversed(st.session_state.history):
    if role == 'user':
        st.markdown(f'**You:** {content}')
    else:
        st.markdown('**Assistant:**')
        if isinstance(content, list):
            try:
                df = pd.DataFrame(content)
                st.dataframe(df)
                if 'total_revenue' in df.columns and 'product_category_name' in df.columns:
                    fig = px.bar(df.sort_values('total_revenue', ascending=False), x='product_category_name', y='total_revenue')
                    st.plotly_chart(fig, use_container_width=True)
                elif 'total_revenue' in df.columns and 'product_id' in df.columns:
                    fig = px.bar(df.sort_values('total_revenue', ascending=False).head(10), x='product_id', y='total_revenue')
                    st.plotly_chart(fig, use_container_width=True)
            except Exception:
                st.write(content)
        elif isinstance(content, str):
            st.write(content)
        else:
            st.write(content)
        if sources:
            st.markdown('**Sources:** ' + ', '.join(sources))
