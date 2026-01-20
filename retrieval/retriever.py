from dotenv import load_dotenv
load_dotenv()

import faiss
import numpy as np
import json
from pathlib import Path
from openai import OpenAI

client = OpenAI()

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

FAISS_PATH = DATA_DIR / "faiss"
EMBEDDINGS_PATH = DATA_DIR / "embeddings"

MODEL = "text-embedding-3-small"

def load_store():
    index = faiss.read_index(str(FAISS_PATH / "index.faiss"))
    texts = json.loads((EMBEDDINGS_PATH / "texts.json").read_text())
    metadata = json.loads((EMBEDDINGS_PATH / "metadata.json").read_text())
    return index, texts, metadata

def embed_query(query: str) -> np.ndarray:
    response = client.embeddings.create(
        model=MODEL,
        input=query
    )
    
    vector = np.array(response.data[0].embedding, dtype="float32")
    vector = np.ascontiguousarray(vector)
    vector = vector.reshape(1, -1)
    
    faiss.normalize_L2(vector)

    return vector

def retrieve(query: str, top_k=5):
    index, texts, metadata = load_store()
    query_vector = embed_query(query)

    scores, indices = index.search(query_vector.reshape(1, -1), top_k)

    results = []
    for idx, score in zip(indices[0], scores[0]):
        results.append({
            "text": texts[idx],
            "metadata": metadata[idx],
            "score": float(score)
        })

    return results

if __name__ == "__main__":
    res = retrieve("How does Snowflake Time Travel work?")
    for r in res:
        print(r["score"], r["metadata"])
