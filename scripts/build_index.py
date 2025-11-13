import os, sys
proj_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, proj_root)
from src.rag.make_docs import create_docs
from src.rag.embedder import build_index

def main():
    docs = create_docs(limit_products=150)
    build_index(docs)
    print("Index build complete.")

if __name__ == '__main__':
    main()
