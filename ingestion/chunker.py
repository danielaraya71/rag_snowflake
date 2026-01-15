import tiktoken
from pathlib import Path

ENCODER = tiktoken.get_encoding("cl100k_base")

def chunk_text(text, chunk_size=500, overlap=100):
    tokens = ENCODER.encode(text)
    chunks = []

    start = 0
    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunk_text = ENCODER.decode(chunk_tokens)

        chunks.append(chunk_text)
        start += chunk_size - overlap

    return chunks

def run():
    input_path = Path("data/clean_docs")
    output_path = Path("data/chunks")
    output_path.mkdir(exist_ok=True)

    for txt in input_path.glob("*.txt"):
        text = txt.read_text(encoding="utf-8")
        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):
            out = output_path / f"{txt.stem}_chunk_{i}.txt"
            out.write_text(chunk, encoding="utf-8")

        print(f"Chunked {txt.stem}: {len(chunks)} chunks")

if __name__ == "__main__":
    run()
