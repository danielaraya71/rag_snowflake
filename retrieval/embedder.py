from pathlib import Path
from openai import OpenAI
import numpy as np
import json

client = OpenAI()

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

CHUNKS_PATH = DATA_DIR / "chunks"
EMBEDDINGS_PATH = DATA_DIR / "embeddings"
EMBEDDINGS_PATH.mkdir(exist_ok=True)

MODEL = "text-embedding-3-small"

def embed_texts(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(
        model=MODEL,
        input=texts
    )
    return [item.embedding for item in response.data]

def run():
    texts = []
    metadatas = []

    for chunk_file in CHUNKS_PATH.glob("*.txt"):
        text = chunk_file.read_text(encoding="utf-8")
        texts.append(text)
        metadatas.append({
            "source": chunk_file.name,
            "doc": chunk_file.stem.split("_chunk_")[0]
        })

    print(f"Embedding {len(texts)} chunks...")
    embeddings = embed_texts(texts)

    np.save(EMBEDDINGS_PATH / "vectors.npy", np.array(embeddings))
    (EMBEDDINGS_PATH / "texts.json").write_text(json.dumps(texts))
    (EMBEDDINGS_PATH / "metadata.json").write_text(json.dumps(metadatas))

    print("Embeddings saved")

if __name__ == "__main__":
    run()
