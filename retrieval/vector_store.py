import faiss
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

EMBEDDINGS_PATH = DATA_DIR / "embeddings"
FAISS_PATH = DATA_DIR / "faiss"
FAISS_PATH.mkdir(exist_ok=True)

def build_index():
    vectors = np.load(EMBEDDINGS_PATH / "vectors.npy")
    vectors = vectors.astype("float32")
    vectors = np.ascontiguousarray(vectors)

    dim = vectors.shape[1]

    faiss.normalize_L2(vectors)
    
    index = faiss.IndexFlatIP(dim)  # cosine similarity
    index.add(vectors)
    faiss.write_index(index, str(FAISS_PATH / "index.faiss"))

    print(f"FAISS index built with {index.ntotal} vectors")

if __name__ == "__main__":
    build_index()
