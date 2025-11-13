# GenAI E-Commerce Insights

This project implements:
- Streamlit chat UI with session memory
- Analytics via pandas (sales by category, avg order value, top products, trends)
- RAG: embeddings via sentence-transformers + FAISS
- LLM wrapper supporting Google Gemini (google-generativeai), OpenAI, OpenRouter
- Small external lookup (Wikipedia)
- Plots using Plotly
- Scripts to build the FAISS index

## Steps to Run

1. Unzip and `cd Genai-ecom`

2. Create virtualenv and install:
   ```
   python -m venv venv
   source venv/bin/activate   # Windows: .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

3. Put the Kaggle dataset CSV files into `data/`:
   - olist_orders_dataset.csv
   - olist_order_items_dataset.csv
   - olist_products_dataset.csv
   - olist_customers_dataset.csv
   - olist_order_payments_dataset.csv

4. Copy `.env.example` to `.env` and set your keys.

5. Build the FAISS index (one-time):
   ```
   python scripts/build_index.py
   ```

6. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

