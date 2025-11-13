from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import os

INDEX_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'faiss_index.bin')
DOCS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'faiss_docs.pkl')
MODEL_NAME = "all-MiniLM-L6-v2"

def build_index(docs):
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(docs, convert_to_numpy=True, show_progress_bar=True)
    faiss.normalize_L2(embeddings)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    faiss.write_index(index, INDEX_PATH)
    with open(DOCS_PATH, 'wb') as f:
        pickle.dump(docs, f)
    print(f"Built index at {INDEX_PATH} with {len(docs)} docs.")
    return index

def load_index():
    if not (os.path.exists(INDEX_PATH) and os.path.exists(DOCS_PATH)):
        return None, None
    index = faiss.read_index(INDEX_PATH)
    with open(DOCS_PATH, 'rb') as f:
        docs = pickle.load(f)
    return index, docs

def query_index(index, docs, text, top_k=5):
    model = SentenceTransformer(MODEL_NAME)
    q = model.encode([text], convert_to_numpy=True)
    faiss.normalize_L2(q)
    D, I = index.search(q, top_k)
    results = []
    for idx in I[0]:
        if idx < len(docs):
            results.append(docs[idx])
    return results
